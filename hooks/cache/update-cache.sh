#!/usr/bin/env bash
#
# update-cache.sh - Update an existing cached pattern
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
BACKUPS_DIR="$CACHE_DIR/backups"
REGISTRY_FILE="$CACHE_DIR/registry.json"
LOCK_FILE="$CACHE_DIR/.registry.lock"

if [ $# -eq 0 ]; then
    echo "Usage: update-cache.sh <tag_id>" >&2
    exit 1
fi

tag_id="$1"

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "✗ Registry not found."
    exit 1
fi

# Check if pattern exists
if ! jq -e --arg tag "$tag_id" '.patterns[] | select(.tag_id == $tag)' "$REGISTRY_FILE" >/dev/null; then
    echo "✗ Pattern '$tag_id' not found in cache."
    exit 1
fi

# Get current pattern info
description=$(jq -r --arg tag "$tag_id" '.patterns[] | select(.tag_id == $tag) | .description' "$REGISTRY_FILE")
current_version=$(jq -r --arg tag "$tag_id" '.patterns[] | select(.tag_id == $tag) | .metadata.version // "1.0"' "$REGISTRY_FILE")

pattern_file="$PATTERNS_DIR/$tag_id.md"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║             Update Cached Pattern                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo
echo "  Tag:         $tag_id"
echo "  Version:     $current_version"
echo "  Description: $description"
echo

# Backup current version
backup_file="$BACKUPS_DIR/${tag_id}_v${current_version}_$(date +%Y%m%d_%H%M%S).md"
if [ -f "$pattern_file" ]; then
    cp "$pattern_file" "$backup_file"
    echo "✓ Current version backed up to: $backup_file"
    echo
fi

# Prompt for new content
echo "Paste the updated pattern content (press Ctrl+D when done):"
echo "─────────────────────────────────────────────────────────"

new_content=$(cat)

if [ -z "$new_content" ]; then
    echo "✗ No content provided"
    exit 1
fi

if [ ${#new_content} -lt 50 ]; then
    echo "✗ Content too short (minimum 50 characters)"
    exit 1
fi

echo
echo "Content captured: ${#new_content} characters"
echo

# Optionally update description
read -rp "Update description? [y/N]: " update_desc

if [[ "$update_desc" =~ ^[Yy]$ ]]; then
    read -rp "Enter new description: " description
fi

# Acquire lock
max_attempts=3
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if mkdir "$LOCK_FILE" 2>/dev/null; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ Could not acquire lock. Try again." >&2
    exit 1
fi

trap 'rmdir "$LOCK_FILE" 2>/dev/null || true' EXIT

# Write updated pattern
temp_file="${pattern_file}.tmp.$$"
echo "$new_content" > "$temp_file"
mv "$temp_file" "$pattern_file"
chmod 644 "$pattern_file"

# Calculate new file size
if [ "$(uname)" = "Darwin" ]; then
    file_size=$(stat -f %z "$pattern_file")
else
    file_size=$(stat -c %s "$pattern_file")
fi

# Increment version
new_version=$(echo "$current_version" | awk -F. '{print $1+1 ".0"}')

# Update registry
timestamp=$(date -Iseconds)
temp_registry="${REGISTRY_FILE}.tmp.$$"

jq \
    --arg tag "$tag_id" \
    --arg desc "$description" \
    --arg size "$file_size" \
    --arg time "$timestamp" \
    --arg ver "$new_version" \
    '.patterns |= map(
        if .tag_id == $tag then
            .description = $desc |
            .stats.last_used = $time |
            .stats.file_size_bytes = ($size | tonumber) |
            .metadata.version = $ver
        else
            .
        end
    ) | .metadata.last_modified = $time' \
    "$REGISTRY_FILE" > "$temp_registry"

mv "$temp_registry" "$REGISTRY_FILE"

echo
echo "✓ Pattern updated successfully!"
echo "  New version: $new_version"
echo "  Size:        $file_size bytes"
echo
