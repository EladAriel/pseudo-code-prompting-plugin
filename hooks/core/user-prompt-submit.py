#!/usr/bin/env python3
"""
Claude Code Hook: UserPromptSubmit
Event: Triggered when user submits a prompt
Purpose: Detect feature-dev/pseudo-prompt commands and inject transformation context

This hook applies PROMPTCONVERTER structuring to incoming prompts by:
1. Detecting /feature-dev or /pseudo-prompt commands
2. Extracting the natural language query
3. Injecting context that activates the prompt-structurer Skill
4. Allowing Claude to apply transformation rules automatically
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

    # Check for explicit plugin invocation
    # Match patterns: "Use pseudo-code prompting plugin", "Use pseudocode prompting with ralph", etc.
    plugin_patterns = [
        r'[Uu]se.*pseudo.*code.*prompting.*(plugin|with.*ralph|with.*Ralph)',
        r'[Uu]se.*pseudocode.*prompting.*(plugin|with.*ralph|with.*Ralph)',
        r'[Ii]nvoke.*(pseudo|pseudocode).*(plugin|workflow)'
    ]

    for pattern in plugin_patterns:
        if re.search(pattern, prompt):
            print(f"""
<plugin-invocation-detected>
CRITICAL: The user explicitly requested to use the pseudo-code prompting plugin.

You MUST invoke the appropriate skill immediately using the Skill tool as your FIRST action:

- If user mentioned "with Ralph" or "with ralph": Use skill="pseudo-code-prompting:ralph-process"
- Otherwise: Use skill="pseudo-code-prompting:complete-process"

DO NOT proceed with manual implementation. DO NOT use other tools first.
IMMEDIATELY invoke the Skill tool, then ask the user what they want to implement.

User's original request: "{prompt}"
</plugin-invocation-detected>
""")
            sys.exit(0)

    # Detect transformation trigger keywords
    # Match patterns: "transform", "convert to pseudo", "structure", etc.
    transform_patterns = [
        r'(transform|convert).*(pseudo|pseudo-code|pseudocode)',
        r'^(structure|formalize).*(request|requirement|query)'
    ]

    for pattern in transform_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            # Extract the actual request (everything after "transform to pseudo code:" or similar)
            request = re.sub(r'^(transform|convert).*(pseudo|pseudo-code|pseudocode):?\s*', '', prompt, flags=re.IGNORECASE)

            print(f"""
<promptconverter-mode>
CRITICAL: You MUST transform the user's request into PROMPTCONVERTER pseudo-code format.

USER REQUEST TO TRANSFORM:
{request}

TRANSFORMATION RULES (apply in order):

1. ANALYZE INTENT: Identify core action (verb) + subject (noun)
   - Action: What operation? (create, implement, add, debug, optimize, fix)
   - Subject: What target? (api, authentication, database, function)

2. CREATE FUNCTION NAME: Combine into snake_case
   - Format: {{action}}_{{subject}} (e.g., create_api, implement_auth)
   - Use descriptive, unambiguous names

3. EXTRACT PARAMETERS: Convert ALL details to named parameters
   - Explicit requirements → direct parameters (language="python")
   - Technologies → framework, database, library parameters
   - Implicit requirements → inferred parameters (operations=["create","read","update","delete"])
   - Scale/performance → add constraint parameters

4. INFER CONSTRAINTS: Add missing but critical parameters
   - Security: authentication, authorization, validation
   - Data: schema, types, formats
   - Performance: caching, pagination, rate_limiting
   - Error handling: error_responses, logging

5. OUTPUT FORMAT: Return EXACTLY this format on a single line:
   function_name(param1="value1", param2=["val2a","val2b"], param3="value3", ...)

REQUIREMENTS:
- Output must be ONE line only
- No code blocks, no markdown, no explanations BEFORE the output
- Format: function_name(param="value", ...)
- After the transformation, you may explain the parameters

EXAMPLE:
Input: "create api for crud operations using python"
Output: create_crud_api(language="python", operations=["create","read","update","delete"], architecture="rest", framework="fastapi", database="postgresql", authentication="jwt", validation="pydantic", error_handling=true, pagination=true)

Now transform the user's request following these rules exactly.
</promptconverter-mode>
""")
            sys.exit(0)

    # Not a pseudo-prompt command, pass through unchanged
    sys.exit(0)

if __name__ == '__main__':
    main()
