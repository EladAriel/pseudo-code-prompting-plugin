#!/usr/bin/env bash
#
# search-cache.sh - Search cached patterns by description or tag
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
REGISTRY_FILE="$CACHE_DIR/registry.json"

if [ $# -eq 0 ]; then
    echo "Usage: search-cache.sh <search_query>" >&2
    exit 1
fi

search_query="$*"

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "No cached patterns found."
    exit 0
fi

echo "Searching for: $search_query"
echo

# Case-insensitive search in tag_id and description
results=$(jq -r --arg query "${search_query,,}" \
    '.patterns[] | select(
        (.tag_id | ascii_downcase | contains($query)) or
        (.description | ascii_downcase | contains($query))
    ) | [.tag_id, .description, (.stats.usage_count // 0 | tostring)] | @tsv' \
    "$REGISTRY_FILE")

if [ -z "$results" ]; then
    echo "No matches found."
    exit 0
fi

printf "%-30s %-10s %s\n" "TAG ID" "USES" "DESCRIPTION"
printf "%-30s %-10s %s\n" "$(printf '─%.0s' {1..30})" "$(printf '─%.0s' {1..10})" "$(printf '─%.0s' {1..50})"

echo "$results" | while IFS=$'\t' read -r tag desc uses; do
    printf "%-30s %-10s %s\n" "$tag" "$uses" "$desc"
done
