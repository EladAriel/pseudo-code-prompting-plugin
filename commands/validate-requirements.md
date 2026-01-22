---
description: Validate pseudo-code requirements for completeness and correctness
argument-hint: [pseudo-code]
---

# Validate Requirements

Analyze transformed pseudo-code to identify missing parameters, ambiguous requirements, and potential implementation risks.

## Memory Phase: Load Context

**Purpose**: Load patterns and validation history from prior sessions

```
Bash(command="mkdir -p .claude/pseudo-code-prompting")
Read(file_path=".claude/pseudo-code-prompting/patterns.md")
Read(file_path=".claude/pseudo-code-prompting/progress.md")
```

**Actions**:
1. Create memory directory if not exists
2. Load patterns.md to check for:
   - Validation patterns learned from previous requirements
   - Domain-specific validation rules
   - Known validation gotchas
3. Load progress.md to check for:
   - Common validation failures that should be watched for
   - What validations passed before

**Result**: Will apply learned validation patterns and flag known issues proactively.

---

## Task

Validate the following pseudo-code: `$ARGUMENTS`

Apply comprehensive requirement validation:

1. **Parameter Completeness** - Verify all required parameters are present
2. **Constraint Validation** - Check for necessary security, performance, and data constraints
3. **Edge Case Identification** - Identify unhandled scenarios and boundary conditions
4. **Clarity Assessment** - Flag vague terms and ensure specificity

## Validation Checklist

Use the requirement-validator skill capabilities:

### Security Requirements
- [ ] Authentication specified (if needed)
- [ ] Authorization/permissions defined
- [ ] Input validation requirements present
- [ ] Sensitive data handling specified

### Data Requirements
- [ ] Data sources identified
- [ ] Data formats specified
- [ ] Validation rules defined
- [ ] Storage strategy clear

### Error Handling
- [ ] Error scenarios identified
- [ ] Error responses defined
- [ ] Fallback behaviors specified
- [ ] Logging requirements present

### Performance Requirements
- [ ] Scalability needs specified
- [ ] Timeout values defined
- [ ] Resource limits present
- [ ] Caching strategy considered

## Output Format

Return validation results in this format:

```
Requirement Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Function: [function_name]

✓ PASSED CHECKS
- [Check description]

⚠ WARNINGS (Medium Priority)
- [Warning description + suggestion]

✗ CRITICAL ISSUES (Must Fix)
- [Issue description + required action]

📋 EDGE CASES TO CONSIDER
- [Edge case description]

💡 RECOMMENDATIONS
- [Recommendation]

Overall Status: [READY/NEEDS REVIEW/BLOCKED]
```

## Issue Severity Levels

- **Critical**: Missing auth, no validation, security vulnerabilities, data loss risks
- **High**: Missing important parameters, ambiguous requirements, incomplete error handling
- **Medium**: Missing optional parameters, documentation gaps, optimization opportunities
- **Low**: Nice-to-have features, enhanced UX details

## Key Validation Patterns

- Authentication: Check for auth=true, roles, permissions
- Data Validation: Look for validation rules, constraints, formats
- Error Handling: Verify error_handling strategy exists
- Performance: Check for timeouts, caching, scale considerations
- Integration: Verify dependencies, API versions specified

---

## Memory Phase: Record Learnings

**Purpose**: Save validation results and learnings for next session

**After validation completes:**

```
Read(file_path=".claude/pseudo-code-prompting/progress.md")

Edit(file_path=".claude/pseudo-code-prompting/progress.md",
     old_string="## Validation Learnings",
     new_string="## Validation Learnings

### Recurring Issues
- [If issues found today]: [Issue type] detected again (added to patterns)
[... keep existing learnings ...]")

Edit(file_path=".claude/pseudo-code-prompting/patterns.md",
     old_string="## Validation Patterns",
     new_string="## Validation Patterns

### New Patterns Found
- [Pattern from today's validation]: [How it was validated]
[... keep existing patterns ...]")

Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="## Last Updated",
     new_string="## Last Updated
2026-01-22 [current time] - Validation completed")
```

**Why**: Future validations will proactively check for recurring issues learned from this session.
