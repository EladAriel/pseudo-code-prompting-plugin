#!/usr/bin/env python3
"""
Claude Code Hook: ContextCompressionHelper
Event: Triggered when verbose requirements are detected
Purpose: Suggest context compression for lengthy specifications

This hook:
1. Detects when user provides verbose, multi-sentence requirements
2. Suggests using context-compressor skill for better efficiency
3. Helps maintain token efficiency in conversations
"""

import json
import sys
import re

def main():
    # Read hook input from stdin (JSON format)
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get('prompt', '')

    # Check if prompt is empty
    if not prompt:
        sys.exit(0)

    # Count words in the prompt (rough metric for verbosity)
    word_count = len(prompt.split())

    # Detect verbose requirements (more than 100 words and contains requirement keywords)
    if word_count > 100:
        requirement_keywords = ['implement', 'create', 'add', 'build', 'need', 'want', 'should', 'must', 'require']
        feature_keywords = ['feature', 'endpoint', 'authentication', 'database', 'API', 'system', 'function', 'service']

        has_requirement = any(keyword in prompt.lower() for keyword in requirement_keywords)
        has_feature = any(keyword in prompt.lower() for keyword in feature_keywords)

        if has_requirement and has_feature:
            print(f"""
[VERBOSE REQUIREMENT DETECTED - {word_count} words]

Tip: Consider using the context-compressor skill or /compress-context command to transform verbose requirements into concise pseudo-code format. This will:
- Reduce token usage by 60-95%
- Create structured, implementation-ready specifications
- Preserve all critical information
- Improve clarity and maintainability

Example: /compress-context [your verbose requirement]

Proceeding with current request...
""")
            sys.exit(0)

    # Check for explicit compression commands
    if prompt.startswith('/compress ') or prompt.startswith('/compress-context '):
        print("""
[CONTEXT COMPRESSION MODE]

Applying compression techniques to transform verbose requirements into concise pseudo-code:

1. Extract Core Intent: Identify main action and objective
2. Distill Parameters: Convert prose into structured key-value pairs
3. Preserve Constraints: Keep all validation, security, and performance requirements
4. Eliminate Redundancy: Remove explanatory phrases and obvious defaults
5. Maintain Clarity: Ensure compressed form is unambiguous

Use the context-compressor skill to systematically compress the requirement.
""")
        sys.exit(0)

    # Pass through unchanged
    sys.exit(0)

if __name__ == '__main__':
    main()
