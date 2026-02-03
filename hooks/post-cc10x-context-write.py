#!/usr/bin/env python3
"""
Post-CC10X Context Write Hook - Recovery Mechanism for Lost Specifications

This hook runs after cc10x writes to activeContext.md (via PostToolUse or custom trigger).

PROBLEM IT SOLVES:
Even with specification markers, cc10x might overwrite activeContext.md completely,
losing the pseudo-code specification reference. This hook acts as a safety net.

MECHANISM:
1. Detects if specification reference was lost from activeContext.md
2. Checks if specification.md exists in .claude/pseudo-code-prompting/
3. If specification exists but isn't in activeContext: restores it
4. Ensures specification is always findable by cc10x

This is a REACTIVE recovery mechanism - prevention happens in post-tool-use.py,
but this catches any edge cases where prevention failed.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime


def load_specification_file() -> str | None:
    """
    Load specification.md from pseudo-code-prompting directory.

    Returns:
        Content of specification.md or None if not found
    """
    spec_file = Path('.claude/pseudo-code-prompting/specification.md')
    if spec_file.exists():
        try:
            with open(spec_file, 'r') as f:
                return f.read()
        except Exception as e:
            if os.environ.get('DEBUG'):
                print(f"DEBUG [PostCC10X]: Could not load specification: {e}", file=sys.stderr)
    return None


def load_activecontext() -> str | None:
    """
    Load activeContext.md from cc10x directory.

    Returns:
        Content of activeContext.md or None if not found
    """
    ctx_file = Path('.claude/cc10x/activeContext.md')
    if ctx_file.exists():
        try:
            with open(ctx_file, 'r') as f:
                return f.read()
        except Exception as e:
            if os.environ.get('DEBUG'):
                print(f"DEBUG [PostCC10X]: Could not load activeContext: {e}", file=sys.stderr)
    return None


def has_specification_reference(content: str) -> bool:
    """
    Check if content has specification reference.

    Returns:
        True if ## Specification section exists with PSEUDO-CODE-CONTEXT marker
    """
    return '## Specification' in content and 'PSEUDO-CODE-CONTEXT' in content


def build_specification_section(spec_content: str) -> str:
    """
    Build a specification section from full specification content.

    Args:
        spec_content: Full specification.md content

    Returns:
        Formatted specification section with preservation markers
    """
    section = f"""## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE. Persisted specification reference. -->
<!-- This section was recovered after context write. -->

**Source:** Pseudo-code specification
**File:** .claude/pseudo-code-prompting/specification.md
**Purpose:** Primary implementation guide generated from requirements
**Recovered:** {datetime.now().isoformat()}

### Full Specification
{spec_content}

<!-- END PSEUDO-CODE-CONTEXT -->
"""
    return section


def inject_specification_section(activecontext: str, spec_section: str) -> str:
    """
    Inject specification section into activeContext content.

    Strategy: Insert before ## Blockers or at end if not present.

    Args:
        activecontext: Current activeContext.md content
        spec_section: Formatted specification section

    Returns:
        Updated activeContext with specification section
    """
    # Find insertion point before ## Blockers
    if '## Blockers' in activecontext:
        pattern = r'(## Blockers)'
        return re.sub(
            pattern,
            spec_section + '\n\n\\1',
            activecontext,
            flags=re.DOTALL
        )

    # Fallback: insert before ## Last Updated if present
    if '## Last Updated' in activecontext:
        pattern = r'(## Last Updated)'
        return re.sub(
            pattern,
            spec_section + '\n\n\\1',
            activecontext,
            flags=re.DOTALL
        )

    # Last resort: append at end
    return activecontext.rstrip() + '\n\n' + spec_section + '\n'


def save_activecontext(content: str) -> bool:
    """
    Save updated activeContext.md.

    Returns:
        True if successful, False otherwise
    """
    try:
        ctx_file = Path('.claude/cc10x/activeContext.md')
        with open(ctx_file, 'w') as f:
            f.write(content)

        if os.environ.get('DEBUG'):
            print(f"DEBUG [PostCC10X]: Saved updated activeContext", file=sys.stderr)

        return True
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG [PostCC10X]: Failed to save activeContext: {e}", file=sys.stderr)
        return False


def check_workflow_state() -> bool:
    """
    Check if pseudo-code workflow is active.

    Returns:
        True if workflow was active (i.e., a transform/validate was done)
    """
    try:
        state_file = Path('.claude/pseudo-code-prompting/workflow-state.json')
        if state_file.exists():
            import json
            with open(state_file, 'r') as f:
                state = json.load(f)
            return state.get('workflow_active', False)
    except Exception:
        pass
    return False


def log_recovery(message: str) -> None:
    """Log recovery action."""
    if os.environ.get('DEBUG'):
        print(f"DEBUG [PostCC10X]: {message}", file=sys.stderr)


def main():
    """
    Main recovery logic.

    1. Check if specification.md exists
    2. Check if activeContext.md exists
    3. If specification exists but not in activeContext: restore it
    4. Save updated activeContext
    """
    # Check if workflow was active (only recover if pseudo-code was generated)
    if not check_workflow_state():
        log_recovery("No active workflow, skipping recovery")
        return

    log_recovery("Checking for lost specification...")

    # Load specification if it exists
    spec_content = load_specification_file()
    if not spec_content:
        log_recovery("No specification.md found, nothing to recover")
        return

    log_recovery("Specification.md found, checking activeContext...")

    # Load activeContext if it exists
    activecontext = load_activecontext()
    if not activecontext:
        log_recovery("No activeContext.md found, recovery not needed")
        return

    # Check if specification reference exists
    if has_specification_reference(activecontext):
        log_recovery("Specification reference already present, no recovery needed")
        return

    # Specification is missing from activeContext - restore it
    log_recovery("Specification reference LOST - recovering...")

    spec_section = build_specification_section(spec_content)
    updated_context = inject_specification_section(activecontext, spec_section)

    if save_activecontext(updated_context):
        log_recovery("✓ Specification reference RECOVERED successfully")
        if os.environ.get('VERBOSE'):
            print("\n📋 Recovery: Pseudo-code specification reference restored to activeContext.md",
                  file=sys.stderr)
    else:
        log_recovery("✗ Failed to save recovered context")


if __name__ == '__main__':
    main()
