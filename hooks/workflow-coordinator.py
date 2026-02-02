#!/usr/bin/env python3
"""
Workflow Coordinator Hook - Prevent cc10x Hijacking

This hook coordinates execution between pseudocode plugin and cc10x router
to prevent cc10x from hijacking the transform workflow.

MECHANISM:
1. Detect if user input is a pseudocode command ("Run transform:" or "Run validate:")
2. If YES: Set environment signals to block cc10x router temporarily
3. Allow pseudocode plugin to complete with bridge handoff
4. Only then allow cc10x to be invoked (via user's bridge YES answer)

SIGNALS EMITTED:
- PSEUDOCODE_PLUGIN_ACTIVE=true  → Plugin is running
- BLOCK_CC10X_ROUTER=true         → cc10x should stand down
- WORKFLOW_PRIORITY=pseudocode    → Transform takes priority
- WORKFLOW_HANDOFF_EXPECTED=true  → Bridge handoff will follow
"""

import re
import sys
import os
import json
from pathlib import Path


def is_pseudocode_command(user_input: str) -> bool:
    """
    Check if input is a pseudocode plugin command.

    Supported patterns:
    - "Run transform: ..."
    - "Run validate: ..."
    """
    pseudocode_patterns = [
        r'^Run\s+transform:',
        r'^Run\s+validate:',
    ]
    for pattern in pseudocode_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False


def extract_task_requirement(user_input: str) -> str:
    """Extract the requirement/task from the command."""
    # Match "Run transform: ..." or "Run validate: ..."
    match = re.search(r'^Run\s+(?:transform|validate):\s+(.+)$', user_input, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def get_command_type(user_input: str) -> tuple[str | None, str | None]:
    """
    Extract which pseudocode command is being run and map to agent.

    Returns: (command_type, agent_name) or (None, None)
    """
    if re.search(r'^Run\s+transform:', user_input, re.IGNORECASE):
        return ('transform', 'pseudo-code-prompting-plugin-v2:requirement-structurer')
    if re.search(r'^Run\s+validate:', user_input, re.IGNORECASE):
        return ('validate', 'pseudo-code-prompting-plugin-v2:requirement-validator')
    return (None, None)


def emit_signal(signal_name: str, value: str) -> None:
    """Emit a control signal for workflow coordination."""
    print(f"{signal_name}={value}")


def create_coordination_state(command_type: str, requirement: str = "") -> dict:
    """Create workflow coordination state file."""
    state = {
        'workflow_active': True,
        'active_plugin': 'pseudo-code-prompting',
        'command_type': command_type,
        'requirement': requirement,
        'cc10x_blocked': True,
        'bridge_expected': True,
        'timestamp': __import__('datetime').datetime.now().isoformat(),
    }
    return state


def save_coordination_state(state: dict) -> None:
    """Save workflow coordination state to file."""
    state_dir = Path('.claude/pseudo-code-prompting')
    state_dir.mkdir(parents=True, exist_ok=True)

    state_file = state_dir / 'workflow-state.json'
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG: Could not save state: {e}", file=sys.stderr)


def log_coordination(message: str) -> None:
    """Log coordination action for debugging."""
    if os.environ.get('DEBUG'):
        print(f"DEBUG [COORDINATOR]: {message}", file=sys.stderr)


def main():
    """
    Main coordination logic.

    If pseudocode command detected:
    1. Emit signals to block cc10x with correct agent mapping
    2. Save coordination state
    3. Allow pseudocode plugin to run
    4. Bridge handoff protocol takes over

    If no pseudocode command:
    1. Don't interfere, let normal flow proceed
    2. Allow cc10x to run if triggered
    """
    user_input = sys.stdin.read().strip()

    if not user_input:
        return

    # Check if this is a pseudocode plugin command
    if not is_pseudocode_command(user_input):
        # Not our concern, let other systems handle it
        log_coordination("Not a pseudocode command, allowing normal flow")
        return

    # Extract command type and agent mapping
    command_type, agent_name = get_command_type(user_input)
    if not command_type or not agent_name:
        return

    log_coordination(f"Detected pseudocode command: {command_type} → {agent_name}")

    # Extract requirement for later injection
    requirement = extract_task_requirement(user_input)

    # Emit coordination signals
    emit_signal("PSEUDOCODE_PLUGIN_ACTIVE", "true")
    emit_signal("BLOCK_CC10X_ROUTER", "true")
    emit_signal("WORKFLOW_PRIORITY", "pseudocode-plugin")
    emit_signal("WORKFLOW_HANDOFF_EXPECTED", "true")
    emit_signal("COMMAND_TYPE", command_type)
    emit_signal("PSEUDOCODE_AGENT", agent_name)

    # Create and save coordination state with requirement
    state = create_coordination_state(command_type, requirement)
    save_coordination_state(state)

    log_coordination(
        f"Coordination state saved. "
        f"Command: {command_type}, Agent: {agent_name}, "
        f"cc10x blocked until bridge handoff"
    )

    # Optional: Provide status message
    if os.environ.get('VERBOSE'):
        print(
            f"\n🔒 Workflow Coordinator: Pseudocode plugin active. "
            f"cc10x router blocked until transform completes."
            f"\n   Command: {command_type}"
            f"\n   Agent: {agent_name}"
            f"\n   Bridge protocol: ENABLED"
            f"\n   When transform asks 'Ready to implement?', answer YES "
            f"to auto-invoke cc10x with specification."
        )


if __name__ == '__main__':
    main()
