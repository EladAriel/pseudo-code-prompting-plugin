#!/usr/bin/env python3
"""
Claude Code Hook: ContextAwareTreeInjection
Event: Triggered on UserPromptSubmit when implementation keywords detected
Purpose: Inject project structure context for architecture-aware suggestions

This hook:
1. Detects implementation keywords (implement, create, add, refactor, etc.)
2. Executes Python script to generate project tree structure
3. Injects tree context into Claude's prompt for better file placement decisions
4. Activates context-aware transformation mode
"""

import json
import sys
import os
import subprocess
import re

def main():
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

    # Keyword detection - match action verbs indicating project implementation work
    implementation_keywords = ['implement', 'create', 'add', 'refactor', 'build', 'generate', 'setup', 'initialize']

    if not any(keyword in prompt.lower() for keyword in implementation_keywords):
        sys.exit(0)

    # Get plugin root directory
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if not plugin_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_root = os.path.dirname(os.path.dirname(script_dir))

    python_script = os.path.join(plugin_root, 'hooks', 'tree', 'get_context_tree.py')

    # Check if Python script exists
    if not os.path.isfile(python_script):
        sys.exit(0)

    # Detect Python command (try python3 first, fallback to python)
    python_cmd = 'python3'
    try:
        subprocess.run([python_cmd, '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        python_cmd = 'python'
        try:
            subprocess.run([python_cmd, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            sys.exit(0)

    # Execute Python script with timeout (15 seconds)
    try:
        result = subprocess.run(
            [python_cmd, python_script, cwd, '--max-depth', '10', '--max-files', '1000'],
            capture_output=True,
            text=True,
            timeout=15
        )
        tree_output = result.stdout
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
        sys.exit(0)

    # Check if tree generation failed or returned error
    if not tree_output or '[ERROR:' in tree_output or tree_output.strip() == '[TREE_ERROR]':
        sys.exit(0)

    # Inject tree context into prompt
    print(f"""
[CONTEXT-AWARE MODE ACTIVATED]

Project Structure:
```
{tree_output}
```

Use this project structure as context for the request: "{prompt}"

When responding:
1. Reference existing files and directories from the structure above
2. Suggest modifications that align with the current architecture
3. Identify where new files should be placed based on existing patterns
4. Detect the technology stack from visible files (package.json, requirements.txt, go.mod, etc.)

If the project is empty (`<<PROJECT_EMPTY_NO_STRUCTURE>>`), use the `/context-aware-transform` command to create a virtual skeleton based on stack detection.
""")
    sys.exit(0)

if __name__ == '__main__':
    main()
