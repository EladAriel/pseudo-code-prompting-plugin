---
name: ralph-process
description: Automated pseudo-code transformation + Ralph Loop integration. Transforms queries, estimates complexity, generates promises, and launches iterative implementation.
allowed-tools: Read, Write, Bash, Skill
model: sonnet
---

# Ralph Process Integration

Transform natural language → Optimized pseudo-code → Automated implementation with Ralph Loop.

## WORKFLOW CHECKLIST

When user invokes `/ralph-process` or says "use pseudocode with ralph", follow these steps IN ORDER:

### ✅ STEP 1: Run Complete-Process Pipeline (30-90s)
```
Display: "Step 1/6: Running transformation pipeline..."
Action: Skill(pseudo-code-prompting:complete-process, args=user_query)
Capture: optimized_pseudo_code, validation_report
Display: "✓ Transformation complete | Tokens: [output_tokens]"
```

### ✅ STEP 2: Parse Validation Report (5s)
```
Display: "Step 2/6: Analyzing validation metrics..."
Extract from validation_report:
  - warnings_count = count lines with "- " under "⚠ WARNINGS"
  - critical_count = count lines with "- " under "✗ CRITICAL ISSUES"
  - edge_cases_count = count lines with "- " under "📋 EDGE CASES"
  - has_security = search for keywords: "auth|security|permission|token"
  - has_error_handling = search for keywords: "error|exception|fallback"

Display:
  "✓ Metrics extracted | Tokens: [output_tokens]
   Warnings: [N] | Critical: [N] | Edge Cases: [N]
   Security: [YES/NO] | Error Handling: [YES/NO]"
```

### ✅ STEP 3: Calculate Complexity (5s)
```
Display: "Step 3/6: Calculating complexity score..."

Formula:
  base_score = (warnings × 2) + (critical × 5) + (edge_cases × 3)
  modifiers = 0
  if has_security: modifiers += 10
  if has_error_handling: modifiers += 5
  if passed_checks > 8: modifiers -= 5
  complexity_score = base_score + modifiers

Classification:
  if score <= 25: level=SIMPLE, iterations=20
  elif score <= 60: level=MEDIUM, iterations=40
  else: level=COMPLEX, iterations=80

Display:
  "✓ Complexity: [LEVEL] (score: [N]) | Tokens: [output_tokens]
   Recommended iterations: [20/40/80]"
```

### ✅ STEP 4: Generate Completion Promise (10s)
```
Display: "Step 4/6: Generating completion criteria..."

Extract from validation_report:
  1. Get top 3-4 items from "✗ CRITICAL ISSUES" section
  2. Convert to positive requirements:
     "Missing auth" → "Authentication implemented"
     "No error handling" → "Error handling complete"
  3. If < 3 critical issues, add top edge cases to reach 3-4 items

Format promise:
  if requirements <= 3:
    promise = "COMPLETE: [req1] AND [req2] AND [req3]"
  elif requirements <= 6:
    promise = f"IMPLEMENTATION COMPLETE: {count} requirements met"
  else:
    promise = "IMPLEMENTATION COMPLETE AND VERIFIED"

Display:
  "✓ Promise generated | Tokens: [output_tokens]
   Requirements:
     • [Requirement 1]
     • [Requirement 2]
     • [Requirement 3]
   Promise: '[promise_text]'"
```

### ✅ STEP 5: Write Files to .claude/ Directory (10s)
```
Display: "Step 5/6: Writing files to .claude/ directory..."

Actions:
  1. Bash: mkdir -p .claude
  2. Write: .claude/ralph-prompt.local.md
     Content:
       # Implementation Task

       ## Optimized Requirements
       [optimized_pseudo_code]

       ## Validation Requirements
       ### Critical Issues Identified
       [critical_issues_list]

       ### Edge Cases to Handle
       [edge_cases_list]

       ## Implementation Guidance
       **Complexity Level:** [SIMPLE/MEDIUM/COMPLEX]
       **Estimated Iterations:** [20/40/80]

       ## Success Criteria
       Implementation is complete when ALL of the following are true:
       [numbered_list_of_requirements]

       ## Completion Signal
       When you have completed ALL requirements above and verified everything works:
       Output this EXACT text:
       <promise>[promise_text]</promise>

  3. Write: .claude/optimized-pseudo-code.local.md
     Content: [optimized_pseudo_code from complete-process]

  4. Write: .claude/completion-promise.local.md
     Content:
       # Completion Promise

       ## Promise Keyword
       `[promise_text]`

       ## Completion Criteria
       You MUST output `<promise>[promise_text]</promise>` when ALL of the following are true:
       [checklist_of_requirements]

Display:
  "✓ Files written successfully | Tokens: [output_tokens]
   Created:
     • .claude/ralph-prompt.local.md ([N] lines)
     • .claude/optimized-pseudo-code.local.md ([N] lines)
     • .claude/completion-promise.local.md ([N] lines)"
```

### ✅ STEP 6: Launch Ralph Loop (5s)
```
Display: "Step 6/6: Launching Ralph Loop..."

Generate task_summary:
  Format: "[Action verb] [main objective] following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"
  Example: "Implement user authentication following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"

Extract promise_keyword:
  If promise contains <promise> tags: extract text between tags
  Else: use promise_text as-is

Invoke:
  Skill(
    skill="ralph-loop:ralph-loop",
    args="[task_summary] --max-iterations [iterations] --completion-promise [promise_keyword]"
  )

Display:
  "═══════════════════════════════════════════════════════════
   Ralph Loop Activated | Tokens: [output_tokens]
   ═══════════════════════════════════════════════════════════

   Task: [task_summary]
   Iterations: [N]
   Promise: '[promise_keyword]'
   Files: .claude/ralph-prompt.local.md, .claude/optimized-pseudo-code.local.md

   ⚠️  Ralph will run continuously until:
       • Promise is fulfilled, OR
       • Max iterations reached

   You can cancel with: /cancel-ralph

   Starting Ralph Loop now..."
```

## CRITICAL RULES

### ❌ NEVER SKIP STEPS
- Do NOT jump directly to Ralph Loop
- Do NOT skip the complete-process pipeline
- Do NOT assume complexity without calculation
- Do NOT generate promises without validation report

### ✅ ALWAYS SHOW PROGRESS
- Display step number (1/6, 2/6, etc.) for each step
- Show token count: "Tokens: [N]" after each step completion
- Use status messages: "Running...", "Complete", "Failed"
- Keep user informed with clear, concise messages

### ✅ ALWAYS WRITE FILES
- Ralph Loop REQUIRES files in .claude/ directory
- NEVER pass inline content to Ralph
- Files must use .local.md extension
- Verify files exist before launching Ralph

### ✅ TOKEN TRACKING
After EVERY step completion, display:
```
"✓ [Step description] | Tokens: [output_tokens_from_this_step]"
```

This helps users track:
- Progress through the workflow
- Token consumption per step
- Which steps are most expensive

## ERROR HANDLING

### Error: Complete-Process Fails
```
Display:
  "❌ Step 1 failed: Complete-process pipeline error
   Reason: [error_message]

   Options:
   1. Retry with original query
   2. Simplify query and retry
   3. Cancel ralph-process

   What would you like to do?"
```

### Error: Validation Report Cannot Be Parsed
```
Display:
  "⚠️  Warning: Could not parse validation report completely
   Using fallback defaults:
     • Complexity: MEDIUM
     • Iterations: 40
     • Promise: 'IMPLEMENTATION COMPLETE AND VERIFIED'

   Proceeding with Ralph Loop launch..."
```

### Error: Ralph Loop Plugin Not Found
```
Display:
  "❌ Error: Ralph Loop plugin not available

   The ralph-loop plugin is required for this integration.
   Please install the official ralph-loop plugin.

   Alternatively:
   • Use /complete-process for query optimization only
   • Use manual implementation workflow"
```

### Error: File Write Fails
```
Display:
  "❌ Error: Could not write files to .claude/ directory
   Reason: [error_message]

   Trying fallback location: ./tmp/claude/
   [If fallback succeeds]: ✓ Files written to ./tmp/claude/
   [If fallback fails]: ❌ Cannot proceed without file storage"
```

## EXAMPLES

### Example 1: Simple Task
```
User: "Add a dark mode toggle to the settings page"

Step 1/6: Running transformation pipeline...
  ✓ Transformation complete | Tokens: 1,234

Step 2/6: Analyzing validation metrics...
  ✓ Metrics extracted | Tokens: 156
   Warnings: 2 | Critical: 0 | Edge Cases: 1
   Security: NO | Error Handling: NO

Step 3/6: Calculating complexity score...
  ✓ Complexity: SIMPLE (score: 7) | Tokens: 45
   Recommended iterations: 20

Step 4/6: Generating completion criteria...
  ✓ Promise generated | Tokens: 89
   Requirements:
     • Dark mode state management added
     • Toggle component implemented
     • Theme persistence working
   Promise: 'COMPLETE: Dark mode toggle implemented AND Theme persistence working'

Step 5/6: Writing files to .claude/ directory...
  ✓ Files written successfully | Tokens: 234
   Created:
     • .claude/ralph-prompt.local.md (142 lines)
     • .claude/optimized-pseudo-code.local.md (67 lines)
     • .claude/completion-promise.local.md (28 lines)

Step 6/6: Launching Ralph Loop...
  ═══════════════════════════════════════════════════════════
   Ralph Loop Activated | Tokens: 67
  ═══════════════════════════════════════════════════════════

   Task: Implement dark mode toggle following specifications in .claude/ralph-prompt.local.md
   Iterations: 20
   Promise: 'COMPLETE: Dark mode toggle implemented AND Theme persistence working'

   Starting Ralph Loop now...
```

### Example 2: Complex Task
```
User: "Build a payment processing endpoint with Stripe integration"

Step 1/6: Running transformation pipeline...
  ✓ Transformation complete | Tokens: 2,345

Step 2/6: Analyzing validation metrics...
  ✓ Metrics extracted | Tokens: 267
   Warnings: 10 | Critical: 6 | Edge Cases: 8
   Security: YES | Error Handling: YES

Step 3/6: Calculating complexity score...
  ✓ Complexity: COMPLEX (score: 89) | Tokens: 56
   Recommended iterations: 80

Step 4/6: Generating completion criteria...
  ✓ Promise generated | Tokens: 178
   Requirements:
     • Stripe API integration complete
     • Payment validation implemented
     • Webhook handling added
     • Error handling comprehensive
     • Security measures in place
     • Idempotency keys configured
   Promise: 'IMPLEMENTATION COMPLETE: 6 requirements met'

Step 5/6: Writing files to .claude/ directory...
  ✓ Files written successfully | Tokens: 456
   Created:
     • .claude/ralph-prompt.local.md (412 lines)
     • .claude/optimized-pseudo-code.local.md (198 lines)
     • .claude/completion-promise.local.md (54 lines)

Step 6/6: Launching Ralph Loop...
  ═══════════════════════════════════════════════════════════
   Ralph Loop Activated | Tokens: 89
  ═══════════════════════════════════════════════════════════

   Task: Implement payment processing endpoint with Stripe following specifications
   Iterations: 80
   Promise: 'IMPLEMENTATION COMPLETE: 6 requirements met'

   ⚠️  This is a complex implementation with security implications.
   Ralph will iterate up to 80 times to ensure proper implementation.

   Starting Ralph Loop now...
```

## QUICK REFERENCE

| Step | Action | Token Display | Time |
|------|--------|---------------|------|
| 1 | Run complete-process | Show after completion | 30-90s |
| 2 | Parse validation report | Show after extraction | 5s |
| 3 | Calculate complexity | Show after calculation | 5s |
| 4 | Generate promise | Show after generation | 10s |
| 5 | Write .claude/ files | Show after all files written | 10s |
| 6 | Launch Ralph Loop | Show before handoff | 5s |

Total time before Ralph starts: **60-120 seconds**

## VERSION

**2.0.0** - Simplified workflow with token tracking and clear progress indicators
