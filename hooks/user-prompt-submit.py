#!/usr/bin/env python3
"""
Simplified auto-detection hook for pseudo-code-prompting-plugin

Detects "Run transform:" and "Run validate:" patterns in user input
and routes to appropriate commands.

Key features:
- Auto-detects explicit "Run {command}:" format
- Routes to correct command file
- Removes orchestration complexity from v1
- No session memory, no context tree injection, no complex chaining
- NEW (v2.1.0): Automatic pseudo-code injection into cc10x activeContext
"""

import re
import sys
import os
from pathlib import Path
from datetime import datetime

def inject_pseudocode_to_cc10x(pseudocode_output: str, requirement: str) -> Path:
    """
    Save pseudo-code specification to cc10x context (v2.1.0).

    Implements specification-driven development by:
    1. Saving specification.md as persistent reference
    2. Updating activeContext.md with pseudo-code context
    3. Linking specification in memory files

    Args:
        pseudocode_output: Generated pseudo-code output
        requirement: Original user requirement

    Returns:
        Path to specification file (.claude/pseudo-code-prompting/specification.md)

    Side Effects:
        - Creates .claude/pseudo-code-prompting/ directory
        - Creates/updates .claude/pseudo-code-prompting/specification.md
        - Creates/updates .claude/cc10x/activeContext.md
    """
    try:
        # Step A: Save specification file
        spec_dir = Path('.claude/pseudo-code-prompting')
        spec_dir.mkdir(parents=True, exist_ok=True)

        spec_file = spec_dir / 'specification.md'
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{requirement}

## Generated Pseudo-Code
```
{pseudocode_output}
```

## Generated At
{datetime.now().isoformat()}
"""
        with open(spec_file, 'w') as f:
            f.write(spec_content)

        if os.environ.get('DEBUG'):
            print(f"DEBUG: Saved specification to {spec_file}", file=sys.stderr)

        # Step B: Create/Update activeContext.md with specification reference
        cc10x_dir = Path('.claude/cc10x')
        cc10x_dir.mkdir(parents=True, exist_ok=True)

        activecontext = cc10x_dir / 'activeContext.md'

        # Prepare focus content with pseudo-code summary
        focus_content = f"""Implementing from pseudo-code specification:

{pseudocode_output[:500]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        if activecontext.exists():
            # Update existing activeContext.md
            with open(activecontext, 'r') as f:
                content = f.read()

            # Use regex to safely update Current Focus section
            if '## Current Focus' in content:
                pattern = r'(## Current Focus\n)(.*?)(\n## )'
                replacement = f'\\1{focus_content}\\3'
                updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

                with open(activecontext, 'w') as f:
                    f.write(updated)

                if os.environ.get('DEBUG'):
                    print(f"DEBUG: Updated Current Focus in {activecontext}", file=sys.stderr)
            else:
                # Fallback: append if section missing
                with open(activecontext, 'a') as f:
                    f.write(f"\n## Current Focus\n{focus_content}\n")

                if os.environ.get('DEBUG'):
                    print(f"DEBUG: Appended Current Focus to {activecontext}", file=sys.stderr)
        else:
            # Create new activeContext.md with specification reference
            template = f"""# Active Context
<!-- CC10X: Do not rename headings. Used as Edit anchors. -->

## Current Focus
{focus_content}

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
                f.write(template)

            if os.environ.get('DEBUG'):
                print(f"DEBUG: Created new activeContext at {activecontext}", file=sys.stderr)

        return spec_file

    except Exception as e:
        # Log error but don't block workflow
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Injection error: {e}", file=sys.stderr)
        raise


def detect_command(user_input: str) -> tuple[str | None, str | None]:
    """
    Detect command pattern and extract task.

    Returns: (command_name, task_description) or (None, None)

    Supported patterns:
    - "Run transform: {requirement}"
    - "Run validate: {pseudo-code}"
    """

    # Pattern 1: Transform command
    transform_match = re.match(
        r'^Run\s+transform:\s+(.+)$',
        user_input.strip(),
        re.IGNORECASE | re.DOTALL
    )
    if transform_match:
        task = transform_match.group(1).strip()
        return ('transform', task)

    # Pattern 2: Validate command
    validate_match = re.match(
        r'^Run\s+validate:\s+(.+)$',
        user_input.strip(),
        re.IGNORECASE | re.DOTALL
    )
    if validate_match:
        task = validate_match.group(1).strip()
        return ('validate', task)

    return (None, None)


def main():
    """
    Entry point for hook execution.

    Reads user input from stdin, detects command, and outputs
    routing instructions.

    NEW (v2.1.0): After agent produces pseudo-code output, this hook
    also triggers injection into cc10x's activeContext.md via a
    companion injection handler (currently handled by agent output).
    """

    # Read user input
    user_input = sys.stdin.read().strip()

    if not user_input:
        return

    # Detect command
    command, task = detect_command(user_input)

    if command is None:
        # Not a pseudo-code-prompting command, skip hook
        return

    # Output routing instruction
    # This will be picked up by Claude Code to route to the appropriate command
    print(f"PSEUDO_CODE_COMMAND={command}")
    print(f"TASK={task}")

    # NEW (v2.1.0): Signal that injection may be needed after transform
    # The requirement-structurer agent will handle calling inject_pseudocode_to_cc10x()
    # after pseudo-code generation completes (Step 6 of pipeline)
    if command == 'transform':
        print(f"INJECT_PSEUDOCODE_AFTER_TRANSFORM=true")

    # Debug output (can be disabled in production)
    if os.environ.get('DEBUG'):
        print(f"DEBUG: Detected command '{command}' with task: {task[:100]}...",
              file=sys.stderr)
        if command == 'transform':
            print(f"DEBUG: Injection will be triggered after pseudo-code generation",
                  file=sys.stderr)


if __name__ == '__main__':
    main()
