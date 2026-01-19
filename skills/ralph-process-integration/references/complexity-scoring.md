# Complexity Scoring Algorithm

## Overview

The complexity scoring algorithm analyzes the validation report from the complete-process pipeline to estimate how many Ralph Loop iterations will be needed for implementation.

## Scoring Formula

### Base Score

```
base_score = (warnings × 2) + (critical_issues × 5) + (edge_cases × 3)
```

### Modifiers

```
modifiers = 0

if has_security_requirements:
    modifiers += 10

if has_error_handling_gaps:
    modifiers += 5

if passed_checks > 8:
    modifiers -= 5  # Well-defined requirements
```

### Final Score

```
complexity_score = base_score + modifiers
```

### Classification

```
if complexity_score <= 25:
    level = "SIMPLE"
    iterations = 20

elif complexity_score <= 60:
    level = "MEDIUM"
    iterations = 40

else:  # complexity_score > 60
    level = "COMPLEX"
    iterations = 80
```

## Weight Rationale

### Critical Issues (Weight: 5)

**Why weight: 5?**
- Block implementation progress
- Require significant design/architecture work
- Often involve multiple files or subsystems
- May require research or external dependencies

**Examples:**
- Missing authentication specification
- No error response definitions
- Undefined data models
- Missing API contracts

**Impact:** Each critical issue can require 3-5 iterations to properly address with testing.

### Edge Cases (Weight: 3)

**Why weight: 3?**
- Represent hidden complexity
- Require additional test scenarios
- Often uncover more edge cases during implementation
- Need defensive programming patterns

**Examples:**
- Handle expired tokens
- Database connection failures
- Invalid data format handling
- Race conditions

**Impact:** Each edge case requires 2-3 iterations for implementation and testing.

### Warnings (Weight: 2)

**Why weight: 2?**
- Suggest refinement opportunities
- May become critical during implementation
- Indicate incomplete specifications
- Often easier to address than critical issues

**Examples:**
- Missing optional parameters
- Unclear validation rules
- Performance considerations
- Documentation gaps

**Impact:** Each warning requires 1-2 iterations to address.

### Security Requirements (Modifier: +10)

**Why +10 points?**
- Security features require careful implementation
- Need thorough testing (happy path + attack scenarios)
- Often involve multiple layers (auth, validation, encryption)
- Mistakes have high consequences

**Indicators:**
- Keywords: "auth", "authentication", "authorization", "security", "permission", "token", "credential"
- Context: User management, payment processing, sensitive data

**Impact:** Adds approximately 5 additional iterations for proper security implementation.

### Error Handling Gaps (Modifier: +5)

**Why +5 points?**
- Comprehensive error handling takes time
- Requires thinking through failure scenarios
- Needs testing of error paths
- Often overlooked in initial implementation

**Indicators:**
- Keywords: "error", "exception", "fallback", "timeout", "retry", "validation"
- Context: External APIs, database operations, user input

**Impact:** Adds approximately 2-3 additional iterations for error handling coverage.

### Well-Defined Requirements (Modifier: -5)

**Why -5 points?**
- More passed checks = clearer requirements
- Less discovery needed during implementation
- Faster implementation with fewer surprises
- Reduces back-and-forth iterations

**Threshold:** > 8 passed checks

**Impact:** Saves approximately 2-3 iterations due to clarity.

## Calibration Examples

### Example 1: Simple Feature - Dark Mode Toggle

**Validation Report:**
```
✓ PASSED CHECKS (6)
- Clear component structure
- State management specified
- Theme values defined
- Persistence method clear
- User preference handling
- Accessibility considerations

⚠ WARNINGS (2)
- Consider system preference detection
- Add transition animations

✗ CRITICAL ISSUES (0)

📋 EDGE CASES (1)
- Handle mid-session theme switching
```

**Calculation:**
```
base = (2 × 2) + (0 × 5) + (1 × 3) = 7
modifiers = 0  # No security, no error handling gaps, < 8 passed
score = 7
level = SIMPLE (score <= 25)
iterations = 20
```

**Rationale:** Straightforward UI feature with clear requirements and minimal complexity.

---

### Example 2: Medium Feature - User Registration

**Validation Report:**
```
✓ PASSED CHECKS (5)
- Email format validation specified
- Password requirements defined
- User model structure clear
- API endpoint route defined
- Success response format

⚠ WARNINGS (5)
- Consider rate limiting
- Add email uniqueness check
- Define password strength meter
- Consider CAPTCHA for bot prevention
- Add terms of service acceptance

✗ CRITICAL ISSUES (2)
- Password hashing algorithm not specified
- Error response format not defined

📋 EDGE CASES (4)
- Duplicate email registration attempts
- Email already exists handling
- Weak password handling
- Network timeout during registration
```

**Calculation:**
```
base = (5 × 2) + (2 × 5) + (4 × 3) = 32
modifiers = +10 (security: authentication, passwords) + 5 (error handling gaps)
score = 47
level = MEDIUM (26 <= score <= 60)
iterations = 40
```

**Rationale:** Authentication feature with security implications, multiple edge cases, and error handling needs.

---

### Example 3: Complex Feature - Payment Processing

**Validation Report:**
```
✓ PASSED CHECKS (3)
- Payment gateway specified (Stripe)
- Currency defined (USD)
- Basic success flow outlined

⚠ WARNINGS (10)
- Add payment retry logic
- Consider PCI compliance requirements
- Add payment method validation
- Define refund workflow
- Add payment status polling
- Consider 3D Secure handling
- Add receipt generation
- Define webhook signature verification
- Add idempotency key handling
- Consider multi-currency support

✗ CRITICAL ISSUES (6)
- No error handling for declined payments
- Missing webhook endpoint specification
- No idempotency mechanism defined
- Missing payment validation rules
- No secure credential storage plan
- Transaction logging not specified

📋 EDGE CASES (8)
- Network timeout during payment
- Webhook delivery failures
- Duplicate payment attempts
- Partial refund scenarios
- Payment method expiration
- Currency conversion edge cases
- Race conditions in payment status
- Webhook replay attacks
```

**Calculation:**
```
base = (10 × 2) + (6 × 5) + (8 × 3) = 74
modifiers = +10 (security: payments, credentials) + 5 (extensive error handling needed)
score = 89
level = COMPLEX (score > 60)
iterations = 80
```

**Rationale:** High-stakes financial feature with security requirements, extensive edge cases, and comprehensive error handling needs.

---

### Example 4: Edge Case - Very Simple Typo Fix

**Validation Report:**
```
✓ PASSED CHECKS (2)
- File location identified
- Correct spelling provided

⚠ WARNINGS (0)

✗ CRITICAL ISSUES (0)

📋 EDGE CASES (0)
```

**Calculation:**
```
base = (0 × 2) + (0 × 5) + (0 × 3) = 0
modifiers = 0
score = 0
level = SIMPLE (score <= 25)
iterations = 20
```

**Rationale:** Trivial change, but Ralph still needs iterations to read file, make change, verify, commit.

---

### Example 5: Edge Case - Extremely Complex Migration

**Validation Report:**
```
✓ PASSED CHECKS (1)
- Target architecture identified

⚠ WARNINGS (15)
- [extensive list of considerations]

✗ CRITICAL ISSUES (10)
- [many blocking issues]

📋 EDGE CASES (12)
- [numerous edge cases]
```

**Calculation:**
```
base = (15 × 2) + (10 × 5) + (12 × 3) = 116
modifiers = +10 (security) + 5 (error handling)
score = 131
level = COMPLEX (score > 60, capped at 150)
iterations = 80
```

**Rationale:** Extremely complex, but capped at 80 iterations. User should consider breaking into smaller tasks.

## Adjustment Guidelines

### When Score Seems Wrong

**Score too low for actual complexity:**
- Check if validation report is incomplete
- Consider if requirements are vague (may discover complexity later)
- Manual override: Use `/ralph-loop` directly with higher iterations

**Score too high for actual complexity:**
- Check if warnings are overly cautious
- Consider if edge cases are unlikely/not relevant
- Manual override: Use `/ralph-loop` directly with lower iterations

### Iteration Budget Philosophy

**Conservative by design:**
- Better to have extra iterations than run out
- Ralph can complete early if promise fulfilled
- Running out of iterations = incomplete work
- Extra iterations cost nothing if not used

**Actual iteration usage patterns:**
- Simple tasks typically use 5-15 iterations
- Medium tasks typically use 15-35 iterations
- Complex tasks typically use 35-75 iterations
- Buffer of 5-10 iterations is healthy

### Fine-Tuning Weights

If you find scores consistently off, consider:

**If features consistently complete early:**
- Reduce weights (e.g., critical: 5 → 4)
- Reduce security modifier (10 → 8)
- This increases efficiency but risks running out

**If features consistently run out of iterations:**
- Increase weights (e.g., critical: 5 → 6)
- Increase security modifier (10 → 12)
- This improves completion rate but wastes iterations

**Current weights are calibrated for:**
- Thorough implementation (not minimal)
- Comprehensive testing
- Production-ready code quality
- Documentation and comments included

## Score Interpretation

| Score Range | Level | Iterations | Typical Features |
|-------------|-------|------------|------------------|
| 0-10 | SIMPLE | 20 | Typos, simple UI tweaks, documentation |
| 11-25 | SIMPLE | 20 | Single-component features, basic CRUD |
| 26-40 | MEDIUM | 40 | Multi-component features, simple APIs |
| 41-60 | MEDIUM | 40 | Authentication, data validation, integrations |
| 61-80 | COMPLEX | 80 | Payment processing, complex workflows |
| 81-150 | COMPLEX | 80 | Migrations, architectural changes, security-critical |

## Implementation Notes

### Parsing Considerations

- Validation reports are structured but format may vary slightly
- Use robust regex patterns that tolerate whitespace variations
- Count list items (lines starting with "-") under each section
- Keyword searches should be case-insensitive
- Handle missing sections gracefully (treat as 0 items)

### Error Handling

**If validation report malformed:**
- Use default: MEDIUM, 40 iterations
- Log warning to user
- Better to proceed with reasonable default than fail

**If score calculation fails:**
- Use default: MEDIUM, 40 iterations
- Display error details to user
- Offer option to specify iterations manually

**If score > 150:**
- Cap at 150, classify as COMPLEX
- Warn user about very high complexity
- Suggest breaking into smaller tasks

**If score < 0 (shouldn't happen but defensive):**
- Set to 0, classify as SIMPLE
- This handles any arithmetic edge cases

## Future Enhancements

### Machine Learning Approach

Could train a model on:
- Historical validation reports
- Actual iterations used
- User feedback on estimates

Advantages:
- Adapt to user's coding patterns
- Learn project-specific complexity factors
- Improve over time

Challenges:
- Need training data
- Model maintenance
- Less transparent/debuggable

### Dynamic Adjustment

Could adjust estimates mid-loop:
- If Ralph completes at 50% of iterations: reduce next estimate
- If Ralph hits max without completing: increase next estimate
- Track success rate and calibrate

### User Customization

Could allow user to:
- Set preferred iteration buffer (e.g., +20% safety margin)
- Adjust weight factors for their projects
- Define custom complexity thresholds
- Save per-project calibration settings

## Version History

**1.0.0** - Initial calibration with 2/5/3 weights and 10/5 modifiers
