---
name: Validate Pseudo-Code
description: Check pseudo-code across 6 critical dimensions (security, completeness, error handling, data handling, performance, edge cases) with severity levels
arguments:
  - name: pseudo-code
    description: Pseudo-code to validate
    required: false
when-to-use: |
  - When you want to validate pseudo-code before implementation
  - When reviewing specifications from other team members
  - When you want to catch security/completeness issues early
  - When you need a structured quality report
examples:
  - "Validate API endpoint specification"
  - "Check security of authentication pseudo-code"
---

# Validate Pseudo-Code

This command validates pseudo-code across **6 critical dimensions**:

1. **Security** - Auth specified? Rate limiting? Input validation? Injection risks?
2. **Completeness** - All required parameters present? Data flows defined?
3. **Error Handling** - Every error scenario covered with correct status codes?
4. **Data Handling** - Where does data come from? How is it validated? Storage?
5. **Performance** - Scalable? Timeouts specified? Caching strategy?
6. **Edge Cases** - Concurrent requests? Failure modes? Recovery?

Each dimension returns severity levels:
- **✗ CRITICAL** - Must fix before implementation (security vulnerabilities, missing auth)
- **⚠ HIGH** - Should fix (incomplete error handling, missing rate limiting)
- **📋 MEDIUM** - Nice to have (optimization suggestions)

## Usage

Simply say:
> **Validate my pseudocode:** implement_oauth_authentication( providers=["google", "github"], token_type="jwt", ... )

## Output Example

```
PSEUDO-CODE VALIDATION REPORT
═══════════════════════════════════════════════════════════════

✓ PASSED CHECKS
  ✓ Security requirements specified (auth, PKCE, secure cookies)
  ✓ Error codes defined for all scenarios
  ✓ Rate limiting configured
  ✓ Timeout specified (5s)
  ✓ Retry logic with backoff
  ✓ Logging enabled

✗ CRITICAL ISSUES (Must Fix)
  None

⚠ HIGH WARNINGS (Should Fix)
  ⚠ Token refresh concurrency not explicitly handled
    → Consider adding mutex or similar mechanism

📋 MEDIUM (Nice to Have)
  ✓ PKCE enabled—good!
  → Consider adding token rotation strategy for extra security
  → Consider logging failed OAuth provider attempts for analytics

EDGE CASES TO CONSIDER
  ⚠ What happens if user logs in from multiple devices simultaneously?
  ⚠ How do you handle provider API downtime during login?
  ⚠ Token expiration during long-running user action?

═══════════════════════════════════════════════════════════════
OVERALL STATUS: READY
Recommendation: Ready for implementation. Address HIGH warnings before going to production.
```

## Severity Levels Explained

### CRITICAL Issues
These must be fixed before implementation. Examples:
- No authentication specified
- SQL injection vulnerability
- No error codes defined
- Missing authorization checks

### HIGH Warnings
These should be fixed. Examples:
- Incomplete error handling
- Missing rate limiting on public endpoints
- No input validation
- Missing timeout specifications

### MEDIUM Notes
These are optimizations and edge case considerations:
- Performance improvements
- Caching strategies
- Monitoring suggestions
- Recovery mechanisms

## Validation Dimensions

### 1. Security
- Is authentication specified? (OAuth, JWT, API keys, etc.)
- Is authorization (who can do what) specified?
- Are rate limits defined?
- Input validation mentioned?
- Secure data handling (encryption, hashing)?
- HTTPS/secure communication?

### 2. Completeness
- All parameters needed specified?
- Data types clear?
- Constraints documented (max length, valid values)?
- File paths mentioned?
- Dependencies called out?

### 3. Error Handling
- HTTP status codes defined? (400, 401, 403, 500, etc.)
- All error paths covered?
- Retry strategy specified?
- Fallback behavior defined?
- Error logging enabled?

### 4. Data Handling
- Data sources clear? (request body, database, cache, etc.)
- Data validation strategy?
- Where is data stored?
- Data lifecycle? (how long kept?)
- Sensitive data handling? (PII, secrets)

### 5. Performance
- Timeouts specified? (prevent hanging)
- Caching strategy defined?
- Database query efficiency considered?
- Scalability constraints?
- Concurrent request handling?

### 6. Edge Cases
- Concurrent requests?
- Provider/service downtime?
- Network failures?
- Partial failures?
- Boundary conditions (empty, max size, etc.)?

## Tips

- **Validation is strict intentionally** - Production code needs these checks. MEDIUM warnings can be ignored if truly not applicable to your use case.
- **Use validation early** - Catch issues before implementation saves time and money.
- **Address CRITICAL first** - These will cause failures or security issues.
- **Team alignment** - Share validation reports to ensure everyone understands the specification.

## See Also

- **Transform to pseudocode:** - Convert requirements to pseudo-code
- **Explain my project:** - Generate project explanations
- `skills/requirement-validator/references/validation-checklist.md` - Validation patterns and checklists
