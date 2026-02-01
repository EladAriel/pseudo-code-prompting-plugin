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
"""

import re
import sys
import os

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

    # Debug output (can be disabled in production)
    if os.environ.get('DEBUG'):
        print(f"DEBUG: Detected command '{command}' with task: {task[:100]}...",
              file=sys.stderr)


if __name__ == '__main__':
    main()
