#!/usr/bin/env bash

# Claude Code Hook: ContextAwareTreeInjection
# Event: Triggered on UserPromptSubmit when implementation keywords detected
# Purpose: Inject project structure context for architecture-aware suggestions
#
# This hook:
# 1. Detects implementation keywords (implement, create, add, refactor, etc.)
# 2. Executes Python script to generate project tree structure
# 3. Injects tree context into Claude's prompt for better file placement decisions
# 4. Activates context-aware transformation mode

set -euo pipefail

# Read hook input from stdin (JSON format)
# Schema: { session_id, transcript_path, cwd, permission_mode, hook_event_name, prompt }
INPUT=$(cat)

# Extract the user prompt using pure bash (no jq dependency)
# Use a more lenient regex that handles escaped characters
if [[ "$INPUT" =~ \"prompt\":[[:space:]]*\"([^\"]+)\" ]]; then
  PROMPT="${BASH_REMATCH[1]}"
else
  exit 0
fi

# Check if prompt is empty
if [[ -z "$PROMPT" ]]; then
  exit 0
fi

# Extract CWD from hook input (working directory)
CWD="$(pwd)"
if [[ "$INPUT" =~ \"cwd\":[[:space:]]*\"([^\"]+)\" ]]; then
  CWD="${BASH_REMATCH[1]}"
fi

# Keyword detection - match action verbs indicating project implementation work
# Keywords: implement, create, add, refactor, build, generate, setup, initialize
if [[ "$PROMPT" =~ (implement|create|add|refactor|build|generate|setup|initialize) ]]; then

  # Get plugin root directory
  if [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    PLUGIN_ROOT="$CLAUDE_PLUGIN_ROOT"
  else
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"
  fi


  PYTHON_SCRIPT="${PLUGIN_ROOT}/hooks/tree/get_context_tree.py"

  # Check if Python script exists
  if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    # Graceful degradation - script missing
    exit 0
  fi

  # Detect Python command (try python3 first, fallback to python)
  PYTHON_CMD=""
  if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
  elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
  else
    # Python not available - graceful degradation
    exit 0
  fi

  # Execute Python script with timeout (15 seconds)
  # Capture output, handle errors gracefully
  TREE_OUTPUT=""
  if command -v timeout &> /dev/null; then
    # Use timeout command if available (Linux/macOS with coreutils)
    TREE_OUTPUT=$($PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1 || echo "[TREE_ERROR]")
  elif command -v gtimeout &> /dev/null; then
    # macOS with GNU coreutils (brew install coreutils)
    TREE_OUTPUT=$(gtimeout 15s $PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1 || echo "[TREE_ERROR]")
  else
    # No timeout command - run without timeout (risk of hanging)
    TREE_OUTPUT=$($PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1 || echo "[TREE_ERROR]")
  fi

  # Check if tree generation failed or returned error
  if [[ "$TREE_OUTPUT" == "[TREE_ERROR]" ]] || [[ -z "$TREE_OUTPUT" ]] || [[ "$TREE_OUTPUT" == *"[ERROR:"* ]]; then
    # Graceful degradation - no tree injection
    exit 0
  fi

  # Inject tree context into prompt
  cat <<EOF

[CONTEXT-AWARE MODE ACTIVATED]

Project Structure:
\`\`\`
$TREE_OUTPUT
\`\`\`

Use this project structure as context for the request: "$PROMPT"

When responding:
1. Reference existing files and directories from the structure above
2. Suggest modifications that align with the current architecture
3. Identify where new files should be placed based on existing patterns
4. Detect the technology stack from visible files (package.json, requirements.txt, go.mod, etc.)

If the project is empty (\`<<PROJECT_EMPTY_NO_STRUCTURE>>\`), use the \`/context-aware-transform\` command to create a virtual skeleton based on stack detection.

EOF

  exit 0
fi

# Pass through unchanged
exit 0
