# Ralph Process Integration Skill

## Purpose

The **Ralph Process Integration** skill combines the pseudo-code prompting plugin's complete-process workflow with the Ralph Loop plugin to provide an end-to-end automated implementation workflow.

This skill:
1. Optimizes user queries through the complete-process pipeline (transform → validate → optimize)
2. Analyzes the validation report to estimate complexity and iteration requirements
3. Generates specific completion promises from validation requirements
4. Writes all required files to `.claude/` directory for Ralph Loop
5. Extracts promise keywords and generates task summaries
6. Launches Ralph Loop with file references and optimized parameters for automated iterative implementation

## When to Use This Skill

**Use /ralph-process when:**
- You want automated iterative implementation after query optimization
- The task requires multiple refinement cycles
- You want complexity-based iteration planning
- You need automatic completion criteria generation

**Use /complete-process instead when:**
- You only need query optimization without implementation
- You want to review the optimized query before proceeding
- You plan to implement manually

**Use /ralph-loop directly when:**
- You already have a well-formed query
- You know the exact iteration count needed
- You have specific completion criteria ready

## Execution Workflow

The skill follows an 8-step workflow. Track token usage per step following [token-tracking.md](references/token-tracking.md).

### Step 1: Invoke Complete-Process Skill (30-90s)

**Action:** Use the Skill tool to invoke complete-process

```
Skill tool with:
  skill="pseudo-code-prompting:complete-process"
  args="[user's query text]"
```

**Outputs to Capture:**
- Optimized pseudo-code
- Validation report (with ✓ PASSED, ⚠ WARNINGS, ✗ CRITICAL ISSUES, 📋 EDGE CASES sections)
- Optimization summary
- Statistics

**Error Handling:**
- If complete-process fails: Display error, offer retry or cancel
- If output is incomplete: Use fallback defaults (medium complexity, 40 iterations)

**Display Format:**
```
═══════════════════════════════════════════════════════════
Ralph Process Integration
═══════════════════════════════════════════════════════════

Original Query:
  "[user's query]"

Step 1/8: Running complete-process pipeline...
  ✓ Transform complete
  ✓ Validation complete
  ✓ Optimization complete
  Duration: [X]s
```

### Step 2: Parse Validation Report

**Action:** Extract metrics from the validation report text

**What to Extract:**
- Count WARNINGS (lines with "-" under "⚠ WARNINGS" section)
- Count CRITICAL ISSUES (lines with "-" under "✗ CRITICAL ISSUES" section)
- Count EDGE CASES (lines with "-" under "📋 EDGE CASES" section)
- Count PASSED CHECKS (lines with "-" under "✓ PASSED CHECKS" section)
- Detect security requirements (keywords: auth, security, permission, token, credential)
- Detect error handling gaps (keywords: error, exception, fallback, timeout, retry)

**See:** [references/complexity-scoring.md](references/complexity-scoring.md) for detailed parsing logic

**Display Format:**
```
Step 2/8: Analyzing complexity...
  Warnings: [N]
  Critical Issues: [N]
  Edge Cases: [N]
  Security Requirements: [YES/NO]
  Error Handling Gaps: [YES/NO]
```

### Step 3: Calculate Complexity Score

**Formula:**
```
base_score = (warnings × 2) + (critical × 5) + (edge_cases × 3)
modifiers = security(+10) + error_handling(+5) - many_passed_checks(-5)
complexity_score = base_score + modifiers
```

**Classification:**

- Score ≤ 25: SIMPLE (20 iterations)
- Score 26-60: MEDIUM (40 iterations)
- Score ≥ 61: COMPLEX (80 iterations)

**See:** [references/complexity-scoring.md](references/complexity-scoring.md) for complete algorithm

**Display Format:**
```
  Complexity Score: [N] ([LEVEL])
  ✓ Recommended iterations: [20/40/80]
```

### Step 4: Generate Completion Promise

**Action:** Extract critical requirements from validation report and format as specific promise

**Promise Generation Rules:**

1. Extract top 3-4 critical issues
2. Convert negative statements to positive requirements
3. Add edge cases if needed to reach 3-4 requirements
4. Format as testable promise (max 100 chars)

**See:** [references/promise-generation.md](references/promise-generation.md) for detailed extraction rules

**Display Format:**
```
Step 3/8: Generating completion criteria...
  Critical requirements identified:
    • [Requirement 1]
    • [Requirement 2]
    • [Requirement 3]

  ✓ Promise: "[GENERATED_PROMISE_TEXT]"
```

### Step 5: Write Files to .claude/ Directory

**Action:** Create the `.claude/` directory and write all required files

**CRITICAL:** Ralph Loop requires files, NOT inline content. You MUST write files before invoking Ralph.

**Files to Write:**

1. **ralph-prompt.local.md** - Full prompt with requirements, validation, guidance
2. **optimized-pseudo-code.local.md** - Optimized pseudo-code from complete-process
3. **completion-promise.local.md** - Promise keyword and criteria

**See:** [templates/ralph-prompt-template.md](templates/ralph-prompt-template.md) for file structure

**Display Format:**
```
Step 4/8: Writing files to .claude/ directory...
  ✓ Created .claude/ directory
  ✓ Wrote ralph-prompt.local.md ([N] lines)
  ✓ Wrote optimized-pseudo-code.local.md ([N] lines)
  ✓ Wrote completion-promise.local.md ([N] lines)
```

### Step 6: Extract Promise Keyword

**Action:** Extract the promise keyword from generated promise text

**CRITICAL:** Ralph Loop expects ONLY the promise keyword, NOT the full text or `<promise>` tags.

**Extraction Logic:**

1. If promise contains `<promise>` tags: Extract text between tags
2. Otherwise: Use the promise text as-is
3. Validate: No `<` or `>` characters, uppercase, < 100 chars

**Display Format:**
```
Step 5/8: Extracting promise keyword...
  ✓ Promise: "[PROMISE_KEYWORD]"
```

### Step 7: Generate Task Summary

**Action:** Create a concise task summary for Ralph Loop invocation

**Format:**
```
"[Action verb] [main objective] following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"
```

**Examples:**
- "Implement user authentication following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"
- "Create working hours tracker app following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"

**Display Format:**
```
Step 6/8: Preparing Ralph Loop invocation...
  ✓ Task summary: "[TASK_SUMMARY]"
```

### Step 8: Launch Ralph Loop

**Action:** Invoke Ralph Loop via Skill tool with file references

**CRITICAL INVOCATION FORMAT:**

```
Skill tool with:
  skill="ralph-loop:ralph-loop"
  args="[task_summary] following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md --max-iterations [iterations] --completion-promise [promise_keyword]"
```

**See:** [references/ralph-invocation-specification.md](references/ralph-invocation-specification.md) for complete invocation rules

**Display Format:**
```
Step 7/8: Starting Ralph Loop...
  Task: [task_summary]
  Iterations: [N]
  Promise: "[promise_keyword]"
  Files: .claude/ralph-prompt.local.md, .claude/optimized-pseudo-code.local.md

  ⚠️  IMPORTANT: Ralph will run continuously until:
      • Promise is fulfilled, OR
      • Max iterations reached

  You can cancel with: /cancel-ralph

Step 8/8: Ralph Loop activated
═══════════════════════════════════════════════════════════
Ralph Loop Activated
═══════════════════════════════════════════════════════════
```

## Error Handling

### Complete-Process Failure

If complete-process skill fails, display error with options:

1. Retry with original query
2. Simplify query and retry
3. Cancel ralph-process

### Parsing Failure

If validation report cannot be parsed, use fallback defaults:

- Complexity: MEDIUM
- Iterations: 40
- Promise: "IMPLEMENTATION COMPLETE AND VERIFIED"

### Ralph Loop Unavailable

If ralph-loop skill not found:
```
Error: Ralph Loop plugin not available

The ralph-loop plugin is required for this integration.
Please install the official ralph-loop plugin from Claude plugins.
```

### Very High Complexity

If complexity_score > 100, warn user and recommend breaking task into smaller parts.

## Reference Documentation

- **[Complexity Scoring Algorithm](references/complexity-scoring.md)** - Detailed scoring rules and parsing logic
- **[Promise Generation Rules](references/promise-generation.md)** - How to extract and format completion promises
- **[Ralph Invocation Specification](references/ralph-invocation-specification.md)** - Complete Ralph Loop integration details
- **[Ralph Prompt Template](templates/ralph-prompt-template.md)** - Structure for .claude/ directory files
- **[Token Tracking](references/token-tracking.md)** - Real-time token consumption tracking and cost visibility

## Dependencies

- **complete-process-orchestrator v1.1.0+** - For query optimization pipeline
- **ralph-loop** - For iterative implementation execution

## Version

**1.5.0** - Refactored to modular structure with external references (under 250 lines)
