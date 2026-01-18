#!/usr/bin/env bash
#
# validate-cache.sh - Check cache integrity
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$HOOKS_DIR")"
CACHE_DIR="$PLUGIN_DIR/.claude/prompt_cache"
PATTERNS_DIR="$CACHE_DIR/patterns"
BACKUPS_DIR="$CACHE_DIR/backups"
REGISTRY_FILE="$CACHE_DIR/registry.json"

errors=0
warnings=0

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              Cache Integrity Check                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Check 1: Registry exists and is valid JSON
echo "[1/5] Checking registry file..."
if [ ! -f "$REGISTRY_FILE" ]; then
    echo "  ✗ Registry file not found"
    ((errors++))
else
    if jq empty "$REGISTRY_FILE" 2>/dev/null; then
        echo "  ✓ Registry JSON is valid"
    else
        echo "  ✗ Registry JSON is corrupted"
        ((errors++))
    fi
fi

# Check 2: All pattern files referenced in registry exist
echo "[2/5] Checking pattern file references..."
if [ -f "$REGISTRY_FILE" ]; then
    missing_files=0
    while IFS= read -r tag_id; do
        pattern_file="$PATTERNS_DIR/$tag_id.md"
        if [ ! -f "$pattern_file" ]; then
            echo "  ✗ Missing file for tag: $tag_id"
            ((missing_files++))
            ((errors++))
        fi
    done < <(jq -r '.patterns[].tag_id' "$REGISTRY_FILE")

    if [ $missing_files -eq 0 ]; then
        echo "  ✓ All pattern files exist"
    else
        echo "  ✗ Found $missing_files missing pattern files"
    fi
fi

# Check 3: Check for orphaned pattern files
echo "[3/5] Checking for orphaned files..."
if [ -d "$PATTERNS_DIR" ] && [ -f "$REGISTRY_FILE" ]; then
    orphaned=0
    for pattern_file in "$PATTERNS_DIR"/*.md; do
        [ -e "$pattern_file" ] || continue
        [ "$(basename "$pattern_file")" = "*.md" ] && continue

        tag_id=$(basename "$pattern_file" .md)
        if ! jq -e --arg tag "$tag_id" '.patterns[] | select(.tag_id == $tag)' "$REGISTRY_FILE" >/dev/null 2>&1; then
            echo "  ⚠ Orphaned file: $tag_id.md"
            ((orphaned++))
            ((warnings++))
        fi
    done

    if [ $orphaned -eq 0 ]; then
        echo "  ✓ No orphaned files found"
    else
        echo "  ⚠ Found $orphaned orphaned files"
    fi
fi

# Check 4: Verify file sizes match registry
echo "[4/5] Checking file size consistency..."
if [ -f "$REGISTRY_FILE" ]; then
    size_mismatches=0
    while IFS=$'\t' read -r tag_id expected_size; do
        pattern_file="$PATTERNS_DIR/$tag_id.md"
        if [ -f "$pattern_file" ]; then
            if [ "$(uname)" = "Darwin" ]; then
                actual_size=$(stat -f %z "$pattern_file")
            else
                actual_size=$(stat -c %s "$pattern_file")
            fi

            if [ "$actual_size" != "$expected_size" ]; then
                echo "  ⚠ Size mismatch for $tag_id: expected $expected_size, got $actual_size"
                ((size_mismatches++))
                ((warnings++))
            fi
        fi
    done < <(jq -r '.patterns[] | [.tag_id, (.stats.file_size_bytes // 0 | tostring)] | @tsv' "$REGISTRY_FILE")

    if [ $size_mismatches -eq 0 ]; then
        echo "  ✓ File sizes match registry"
    else
        echo "  ⚠ Found $size_mismatches size mismatches"
    fi
fi

# Check 5: Check directory structure
echo "[5/5] Checking directory structure..."
all_dirs_exist=true
for dir in "$CACHE_DIR" "$PATTERNS_DIR" "$BACKUPS_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "  ✗ Missing directory: $dir"
        ((errors++))
        all_dirs_exist=false
    fi
done

if [ "$all_dirs_exist" = true ]; then
    echo "  ✓ Directory structure is correct"
fi

echo
echo "═══════════════════════════════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════════════════════════════"
echo

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo "✓ Cache is healthy!"
    exit 0
else
    echo "Errors:   $errors"
    echo "Warnings: $warnings"
    echo

    if [ $errors -gt 0 ]; then
        echo "⚠ Cache has integrity issues that need attention."
        exit 1
    else
        echo "⚠ Cache has minor issues but is functional."
        exit 0
    fi
fi
