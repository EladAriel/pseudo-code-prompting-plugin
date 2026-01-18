#!/usr/bin/env bash
#
# cache-stats.sh - Show cache statistics and metrics
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
REGISTRY_FILE="$CACHE_DIR/registry.json"

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "No cache found."
    exit 0
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              Semantic Cache Statistics                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Total patterns
total_patterns=$(jq '.patterns | length' "$REGISTRY_FILE")
echo "Total Patterns:        $total_patterns"

if [ "$total_patterns" -eq 0 ]; then
    echo
    echo "Cache is empty."
    exit 0
fi

# Total usage count
total_uses=$(jq '[.patterns[].stats.usage_count // 0] | add // 0' "$REGISTRY_FILE")
echo "Total Uses:            $total_uses"

# Average usage
if [ "$total_patterns" -gt 0 ]; then
    avg_uses=$(echo "scale=2; $total_uses / $total_patterns" | bc)
    echo "Average Uses:          $avg_uses"
fi

# Breakdown by query type
regular_count=$(jq '[.patterns[] | select(.metadata.query_type == "regular" or (.metadata.query_type // "regular") == "regular")] | length' "$REGISTRY_FILE")
optimized_count=$(jq '[.patterns[] | select(.metadata.query_type == "optimized")] | length' "$REGISTRY_FILE")
regular_uses=$(jq '[.patterns[] | select(.metadata.query_type == "regular" or (.metadata.query_type // "regular") == "regular") | .stats.usage_count // 0] | add // 0' "$REGISTRY_FILE")
optimized_uses=$(jq '[.patterns[] | select(.metadata.query_type == "optimized") | .stats.usage_count // 0] | add // 0' "$REGISTRY_FILE")

echo
echo "Breakdown by Type:"
echo "  Regular:   $regular_count patterns ($regular_uses uses)"
echo "  Optimized: $optimized_count patterns ($optimized_uses uses)"

# Total cache size
if [ -d "$PATTERNS_DIR" ]; then
    if [ "$(uname)" = "Darwin" ]; then
        total_size=$(find "$PATTERNS_DIR" -type f -name "*.md" -exec stat -f %z {} \; | awk '{sum+=$1} END {print sum}')
    else
        total_size=$(find "$PATTERNS_DIR" -type f -name "*.md" -exec stat -c %s {} \; | awk '{sum+=$1} END {print sum}')
    fi

    total_size=${total_size:-0}
    size_mb=$(echo "scale=2; $total_size / 1048576" | bc)
    echo "Total Cache Size:      ${size_mb} MB"
fi

# Last modified
last_modified=$(jq -r '.metadata.last_modified // "unknown"' "$REGISTRY_FILE" | cut -d'T' -f1)
echo "Last Modified:         $last_modified"

echo
echo "═══════════════════════════════════════════════════════════════"
echo "  Top 5 Most Used Patterns"
echo "═══════════════════════════════════════════════════════════════"
echo

printf "%-30s %-10s %s\n" "TAG ID" "USES" "DESCRIPTION"
printf "%-30s %-10s %s\n" "$(printf '─%.0s' {1..30})" "$(printf '─%.0s' {1..10})" "$(printf '─%.0s' {1..40})"

jq -r '.patterns | sort_by(-.stats.usage_count) | .[0:5] | .[] |
    [.tag_id, (.stats.usage_count // 0 | tostring), (.description | .[0:40])] |
    @tsv' "$REGISTRY_FILE" | \
while IFS=$'\t' read -r tag uses desc; do
    printf "%-30s %-10s %s\n" "$tag" "$uses" "$desc"
done

echo
