#!/usr/bin/env bash
#
# cache-success.sh - Save generated pseudo-code pattern to semantic cache
# Captures last generated output and saves it with semantic metadata
#

set -euo pipefail

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
BACKUPS_DIR="$CACHE_DIR/backups"
REGISTRY_FILE="$CACHE_DIR/registry.json"
LOCK_FILE="$CACHE_DIR/.registry.lock"
LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/semantic_cache.log"

# Ensure directories exist
mkdir -p "$CACHE_DIR" "$PATTERNS_DIR" "$BACKUPS_DIR" "$LOG_DIR"

# ═══════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════

log() {
    local level="$1"
    shift
    local message="$*"
    echo "[$(date -Iseconds)] [$level] $message" >> "$LOG_FILE"
}

# ═══════════════════════════════════════════════════════════
# LOCK MANAGEMENT
# ═══════════════════════════════════════════════════════════

acquire_lock() {
    local max_attempts=3
    local attempt=0
    local backoff=100

    while [ $attempt -lt $max_attempts ]; do
        if mkdir "$LOCK_FILE" 2>/dev/null; then
            log "INFO" "Lock acquired"
            return 0
        fi

        # Check for stale lock (older than 60 seconds)
        if [ -d "$LOCK_FILE" ]; then
            local lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0)))
            if [ $lock_age -gt 60 ]; then
                log "WARNING" "Removing stale lock (age: ${lock_age}s)"
                rmdir "$LOCK_FILE" 2>/dev/null || true
                continue
            fi
        fi

        attempt=$((attempt + 1))
        log "INFO" "Lock busy, retry $attempt/$max_attempts"
        sleep "0.$backoff"
        backoff=$((backoff * 2))
    done

    log "ERROR" "Failed to acquire lock after $max_attempts attempts"
    return 1
}

release_lock() {
    rmdir "$LOCK_FILE" 2>/dev/null || true
    log "INFO" "Lock released"
}

# Ensure lock is released on exit
trap release_lock EXIT

# ═══════════════════════════════════════════════════════════
# INPUT VALIDATION
# ═══════════════════════════════════════════════════════════

sanitize_tag() {
    local input="$1"
    # Convert to lowercase, replace spaces with underscores, remove special chars
    echo "$input" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | sed 's/[^a-z0-9_]//g' | cut -c1-100
}

validate_tag() {
    local tag="$1"

    # Check format
    if ! echo "$tag" | grep -qE '^[a-z0-9_]+$'; then
        echo "ERROR: Invalid tag format. Use only lowercase letters, numbers, and underscores." >&2
        return 1
    fi

    # Check reserved names
    if [[ "$tag" == "registry" || "$tag" == "backup" || "$tag" == "lock" ]]; then
        echo "ERROR: Tag name is reserved." >&2
        return 1
    fi

    # Check for path traversal
    if [[ "$tag" == *".."* || "$tag" == *"/"* || "$tag" == *"\\"* ]]; then
        echo "ERROR: Invalid characters in tag." >&2
        return 1
    fi

    return 0
}

# ═══════════════════════════════════════════════════════════
# REGISTRY OPERATIONS
# ═══════════════════════════════════════════════════════════

initialize_registry() {
    if [ ! -f "$REGISTRY_FILE" ]; then
        log "INFO" "Creating new registry"
        cat > "$REGISTRY_FILE" <<EOF
{
  "patterns": [],
  "version": "1.0",
  "metadata": {
    "created_at": "$(date -Iseconds)",
    "last_modified": "$(date -Iseconds)",
    "pattern_count": 0
  }
}
EOF
    fi
}

update_registry() {
    local tag_id="$1"
    local description="$2"
    local file_path="$3"
    local file_size="$4"
    local query_type="$5"
    local is_update="${6:-false}"

    # Read current registry
    local registry
    registry=$(cat "$REGISTRY_FILE")

    # Check if tag already exists
    local existing
    existing=$(echo "$registry" | jq -r ".patterns[] | select(.tag_id == \"$tag_id\") | .tag_id")

    if [ -n "$existing" ] && [ "$is_update" = "false" ]; then
        # Tag exists and we're not updating
        return 2
    fi

    local timestamp
    timestamp=$(date -Iseconds)

    if [ -n "$existing" ]; then
        # Update existing pattern
        log "INFO" "Updating existing pattern: $tag_id"
        registry=$(echo "$registry" | jq \
            --arg tag "$tag_id" \
            --arg desc "$description" \
            --arg size "$file_size" \
            --arg time "$timestamp" \
            --arg qtype "$query_type" \
            '.patterns |= map(
                if .tag_id == $tag then
                    .description = $desc |
                    .stats.last_used = $time |
                    .stats.file_size_bytes = ($size | tonumber) |
                    .metadata.version = ((.metadata.version // "1.0" | split(".")[0] | tonumber) + 1 | tostring) |
                    .metadata.query_type = $qtype
                else
                    .
                end
            ) | .metadata.last_modified = $time'
        )
    else
        # Add new pattern
        log "INFO" "Adding new pattern: $tag_id"
        local new_pattern
        new_pattern=$(cat <<EOF
{
  "tag_id": "$tag_id",
  "description": "$description",
  "file_path": "$file_path",
  "stats": {
    "usage_count": 0,
    "last_used": "$timestamp",
    "created_at": "$timestamp",
    "file_size_bytes": $file_size
  },
  "metadata": {
    "tags": [],
    "author": "${USER:-unknown}",
    "version": "1.0",
    "query_type": "$query_type"
  }
}
EOF
        )

        registry=$(echo "$registry" | jq \
            --argjson pattern "$new_pattern" \
            --arg time "$timestamp" \
            '.patterns += [$pattern] |
             .metadata.last_modified = $time |
             .metadata.pattern_count = (.patterns | length)'
        )
    fi

    # Write atomically
    local temp_file="${REGISTRY_FILE}.tmp.$$"
    echo "$registry" | jq '.' > "$temp_file"
    mv "$temp_file" "$REGISTRY_FILE"

    log "INFO" "Registry updated successfully"
    return 0
}

# ═══════════════════════════════════════════════════════════
# MAIN LOGIC
# ═══════════════════════════════════════════════════════════

main() {
    echo "╔════════════════════════════════════════════════════╗"
    echo "║     Cache Pseudo-Code Pattern                      ║"
    echo "╚════════════════════════════════════════════════════╝"
    echo

    # Initialize registry if needed
    initialize_registry

    # Get content from stdin or last output
    echo "Paste your pseudo-code pattern (press Ctrl+D when done):"
    echo "─────────────────────────────────────────────────────"

    local content
    content=$(cat)

    # Validate content
    if [ -z "$content" ]; then
        echo "✗ Error: No content provided" >&2
        exit 1
    fi

    local content_length=${#content}
    if [ "$content_length" -lt 50 ]; then
        echo "✗ Error: Content too short (minimum 50 characters)" >&2
        exit 1
    fi

    if [ "$content_length" -gt 5000000 ]; then
        echo "✗ Error: Content too large (maximum 5MB)" >&2
        exit 1
    fi

    echo
    echo "Content captured: $content_length characters"
    echo

    # Prompt for tag name
    read -rp "Enter tag name (e.g., 'auth_google_oauth'): " tag_input

    if [ -z "$tag_input" ]; then
        echo "✗ Error: Tag name required" >&2
        exit 1
    fi

    # Sanitize and validate tag
    local tag_id
    tag_id=$(sanitize_tag "$tag_input")

    if ! validate_tag "$tag_id"; then
        exit 1
    fi

    echo "Sanitized tag: $tag_id"
    echo

    # Prompt for description
    read -rp "Enter description (for semantic matching): " description

    if [ -z "$description" ]; then
        echo "✗ Error: Description required" >&2
        exit 1
    fi

    if [ ${#description} -gt 500 ]; then
        echo "⚠ Warning: Description truncated to 500 characters"
        description="${description:0:500}"
    fi

    # Prompt for query type
    echo
    echo "Query Type:"
    echo "  Regular   - Standard pattern (70% match threshold)"
    echo "  Optimized - Enhanced/validated pattern (65% threshold, 1.5x priority)"
    echo
    read -rp "Tag this as optimized query? [y/N]: " query_type_input

    local query_type="regular"
    if [[ "$query_type_input" =~ ^[Yy]$ ]]; then
        query_type="optimized"
        echo "✓ Pattern marked as optimized (higher priority in matching)"
    else
        echo "✓ Pattern marked as regular"
    fi
    echo

    # Check for collision
    local pattern_file="$PATTERNS_DIR/$tag_id.md"
    local is_update="false"

    if [ -f "$pattern_file" ]; then
        echo
        echo "⚠ Pattern '$tag_id' already exists!"
        echo
        echo "Options:"
        echo "  1) Overwrite (backup will be created)"
        echo "  2) Cancel"
        echo
        read -rp "Choose [1-2]: " choice

        case "$choice" in
            1)
                # Backup existing file
                local backup_file
                backup_file="$BACKUPS_DIR/${tag_id}_$(date +%Y%m%d_%H%M%S).md"
                cp "$pattern_file" "$backup_file"
                echo "✓ Backup created: $backup_file"
                is_update="true"
                ;;
            *)
                echo "Cancelled."
                exit 0
                ;;
        esac
    fi

    # Acquire lock for registry update
    if ! acquire_lock; then
        echo "✗ Error: Could not acquire registry lock. Try again." >&2
        exit 1
    fi

    # Write pattern file atomically
    local temp_pattern="${pattern_file}.tmp.$$"
    echo "$content" > "$temp_pattern"

    # Verify write succeeded
    if [ ! -f "$temp_pattern" ]; then
        echo "✗ Error: Failed to write pattern file" >&2
        exit 1
    fi

    # Move atomically
    mv "$temp_pattern" "$pattern_file"
    chmod 644 "$pattern_file"

    # Calculate file size
    local file_size
    if [ "$(uname)" = "Darwin" ]; then
        file_size=$(stat -f %z "$pattern_file")
    else
        file_size=$(stat -c %s "$pattern_file")
    fi

    # Update registry
    local relative_path="patterns/$tag_id.md"

    if update_registry "$tag_id" "$description" "$relative_path" "$file_size" "$query_type" "$is_update"; then
        echo
        echo "╔════════════════════════════════════════════════════╗"
        echo "║  ✓ Pattern Cached Successfully                     ║"
        echo "╚════════════════════════════════════════════════════╝"
        echo
        echo "  Tag:         $tag_id"
        echo "  File:        $relative_path"
        echo "  Size:        $file_size bytes"
        echo "  Description: $description"
        echo
        echo "💡 Use this pattern by running your query - it will be"
        echo "   automatically matched if semantically relevant."
        echo

        log "INFO" "Pattern saved: $tag_id"
    else
        # Registry update failed
        echo "✗ Error: Failed to update registry" >&2
        rm -f "$pattern_file"
        exit 1
    fi
}

main "$@"
