#!/usr/bin/env bash
#
# inject-context-paths.sh - Context-aware path injection for cached patterns
# Replaces cached file paths with current project structure paths
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/cache_path_injection.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Logging function
log() {
    local level="$1"
    shift
    echo "[$(date -Iseconds)] [$level] $*" >> "$LOG_FILE"
}

# Arguments
TAG_ID="$1"
PROJECT_ROOT="${2:-$(pwd)}"

if [ -z "$TAG_ID" ]; then
    log "ERROR" "No tag_id provided to path injection"
    exit 1
fi

PATTERN_FILE="$PATTERNS_DIR/$TAG_ID.md"

if [ ! -f "$PATTERN_FILE" ]; then
    log "ERROR" "Pattern file not found: $TAG_ID"
    exit 1
fi

log "INFO" "Injecting context paths for tag: $TAG_ID, project: $PROJECT_ROOT"

# Read the cached pattern
CACHED_CONTENT=$(cat "$PATTERN_FILE")

# ═══════════════════════════════════════════════════════════
# STRATEGY: Path-Agnostic Caching with Context Injection
# ═══════════════════════════════════════════════════════════
#
# The semantic router matches queries based on INTENT, not file paths.
# This script adapts cached patterns to the current project by:
#
# 1. Preserving relative directory structures (src/, lib/, hooks/, etc.)
# 2. NOT replacing project-specific paths in the pattern itself
# 3. Instead, INJECTING current project context as a header
# 4. Letting Claude understand the mapping between cached and current structure
#
# Why this works:
# - Claude can understand "apply this pattern to my current project"
# - Pattern remains reusable across different project structures
# - No brittle path replacement logic needed
# - Works even when directory structures differ
# ═══════════════════════════════════════════════════════════

# Get current project tree context (lightweight, max 3 levels)
PROJECT_TREE=""
if command -v tree &> /dev/null; then
    PROJECT_TREE=$(tree -L 3 -I 'node_modules|.git|dist|build|__pycache__|*.pyc' "$PROJECT_ROOT" 2>/dev/null | head -n 50 || echo "")
elif [ -d "$PROJECT_ROOT" ]; then
    # Fallback: Simple directory listing
    PROJECT_TREE=$(find "$PROJECT_ROOT" -maxdepth 3 -type d ! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/dist/*' ! -path '*/build/*' 2>/dev/null | head -n 50 | sed "s|^$PROJECT_ROOT|.|" || echo "")
fi

# Get current project technology stack indicators
STACK_INDICATORS=""
if [ -f "$PROJECT_ROOT/package.json" ]; then
    STACK_INDICATORS="${STACK_INDICATORS}📦 Node.js/JavaScript project (package.json found)\n"
fi
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    STACK_INDICATORS="${STACK_INDICATORS}🐍 Python project (requirements.txt found)\n"
fi
if [ -f "$PROJECT_ROOT/go.mod" ]; then
    STACK_INDICATORS="${STACK_INDICATORS}🔷 Go project (go.mod found)\n"
fi
if [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
    STACK_INDICATORS="${STACK_INDICATORS}🦀 Rust project (Cargo.toml found)\n"
fi
if [ -f "$PROJECT_ROOT/pom.xml" ] || [ -f "$PROJECT_ROOT/build.gradle" ]; then
    STACK_INDICATORS="${STACK_INDICATORS}☕ Java project (pom.xml/build.gradle found)\n"
fi

# Construct context injection header
CONTEXT_HEADER=$(cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 CACHED PATTERN LOADED: $TAG_ID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  CONTEXT-AWARE MODE: This pattern is being adapted to your current project

Current Project Root: $PROJECT_ROOT

Project Stack:
$(echo -e "$STACK_INDICATORS" | sed 's/^/  /')

Current Project Structure (top 3 levels):
\`\`\`
$PROJECT_TREE
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CACHED PATTERN BELOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When applying this pattern:
1. Map the cached file paths to your current project structure shown above
2. Preserve the relative directory relationships from the pattern
3. Adapt file names/paths to match your current technology stack
4. If a suggested file/directory doesn't exist, create it or use the closest match

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
)

# Output: Context header + Original cached pattern
echo "$CONTEXT_HEADER"
echo ""
echo "$CACHED_CONTENT"

log "INFO" "Successfully injected context for tag: $TAG_ID"

exit 0
