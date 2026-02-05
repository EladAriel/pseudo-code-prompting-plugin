# Requirement Validator Skill

Validates pseudo-code specifications across 6 critical dimensions with customizable checks per tech stack and severity levels.

## What This Skill Does

Validates pseudo-code specifications to catch missing details before implementation:

```
VALIDATION REPORT

✓ PASSED CHECKS
  ✓ Error codes defined
  ✓ Security requirements specified
  ✓ Timeouts included

✗ CRITICAL ISSUES (Must Fix)
  - No rate limiting on public endpoint

⚠ HIGH WARNINGS (Should Fix)
  - Token refresh concurrency not handled

📋 MEDIUM (Nice to Have)
  - Consider adding request tracing
```

Key features:
- **6 dimensions**: Security, completeness, error handling, data handling, performance, edge cases
- **Severity levels**: CRITICAL (must fix), HIGH (should fix), MEDIUM (nice to have)
- **Tech-stack aware**: Validation rules customized for detected tech stack
- **Actionable**: Each issue includes explanation and suggested fix

## When to Use

- Before implementing—catch issues early
- Reviewing specifications from team members
- Quality gate for specification release
- Validating pseudo-code across all dimensions

## 6 Validation Dimensions

### 1. Security

Checks for authentication, authorization, data protection, and attack prevention.

**Questions:**
- Is authentication specified? (type, providers, tokens)
- Is authorization (access control) defined?
- Input validation mentioned?
- Rate limiting specified?
- Sensitive data encryption required?
- Secure communication (HTTPS)?
- Secure cookie settings?

**CRITICAL issues:**
- No authentication for sensitive operations
- SQL/command injection vulnerability
- Plaintext secrets or PII
- No authorization checks
- Missing rate limiting on public endpoints

**HIGH issues:**
- Weak hashing algorithms
- Overly broad permissions
- Missing input sanitization
- No CSRF protection

**Customization by tech stack:**

**Node.js/Next.js:**
- Check for CORS configuration
- Check for helmet/security middleware
- JWT secret management

**Python/Django:**
- Check for CSRF middleware
- Check for permission classes
- Password validation rules

**Go:**
- Check for middleware chain
- Check for goroutine safety
- Context timeout usage

### 2. Completeness

Checks that all required parameters and details are specified.

**Questions:**
- All function parameters named and valued?
- Data types clear or implied?
- Constraints documented? (max length, valid values)
- Data provenance clear? (where does it come from)
- File paths mentioned?
- External dependencies called out?
- Tech stack context clear?

**CRITICAL issues:**
- Key parameters missing
- Vague requirements ("make it secure")
- No data types for complex objects
- Missing timeouts

**HIGH issues:**
- Constraints not documented
- File paths not specified
- Dependencies unclear

### 3. Error Handling

Checks that all error scenarios have defined handling with status codes.

**Questions:**
- Error codes defined for each scenario? (400, 401, 403, 404, 500, 503)
- Every error path covered?
- Retry strategies specified?
- Fallback behavior defined?
- Error logging enabled?
- Timeout scenarios handled?
- Rate limit exceeded handling specified?

**CRITICAL issues:**
- No error codes defined
- Silent failures
- Missing auth failure handling (no 401)
- Missing authorization failure handling (no 403)
- Unhandled exceptions

**HIGH issues:**
- Inconsistent error codes
- No retry logic for transient failures
- No timeout handling
- Inadequate logging

### 4. Data Handling

Checks how data flows through the system and is protected.

**Questions:**
- Data source clear? (user input, database, cache, API)
- Validation strategy specified?
- Storage location mentioned?
- Data lifecycle clear? (retention, deletion)
- Sensitive data handling? (PII, passwords, tokens)
- Safe serialization? (prevent XXE, injection)
- Concurrency considered? (race conditions)

**CRITICAL issues:**
- No data validation
- Sensitive data in logs
- Unencrypted sensitive data
- Injection vulnerability
- Unencrypted storage of PII

**HIGH issues:**
- Data lifetime not specified
- Missing encryption in transit
- No input sanitization
- Concurrent modification not handled

### 5. Performance

Checks for scalability, resource management, and optimization.

**Questions:**
- Timeouts specified? (API calls, queries, operations)
- Caching strategy defined?
- Database queries optimized?
- Scalability considered? (10x load)
- Rate limits specified?
- Resource usage bounded? (memory, CPU)
- Pagination used for large datasets?

**CRITICAL issues:**
- No timeout specified (can hang indefinitely)
- Unbounded loops or recursion
- No rate limiting on expensive operations

**HIGH issues:**
- Inefficient queries (full table scans)
- Missing caching
- Unbounded result sets
- No pagination

### 6. Edge Cases

Checks for boundary conditions and failure modes.

**Questions:**
- Concurrent requests handled?
- External service downtime handled?
- Network failures considered?
- Partial failures handled?
- Boundary conditions checked? (empty, zero, max)
- Resource cleanup specified?
- Recovery specified?
- Retryable operations idempotent?

**CRITICAL issues:**
- Race condition causes corruption
- No handling for service downtime
- Partial failures crash system

**HIGH issues:**
- Concurrency not considered
- No idempotency for retries
- Boundary conditions untested (empty, zero, max)
- Resource leaks on failure

## Tech Stack Customization

Validation rules adapted per tech stack:

### Node.js/Next.js-Specific
- Check for route handler error boundaries
- Check for middleware chain completeness
- Database connection pooling
- Async/await error handling

### Python/Django-Specific
- Check for middleware registration
- Check for decorator usage (login_required, permission_required)
- ORM query optimization
- Signal handler cleanup

### Go-Specific
- Check for error unwrapping (errors.Is, errors.As)
- Goroutine cleanup (WaitGroup, context cancellation)
- Channel close semantics
- Defer block cleanup

### Rust-Specific
- Check for Result/Option handling
- Check for lifetime annotations
- Check for mutex deadlock prevention
- Check for panic handling

## Severity Guidelines

### CRITICAL (Must Fix)
- Security vulnerabilities (injection, auth bypass, data breach)
- System crashes or infinite loops
- Race conditions causing data corruption
- Missing required functionality
- Prevents production deployment

### HIGH (Should Fix)
- Important edge cases not handled
- Incomplete implementations
- Performance issues
- Security best practices violated
- Should fix before deployment, but not blocking

### MEDIUM (Nice to Have)
- Optimizations
- Observability improvements
- Unlikely edge cases
- Code quality suggestions
- Can defer to future iterations

## Non-Applicable Checks

Some checks don't apply to all specifications. Handle gracefully:

```
Security: [SKIPPED - not a security-sensitive operation]
  Reasoning: This is data formatting, not authentication

Performance: [SKIPPED - batch operation, not real-time]
  Reasoning: Specification doesn't require response time guarantees
```

## Validation Report Format

```
PSEUDO-CODE VALIDATION REPORT
═══════════════════════════════════════════════════════════════

✓ PASSED CHECKS
  ✓ Check description here
  ✓ Another passed check
  [... list all passed checks ...]

✗ CRITICAL ISSUES (Must Fix)
  Issue Title
    Problem: [Explanation of what's wrong]
    Impact: [Why this matters]
    Fix: [Specific recommendation]

⚠ HIGH WARNINGS (Should Fix)
  Warning Title
    Problem: [What's missing or incorrect]
    Impact: [Consequence if not fixed]
    Fix: [Suggested improvement]

📋 MEDIUM (Nice to Have)
  Suggestion Title
    Why: [Why this would improve the spec]
    How: [Suggested approach]

═══════════════════════════════════════════════════════════════
DIMENSION SUMMARY

  Security:     ✓ PASSED (5/5 checks)
  Completeness: ⚠ 1 ISSUE (4/5 checks)
  Error Hdlg:   ✓ PASSED (6/6 checks)
  Data Hdlg:    ✓ PASSED (4/4 checks)
  Performance:  ⚠ 1 ISSUE (3/4 checks)
  Edge Cases:   ⚠ 1 ISSUE (3/4 checks)

OVERALL STATUS: [READY / NEEDS REVIEW / BLOCKED]

RECOMMENDATION:
  [Specific guidance on priority and next steps]

═══════════════════════════════════════════════════════════════
```

## Example Validations

### Example 1: Authentication Spec

INPUT:
```
implement_oauth_authentication(
  providers=["google", "github"],
  token_type="jwt",
  access_token_ttl="15m",
  refresh_token_enabled=true,
  session_timeout="24h",
  rate_limiting={"login_attempts": "10/1h"},
  error_handling={
    "invalid_provider": 400,
    "token_expired": 401,
    "insufficient_scope": 403,
    "rate_limit_exceeded": 429
  },
  security={
    "validate_redirect_uri": true,
    "use_pkce": true,
    "secure_cookie": true
  },
  logging=true,
  timeout="5s",
  retry={"max_attempts": 3}
)
```

OUTPUT:
```
✓ PASSED CHECKS
  ✓ Security: All OAuth best practices (PKCE, secure cookies)
  ✓ Error Handling: Comprehensive error codes
  ✓ Performance: Timeout specified
  ✓ Logging: Enabled

✗ CRITICAL ISSUES
  None

⚠ HIGH WARNINGS
  ⚠ Token refresh concurrency
    Problem: No mutex or lock specified for concurrent token refresh
    Fix: Add refresh_token_lock="redis" or equivalent

📋 MEDIUM
  → Consider token rotation strategy
  → Consider adding device tracking

OVERALL STATUS: READY
```

## Tips for Validators

1. **Skip gracefully**: If a dimension doesn't apply, explain why
2. **Explain severity**: Users should understand why each issue matters
3. **Be specific**: Don't say "add error handling"—specify which error codes
4. **Prioritize**: CRITICAL first, then HIGH
5. **Provide solutions**: Don't just identify problems
6. **Consider context**: Same issue could be CRITICAL in one context, MEDIUM in another

## See Also

- `prompt-structurer/` - Requirements transformation
- `/pseudo-code:validate` command - User-facing validation
- `/pseudo-code:transform` command - Transformation to pseudo-code
