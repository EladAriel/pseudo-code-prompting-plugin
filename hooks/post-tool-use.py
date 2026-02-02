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


def inject_into_activecontext(pseudocode_summary: str) -> None:
    """Update cc10x activeContext.md with pseudo-code summary."""
    try:
        cc10x_dir = Path('.claude/cc10x')
        cc10x_dir.mkdir(parents=True, exist_ok=True)

        activecontext = cc10x_dir / 'activeContext.md'

        focus_content = f"""Implementing from pseudo-code specification:

{pseudocode_summary[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        if activecontext.exists():
            with open(activecontext, 'r') as f:
                content = f.read()

            if '## Current Focus' in content:
                pattern = r'(## Current Focus\n)(.*?)(\n## )'
                replacement = f'\\1{focus_content}\\3'
                updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

                with open(activecontext, 'w') as f:
                    f.write(updated)

                if os.environ.get('DEBUG'):
                    print(f"DEBUG: Updated Current Focus in {activecontext}", file=sys.stderr)

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
