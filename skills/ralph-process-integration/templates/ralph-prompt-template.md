# Ralph Loop Prompt Template

This template is used to construct the prompt that will be fed to Ralph Loop for iterative implementation.

## Template Structure

```markdown
# Implementation Task

## Optimized Requirements

{{OPTIMIZED_PSEUDO_CODE}}

## Validation Requirements

### Critical Issues Identified

{{#each CRITICAL_ISSUES}}
- {{this}}
{{/each}}

### Edge Cases to Handle

{{#each EDGE_CASES}}
- {{this}}
{{/each}}

## Implementation Guidance

**Complexity Level:** {{COMPLEXITY_LEVEL}}
**Estimated Iterations:** {{ITERATIONS}}

{{#if IS_COMPLEX}}
This is a complex implementation. Take a systematic approach:
1. Start with core functionality
2. Add error handling and validation
3. Implement edge case handling
4. Add comprehensive tests
5. Verify all requirements before outputting promise
{{/if}}

{{#if HAS_SECURITY}}
### Security Requirements Identified

Important security considerations for this implementation:
- Implement proper authentication/authorization
- Validate all inputs thoroughly
- Handle sensitive data securely
- Follow security best practices for {{FEATURE_TYPE}}
- Test security edge cases (invalid tokens, unauthorized access, etc.)
{{/if}}

{{#if HAS_ERROR_HANDLING}}
### Error Handling Requirements

This implementation requires comprehensive error handling:
- Handle all failure scenarios
- Provide clear error messages
- Implement fallback mechanisms
- Test error paths thoroughly
- Consider timeouts and retries where appropriate
{{/if}}

## Success Criteria

Implementation is complete when ALL of the following are true:

{{#each REQUIREMENTS}}
{{@index}}. {{this}} is fully implemented and tested
{{/each}}

{{BASE_INDEX}}. All tests pass (unit, integration, and e2e as applicable)
{{BASE_INDEX+1}}. Code follows best practices and is well-structured
{{BASE_INDEX+2}}. Error handling is comprehensive
{{BASE_INDEX+3}}. Edge cases are properly handled
{{BASE_INDEX+4}}. Code is production-ready and documented

## Verification Checklist

Before claiming completion, verify:

{{#each REQUIREMENTS}}
- [ ] {{this}}
{{/each}}
- [ ] Tests are passing
- [ ] No errors or warnings in output
- [ ] Edge cases handled gracefully
- [ ] Code is clean and maintainable
- [ ] Documentation is complete (README, comments, etc.)

## Completion Signal

When you have completed ALL requirements above and verified everything works:

Output this EXACT text:
<promise>{{PROMISE_TEXT}}</promise>

### IMPORTANT RULES

- **Match exactly:** The promise text must match character-for-character (including capitalization and spaces)
- **Verify first:** Check ALL requirements before outputting the promise
- **Be truthful:** Only output when genuinely complete - do not lie to exit the loop
- **If blocked:** If you cannot complete, document the blocker and what you tried instead of faking completion
- **Test thoroughly:** Run tests, check for errors, verify behavior before claiming done

Remember: The goal is to produce working, production-ready code. Take the time needed to do it right.
```

## Variable Mapping

When constructing the actual prompt, replace template variables with actual values:

| Variable | Source | Example |
|----------|--------|---------|
| `{{OPTIMIZED_PSEUDO_CODE}}` | Output from complete-process skill | "implement_authentication(type='jwt', ...)" |
| `{{CRITICAL_ISSUES}}` | Extracted from validation report | ["Missing auth spec", "No error handling"] |
| `{{EDGE_CASES}}` | Extracted from validation report | ["Handle expired tokens", "DB failures"] |
| `{{COMPLEXITY_LEVEL}}` | Calculated complexity | "MEDIUM" |
| `{{ITERATIONS}}` | Calculated iterations | 40 |
| `{{IS_COMPLEX}}` | complexity_level == "COMPLEX" | true/false |
| `{{HAS_SECURITY}}` | Security requirements detected | true/false |
| `{{HAS_ERROR_HANDLING}}` | Error handling gaps detected | true/false |
| `{{FEATURE_TYPE}}` | Inferred from query | "authentication", "API", "UI component" |
| `{{REQUIREMENTS}}` | List of positive requirements | ["Auth implemented", "Tests passing"] |
| `{{PROMISE_TEXT}}` | Generated promise | "COMPLETE: Auth added AND Tests passing" |
| `{{BASE_INDEX}}` | len(REQUIREMENTS) + 1 | Used for continuing numbered list |

## Example: Simple Feature

**Input:**
- Query: "Add dark mode toggle"
- Complexity: SIMPLE (score: 7)
- Iterations: 20
- Requirements: ["Dark mode toggle implemented", "Theme persistence working"]

**Output:**

```markdown
# Implementation Task

## Optimized Requirements

implement_dark_mode_toggle(
  component="SettingsPage",
  state_management="context",
  persistence="localStorage",
  theme_values={"light": {...}, "dark": {...}},
  transition="smooth"
)

## Validation Requirements

### Critical Issues Identified

(None identified)

### Edge Cases to Handle

- Handle mid-session theme switching
- System preference detection

## Implementation Guidance

**Complexity Level:** SIMPLE
**Estimated Iterations:** 20

## Success Criteria

Implementation is complete when ALL of the following are true:

1. Dark mode toggle implemented is fully implemented and tested
2. Theme persistence working is fully implemented and tested
3. All tests pass (unit, integration, and e2e as applicable)
4. Code follows best practices and is well-structured
5. Error handling is comprehensive
6. Edge cases are properly handled
7. Code is production-ready and documented

## Verification Checklist

Before claiming completion, verify:

- [ ] Dark mode toggle implemented
- [ ] Theme persistence working
- [ ] Tests are passing
- [ ] No errors or warnings in output
- [ ] Edge cases handled gracefully
- [ ] Code is clean and maintainable
- [ ] Documentation is complete (README, comments, etc.)

## Completion Signal

When you have completed ALL requirements above and verified everything works:

Output this EXACT text:
<promise>COMPLETE: Dark mode toggle implemented AND Theme persistence working</promise>

### IMPORTANT RULES

- **Match exactly:** The promise text must match character-for-character
- **Verify first:** Check ALL requirements before outputting the promise
- **Be truthful:** Only output when genuinely complete
- **If blocked:** Document the blocker instead of faking completion
- **Test thoroughly:** Run tests before claiming done
```

## Example: Medium Feature with Security

**Input:**
- Query: "Implement user registration"
- Complexity: MEDIUM (score: 47)
- Iterations: 40
- Has Security: true
- Requirements: ["Auth implemented", "Validation added", "Error handling complete", "Tests passing"]

**Output:**

```markdown
# Implementation Task

## Optimized Requirements

implement_user_registration(
  authentication={
    "type": "email_password",
    "hashing": "bcrypt",
    "salt_rounds": 12
  },
  validation={
    "email": "RFC5322",
    "password": "min_8_with_special"
  },
  endpoints={
    "register": "/api/auth/register",
    "verify": "/api/auth/verify-email"
  },
  error_handling=true,
  rate_limiting="5_per_15min"
)

## Validation Requirements

### Critical Issues Identified

- Password hashing algorithm not specified
- Error response format not defined

### Edge Cases to Handle

- Duplicate email registration attempts
- Email already exists handling
- Weak password handling
- Network timeout during registration

## Implementation Guidance

**Complexity Level:** MEDIUM
**Estimated Iterations:** 40

### Security Requirements Identified

Important security considerations for this implementation:
- Implement proper authentication/authorization
- Validate all inputs thoroughly
- Handle sensitive data securely
- Follow security best practices for authentication
- Test security edge cases (invalid tokens, unauthorized access, etc.)

### Error Handling Requirements

This implementation requires comprehensive error handling:
- Handle all failure scenarios
- Provide clear error messages
- Implement fallback mechanisms
- Test error paths thoroughly
- Consider timeouts and retries where appropriate

## Success Criteria

Implementation is complete when ALL of the following are true:

1. Auth implemented is fully implemented and tested
2. Validation added is fully implemented and tested
3. Error handling complete is fully implemented and tested
4. Tests passing is fully implemented and tested
5. All tests pass (unit, integration, and e2e as applicable)
6. Code follows best practices and is well-structured
7. Error handling is comprehensive
8. Edge cases are properly handled
9. Code is production-ready and documented

## Verification Checklist

Before claiming completion, verify:

- [ ] Auth implemented
- [ ] Validation added
- [ ] Error handling complete
- [ ] Tests passing
- [ ] Tests are passing
- [ ] No errors or warnings in output
- [ ] Edge cases handled gracefully
- [ ] Code is clean and maintainable
- [ ] Documentation is complete (README, comments, etc.)

## Completion Signal

When you have completed ALL requirements above and verified everything works:

Output this EXACT text:
<promise>IMPLEMENTATION COMPLETE: 4 requirements met</promise>

### IMPORTANT RULES

- **Match exactly:** The promise text must match character-for-character
- **Verify first:** Check ALL requirements before outputting the promise
- **Be truthful:** Only output when genuinely complete
- **If blocked:** Document the blocker instead of faking completion
- **Test thoroughly:** Run tests before claiming done
```

## Usage in Code

```
# Construct the prompt
prompt = ralph_prompt_template.render(
    optimized_pseudo_code=optimized_query,
    critical_issues=extracted_critical_issues,
    edge_cases=extracted_edge_cases,
    complexity_level=calculated_level,
    iterations=calculated_iterations,
    is_complex=(calculated_level == "COMPLEX"),
    has_security=detected_security,
    has_error_handling=detected_error_handling,
    feature_type=inferred_type,
    requirements=generated_requirements,
    promise_text=generated_promise
)

# Invoke Ralph Loop
invoke_ralph_loop(prompt, iterations, promise_text)
```

## Notes

- The template emphasizes verification and truthfulness
- It provides clear structure for Ralph to follow
- It includes multiple reminders not to fake completion
- Success criteria are explicit and checkable
- The promise format is highlighted and explained
- Security and error handling get special attention when detected
