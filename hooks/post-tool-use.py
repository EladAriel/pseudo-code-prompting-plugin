#!/usr/bin/env python3
"""
PostToolUse Hook - Inject Generated Pseudo-Code into CC10X Context

This hook runs after any tool completes. It checks if:
1. A pseudo-code transformation was active (via workflow state file)
2. Output was generated (pseudo-code in stdout)
3. If both true: saves specification to .claude/pseudo-code-prompting/specification.md

This ensures the pseudo-code is persisted even if the agent doesn't explicitly
call the injection function.
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime


def load_workflow_state() -> dict | None:
    """Load the workflow coordination state to check if transform was active."""
    try:
        state_file = Path('.claude/pseudo-code-prompting/workflow-state.json')
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Could not load state: {e}", file=sys.stderr)
    return None


def extract_pseudocode(output: str) -> str | None:
    """
    Extract pseudo-code from tool output.

    Looks for patterns like:
    - implement_function_name(...)
    - TRANSFORMED PSEUDO-CODE section
    """
    # Pattern 1: Function-style pseudo-code
    func_pattern = r'(implement_\w+\([^)]*(?:\n[^)]*)*?\))'
    match = re.search(func_pattern, output, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)

    # Pattern 2: TRANSFORMED PSEUDO-CODE section
    if 'TRANSFORMED PSEUDO-CODE' in output:
        start = output.find('TRANSFORMED PSEUDO-CODE')
        end = output.find('OPTIMIZATION SUMMARY', start)
        if end > start:
            return output[start:end].strip()

    # Pattern 3: PSEUDO-CODE STRUCTURE section
    if 'PSEUDO-CODE STRUCTURE' in output:
        start = output.find('PSEUDO-CODE STRUCTURE')
        end = output.find('OPTIMIZATION SUMMARY', start)
        if end > start:
            return output[start:end].strip()

    return None


def save_specification(pseudocode: str, requirement: str) -> Path:
    """Save pseudo-code as specification for cc10x."""
    try:
        spec_dir = Path('.claude/pseudo-code-prompting')
        spec_dir.mkdir(parents=True, exist_ok=True)

        spec_file = spec_dir / 'specification.md'
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{requirement}

## Generated Pseudo-Code
```
{pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        with open(spec_file, 'w') as f:
            f.write(spec_content)

        if os.environ.get('DEBUG'):
            print(f"DEBUG: Saved specification to {spec_file}", file=sys.stderr)

        return spec_file
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Failed to save specification: {e}", file=sys.stderr)
        raise


def add_specification_reference_section(spec_summary: str) -> str:
    """
    Create a specification reference section with preservation markers.

    This section includes special markers that signal to cc10x and other tools
    to preserve this section when updating context. The section is self-contained
    and references the specification file.

    Args:
        spec_summary: Brief summary of the specification

    Returns:
        Formatted specification section with preservation markers
    """
    spec_section = f"""## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE. Persisted specification reference. -->
<!-- This section contains critical implementation guidance and should be preserved. -->

**Source:** Pseudo-code specification
**File:** .claude/pseudo-code-prompting/specification.md
**Purpose:** Primary implementation guide generated from requirements
**Generated:** {datetime.now().isoformat()}

### Summary
{spec_summary[:400]}...

### How to Use
1. Review full specification at: `.claude/pseudo-code-prompting/specification.md`
2. Follow the pseudo-code phases and structure
3. Reference specification section in this context for quick access

<!-- END PSEUDO-CODE-CONTEXT -->
"""
    return spec_section


def inject_into_activecontext(pseudocode_summary: str) -> None:
    """
    Update cc10x activeContext.md with pseudo-code summary and specification reference.

    Strategy: Adds specification reference as a dedicated section with preservation
    markers. This makes the context "sticky" so it survives cc10x rewrites.
    """
    try:
        cc10x_dir = Path('.claude/cc10x')
        cc10x_dir.mkdir(parents=True, exist_ok=True)

        activecontext = cc10x_dir / 'activeContext.md'

        focus_content = f"""Implementing from pseudo-code specification:

{pseudocode_summary[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        spec_section = add_specification_reference_section(pseudocode_summary)

        if activecontext.exists():
            with open(activecontext, 'r') as f:
                content = f.read()

            # Strategy 1: Update Current Focus section
            if '## Current Focus' in content:
                pattern = r'(## Current Focus\n)(.*?)(\n## )'
                replacement = f'\\1{focus_content}\\3'
                updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
            else:
                updated = content

            # Strategy 2: Add or update Specification section
            # Check if specification section already exists
            if '## Specification' in updated:
                # Replace existing specification section
                pattern = r'(## Specification\n).*?(## |\Z)'
                replacement = f'{spec_section}\\2'
                updated = re.sub(pattern, replacement, updated, flags=re.DOTALL)
            else:
                # Append specification section before last section or at end
                # Insert before ## Blockers or ## Last Updated if they exist
                if '## Blockers' in updated:
                    pattern = r'(## Blockers)'
                    replacement = f'{spec_section}\\1'
                    updated = re.sub(pattern, replacement, updated)
                else:
                    # Append at end
                    updated = updated.rstrip() + '\n\n' + spec_section

            with open(activecontext, 'w') as f:
                f.write(updated)

            if os.environ.get('DEBUG'):
                print(f"DEBUG: Updated activeContext with Current Focus and Specification section", file=sys.stderr)

        else:
            # Create new activeContext with both sections
            new_context = f"""# Active Context
<!-- CC10X: Do not rename headings. Used as Edit anchors. -->

## Current Focus
{focus_content}

{spec_section}

## Recent Changes
- Pseudo-code specification generated from requirements

## Next Steps
1. Implement per pseudo-code specification phases
2. Follow BUILD workflow: component-builder → review → verify

## Decisions
- Use pseudo-code as primary specification
- Validate implementation against specification

## Learnings

## References
- Specification: .claude/pseudo-code-prompting/specification.md

## Blockers

## Last Updated
{datetime.now().isoformat()}
"""
            with open(activecontext, 'w') as f:
                f.write(new_context)

            if os.environ.get('DEBUG'):
                print(f"DEBUG: Created new activeContext with Specification section", file=sys.stderr)

    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Failed to update activeContext: {e}", file=sys.stderr)


def main():
    """
    Main logic: check workflow state and inject pseudo-code if needed.
    """
    # Read tool output from stdin
    output = sys.stdin.read().strip()

    if not output:
        return

    # Check if a pseudo-code workflow is active
    state = load_workflow_state()
    if not state or not state.get('workflow_active'):
        return

    # Check if this looks like pseudo-code output
    if 'TRANSFORMED PSEUDO-CODE' not in output and 'implement_' not in output:
        return

    if os.environ.get('DEBUG'):
        print(f"DEBUG: Pseudo-code workflow detected, checking for output", file=sys.stderr)

    # Extract pseudo-code from output
    pseudocode = extract_pseudocode(output)
    if not pseudocode:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: No pseudo-code pattern found in output", file=sys.stderr)
        return

    if os.environ.get('DEBUG'):
        print(f"DEBUG: Extracted pseudo-code, saving specification", file=sys.stderr)

    # Get requirement from state or use generic label
    requirement = state.get('requirement', 'Transform requirement')

    # Save the specification
    try:
        save_specification(pseudocode, requirement)
        inject_into_activecontext(pseudocode)

        if os.environ.get('DEBUG'):
            print(f"DEBUG: Successfully injected pseudo-code", file=sys.stderr)
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Injection failed: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
