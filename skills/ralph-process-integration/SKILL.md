---
name: ralph-process
description: Auto transform + complexity estimation + Ralph Loop launch
allowed-tools: Read, Write, Bash, Skill
model: sonnet
---

# Ralph Process Integration

Transform query → Estimate complexity → Generate promise → Launch Ralph Loop

## MUST FOLLOW THIS 6-STEP WORKFLOW

### Step 1: Run Complete-Process (30-90s)

```text
Action: Skill(pseudo-code-prompting:complete-process, args=user_query)
Capture: optimized_pseudo_code, validation_report
Display: "✓ Step 1/6 complete | Tokens: [N]"
```

### Step 2: Parse Validation Metrics (5s)

```text
Extract from validation_report:
  warnings = count "- " under "⚠ WARNINGS"
  critical = count "- " under "✗ CRITICAL ISSUES"
  edge_cases = count "- " under "📋 EDGE CASES"
  has_security = search "auth|security|permission|token"
  has_error = search "error|exception|fallback"

Display: "✓ Step 2/6 complete | Tokens: [N]
         Warnings: [N] | Critical: [N] | Edge: [N]"
```

### Step 3: Calculate Complexity (5s)

```text
score = (warnings × 2) + (critical × 5) + (edge_cases × 3)
if has_security: score += 10
if has_error: score += 5

if score ≤ 25: level=SIMPLE, iterations=20
elif score ≤ 60: level=MEDIUM, iterations=40
else: level=COMPLEX, iterations=80

Display: "✓ Step 3/6 complete | Tokens: [N]
         Complexity: [LEVEL] (score: [N])
         Iterations: [N]"
```

### Step 4: Generate Promise (10s)

```text
1. Extract top 3-4 items from "✗ CRITICAL ISSUES"
2. Convert to positive: "Missing X" → "X implemented"
3. Format:
   - If ≤3 items: "COMPLETE: [req1] AND [req2] AND [req3]"
   - If 4-6 items: "IMPLEMENTATION COMPLETE: N requirements met"
   - Else: "IMPLEMENTATION COMPLETE AND VERIFIED"

Display: "✓ Step 4/6 complete | Tokens: [N]
         Promise: '[text]'"
```

### Step 5: Write Files to .claude/ (10s)

```text
Bash: mkdir -p .claude

Write .claude/ralph-prompt.local.md:
  # Implementation Task
  ## Optimized Requirements
  [optimized_pseudo_code]
  ## Critical Issues
  [list from validation]
  ## Success Criteria
  [numbered requirements]
  ## Completion Signal
  Output: <promise>[text]</promise>

Write .claude/optimized-pseudo-code.local.md:
  [optimized_pseudo_code]

Write .claude/completion-promise.local.md:
  # Completion Promise
  `[promise]`
  ## Criteria
  [checklist]

Display: "✓ Step 5/6 complete | Tokens: [N]
         Files: 3 created in .claude/"
```

### Step 6: Launch Ralph Loop (5s)

```text
task = "[verb] [objective] following specifications in .claude/ralph-prompt.local.md"

Skill(
  skill="ralph-loop:ralph-loop",
  args=task + " --max-iterations [N] --completion-promise [promise]"
)

Display: "✓ Step 6/6 complete | Tokens: [N]

         ═══════════════════════════════════════
         Ralph Loop Activated
         ═══════════════════════════════════════

         Task: [task]
         Iterations: [N]
         Promise: '[promise]'

         Starting now..."
```

## CRITICAL RULES

### Never Skip Steps

- ALWAYS run complete-process first
- ALWAYS calculate complexity (don't guess)
- ALWAYS write files before Ralph
- ALWAYS show token count after each step

### Always Show Progress

```text
Format: "✓ Step N/6 complete | Tokens: [output_tokens]"
```

Display after EVERY step completion to show:

- Which step just finished
- Token consumption for that step
- Progress through workflow (N/6)

### Always Write Files

Ralph REQUIRES files. Never pass inline content.

- Use `.local.md` extension
- Write to `.claude/` directory
- Verify files exist before launching

## ERROR HANDLING

### Complete-Process Fails

```text
"❌ Step 1 failed: [reason]
 Options: 1) Retry 2) Simplify 3) Cancel"
```

### Can't Parse Validation

```text
"⚠️  Using defaults: MEDIUM, 40 iterations
 Proceeding..."
```

### Ralph Plugin Missing

```text
"❌ Ralph Loop plugin required
 Install: claude plugins install ralph-loop"
```

### File Write Fails

```text
"❌ Can't write .claude/ files: [reason]
 Trying: ./tmp/claude/"
```

## EXAMPLES

### Simple Task

```text
User: "Add dark mode toggle"

Step 1/6: Running transformation...
✓ Step 1/6 complete | Tokens: 1,234

Step 2/6: Analyzing metrics...
✓ Step 2/6 complete | Tokens: 156
  Warnings: 2 | Critical: 0 | Edge: 1

Step 3/6: Calculating complexity...
✓ Step 3/6 complete | Tokens: 45
  Complexity: SIMPLE (score: 7)
  Iterations: 20

Step 4/6: Generating promise...
✓ Step 4/6 complete | Tokens: 89
  Promise: 'COMPLETE: Toggle implemented AND Persistence working'

Step 5/6: Writing files...
✓ Step 5/6 complete | Tokens: 234
  Files: 3 created in .claude/

Step 6/6: Launching Ralph...
✓ Step 6/6 complete | Tokens: 67

═══════════════════════════════════════
Ralph Loop Activated
═══════════════════════════════════════

Task: Implement dark mode toggle following specifications
Iterations: 20
Promise: 'COMPLETE: Toggle implemented AND Persistence working'

Starting now...
```

### Complex Task

```text
User: "Build payment processing with Stripe"

Step 1/6: Running transformation...
✓ Step 1/6 complete | Tokens: 2,345

Step 2/6: Analyzing metrics...
✓ Step 2/6 complete | Tokens: 267
  Warnings: 10 | Critical: 6 | Edge: 8

Step 3/6: Calculating complexity...
✓ Step 3/6 complete | Tokens: 56
  Complexity: COMPLEX (score: 89)
  Iterations: 80

Step 4/6: Generating promise...
✓ Step 4/6 complete | Tokens: 178
  Promise: 'IMPLEMENTATION COMPLETE: 6 requirements met'

Step 5/6: Writing files...
✓ Step 5/6 complete | Tokens: 456
  Files: 3 created in .claude/

Step 6/6: Launching Ralph...
✓ Step 6/6 complete | Tokens: 89

═══════════════════════════════════════
Ralph Loop Activated
═══════════════════════════════════════

Task: Implement payment processing following specifications
Iterations: 80
Promise: 'IMPLEMENTATION COMPLETE: 6 requirements met'

⚠️  Complex task with security implications
Ralph will iterate up to 80 times

Starting now...
```

## QUICK REFERENCE

| Step | Action | Time | Token Display |
| --- | --- | --- | --- |
| 1 | Complete-process | 30-90s | After completion |
| 2 | Parse validation | 5s | After extraction |
| 3 | Calculate complexity | 5s | After calculation |
| 4 | Generate promise | 10s | After generation |
| 5 | Write .claude/ files | 10s | After all writes |
| 6 | Launch Ralph | 5s | Before handoff |

**Total: 60-120 seconds before Ralph starts**

## VERSION

**2.0.0** - Simplified with token tracking (374 → 250 lines)
