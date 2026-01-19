# Ralph Process Integration Skill

## Purpose

The **Ralph Process Integration** skill combines the pseudo-code prompting plugin's complete-process workflow with the Ralph Loop plugin to provide an end-to-end automated implementation workflow.

This skill:
1. Optimizes user queries through the complete-process pipeline (transform → validate → optimize)
2. Analyzes the validation report to estimate complexity and iteration requirements
3. Generates specific completion promises from validation requirements
4. Launches Ralph Loop with optimized parameters for automated iterative implementation

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

### Step 1: Invoke Complete-Process Skill

**Action:** Use the Skill tool to invoke complete-process

```
Skill tool with:
  skill="pseudo-code-prompting:complete-process"
  args="[user's query text]"
```

**Duration:** Approximately 30-90 seconds

**Outputs to Capture:**
- Optimized pseudo-code
- Validation report (with ✓ PASSED, ⚠ WARNINGS, ✗ CRITICAL ISSUES, 📋 EDGE CASES sections)
- Optimization summary
- Statistics

**Error Handling:**
- If complete-process fails: Display error, offer retry or cancel
- If output is incomplete: Use fallback defaults (medium complexity, 40 iterations)

**Display to User:**
```
═══════════════════════════════════════════════════════════
Ralph Process Integration
═══════════════════════════════════════════════════════════

Original Query:
  "[user's query]"

Step 1/5: Running complete-process pipeline...
```

Wait for complete-process to finish, then display:
```
  ✓ Transform complete
  ✓ Validation complete
  ✓ Optimization complete
  Duration: [X]s
```

### Step 2: Parse Validation Report

**Action:** Extract metrics from the validation report text

**Parsing Patterns:**

The validation report follows this structure:
```
✓ PASSED CHECKS
- [item 1]
- [item 2]

⚠ WARNINGS (Medium Priority)
- [warning 1]
- [warning 2]

✗ CRITICAL ISSUES (Must Fix)
- [critical 1]
- [critical 2]

📋 EDGE CASES TO CONSIDER
- [edge case 1]
- [edge case 2]
```

**Extraction Logic:**

1. **Count WARNINGS:** Count lines starting with "-" under the "⚠ WARNINGS" section
2. **Count CRITICAL ISSUES:** Count lines starting with "-" under the "✗ CRITICAL ISSUES" section
3. **Count EDGE CASES:** Count lines starting with "-" under the "📋 EDGE CASES" section
4. **Count PASSED CHECKS:** Count lines starting with "-" under the "✓ PASSED CHECKS" section

5. **Detect Security Requirements:** Search entire validation report for keywords:
   - "auth", "authentication", "authorization", "permission", "security", "token", "credential"
   - If any found: `has_security = true`

6. **Detect Error Handling Gaps:** Search entire validation report for keywords:
   - "error", "exception", "fallback", "timeout", "retry", "validation"
   - If any found: `has_error_handling = true`

**Parsing Implementation:**

```
metrics = {
  warnings: 0,
  critical: 0,
  edge_cases: 0,
  passed: 0,
  has_security: false,
  has_error_handling: false
}

# Extract each section
current_section = null
for each line in validation_report:
  if line contains "⚠ WARNINGS":
    current_section = "warnings"
  elif line contains "✗ CRITICAL ISSUES":
    current_section = "critical"
  elif line contains "📋 EDGE CASES":
    current_section = "edge_cases"
  elif line contains "✓ PASSED CHECKS":
    current_section = "passed"
  elif line starts with "- " and current_section is not null:
    metrics[current_section] += 1

# Keyword detection
if validation_report contains any of ["auth", "security", "permission", "token", "credential"]:
  metrics.has_security = true
if validation_report contains any of ["error", "exception", "fallback", "timeout", "retry"]:
  metrics.has_error_handling = true
```

**Display to User:**
```
Step 2/5: Analyzing complexity...
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

modifiers = 0
if has_security:
  modifiers += 10
if has_error_handling:
  modifiers += 5
if passed > 8:
  modifiers -= 5  # Simpler than expected

complexity_score = base_score + modifiers
```

**Classification:**
```
if complexity_score <= 25:
  complexity_level = "SIMPLE"
  iterations = 20
elif complexity_score <= 60:
  complexity_level = "MEDIUM"
  iterations = 40
else:
  complexity_level = "COMPLEX"
  iterations = 80
```

**Edge Case Handling:**
- If score < 0: Set to 0, classify as SIMPLE
- If score > 150: Cap at 150, classify as COMPLEX, use 80 iterations

**Rationale:**
- **Critical issues (weight: 5):** Block implementation, require significant work
- **Edge cases (weight: 3):** Hidden complexity, need testing cycles
- **Warnings (weight: 2):** Suggest refinement needs
- **Security (+10):** Adds iteration overhead for proper implementation and testing
- **Error handling (+5):** Requires additional testing cycles
- **Many passed checks (-5):** Clearer requirements = less discovery needed

**Display to User:**
```
  Complexity Score: [N] ([LEVEL])
  ✓ Recommended iterations: [20/40/80]
```

### Step 4: Generate Completion Promise

**Action:** Extract critical requirements from validation report and format as specific promise

**Extraction Rules:**

1. **From CRITICAL ISSUES section:**
   - Extract top 3-4 most important issues
   - Convert negative statements to positive requirements
   - Examples:
     - "Missing authentication" → "Authentication implemented"
     - "No error handling" → "Error handling complete"
     - "Missing input validation" → "Input validation added"

2. **From EDGE CASES section (if < 3 critical issues):**
   - Add top 1-2 edge cases to reach 3-4 requirements
   - Convert to positive requirements
   - Examples:
     - "Handle expired tokens" → "Token expiration handled"
     - "Database connection failures" → "DB failure handling added"

**Promise Format:**

**If 1-3 requirements (Simple):**
```
promise = "COMPLETE: [req1] AND [req2] AND [req3]"
```

**If 4-6 requirements (Medium/Complex):**
```
promise = "IMPLEMENTATION COMPLETE: [count] requirements met"
```

**If unable to extract specific requirements (Fallback):**
```
promise = "IMPLEMENTATION COMPLETE AND VERIFIED"
```

**Length Handling:**
- If promise > 100 chars: Simplify to high-level criteria
- Example: "COMPLETE: Auth + Validation + Error handling + Tests passing"

**Extraction Implementation:**

```
requirements = []

# Extract from critical issues
critical_section = extract_section(validation_report, "✗ CRITICAL ISSUES")
for item in critical_section (max 4):
  requirement = convert_to_positive_requirement(item)
  requirements.append(requirement)

# Add edge cases if needed
if len(requirements) < 3:
  edge_cases_section = extract_section(validation_report, "📋 EDGE CASES")
  needed = 3 - len(requirements)
  for item in edge_cases_section[:needed]:
    requirement = convert_to_positive_requirement(item)
    requirements.append(requirement)

# Format promise
if len(requirements) <= 3:
  promise = "COMPLETE: " + " AND ".join(requirements)
elif len(requirements) <= 6:
  promise = f"IMPLEMENTATION COMPLETE: {len(requirements)} requirements met"
else:
  promise = "IMPLEMENTATION COMPLETE AND VERIFIED"

# Length check
if len(promise) > 100:
  promise = f"COMPLETE: {len(requirements)} critical requirements met"
```

**Conversion Examples:**

| Critical Issue | Positive Requirement |
|----------------|---------------------|
| "Missing authentication requirement" | "Authentication added" |
| "No error responses specified" | "Error responses defined" |
| "Input validation not defined" | "Input validation implemented" |
| "No rate limiting" | "Rate limiting configured" |
| "Missing test coverage" | "Tests passing" |

**Display to User:**
```
Step 3/5: Generating completion criteria...
  Critical requirements identified:
    • [Requirement 1]
    • [Requirement 2]
    • [Requirement 3]

  ✓ Promise: "[GENERATED_PROMISE_TEXT]"
```

### Step 5: Build Ralph Loop Prompt

**Action:** Construct a comprehensive prompt for Ralph Loop

**Prompt Structure:**

```markdown
# Implementation Task

## Optimized Requirements

[Insert the optimized pseudo-code from complete-process output]

## Validation Requirements

Critical issues that must be addressed:
[For each critical issue from validation report]
- [Critical issue text]

Edge cases that must be handled:
[For each edge case from validation report (top 5)]
- [Edge case text]

## Implementation Guidance

Complexity Level: [SIMPLE/MEDIUM/COMPLEX]
Estimated Iterations: [20/40/80]

[If COMPLEX:]
This is a complex implementation. Take a systematic approach:
1. Start with core functionality
2. Add error handling and validation
3. Implement edge case handling
4. Add comprehensive tests
5. Verify all requirements before outputting promise

[If security requirements:]
Security Requirements Identified:
- Implement proper authentication/authorization
- Validate all inputs
- Handle sensitive data securely
- Follow security best practices

## Success Criteria

Implementation is complete when ALL of the following are true:

[For each requirement from the promise]
[N]. [Requirement] is fully implemented and tested

[Additional criteria based on complexity:]
[N+1]. All tests pass
[N+2]. Code follows best practices
[N+3]. Error handling is comprehensive
[N+4]. Edge cases are handled
[N+5]. Code is production-ready

## Completion Signal

When you have completed ALL requirements above and verified everything works:

Output this EXACT text:
<promise>[GENERATED_PROMISE_TEXT]</promise>

IMPORTANT RULES:
- Only output this promise when genuinely complete
- Do NOT lie to exit the loop - this defeats the purpose
- If blocked, document the blocker instead of faking completion
- Verify each requirement before claiming completion
```

**Display to User:**
```
Step 4/5: Preparing Ralph Loop prompt...
  ✓ Prompt built ([N] lines)
  ✓ Validation requirements embedded
  ✓ Success criteria documented
```

### Step 6: Launch Ralph Loop

**Action:** Invoke Ralph Loop via Skill tool with computed parameters

**Invocation:**

```
Skill tool with:
  skill="ralph-loop:ralph-loop"
  args="--max-iterations [iterations] --completion-promise '[promise]' [prompt]"
```

**Argument Construction:**

```
args = "--max-iterations " + iterations
args += " --completion-promise '" + promise + "'"
args += " " + prompt_text
```

**Pre-Launch Validation:**

Check if Ralph Loop skill is available:
- If not available: Display error with installation guidance
- Error message: "Ralph Loop plugin not found. Please install the official ralph-loop plugin."

**Display to User:**

```
Step 5/5: Starting Ralph Loop...
  Iterations: [N]
  Promise: "[promise text]"

  ⚠️  IMPORTANT: Ralph will run continuously until:
      • Promise is fulfilled, OR
      • Max iterations reached

  You can cancel with: /cancel-ralph

Starting Ralph Loop now...

═══════════════════════════════════════════════════════════
Ralph Loop Activated
═══════════════════════════════════════════════════════════
```

After this point, Ralph Loop takes over and begins iterating on the implementation.

## Error Handling

### Complete-Process Failure

**If complete-process skill fails:**

```
Error: Complete-process pipeline failed
Reason: [error message]

Options:
1. Retry with original query
2. Simplify query and retry
3. Cancel ralph-process

Please choose an option or provide guidance.
```

### Parsing Failure

**If validation report cannot be parsed:**

```
Warning: Could not parse validation report completely
Using fallback defaults:
  - Complexity: MEDIUM
  - Iterations: 40
  - Promise: "IMPLEMENTATION COMPLETE AND VERIFIED"

Proceeding with Ralph Loop launch...
```

### Promise Generation Failure

**If no requirements can be extracted:**

```
Warning: Could not extract specific requirements
Using generic promise: "IMPLEMENTATION COMPLETE AND VERIFIED"

This may require manual verification when Ralph completes.
```

### Ralph Loop Unavailable

**If ralph-loop skill not found:**

```
Error: Ralph Loop plugin not available

The ralph-loop plugin is required for this integration.
Please install the official ralph-loop plugin from Claude plugins.

Alternatively:
- Use /complete-process for query optimization only
- Use manual implementation workflow
```

### Very High Complexity

**If complexity_score > 100:**

```
Warning: Query complexity is VERY HIGH (score: [N])

This may require more than 80 iterations to complete.

Options:
1. Proceed with 80 iterations (may not complete fully)
2. Break down into smaller, focused tasks
3. Get more detailed requirements before proceeding

Recommendation: Consider breaking this into multiple smaller tasks
for better results.
```

## Examples

### Example 1: Simple Task

**User Query:** "Add a dark mode toggle to the settings page"

**Expected Flow:**
```
Step 1/5: Running complete-process pipeline...
  ✓ Duration: 35s

Step 2/5: Analyzing complexity...
  Warnings: 2
  Critical Issues: 0
  Edge Cases: 1
  Security Requirements: NO
  Error Handling Gaps: NO

  Complexity Score: 7 (SIMPLE)
  ✓ Recommended iterations: 20

Step 3/5: Generating completion criteria...
  Critical requirements identified:
    • Dark mode state management added
    • Toggle component implemented
    • Theme persistence working

  ✓ Promise: "COMPLETE: Dark mode toggle implemented AND Theme persistence working"

Step 4/5: Preparing Ralph Loop prompt...
  ✓ Prompt built (142 lines)

Step 5/5: Starting Ralph Loop...
  Iterations: 20
  Promise: "COMPLETE: Dark mode toggle implemented AND Theme persistence working"

Starting Ralph Loop now...
```

### Example 2: Medium Task

**User Query:** "Implement user registration with email validation"

**Expected Flow:**
```
Step 1/5: Running complete-process pipeline...
  ✓ Duration: 48s

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
    • Authentication flow implemented
    • Email validation added
    • Password hashing configured
    • Error responses defined

  ✓ Promise: "IMPLEMENTATION COMPLETE: 4 requirements met"

Step 4/5: Preparing Ralph Loop prompt...
  ✓ Prompt built (287 lines)

Step 5/5: Starting Ralph Loop...
  Iterations: 40
  Promise: "IMPLEMENTATION COMPLETE: 4 requirements met"

Starting Ralph Loop now...
```

### Example 3: Complex Task

**User Query:** "Build a payment processing endpoint with Stripe integration"

**Expected Flow:**
```
Step 1/5: Running complete-process pipeline...
  ✓ Duration: 62s

Step 2/5: Analyzing complexity...
  Warnings: 10
  Critical Issues: 6
  Edge Cases: 8
  Security Requirements: YES
  Error Handling Gaps: YES

  Complexity Score: 89 (COMPLEX)
  ✓ Recommended iterations: 80

Step 3/5: Generating completion criteria...
  Critical requirements identified:
    • Stripe API integration complete
    • Payment validation implemented
    • Webhook handling added
    • Error handling comprehensive
    • Security measures in place
    • Idempotency keys configured

  ✓ Promise: "IMPLEMENTATION COMPLETE: 6 requirements met"

Step 4/5: Preparing Ralph Loop prompt...
  ✓ Prompt built (412 lines)
  ✓ Security requirements highlighted
  ✓ Comprehensive success criteria included

Step 5/5: Starting Ralph Loop...
  Iterations: 80
  Promise: "IMPLEMENTATION COMPLETE: 6 requirements met"

  ⚠️  IMPORTANT: This is a complex implementation with security implications.
  Ralph will iterate up to 80 times to ensure proper implementation.

Starting Ralph Loop now...
```

## Best Practices

### For Skill Invocation

1. **Always use Skill tool** - Never try to execute scripts directly
2. **Capture all outputs** - Extract optimized query, validation report, and stats
3. **Parse carefully** - Validation reports have consistent structure but be robust to variations
4. **Display progress** - Keep user informed at each step
5. **Handle errors gracefully** - Always provide fallback options

### For Complexity Scoring

1. **Conservative estimates** - Better to have extra iterations than run out
2. **Weight critical issues heavily** - They block implementation
3. **Consider security overhead** - Security features take time to implement correctly
4. **Account for testing** - Complex features need more test cycles

### For Promise Generation

1. **Be specific when possible** - Helps Claude know exactly what to achieve
2. **Keep promises testable** - Should be verifiable by checking code/tests
3. **Use fallback for ambiguity** - Generic promise better than wrong promise
4. **Limit to 3-6 requirements** - Too many makes promise unwieldy

### For Ralph Integration

1. **Always set max-iterations** - Never rely on promise alone for safety
2. **Document success criteria clearly** - Ralph needs to know what "done" means
3. **Include verification steps** - Remind Ralph to test before claiming completion
4. **Warn about consequences** - Lying about completion defeats the purpose

## Technical Notes

- **Skill invocation:** Uses Skill tool following Claude Code patterns
- **Parsing:** Text-based regex patterns, robust to formatting variations
- **Scoring:** Rule-based algorithm, transparent and debuggable
- **Promise format:** Follows Ralph Loop requirements (<promise>TEXT</promise>)
- **Context optimization:** Only final outputs retained, intermediates discarded
- **Error handling:** Graceful degradation with sensible defaults

## Dependencies

- **complete-process-orchestrator v1.1.0+** - For query optimization pipeline
- **ralph-loop** - For iterative implementation execution

## Version

**1.0.0** - Initial release with complexity estimation and promise generation
