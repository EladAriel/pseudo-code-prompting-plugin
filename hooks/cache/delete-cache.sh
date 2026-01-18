#!/usr/bin/env bash
#
# delete-cache.sh - Delete a cached pattern
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
    echo "Usage: delete-cache.sh <tag_id>" >&2
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

# Get pattern info for display
description=$(jq -r --arg tag "$tag_id" '.patterns[] | select(.tag_id == $tag) | .description' "$REGISTRY_FILE")

echo "Pattern to delete:"
echo "  Tag:         $tag_id"
echo "  Description: $description"
echo

read -p "Are you sure you want to delete this pattern? [y/N]: " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
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

# Ensure lock is released
trap 'rmdir "$LOCK_FILE" 2>/dev/null || true' EXIT

# Backup pattern file before deletion
pattern_file="$PATTERNS_DIR/$tag_id.md"
if [ -f "$pattern_file" ]; then
    backup_file="$BACKUPS_DIR/${tag_id}_deleted_$(date +%Y%m%d_%H%M%S).md"
    cp "$pattern_file" "$backup_file"
    echo "✓ Backup created: $backup_file"
    rm "$pattern_file"
fi

# Update registry
timestamp=$(date -Iseconds)
temp_file="${REGISTRY_FILE}.tmp.$$"

jq \
    --arg tag "$tag_id" \
    --arg time "$timestamp" \
    'del(.patterns[] | select(.tag_id == $tag)) |
     .metadata.last_modified = $time |
     .metadata.pattern_count = (.patterns | length)' \
    "$REGISTRY_FILE" > "$temp_file"

mv "$temp_file" "$REGISTRY_FILE"

echo "✓ Pattern '$tag_id' deleted successfully."
