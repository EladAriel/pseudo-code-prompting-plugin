---
name: complete-process
description: Transform → Validate → Optimize pipeline (auto-chained)
allowed-tools: Skill
model: sonnet
---

# Complete Process Orchestrator

Auto-chain: Transform → Validate → Optimize

## MUST FOLLOW THIS 3-STEP WORKFLOW

When user invokes `/complete-process` or says "use complete process", run these 3 skills in sequence:

### Step 1: Transform Query (20-40s)

```text
Skill(pseudo-code-prompting:prompt-structurer, args=user_query)
Output: transformed_pseudo_code

Display: "✓ Step 1/3 complete | Tokens: [N]
         Transformed to pseudo-code"
```

### Step 2: Validate Requirements (15-30s)

```text
Skill(pseudo-code-prompting:requirement-validator, args=transformed_pseudo_code)
Output: validation_report with sections:
  - ✓ PASSED CHECKS
  - ⚠ WARNINGS
  - ✗ CRITICAL ISSUES
  - 📋 EDGE CASES

Display: "✓ Step 2/3 complete | Tokens: [N]
         Validation report generated"
```

### Step 3: Optimize Prompt (15-30s)

```text
Skill(pseudo-code-prompting:prompt-optimizer, args=transformed_pseudo_code + validation_report)
Output: optimized_pseudo_code

Display: "✓ Step 3/3 complete | Tokens: [N]
         Optimization complete"
```

### Final Output

```text
Display:
"═══════════════════════════════════════
 Complete Process Finished
═══════════════════════════════════════

Total Tokens: [sum_of_all_steps]
Duration: [N]s

## Optimized Pseudo-Code
[optimized_pseudo_code]

## Validation Report
[validation_report]

## Statistics
- Passed Checks: [N]
- Warnings: [N]
- Critical Issues: [N]
- Edge Cases: [N]

Ready for implementation!"
```

## CRITICAL RULES

### Never Skip Steps

- ALWAYS run all 3 steps in order
- NEVER skip validation
- NEVER skip optimization
- Each step builds on the previous

### Always Show Progress

After EACH step, display:

```text
"✓ Step N/3 complete | Tokens: [output_tokens]"
```

This shows users:

- Which step just finished (N/3)
- Token consumption for that step
- Progress through pipeline

### Always Return All Outputs

At the end, return:

- Optimized pseudo-code (for implementation)
- Validation report (for quality checks)
- Statistics (for tracking)

## ERROR HANDLING

### Transform Fails

```text
"❌ Step 1 failed: [reason]
 Cannot proceed without transformation
 Please simplify query and retry"
```

### Validation Fails

```text
"❌ Step 2 failed: [reason]
 Using transformed output without validation
 ⚠️  Optimization may be incomplete"
```

### Optimization Fails

```text
"❌ Step 3 failed: [reason]
 Using validated output without optimization
 ⚠️  Some parameters may be missing"
```

## EXAMPLE

### User Input

```text
User: "Build a REST API for managing tasks with authentication"
```

### Execution

```text
Step 1/3: Transforming query...
✓ Step 1/3 complete | Tokens: 567

Transformed to: build_task_api(
  type="rest",
  features=["crud", "auth"],
  endpoints=["/tasks", "/auth"],
  auth_type="jwt"
)

Step 2/3: Validating requirements...
✓ Step 2/3 complete | Tokens: 834

Validation Report:
✓ PASSED CHECKS
- Function name is descriptive
- Core parameters present
- Tech stack specified

⚠ WARNINGS
- Error handling not specified
- Rate limiting not mentioned

✗ CRITICAL ISSUES
- Authentication flow undefined
- Database choice not specified

📋 EDGE CASES
- Token expiration handling
- Concurrent request handling

Step 3/3: Optimizing...
✓ Step 3/3 complete | Tokens: 623

Optimized to: build_task_api(
  type="rest",
  features=["crud", "auth"],
  endpoints={
    "tasks": ["/tasks", "/tasks/:id"],
    "auth": ["/auth/login", "/auth/refresh"]
  },
  authentication={
    "type": "jwt",
    "flow": "login_returns_token",
    "token_expiry": "1h",
    "refresh_enabled": true
  },
  database="postgresql",
  error_handling={
    "validation_errors": "400_with_details",
    "auth_errors": "401_with_message",
    "server_errors": "500_generic"
  },
  rate_limiting={
    "enabled": true,
    "requests_per_minute": 60
  }
)

═══════════════════════════════════════
Complete Process Finished
═══════════════════════════════════════

Total Tokens: 2,024
Duration: 68s

Statistics:
- Passed Checks: 3
- Warnings: 2
- Critical Issues: 2
- Edge Cases: 2

Ready for implementation!
```

## INTEGRATION WITH RALPH

If user wants Ralph Loop integration after complete-process:

```text
User: "Now use Ralph to implement this"

Claude: Use the /ralph-process command instead, which includes
        complete-process automatically:

        /ralph-process Build a REST API for managing tasks with authentication

        This will run:
        1. Complete-process (transform + validate + optimize)
        2. Complexity estimation
        3. Promise generation
        4. Ralph Loop launch with optimized parameters
```

## QUICK REFERENCE

| Step | Skill | Time | Output |
| --- | --- | --- | --- |
| 1 | prompt-structurer | 20-40s | Pseudo-code |
| 2 | requirement-validator | 15-30s | Validation report |
| 3 | prompt-optimizer | 15-30s | Optimized pseudo-code |

**Total: 50-100 seconds**

## VERSION

**2.0.0** - Simplified workflow (885 → 260 lines)
