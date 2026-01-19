# Ralph Loop Integration

End-to-end automated workflow that combines pseudo-code processing with Ralph Loop for iterative implementation.

## Overview

The Ralph Process Integration skill provides a seamless workflow from natural language query to automated iterative implementation:

1. **Optimize Query** - Runs complete-process pipeline (transform → validate → optimize)
2. **Analyze Complexity** - Examines validation report to estimate iteration requirements
3. **Generate Promise** - Creates specific completion criteria from validation requirements
4. **Launch Ralph** - Starts Ralph Loop with optimized parameters

## Quick Start

```bash
/ralph-process "Your implementation request here"
```

That's it! The skill handles everything else automatically.

## Usage Examples

### Simple Task (~20 iterations)

```bash
/ralph-process "Add a dark mode toggle to the settings page"
```

**What happens:**
1. Query is optimized via complete-process
2. Complexity analyzed: SIMPLE (few warnings, no critical issues)
3. Promise generated: "COMPLETE: Dark mode toggle AND Theme persistence working"
4. Ralph Loop starts with 20 iterations

### Medium Task (~40 iterations)

```bash
/ralph-process "Implement user registration with email validation"
```

**What happens:**
1. Query optimized with security considerations
2. Complexity analyzed: MEDIUM (auth + validation + error handling)
3. Promise generated: "IMPLEMENTATION COMPLETE: 4 requirements met"
4. Ralph Loop starts with 40 iterations

### Complex Task (~80 iterations)

```bash
/ralph-process "Build a payment processing endpoint with Stripe integration"
```

**What happens:**
1. Query optimized with comprehensive security and error handling
2. Complexity analyzed: COMPLEX (high security + many edge cases)
3. Promise generated: "IMPLEMENTATION COMPLETE: 6 requirements met"
4. Ralph Loop starts with 80 iterations

## How Complexity Estimation Works

The skill analyzes the validation report from complete-process and scores complexity based on:

| Factor | Weight | Impact |
|--------|--------|--------|
| Critical Issues | ×5 | Block implementation, require significant work |
| Edge Cases | ×3 | Hidden complexity, need testing cycles |
| Warnings | ×2 | Suggest refinement needs |
| Security Requirements | +10 | Adds testing overhead |
| Error Handling Gaps | +5 | Requires additional cycles |

**Score Ranges:**
- **0-25:** SIMPLE → 20 iterations
- **26-60:** MEDIUM → 40 iterations
- **61+:** COMPLEX → 80 iterations

## How Promise Generation Works

The skill extracts critical requirements from the validation report and formats them as a testable completion promise.

**Extraction Sources:**
1. Critical Issues section (✗ CRITICAL ISSUES)
2. Edge Cases section (📋 EDGE CASES)

**Promise Formats:**

```
1-3 requirements:
"COMPLETE: [req1] AND [req2] AND [req3]"

4-6 requirements:
"IMPLEMENTATION COMPLETE: N requirements met"

Unable to extract:
"IMPLEMENTATION COMPLETE AND VERIFIED"
```

**Example Conversions:**

| Validation Issue | Promise Requirement |
|-----------------|---------------------|
| "Missing authentication" | "Authentication implemented" |
| "No error handling" | "Error handling added" |
| "Input validation not defined" | "Input validation implemented" |

## When to Use What

### Use /ralph-process when:
- ✅ You want end-to-end automated implementation
- ✅ Task requires multiple refinement cycles
- ✅ You want automatic complexity estimation
- ✅ You need completion criteria generated automatically
- ✅ You're starting from a natural language query

### Use /complete-process when:
- ✅ You only need query optimization
- ✅ You want to review the optimized query before proceeding
- ✅ You plan to implement manually
- ✅ You want to see validation results without auto-execution

### Use /ralph-loop directly when:
- ✅ You already have a well-formed, optimized query
- ✅ You know the exact iteration count you need
- ✅ You have specific completion criteria ready
- ✅ You want full control over Ralph parameters

## Output Format

The skill provides detailed progress feedback:

```
═══════════════════════════════════════════════════════════
Ralph Process Integration
═══════════════════════════════════════════════════════════

Original Query:
  "Your query here"

Step 1/5: Running complete-process pipeline...
  ✓ Transform complete
  ✓ Validation complete
  ✓ Optimization complete
  Duration: 45s

Step 2/5: Analyzing complexity...
  Warnings: 5
  Critical Issues: 2
  Edge Cases: 4
  Security Requirements: YES
  Error Handling Gaps: YES

  Complexity Score: 47 (MEDIUM)
  ✓ Recommended iterations: 40

Step 3/5: Generating completion criteria...
  Critical requirements identified:
    • Requirement 1
    • Requirement 2
    • Requirement 3

  ✓ Promise: "IMPLEMENTATION COMPLETE: 3 requirements met"

Step 4/5: Preparing Ralph Loop prompt...
  ✓ Prompt built (287 lines)
  ✓ Validation requirements embedded
  ✓ Success criteria documented

Step 5/5: Starting Ralph Loop...
  Iterations: 40
  Promise: "IMPLEMENTATION COMPLETE: 3 requirements met"

  ⚠️  IMPORTANT: Ralph will run continuously until:
      • Promise is fulfilled, OR
      • Max iterations reached

  You can cancel with: /cancel-ralph

Starting Ralph Loop now...

═══════════════════════════════════════════════════════════
Ralph Loop Activated
═══════════════════════════════════════════════════════════
```

## Troubleshooting

### Error: "Complete-process pipeline failed"

**Cause:** The query couldn't be processed by complete-process

**Solution:**
- Check if your query is clear and actionable
- Try simplifying the query
- Use /complete-process directly to see detailed error

### Warning: "Could not parse validation report"

**Cause:** Validation report format was unexpected

**Solution:**
- Skill will use default values (MEDIUM, 40 iterations)
- Implementation proceeds with reasonable defaults
- No action needed, but results may be suboptimal

### Warning: "Query complexity is VERY HIGH"

**Cause:** Complexity score > 100

**Solution:**
- Consider breaking into smaller tasks
- Proceed with 80 iterations (may not complete fully)
- Review requirements for clarity

### Error: "Ralph Loop plugin not available"

**Cause:** Ralph Loop plugin is not installed

**Solution:**
- Install the official ralph-loop plugin
- Or use /complete-process for optimization only
- Or implement manually

## Advanced Usage

### Monitoring Progress

While Ralph Loop is running:

```bash
# View current state
cat .claude/ralph-loop.local.md

# Check iteration number
grep '^iteration:' .claude/ralph-loop.local.md
```

### Canceling

```bash
/cancel-ralph
```

### Manual Overrides

If you want to override the automatic settings:

```bash
# Step 1: Get optimized query
/complete-process "Your query"

# Step 2: Review output, note the validation report

# Step 3: Launch Ralph manually with custom params
/ralph-loop "Your optimized query" --max-iterations 100 --completion-promise "CUSTOM PROMISE"
```

## Technical Details

### Dependencies

- **complete-process-orchestrator** (v1.1.0+) - Query optimization
- **ralph-loop** (official Claude plugin) - Iterative implementation

### Architecture

- **Location:** `skills/ralph-process-integration/`
- **Type:** Orchestration skill
- **Invocation:** Via Skill tool
- **Context:** Uses Claude Code skill patterns

### Files

- `SKILL.md` - Main skill instructions with orchestration logic
- `capabilities.json` - Skill metadata and discovery
- `references/complexity-scoring.md` - Detailed scoring algorithm
- `references/promise-generation.md` - Promise creation patterns
- `templates/ralph-prompt-template.md` - Ralph prompt structure

## Best Practices

1. **Start with natural language** - The skill works best with clear, natural queries
2. **Trust the complexity estimation** - The algorithm is calibrated conservatively
3. **Review the summary** - Check the analysis before Ralph starts
4. **Let Ralph finish** - Don't cancel prematurely; iterations are conservative
5. **Check the promise** - Ensure the generated promise makes sense

## Limitations

- Requires both complete-process and ralph-loop to be available
- Complexity estimation is rule-based, not adaptive (yet)
- Promise generation may be generic for very ambiguous queries
- Maximum iterations capped at 80 (break large tasks into smaller ones)

## Version

**1.0.0** - Initial release (Plugin v1.0.8)

## Support

For issues or questions:
- Check the [main plugin README](../README.md)
- Review the [PROMPTCONVERTER documentation](../../PROMPTCONVERTER.md)
- See [complexity scoring details](../skills/ralph-process-integration/references/complexity-scoring.md)
- See [promise generation details](../skills/ralph-process-integration/references/promise-generation.md)
