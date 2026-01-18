#!/usr/bin/env bash
#
# confirm-cache-use.sh - Interactive confirmation prompt for cache usage
# Asks user whether to use cached pattern before retrieval
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
REGISTRY_FILE="$CACHE_DIR/registry.json"

# Arguments
TAG_ID="$1"
SIMILARITY_SCORE="${2:-unknown}"

if [ -z "$TAG_ID" ]; then
    echo "no"
    exit 0
fi

# Check if pattern file exists
PATTERN_FILE="$PATTERNS_DIR/$TAG_ID.md"
if [ ! -f "$PATTERN_FILE" ]; then
    echo "no"
    exit 1
fi

# Get pattern metadata from registry
if [ ! -f "$REGISTRY_FILE" ]; then
    echo "no"
    exit 1
fi

# Extract metadata using jq
METADATA=$(jq -r --arg tag "$TAG_ID" '.patterns[] | select(.tag_id == $tag) | @json' "$REGISTRY_FILE" 2>/dev/null || echo "{}")

if [ "$METADATA" = "{}" ]; then
    echo "no"
    exit 1
fi

# Parse metadata
DESCRIPTION=$(echo "$METADATA" | jq -r '.description // "No description"' 2>/dev/null || echo "No description")
PATTERN_TYPE=$(echo "$METADATA" | jq -r '.pattern_type // "regular"' 2>/dev/null || echo "regular")
USAGE_COUNT=$(echo "$METADATA" | jq -r '.stats.usage_count // 0' 2>/dev/null || echo "0")
LAST_USED=$(echo "$METADATA" | jq -r '.stats.last_used // "Never"' 2>/dev/null || echo "Never")
FILE_SIZE=$(du -h "$PATTERN_FILE" 2>/dev/null | cut -f1 || echo "unknown")

# Get pattern preview (first 10 lines)
PREVIEW=$(head -n 10 "$PATTERN_FILE" 2>/dev/null || echo "Preview unavailable")

# Check if running in non-interactive mode
if [ ! -t 0 ] || [ ! -t 1 ]; then
    # Non-interactive mode (CI/CD, piped input, etc.)
    echo "yes"
    exit 0
fi

# Check for environment variable override
if [ "${CACHE_AUTO_CONFIRM:-}" = "yes" ]; then
    echo "yes"
    exit 0
fi

if [ "${CACHE_AUTO_CONFIRM:-}" = "no" ]; then
    echo "no"
    exit 0
fi

# Display cache hit information
cat >&2 <<EOF

╔════════════════════════════════════════════════════════════════╗
║                    Cached Pattern Found                        ║
╚════════════════════════════════════════════════════════════════╝

Tag ID:           $TAG_ID
Type:             $PATTERN_TYPE
Description:      $DESCRIPTION
Similarity:       $SIMILARITY_SCORE
Usage Count:      $USAGE_COUNT
Last Used:        $LAST_USED
File Size:        $FILE_SIZE

Preview:
────────────────────────────────────────────────────────────────
$PREVIEW
────────────────────────────────────────────────────────────────

💡 Tip: Cache hits save ~90% cost and 5-15x faster than generation

EOF

# Interactive prompt with timeout
echo -n "Would you like to use this cached pattern? [Y]es / [N]o / [V]iew full / [C]ancel: " >&2

# Read with timeout (30 seconds)
if read -t 30 -r RESPONSE; then
    RESPONSE=$(echo "$RESPONSE" | tr '[:upper:]' '[:lower:]' | xargs)

    case "$RESPONSE" in
        y|yes|"")
            echo "yes"
            exit 0
            ;;
        n|no)
            echo "no"
            exit 0
            ;;
        v|view)
            # Show full pattern
            cat >&2 <<EOF

════════════════════════════════════════════════════════════════
FULL PATTERN CONTENT
════════════════════════════════════════════════════════════════

EOF
            cat "$PATTERN_FILE" >&2
            cat >&2 <<EOF

════════════════════════════════════════════════════════════════

EOF
            echo -n "Use this pattern? [Y]es / [N]o: " >&2
            if read -t 30 -r FINAL_RESPONSE; then
                FINAL_RESPONSE=$(echo "$FINAL_RESPONSE" | tr '[:upper:]' '[:lower:]' | xargs)
                case "$FINAL_RESPONSE" in
                    y|yes|"")
                        echo "yes"
                        exit 0
                        ;;
                    *)
                        echo "no"
                        exit 0
                        ;;
                esac
            else
                # Timeout on second prompt - default to yes
                echo "yes"
                exit 0
            fi
            ;;
        c|cancel)
            echo "cancel"
            exit 2
            ;;
        *)
            # Invalid input - ask again (max 2 more times)
            for _attempt in 1 2; do
                echo -n "Invalid option. Please enter Y/N/V/C: " >&2
                if read -t 10 -r RETRY_RESPONSE; then
                    RETRY_RESPONSE=$(echo "$RETRY_RESPONSE" | tr '[:upper:]' '[:lower:]' | xargs)
                    case "$RETRY_RESPONSE" in
                        y|yes)
                            echo "yes"
                            exit 0
                            ;;
                        n|no)
                            echo "no"
                            exit 0
                            ;;
                        v|view)
                            cat "$PATTERN_FILE" >&2
                            echo -n "Use this pattern? [Y/N]: " >&2
                            read -t 30 -r FINAL_RESPONSE || FINAL_RESPONSE="yes"
                            FINAL_RESPONSE=$(echo "$FINAL_RESPONSE" | tr '[:upper:]' '[:lower:]' | xargs)
                            if [[ "$FINAL_RESPONSE" =~ ^(y|yes|)$ ]]; then
                                echo "yes"
                            else
                                echo "no"
                            fi
                            exit 0
                            ;;
                        c|cancel)
                            echo "cancel"
                            exit 2
                            ;;
                    esac
                fi
            done
            # Too many invalid attempts - default to no
            echo "no"
            exit 0
            ;;
    esac
else
    # Timeout - default to yes
    echo "" >&2
    echo "⏱️ Timeout (30s) - Using cached pattern (default)" >&2
    echo "yes"
    exit 0
fi
