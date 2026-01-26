#!/usr/bin/env python3
"""
Claude Code Hook: Complete-Process Tree Injection
Event: Triggered on UserPromptSubmit when /complete-process command detected
Purpose: Inject project structure context before complete-process pipeline starts

This pre-execution hook:
1. Detects /complete-process command invocation
2. Extracts implementation keywords from the query
3. Generates project structure tree
4. Injects context with marker [COMPLETE_PROCESS_CONTEXT_INJECTION]
5. Activates context-aware transformation mode

The injected context helps Claude understand:
- Project structure for intelligent file placement
- Technology stack for implementation guidance
- Existing patterns for consistency
"""

import json
import sys
import os
import subprocess
import re
from pathlib import Path


def get_plugin_root():
    """Get plugin root directory from environment or calculate from script location."""
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if plugin_root:
        return plugin_root

    # Fallback: calculate from script location
    # hooks/orchestration/complete-process-tree-injection.py -> plugin root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))


def main():
    """Main pre-execution hook logic."""
    # Read hook input from stdin (JSON format)
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get('prompt', '')
    cwd = data.get('cwd', os.getcwd())

    # Check if prompt is empty
    if not prompt:
        sys.exit(0)

    # Detect complete-process command patterns
    complete_process_patterns = [
        r'/complete-process\s+',
        r'/complete\s+',
        r'/full-transform\s+',
        r'/orchestrate\s+',
        r'[Rr]un\s+complete-process',
        r'[Rr]un\s+complete\s+',
        r'[Uu]se\s+complete-process',
    ]

    is_complete_process = any(
        re.search(pattern, prompt) for pattern in complete_process_patterns
    )

    if not is_complete_process:
        sys.exit(0)

    # Extract the query part (after the command)
    query_match = re.search(r'/(?:complete-process|complete|full-transform|orchestrate)\s+(.+?)$', prompt)
    query = query_match.group(1) if query_match else prompt

    # Check for implementation keywords to confirm tree injection is needed
    implementation_keywords = [
        'implement', 'create', 'add', 'refactor', 'build', 'generate',
        'setup', 'initialize', 'develop', 'design', 'architect'
    ]

    has_implementation_keyword = any(
        keyword in query.lower() for keyword in implementation_keywords
    )

    # If no implementation keywords, still proceed but be conservative
    # (tree injection can help even for questions)

    # Get plugin root and locate tree generation script
    plugin_root = get_plugin_root()
    python_script = os.path.join(plugin_root, 'hooks', 'tree', 'get_context_tree.py')

    # Check if Python script exists
    if not os.path.isfile(python_script):
        sys.exit(0)

    # Generate project tree
    try:
        # Try python3 first, fallback to python
        python_cmd = 'python3'
        try:
            result = subprocess.run(
                [python_cmd, python_script, cwd, '--max-depth', '10', '--max-files', '1000'],
                capture_output=True,
                text=True,
                timeout=15
            )
        except FileNotFoundError:
            # Fallback to 'python'
            python_cmd = 'python'
            result = subprocess.run(
                [python_cmd, python_script, cwd, '--max-depth', '10', '--max-files', '1000'],
                capture_output=True,
                text=True,
                timeout=15
            )

        if result.returncode != 0:
            # Tree generation failed, pass through
            sys.exit(0)

        tree_output = result.stdout.strip()

        # Check if tree is empty
        if not tree_output or tree_output.startswith('<<PROJECT_EMPTY'):
            # Empty project, skip context injection
            sys.exit(0)

        # Inject context
        print(f"""
[COMPLETE_PROCESS_CONTEXT_INJECTION]

Project structure will be analyzed for context-aware transformation:

[COMPLETE_PROCESS_CONTEXT_START]
```
{tree_output}
```
[COMPLETE_PROCESS_CONTEXT_END]

This project context will help the complete-process pipeline:
- Make intelligent decisions about file placement
- Understand the technology stack
- Apply consistent patterns with existing code
- Generate implementation-ready pseudo-code

Proceeding with complete-process pipeline...
""")
        sys.exit(0)

    except subprocess.TimeoutExpired:
        # Tree generation timed out, pass through
        sys.exit(0)

    except Exception as e:
        # Any other error, pass through silently
        sys.stderr.write(f"Tree injection error: {e}\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
