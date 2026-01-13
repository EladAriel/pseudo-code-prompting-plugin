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

# Detect transformation trigger keywords
# Match patterns: "transform", "convert to pseudo", "structure", etc.
if [[ "$PROMPT" =~ (transform|convert).*(pseudo|pseudo-code|pseudocode) ]] || \
   [[ "$PROMPT" =~ ^(structure|formalize).*(request|requirement|query) ]]; then

  # Build context to inject that tells Claude to use the prompt-transformer agent
  cat <<EOF

<transformation-context>
The user is requesting pseudo-code transformation using the PROMPTCONVERTER methodology.

You should use the Task tool to launch the prompt-transformer agent to convert this request into function-like pseudo-code format.

Use: Task tool with subagent_type="prompt-transformer" and provide the user's request as the prompt.

The agent will apply the 5 PROMPTCONVERTER rules to produce output like:
function_name(param="value", param2="value2", ...)

After transformation, you can proceed with implementation if requested.
</transformation-context>
EOF

  exit 0
fi

# Not a pseudo-prompt command, pass through unchanged
exit 0
