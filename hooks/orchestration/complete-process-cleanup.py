#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Hook: Complete-Process Cleanup
Event: Triggered on PostToolUse when complete-process pipeline completes
Purpose: Clean intermediate messages and format final output for new conversations

This post-execution hook:
1. Detects when the entire pipeline is complete (WORKFLOW_CONTINUES: NO)
2. Extracts final optimized pseudo-code
3. Removes intermediate transform/validate outputs
4. Formats clean final message with optimizations summary and TODOs
5. Signals readiness for next phase (feature implementation)

Output formatting removes cognitive load by presenting only:
- Final optimized pseudo-code (the main deliverable)
- What improvements were applied (context for implementation)
- Implementation tasks (ready for /feature-dev)
"""

import json
import sys
import os
import re
from pathlib import Path

# Handle encoding for Windows
if sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_plugin_root():
    """Get plugin root directory from environment or calculate from script location."""
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if plugin_root:
        return plugin_root

    # Fallback: calculate from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))


def get_memory_file(filename):
    """Get path to memory file in .claude/pseudo-code-prompting directory."""
    plugin_root = get_plugin_root()
    memory_dir = Path(plugin_root) / '.claude' / 'pseudo-code-prompting'
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir / filename


def extract_optimized_code(output):
    """Extract optimized pseudo-code function from output."""
    # Pattern 1: Optimized: function_name(...)
    match = re.search(
        r'(Optimized:)?\s*(\w+\([^)]*(?:\n[^)]*)*\))',
        output,
        re.DOTALL
    )
    if match:
        return match.group(2).strip()

    # Pattern 2: Multi-line function with brackets
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if re.search(r'^\w+\s*\(', line):
            func_lines = [line]
            paren_count = line.count('(') - line.count(')')
            for next_line in lines[i+1:]:
                func_lines.append(next_line)
                paren_count += next_line.count('(') - next_line.count(')')
                if paren_count == 0:
                    break
            return '\n'.join(func_lines)

    return output


def extract_todos(output):
    """Extract TODO items from output."""
    todos = []

    # Pattern 1: TODO_LIST in JSON array
    todo_match = re.search(r'TODO_LIST:\s*\[(.*?)\]', output, re.DOTALL)
    if todo_match:
        items_str = todo_match.group(1)
        # Split by comma and clean up
        items = [item.strip().strip('"\'') for item in items_str.split(',')]
        todos.extend([item for item in items if item])

    # Pattern 2: Markdown list items (- or • or *)
    md_items = re.findall(r'^\s*[-•*]\s+(.+?)$', output, re.MULTILINE)
    todos.extend([item.strip() for item in md_items])

    # Pattern 3: Numbered items
    numbered = re.findall(r'^\s*\d+\.\s+(.+?)$', output, re.MULTILINE)
    todos.extend([item.strip() for item in numbered])

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for todo in todos:
        if todo not in seen:
            seen.add(todo)
            unique.append(todo)

    return unique


def extract_improvements(output):
    """Extract improvement items from optimizer output."""
    improvements = []

    # Look for improvements section
    improvements_match = re.search(
        r'(?:IMPROVEMENTS?|Improvements?)[:\s]*(?:MADE|Applied)?:?\s*(.*?)(?=\n\n|\n\[|$)',
        output,
        re.DOTALL | re.IGNORECASE
    )

    if improvements_match:
        improvements_text = improvements_match.group(1)
        # Extract items (bullet, numbered, or category headers)
        items = re.findall(r'[-•*✓]\s+(.+?)(?=\n[-•*✓]|\n\n|$)', improvements_text, re.DOTALL)
        improvements.extend([item.strip() for item in items])

    return improvements


def detect_validation_status(output):
    """Detect validation status from output."""
    # Look for validation results
    if re.search(r'(?:All checks passed|✓.*passed|PASSED)', output, re.IGNORECASE):
        return 'passed'
    elif re.search(r'(?:warnings?|⚠)', output, re.IGNORECASE):
        return 'warnings'
    elif re.search(r'(?:failed|✗|FAILED)', output, re.IGNORECASE):
        return 'failed'

    return 'unknown'


def main():
    """Main post-execution cleanup hook logic."""
    # Read hook input from stdin (JSON format)
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get('prompt', '')
    tool_output = data.get('tool_output', '')

    # Check if prompt is empty
    if not prompt:
        sys.exit(0)

    # Combine for analysis
    full_output = f"{prompt}\n{tool_output}" if tool_output else prompt

    # Check if pipeline is complete (WORKFLOW_CONTINUES: NO or CHAIN_COMPLETE marker)
    if not re.search(
        r'WORKFLOW_CONTINUES:\s*("NO"|NO)|CHAIN_COMPLETE:',
        full_output
    ):
        # Pipeline not complete yet, pass through
        sys.exit(0)

    # Load pipeline state if available
    state_file = get_memory_file('pipeline-state.json')
    pipeline_state = {}
    if state_file.exists():
        try:
            pipeline_state = json.loads(state_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass

    # Extract final results
    optimized_code = extract_optimized_code(full_output)
    todos = extract_todos(full_output)
    improvements = extract_improvements(full_output)
    validation_status = detect_validation_status(full_output)

    # Build cleaned output
    output_lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "✓ COMPLETE-PROCESS PIPELINE COMPLETE",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "OPTIMIZED PSEUDO-CODE:",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        optimized_code,
        "",
    ]

    # Add validation status if there were warnings
    if validation_status == 'warnings':
        output_lines.extend([
            "VALIDATION STATUS: ⚠ Warnings resolved during optimization",
            "",
        ])
    elif validation_status == 'failed':
        output_lines.extend([
            "VALIDATION STATUS: ⚠ Some issues remain (review above)",
            "",
        ])

    # Add improvements if any
    if improvements:
        output_lines.extend([
            "IMPROVEMENTS APPLIED:",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ])
        for improvement in improvements[:5]:  # Limit to top 5
            output_lines.append(f"✓ {improvement}")
        if len(improvements) > 5:
            output_lines.append(f"+ {len(improvements) - 5} more improvements")
        output_lines.append("")

    # Add TODOs if any
    if todos:
        output_lines.extend([
            "READY FOR IMPLEMENTATION - TODOs:",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ])
        for i, todo in enumerate(todos, 1):
            output_lines.append(f"{i}. {todo}")
        output_lines.extend([
            "",
            "→ Use /feature-dev to implement with this pseudo-code",
        ])
    else:
        output_lines.extend([
            "",
            "→ Ready for implementation! Use /feature-dev with the optimized pseudo-code above.",
        ])

    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Pipeline state: mark as complete
    pipeline_state['status'] = 'complete'
    pipeline_state['final_code'] = optimized_code
    pipeline_state['todos'] = todos

    # Save final state
    try:
        state_file.write_text(json.dumps(pipeline_state, indent=2))
    except IOError:
        pass  # Silently fail if can't write

    # Output the cleaned final message
    print('\n'.join(output_lines))
    sys.exit(0)


if __name__ == '__main__':
    main()
