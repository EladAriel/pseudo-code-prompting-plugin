#!/usr/bin/env bash
#
# list-cache.sh - List all cached patterns with stats
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
REGISTRY_FILE="$CACHE_DIR/registry.json"

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "No cached patterns found."
    exit 0
fi

# Check if registry has patterns
pattern_count=$(jq '.patterns | length' "$REGISTRY_FILE")

if [ "$pattern_count" -eq 0 ]; then
    echo "No cached patterns found."
    exit 0
fi

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                         Cached Patterns                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo

printf "%-30s %-5s %-10s %-20s %s\n" "TAG ID" "TYPE" "USES" "LAST USED" "DESCRIPTION"
printf "%-30s %-5s %-10s %-20s %s\n" "$(printf '─%.0s' {1..30})" "$(printf '─%.0s' {1..5})" "$(printf '─%.0s' {1..10})" "$(printf '─%.0s' {1..20})" "$(printf '─%.0s' {1..35})"

jq -r '.patterns | sort_by(-.stats.usage_count) | .[] |
    [.tag_id, (.metadata.query_type // "reg" | if . == "optimized" then "OPT" else "REG" end), (.stats.usage_count // 0 | tostring), (.stats.last_used // "never" | split("T")[0]), (.description | .[0:45])] |
    @tsv' "$REGISTRY_FILE" | \
while IFS=$'\t' read -r tag type uses last_used desc; do
    printf "%-30s %-5s %-10s %-20s %s\n" "$tag" "$type" "$uses" "$last_used" "$desc"
done

echo
echo "Total patterns: $pattern_count"
