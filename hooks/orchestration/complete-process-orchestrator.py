#!/usr/bin/env python3
"""
Claude Code Hook: Complete-Process Orchestrator
Event: Triggered on PostToolUse when complete-process pipeline agents complete
Purpose: Monitor transformation stages and filter outputs for clarity

This hook orchestrates the complete-process pipeline by:
1. Detecting which stage just completed (transform, validate, optimize)
2. Filtering output based on stage-specific requirements
3. Injecting stage transition markers for clarity
4. Accumulating pipeline state for post-execution cleanup

Stage-specific filtering:
- Transform: Extract ONLY pseudo-code function (remove verbose explanations)
- Validate: Keep FULL validation report (show all checks)
- Optimize: Extract ONLY optimized code + TODOs (remove intermediate steps)

Output markers signal pipeline progression:
- [TRANSFORM_COMPLETE] → [VALIDATE_COMPLETE] → [OPTIMIZE_COMPLETE]
"""

import json
import sys
import os
import re
from pathlib import Path

# Import the stage filter utility
# Handle relative import since this runs as subprocess
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from stage_output_filter import StageOutputFilter
except ImportError:
    # Fallback: define minimal filter if import fails
    class StageOutputFilter:
        @staticmethod
        def detect_stage(output):
            if 'requirement-validator' in output.lower() or 'NEXT_AGENT' in output:
                if 'requirement-validator' in output:
                    return 'transform'
                elif 'prompt-optimizer' in output:
                    return 'validate'
            if 'WORKFLOW_CONTINUES' in output and 'NO' in output:
                return 'optimize'
            return None

        @staticmethod
        def filter_transform_output(output):
            return f"[TRANSFORM_COMPLETE]\n{output}\n[PROCEEDING_TO_VALIDATION]"

        @staticmethod
        def filter_validate_output(output):
            return f"[VALIDATE_COMPLETE]\n{output}\n[PROCEEDING_TO_OPTIMIZATION]"

        @staticmethod
        def filter_optimize_output(output):
            return f"[OPTIMIZE_COMPLETE]\n{output}"

        @staticmethod
        def is_pipeline_complete(output):
            return 'WORKFLOW_CONTINUES' in output and 'NO' in output


def get_plugin_root():
    """Get plugin root directory from environment or parent directory calculation."""
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if plugin_root:
        return plugin_root

    # Fallback: calculate from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # hooks/orchestration/complete-process-orchestrator.py -> plugin root
    return os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))


def get_memory_file(filename):
    """Get path to memory file in .claude/pseudo-code-prompting directory."""
    plugin_root = get_plugin_root()
    memory_dir = Path(plugin_root) / '.claude' / 'pseudo-code-prompting'
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir / filename


def load_pipeline_state():
    """Load current pipeline state from memory."""
    state_file = get_memory_file('pipeline-state.json')
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {'current_stage': None, 'stages_completed': [], 'outputs': {}}


def save_pipeline_state(state):
    """Save pipeline state to memory."""
    state_file = get_memory_file('pipeline-state.json')
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError:
        pass  # Silently fail if can't write state


def detect_pipeline_trigger(prompt):
    """Detect if this is a complete-process pipeline skill invocation."""
    # Check if the prompt indicates a transformation pipeline skill was invoked
    pipeline_skills = [
        'prompt-structurer',
        'prompt-transformer',
        'requirement-validator',
        'prompt-optimizer',
        'complete-process-orchestrator'
    ]

    for skill in pipeline_skills:
        if skill in prompt.lower():
            return True

    # Also check for workflow control markers
    if 'WORKFLOW_CONTINUES' in prompt or 'NEXT_AGENT' in prompt:
        return True

    return False


def main():
    """Main orchestrator hook logic."""
    # Read hook input from stdin (JSON format)
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get('prompt', '')
    tool_output = data.get('tool_output', '')
    tool_name = data.get('tool_name', '')

    # Check if prompt is empty
    if not prompt:
        sys.exit(0)

    # Only process if this is a pipeline skill invocation
    if not detect_pipeline_trigger(prompt):
        sys.exit(0)

    # Combine prompt and output for analysis
    full_output = f"{prompt}\n{tool_output}" if tool_output else prompt

    # Detect which stage just completed
    stage = StageOutputFilter.detect_stage(full_output)

    if not stage:
        # Not a recognized stage, pass through
        sys.exit(0)

    # Load current pipeline state
    state = load_pipeline_state()

    # Filter output based on detected stage
    try:
        if stage == 'transform':
            filtered_output = StageOutputFilter.filter_transform_output(full_output)
        elif stage == 'validate':
            filtered_output = StageOutputFilter.filter_validate_output(full_output)
        elif stage == 'optimize':
            filtered_output = StageOutputFilter.filter_optimize_output(full_output)
        else:
            filtered_output = full_output
    except Exception as e:
        # Graceful degradation: if filtering fails, pass through
        sys.stderr.write(f"Filter error: {e}\n")
        sys.exit(0)

    # Update pipeline state
    state['current_stage'] = stage
    if stage not in state['stages_completed']:
        state['stages_completed'].append(stage)
    state['outputs'][stage] = filtered_output

    # Save updated state
    save_pipeline_state(state)

    # Output filtered result to stdout
    print(filtered_output)
    sys.exit(0)


if __name__ == '__main__':
    main()
