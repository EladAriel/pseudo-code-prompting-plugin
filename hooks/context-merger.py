#!/usr/bin/env python3
"""
Context Merger Utility - Intelligently merge pseudo-code and cc10x contexts

This utility handles merging of pseudo-code context with cc10x's session-memory context
to prevent context overwrites from losing critical information.

PROBLEM IT SOLVES:
When cc10x writes to activeContext.md, it replaces the entire file. This loses any
pseudo-code specification references that were injected by the pseudo-code plugin.

SOLUTION:
This merger extracts pseudo-code context before cc10x writes, then merges it back
after to preserve both contexts.

USAGE:
From other hooks or tools:
    merged = merge_contexts(existing_cc10x, preserved_pseudo_code)
"""

import re
import os
import sys
from pathlib import Path
from typing import Tuple


def extract_pseudo_context(content: str) -> str | None:
    """
    Extract PSEUDO-CODE-CONTEXT section from markdown content.

    Returns:
        The Specification section if found, None otherwise
    """
    # Pattern: from ## Specification to next ## section or end of file
    match = re.search(
        r'(## Specification\n<!--.*?END PSEUDO-CODE-CONTEXT -->)',
        content,
        re.DOTALL
    )
    if match:
        return match.group(1)
    return None


def remove_pseudo_context(content: str) -> str:
    """
    Remove PSEUDO-CODE-CONTEXT section from markdown content.

    This is used when preparing content for backup or analysis.

    Returns:
        Content with Specification section removed
    """
    # Remove ## Specification section and its content
    pattern = r'\n## Specification\n<!--.*?END PSEUDO-CODE-CONTEXT -->\n'
    return re.sub(pattern, '\n', content, flags=re.DOTALL)


def merge_contexts(cc10x_context: str, pseudo_context: str | None) -> str:
    """
    Merge cc10x context with preserved pseudo-code context.

    Algorithm:
    1. Start with cc10x's fresh context
    2. If pseudo-context exists and cc10x doesn't have it, insert it
    3. Preserve section order for readability
    4. Return merged context

    Args:
        cc10x_context: The fresh context from cc10x
        pseudo_context: Preserved pseudo-code context (if any)

    Returns:
        Merged context with both sections intact
    """
    if not pseudo_context:
        return cc10x_context

    # Check if Specification section already exists in cc10x context
    if '## Specification' in cc10x_context:
        # Already has it, return as-is
        return cc10x_context

    # Find insertion point: before ## Blockers or ## Last Updated
    # These are typically near the end, so insert Specification before them
    insertion_point_patterns = [
        r'(## Blockers)',
        r'(## Last Updated)',
        r'(## References)',
    ]

    for pattern in insertion_point_patterns:
        if re.search(pattern, cc10x_context):
            # Insert before this section
            return re.sub(
                pattern,
                pseudo_context + '\n\n\\1',
                cc10x_context,
                flags=re.DOTALL
            )

    # Fallback: append before final newlines
    return cc10x_context.rstrip() + '\n\n' + pseudo_context + '\n'


def preserve_specification_from_file(spec_file: Path) -> str | None:
    """
    Load specification from file and format as context section.

    This is used by recovery mechanisms to restore lost specifications.

    Args:
        spec_file: Path to specification.md file

    Returns:
        Formatted specification section or None if file not found
    """
    if not spec_file.exists():
        return None

    try:
        with open(spec_file, 'r') as f:
            spec_content = f.read()

        # Format as context section
        section = f"""## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE. Persisted specification reference. -->
<!-- Recovered from: {spec_file} -->

**Source:** Pseudo-code specification
**File:** .claude/pseudo-code-prompting/specification.md
**Purpose:** Primary implementation guide generated from requirements

### Full Specification
{spec_content}

<!-- END PSEUDO-CODE-CONTEXT -->
"""
        return section

    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"DEBUG [ContextMerger]: Could not load specification: {e}", file=sys.stderr)
        return None


def verify_context_integrity(content: str, requirement: str = "has specification") -> bool:
    """
    Verify that context contains expected sections.

    Args:
        content: Markdown content to verify
        requirement: What to check for (e.g., "has specification")

    Returns:
        True if requirement is met, False otherwise
    """
    if requirement == "has specification":
        return '## Specification' in content and 'PSEUDO-CODE-CONTEXT' in content
    elif requirement == "has current focus":
        return '## Current Focus' in content
    elif requirement == "is valid context":
        return '# Active Context' in content or '## Current Focus' in content

    return False


def log_merge_action(message: str) -> None:
    """Log merge action for debugging."""
    if os.environ.get('DEBUG'):
        print(f"DEBUG [ContextMerger]: {message}", file=sys.stderr)


def main():
    """
    CLI usage for context merger utility.

    Reads from stdin and outputs merged context.

    Usage:
        echo "$cc10x_context" | python3 context-merger.py --extract
        echo "$cc10x_context" | python3 context-merger.py --verify
    """
    content = sys.stdin.read()

    if '--extract' in sys.argv:
        # Extract pseudo-code context
        pseudo_ctx = extract_pseudo_context(content)
        if pseudo_ctx:
            print(pseudo_ctx)
        sys.exit(0)

    if '--verify' in sys.argv:
        # Verify context integrity
        has_spec = verify_context_integrity(content, "has specification")
        print("1" if has_spec else "0")
        sys.exit(0)

    if '--remove-pseudo' in sys.argv:
        # Remove pseudo-context
        cleaned = remove_pseudo_context(content)
        print(cleaned)
        sys.exit(0)

    # Default: output content as-is with merge markers
    print(content)


if __name__ == '__main__':
    main()
