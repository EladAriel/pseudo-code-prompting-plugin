# Validate: Check Pseudo-Code for Production Readiness

Validate pseudo-code completeness, security, and implementation readiness. Identifies gaps, ambiguities, and critical issues.

## Usage

```
Run validate: your_pseudo_code_here
```

## Quick Examples

### JWT Authentication Validation
```
Run validate: implement_jwt_authentication(
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={"secure": true, "httponly": true},
  rate_limiting={"max_attempts": 5, "window": "15m"}
)
```

### API Endpoint Validation
```
Run validate: create_endpoint(
  path="/api/users",
  method="POST",
  auth=true,
  schema={"email": "email:required:unique", "name": "string:max(100)"},
  rate_limit="100/hour"
)
```

### Database Query Validation
```
Run validate: query_users(
  filter={"status": "active"},
  pagination={"per_page": 20},
  fields=["id", "name", "email"],
  timeout="10s"
)
```

## What This Command Does

Your pseudo-code goes through **comprehensive validation** across 6 dimensions:

### 1. 🔒 Security Validation (CRITICAL)
- Is authentication specified for sensitive operations?
- Are roles/permissions defined?
- Is input validation/sanitization required?
- Are sensitive data protection mechanisms in place? (encryption, secure cookies, logging)
- Is rate limiting specified for APIs/exposed endpoints?
- Any OWASP Top 10 vulnerabilities?

### 2. ✅ Parameter Completeness (HIGH)
- Are all required parameters present?
- Are parameter types and formats specified?
- Do parameters have appropriate constraints?
- Are default values defined where needed?
- Any conflicting parameters?

### 3. ⚠️ Error Handling (HIGH)
- Are error scenarios identified?
- Are error responses defined? (HTTP codes, error messages)
- Are fallback behaviors specified?
- Are retry strategies present where needed?
- Are logging requirements clear?

### 4. 📊 Data Handling (MEDIUM)
- Are data sources identified?
- Are data formats specified?
- Are validation rules defined?
- Is storage strategy clear?
- Are data relationships documented?

### 5. ⚡ Performance/Scalability (MEDIUM)
- Are scalability requirements specified?
- Are timeout values defined?
- Are resource limits present?
- Is caching strategy considered?
- Are optimization criteria clear?

### 6. 🎯 Edge Cases (MEDIUM)
- Is empty/null input handling specified?
- Are boundary conditions covered?
- Are concurrent access scenarios handled?
- Are failure mode behaviors defined?
- Are invalid state transitions handled?

## Severity Levels

| Level | Examples | Action |
|-------|----------|--------|
| **CRITICAL** | Missing auth on sensitive ops, no input validation, undefined error handling, security vulnerabilities | **Must fix before implementation** |
| **HIGH** | Missing important parameters, ambiguous requirements, incomplete error handling | **Should fix before implementation** |
| **MEDIUM** | Missing optional parameters, documentation gaps, optimization opportunities | **Address during implementation** |
| **LOW** | Extra convenience features, additional monitoring, future extensibility | **Nice to have** |

## Example: Validation Report

### Input
```
Run validate: create_user_endpoint(
  path="/api/users",
  method="POST",
  schema={"email": "email:required:unique", "name": "string:max(100)"}
)
```

### Output

```
REQUIREMENT VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Function: create_user_endpoint(path="/api/users", method="POST", ...)

✓ PASSED CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Path and method specified clearly
- Request schema defined with field validation
- Email uniqueness constraint identified

✗ CRITICAL ISSUES (Must Fix)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Missing authentication
   Description: No auth specified on sensitive user creation endpoint
   Required Action: Add auth=true and define roles/permissions
   Example: auth=true, roles=["admin"], permissions=["users:write"]

2. No error response codes defined
   Description: Error scenarios not specified (400, 401, 403, 409, 500)
   Required Action: Define error_responses for validation failure, auth failure, conflict (duplicate), and server errors
   Example: error_responses={400, 401, 403, 409, 500}

3. Missing rate limiting
   Description: No protection against account creation abuse (signup bombing)
   Required Action: Specify rate_limit to prevent spam/abuse
   Example: rate_limit="10/hour", rate_limit_key="ip_address"

⚠ WARNINGS (Medium Priority)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. No password requirements specified
   Description: Password strength/length not defined
   Suggestion: Add password_requirements={"min_length": 12, "requires_uppercase": true, "requires_symbols": true}

2. Missing CORS configuration
   Description: No cross-origin access specified
   Suggestion: Add cors=["https://example.com"] if frontend is separate domain

📋 EDGE CASES TO CONSIDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Duplicate user creation (409 Conflict - user with same email exists)
  → Suggestion: Return 409 with message "Email already registered"

- Invalid email format (400 Bad Request)
  → Suggestion: Validate email format before database insert

- Database connection failure (500 Server Error)
  → Suggestion: Return 500 with generic message (don't expose internal errors)

- Malformed JSON in request body
  → Suggestion: Return 400 with schema validation errors

- Name containing special characters or scripts
  → Suggestion: Sanitize input, reject if suspicious patterns detected

💡 RECOMMENDATIONS FOR OPTIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Add timeout to prevent hanging requests: timeout="5s"
- Add logging for security audit trail: logging=true
- Add request validation schema: request_schema={...}
- Consider email verification: email_verification=true

OVERALL STATUS: BLOCKED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This requirement cannot proceed to implementation until the 3 critical
security issues are resolved (authentication, error handling, rate limiting).

NEXT STEPS:
1. Add auth=true with role-based access control
2. Define error_responses for all failure scenarios
3. Add rate_limit to prevent signup abuse
4. Re-run validation to verify issues are resolved
```

## Validation Scenarios

### ✅ Good Pseudo-Code (READY)

```
implement_jwt_authentication(
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={"secure": true, "httponly": true, "samesite": "strict"},
  rate_limiting={"max_attempts": 5, "window": "15m"},
  error_handling={"invalid_credentials": 401, "expired_token": 403, "rate_limit": 429},
  logging=true
)
```

**Validation Result:**
```
✓ PASSED CHECKS
- All security requirements specified
- Password hashing defined
- Cookie security: secure + httponly + samesite
- Rate limiting configured
- Error handling comprehensive
- Logging enabled

OVERALL STATUS: READY
This requirement is production-ready and can proceed to implementation.
```

### ⚠️ Incomplete Pseudo-Code (NEEDS REVIEW)

```
create_api_endpoint(path="/api/users", method="POST")
```

**Validation Result:**
```
✗ CRITICAL ISSUES
- No authentication specified
- Missing request body schema
- No error response codes defined

⚠ WARNINGS
- No rate limiting

OVERALL STATUS: BLOCKED
Address critical issues before proceeding to implementation.
```

### 💡 Optimizable Pseudo-Code (CAN PROCEED)

```
fetch_users(query={"status": "active"})
```

**Validation Result:**
```
✓ PASSED CHECKS
- Query filter specified

⚠ WARNINGS
- No pagination (could return huge result sets)
- No timeout specified
- No field projection (returns all fields)

💡 RECOMMENDATIONS
- Add pagination: pagination={"per_page": 20, "max": 100}
- Add timeout: timeout="10s"
- Add field projection: fields=["id", "name", "email"]
- Consider caching: cache={"ttl": "5m"}

OVERALL STATUS: NEEDS REVIEW
Can proceed with implementation, but strongly recommended to address warnings.
```

## Common Validation Patterns

### REST API Endpoint
```
✗ Missing: auth, error_responses, rate_limit
⚠ Consider: timeout, request_schema, response_schema
```

### Database Query
```
✗ Missing: pagination (for large result sets), timeout
⚠ Consider: field_projection, caching, sorting
```

### Authentication
```
✗ Missing: logout, token_invalidation, refresh_strategy
⚠ Consider: email_verification, password_strength, account_lockout
```

### Cache Layer
```
✗ Missing: cache_invalidation, fallback_strategy, ttl
⚠ Consider: cache_key_strategy, monitoring, statistics
```

## Memory Integration (Optional)

Session memory enhances validation by learning from previous validation sessions and catching recurring issues. This is **optional but valuable**.

### How Memory Helps Validation

**Session 1:** You validate an endpoint pseudo-code
- Validator finds: "Missing rate limiting" (CRITICAL issue)
- Memory learns: This is a recurring pattern for public endpoints

**Session 2:** You validate another endpoint pseudo-code
- Memory automatically:
  - Checks for rate limiting BEFORE generic validation runs
  - Catches the issue proactively (you might not have noticed)
  - Records that this pattern has failed 2+ times
- Result: 5-10% better validation quality, fewer missed issues

### Enabling Memory Integration

Memory is **automatic if available**, but you can control it:

- **Automatic (default):** If `.claude/pseudo-code-prompting/` exists, memory loads and enhances validation
- **Explicit:** Include project context if needed for domain-specific patterns
- **Disable if needed:** Include "ignore memory" in your pseudo-code if you want strict validation only

### What Memory Remembers About Validation

Memory learns and recalls:

| What | Where | How It Helps Validation |
|------|-------|------------------------|
| Recurring validation failures | progress.md | Proactively checks before validation |
| Domain-specific patterns | patterns.md | Applies domain knowledge (REST API, Auth, etc.) |
| Security patterns | patterns.md | Catches security gaps faster |
| Validation improvements | progress.md | Shows quality trends (pass rate improving) |
| Edge cases discovered | patterns.md | Checks edge cases learned from history |

### Interpreting Memory-Enhanced Validation

When validation report includes memory insights:

```
✗ CRITICAL ISSUES
1. No rate limiting
   [This pattern has caused 2 critical failures in previous validations]
   Required Action: Add rate_limit parameter

⚠ WARNINGS
2. Missing error response codes
   [Memory note: 85% of endpoints with this issue validated successfully after fix]
   Suggestion: Define error_responses for all failure scenarios
```

The "[Memory note]" lines show what was learned from previous sessions.

### Checking Validation Patterns

View learned validation patterns:
```
.claude/pseudo-code-prompting/patterns.md
  → Look for "## Common Gotchas" section
  → Shows issues found repeatedly across validations
```

View validation history and success rates:
```
.claude/pseudo-code-prompting/progress.md
  → "Validation Pass Rate" section
  → Shows improvement trends (87% → 95%)
  → "Recurring Issues" shows top validation failures
```

### Resetting Memory

If you want fresh validation without learned patterns:
- Delete `.claude/pseudo-code-prompting/` directory
- Memory will rebuild from scratch with this session
- Useful if switching to new tech stack or domain

## Validation Checklist

Before implementing, your pseudo-code should pass these checks:

### Security ✓
- [ ] Authentication specified for sensitive operations
- [ ] Authorization/roles/permissions defined
- [ ] Input validation requirements clear
- [ ] Sensitive data protection specified
- [ ] Rate limiting present where needed
- [ ] No obvious OWASP vulnerabilities

### Completeness ✓
- [ ] All required parameters present
- [ ] Parameter types and constraints clear
- [ ] Default values specified where needed
- [ ] No ambiguous parameters

### Error Handling ✓
- [ ] Error scenarios identified
- [ ] Error response codes defined
- [ ] Fallback behaviors specified
- [ ] Logging requirements clear

### Data ✓
- [ ] Data sources identified
- [ ] Data formats specified
- [ ] Validation rules defined
- [ ] Storage strategy clear

### Performance ✓
- [ ] Scalability requirements specified
- [ ] Timeout values defined
- [ ] Resource limits present
- [ ] Optimization opportunities identified

### Edge Cases ✓
- [ ] Empty/null inputs handled
- [ ] Boundary conditions covered
- [ ] Concurrent access scenarios handled
- [ ] Failure modes defined

## When to Use Validate

✅ **Use this command when:**
- You have pseudo-code and want to check for issues before implementation
- You want security/completeness validation
- You want recommendations for optimization
- You want a structured validation report
- You're sharing specs with a team and want approval

❌ **Don't use if:**
- You're writing pseudo-code from scratch (use `Run transform:` instead)
- You've already validated and are ready to implement
- You're debugging existing code

## Next Steps

After validation:

### If Status: READY ✓
→ Proceed to implementation
→ Use Transform command's cc10x bridge if available
→ Start TDD workflow

### If Status: NEEDS REVIEW ⚠️
→ Address high-priority warnings
→ Re-run validation
→ Proceed when confident

### If Status: BLOCKED ✗
→ Fix critical issues first
→ Re-run validation to verify
→ Then proceed to implementation

## Learn More

- [Quick Start Guide](../docs/quick-start.md)
- [Transform Command](./transform.md)
- [Bridge to cc10x Guide](../docs/bridge-to-cc10x.md)
