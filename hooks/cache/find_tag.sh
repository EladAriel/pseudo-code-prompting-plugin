#!/usr/bin/env bash
#
# find_tag.sh - Hook wrapper for semantic router
# Intercepts transform-query command to check cache before generation
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
REGISTRY_FILE="$CACHE_DIR/registry.json"
LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/semantic_cache.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Logging function
log() {
    local level="$1"
    shift
    echo "[$(date -Iseconds)] [$level] $*" >> "$LOG_FILE"
}

# Update pattern usage stats
update_usage_stats() {
    local tag_id="$1"
    local lock_file="$CACHE_DIR/.registry.lock"
    local max_attempts=3
    local attempt=0

    # Try to acquire lock
    while [ $attempt -lt $max_attempts ]; do
        if mkdir "$lock_file" 2>/dev/null; then
            break
        fi
        attempt=$((attempt + 1))
        sleep 0.1
    done

    if [ $attempt -eq $max_attempts ]; then
        log "WARNING" "Could not update usage stats for $tag_id (lock timeout)"
        return 1
    fi

    # Update registry
    local timestamp
    timestamp=$(date -Iseconds)

    local temp_file="${REGISTRY_FILE}.tmp.$$"

    if jq \
        --arg tag "$tag_id" \
        --arg time "$timestamp" \
        '.patterns |= map(
            if .tag_id == $tag then
                .stats.usage_count = (.stats.usage_count // 0) + 1 |
                .stats.last_used = $time
            else
                .
            end
        ) | .metadata.last_modified = $time' \
        "$REGISTRY_FILE" > "$temp_file" 2>/dev/null; then
        mv "$temp_file" "$REGISTRY_FILE"
        log "INFO" "Updated usage stats for: $tag_id"
    else
        rm -f "$temp_file"
        log "ERROR" "Failed to update usage stats for: $tag_id"
    fi

    # Release lock
    rmdir "$lock_file" 2>/dev/null || true
}

# Main cache lookup logic
main() {
    local user_query="$*"

    if [ -z "$user_query" ]; then
        log "WARNING" "Empty query provided to cache lookup"
        echo "None"
        exit 0
    fi

    log "INFO" "Cache lookup for query: ${user_query:0:100}..."

    # Check if Python and find_tag.py are available
    if ! command -v python3 &>/dev/null; then
        log "ERROR" "python3 not found"
        echo "None"
        exit 0
    fi

    if [ ! -f "$SCRIPT_DIR/find_tag.py" ]; then
        log "ERROR" "find_tag.py not found"
        echo "None"
        exit 0
    fi

    # Check if registry exists
    if [ ! -f "$REGISTRY_FILE" ]; then
        log "INFO" "Registry not found, cache empty"
        echo "None"
        exit 0
    fi

    # Call semantic router with timeout
    local result
    if result=$(timeout 15s python3 "$SCRIPT_DIR/find_tag.py" "$user_query" 2>>"$LOG_FILE"); then
        result=$(echo "$result" | tr -d '\n\r' | xargs)

        if [ "$result" = "None" ] || [ -z "$result" ]; then
            log "INFO" "Cache miss"
            echo "None"
            exit 0
        fi

        # Validate result format
        if ! echo "$result" | grep -qE '^[a-z0-9_]+$'; then
            log "WARNING" "Invalid tag format returned: $result"
            echo "None"
            exit 0
        fi

        # Check if pattern file exists
        local pattern_file="$PATTERNS_DIR/$result.md"
        if [ ! -f "$pattern_file" ]; then
            log "ERROR" "Pattern file not found: $result"
            echo "None"
            exit 0
        fi

        # Cache hit!
        log "INFO" "Cache hit: $result"

        # Update usage stats (non-blocking)
        update_usage_stats "$result" &

        # Check if path injection script is available
        PATH_INJECTOR="$SCRIPT_DIR/inject-context-paths.sh"
        if [ -x "$PATH_INJECTOR" ]; then
            # Inject current project context into cached pattern
            PROJECT_ROOT="${PWD:-$(pwd)}"
            if "$PATH_INJECTOR" "$result" "$PROJECT_ROOT" 2>>"$LOG_FILE"; then
                log "INFO" "Context-aware cache hit with path injection: $result"
                exit 0
            else
                log "WARNING" "Path injection failed, returning tag_id only: $result"
                echo "$result"
                exit 0
            fi
        else
            # Fallback: Return tag_id without path injection (backward compatibility)
            log "INFO" "Path injection script not available, returning tag_id: $result"
            echo "$result"
            exit 0
        fi
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            log "ERROR" "Semantic router timeout"
        else
            log "ERROR" "Semantic router failed with exit code: $exit_code"
        fi
        echo "None"
        exit 0
    fi
}

main "$@"
