#!/bin/bash

# Claude Code Hook: UserPromptSubmit
# Event: Triggered when user submits a prompt
# Purpose: Detect feature-dev/pseudo-prompt commands and inject transformation context
#
# This hook applies PROMPTCONVERTER structuring to incoming prompts by:
# 1. Detecting /feature-dev or /pseudo-prompt commands
# 2. Extracting the natural language query
# 3. Injecting context that activates the prompt-structurer Skill
# 4. Allowing Claude to apply transformation rules automatically

set -e

# Read hook input from stdin (JSON format)
# Schema: { session_id, transcript_path, cwd, permission_mode, hook_event_name, prompt }
INPUT=$(cat)

# Extract the user prompt
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

# Check if prompt is empty
if [[ -z "$PROMPT" ]]; then
  exit 0
fi

# Detect if this is a feature-dev or pseudo-prompt command
# Match patterns: /feature-dev ..., /pseudo-prompt ...
if [[ "$PROMPT" =~ ^/feature-dev[[:space:]]+(.+)$ ]] || [[ "$PROMPT" =~ ^/pseudo-prompt[[:space:]]+(.+)$ ]]; then
  # Extract the query text (everything after the command)
  QUERY="${BASH_REMATCH[1]}"
  
  # Build context to inject that activates the prompt-structurer Skill
  # Use plain stdout (exit code 0) which Claude automatically adds as context
  cat <<EOF

[PSEUDO-CODE TRANSFORMATION ACTIVATED]

Your request should be transformed using the prompt-structurer Skill to convert it into PROMPTCONVERTER format.

Original request: $QUERY

Transform this using the 5 PROMPTCONVERTER rules:
1. Analyze Intent: Identify core action (verb) and subject (noun)
2. Create Function Name: Combine into snake_case (e.g., implement_authentication)
3. Extract Parameters: Convert details into named parameters (e.g., providers=["google"])
4. Infer Constraints: Detect implicit requirements as additional parameters
5. Output Format: Return ONLY single-line pseudo-code: Transformed: function_name(param="value")

Provide the transformed pseudo-code, then proceed with the feature-dev workflow.
EOF
  
  exit 0
fi

# Not a pseudo-prompt command, pass through unchanged
exit 0
