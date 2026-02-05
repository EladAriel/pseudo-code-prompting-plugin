# Validation Checklist

Quick reference for validating pseudo-code across 6 dimensions.

## Security Dimension Checklist

### Authentication & Authorization
- [ ] Authentication type specified (OAuth, JWT, API key, mTLS, basic auth)
- [ ] If OAuth: providers named (Google, GitHub, etc.)
- [ ] If JWT: signing algorithm specified
- [ ] Authorization/access control defined (who can access what)
- [ ] Token TTLs specified (access token, refresh token)
- [ ] Session timeout specified (if applicable)

**CRITICAL if missing:**
- Authentication completely unspecified
- No authorization for sensitive operations

### Input & Data Protection
- [ ] Input validation strategy mentioned
- [ ] Data encryption specified for sensitive data
- [ ] Password hashing algorithm mentioned (if applicable)
- [ ] PII handling specified (how stored, protected, transmitted)
- [ ] Secrets management mentioned (not hardcoded)

**CRITICAL if missing:**
- No input validation
- Passwords stored in plaintext
- PII transmitted unencrypted

### Network & API Security
- [ ] HTTPS/secure transport specified
- [ ] CORS configuration mentioned (if browser-based)
- [ ] CSRF protection mentioned (if session-based)
- [ ] Rate limiting specified
- [ ] Secure cookie settings (HttpOnly, SameSite, Secure)

**CRITICAL if missing:**
- No HTTPS specified for sensitive operations
- No rate limiting on public endpoints
- Vulnerable cookie settings

### Attack Prevention
- [ ] SQL/NoSQL injection prevention mentioned
- [ ] Command injection prevention mentioned (if shell operations)
- [ ] XXE prevention (if XML parsing)
- [ ] SSRF prevention (if making external requests)
- [ ] Open redirect prevention (if redirects involved)

**CRITICAL if missing:**
- Clear injection vulnerability
- Unprotected redirect with user input

---

## Completeness Dimension Checklist

### Parameters & Specifications
- [ ] All function parameters named and valued
- [ ] No vague terms like "optimize", "handle", "improve"
- [ ] Every constraint specified with values
- [ ] Data types clear for complex objects
- [ ] External dependencies named (databases, services, APIs)

**CRITICAL if missing:**
- Key parameters undefined
- Vague requirements ("make it secure")

### File Paths & Architecture
- [ ] Target files or modules specified
- [ ] Folder structure implied or mentioned
- [ ] Integration points clear
- [ ] Tech stack context evident

**HIGH if missing:**
- No file paths mentioned
- Architecture unclear

### Constraints & Limits
- [ ] Timeout values specified
- [ ] Rate limit values specified (requests/time, attempts/window)
- [ ] TTL values specified (tokens, caches)
- [ ] Max value constraints (payload size, result count)
- [ ] Resource limits mentioned (connections, memory)

**CRITICAL if missing:**
- No timeout (can hang indefinitely)
- No rate limits on public endpoints

---

## Error Handling Dimension Checklist

### Error Codes & Responses
- [ ] HTTP status codes defined for each error scenario
- [ ] 4xx codes for client errors (400, 401, 403, 404, 409, 429)
- [ ] 5xx codes for server errors (500, 503)
- [ ] 3xx codes for redirects (if applicable)
- [ ] Consistent error code mapping (same error = same code)

**CRITICAL if missing:**
- No error codes defined at all
- No auth failure code (401)
- No permission failure code (403)
- No rate limit code (429)

### Error Recovery & Retry
- [ ] Retry logic specified (when to retry, max attempts)
- [ ] Backoff strategy specified (linear, exponential, jitter)
- [ ] Idempotency addressed (safe to retry)
- [ ] Fallback behavior defined (if retry fails)
- [ ] Circuit breaker pattern mentioned (if calling unreliable service)

**HIGH if missing:**
- No retry logic for transient failures
- Retry without backoff (thundering herd)
- Non-idempotent operations without safeguards

### Logging & Monitoring
- [ ] Logging enabled
- [ ] What gets logged specified (operations, errors, security events)
- [ ] Log level specified (debug, info, warn, error)
- [ ] Sensitive data NOT logged (passwords, tokens)
- [ ] Error details logged for debugging

**HIGH if missing:**
- Logging not mentioned
- Logging of sensitive data

---

## Data Handling Dimension Checklist

### Data Flow & Sources
- [ ] Data sources clear (user input, database, cache, external API)
- [ ] Data destination clear (where stored, transmitted)
- [ ] Data transformation steps mentioned
- [ ] Data serialization format specified (JSON, Protocol Buffers, etc.)

**CRITICAL if missing:**
- Data source/destination completely unclear

### Data Validation
- [ ] Input validation strategy specified
- [ ] Schema validation mentioned (if structured data)
- [ ] Format validation (email, URL, phone, etc.)
- [ ] Length/size validation (min, max)
- [ ] Business logic validation (can user do this?)

**CRITICAL if missing:**
- No validation mentioned
- Untrusted input not validated

### Data Storage & Lifecycle
- [ ] Storage location specified (database, cache, files)
- [ ] Retention period specified (how long kept)
- [ ] Deletion strategy specified (when removed)
- [ ] Backup/recovery strategy mentioned
- [ ] Encryption at rest specified (if sensitive)

**HIGH if missing:**
- Data lifetime not specified
- Sensitive data not encrypted at rest

### Concurrency & Data Integrity
- [ ] Concurrent access considered (multiple users simultaneously)
- [ ] Locking/synchronization strategy mentioned
- [ ] Race condition prevention addressed
- [ ] Dirty read prevention mentioned (if database)
- [ ] Eventual consistency acknowledged (if distributed)

**HIGH if missing:**
- Concurrency completely unaddressed
- Clear race condition in specification

---

## Performance Dimension Checklist

### Timeouts & Responsiveness
- [ ] Overall timeout specified (total operation time)
- [ ] API call timeout specified
- [ ] Database query timeout specified
- [ ] Connection timeout specified
- [ ] All timeouts have reasonable values (not 0)

**CRITICAL if missing:**
- No timeout specified (can hang indefinitely)
- Timeout of 0 or infinite

### Caching & Optimization
- [ ] Caching strategy defined (where, what, TTL)
- [ ] Cache invalidation strategy mentioned
- [ ] Cache backend specified (memory, Redis, database)
- [ ] Database query efficiency considered (indexes, pagination)
- [ ] Pagination used for large result sets

**HIGH if missing:**
- No caching for frequently accessed data
- Unbounded result sets (could return millions)
- No pagination mentioned

### Scalability & Resource Management
- [ ] Scalability constraints mentioned (10x load)
- [ ] Connection pooling mentioned (if database/HTTP)
- [ ] Resource limits specified (memory, CPU, disk)
- [ ] Batch size limits specified (if batch processing)
- [ ] Queue depth limits mentioned (if queue-based)

**HIGH if missing:**
- Unbounded resource growth
- Connection exhaustion risk
- Memory leak scenarios

---

## Edge Cases Dimension Checklist

### Concurrency & Simultaneous Operations
- [ ] Multiple simultaneous requests handled
- [ ] Race conditions prevented
- [ ] Deadlock prevention addressed
- [ ] Queue ordering specified (if queue-based)
- [ ] Duplicate request handling specified

**CRITICAL if missing:**
- Race condition causes data corruption
- Deadlock possible

### External Service Failures
- [ ] Provider/service downtime handled
- [ ] Retry strategy for failed calls
- [ ] Fallback behavior if service unavailable
- [ ] Graceful degradation mentioned
- [ ] Timeout prevents indefinite waiting

**CRITICAL if missing:**
- No handling for external service down
- System completely breaks if dependency fails

### Network & Partial Failures
- [ ] Network timeout handled
- [ ] Partial request/response handled
- [ ] Connection reset handled
- [ ] DNS failure handled
- [ ] SSL/TLS handshake failure handled

**HIGH if missing:**
- Network failures not acknowledged
- System assumes network always works

### Boundary Conditions
- [ ] Empty input handled (empty list, empty string, null)
- [ ] Maximum input handled (max size, max count)
- [ ] Negative numbers handled (if applicable)
- [ ] Zero values handled
- [ ] Special characters handled (if string processing)

**HIGH if missing:**
- Clear crash on empty input
- Unbounded behavior on max input

### Resource Cleanup
- [ ] File handles closed
- [ ] Database connections returned to pool
- [ ] Memory cleaned up on failure
- [ ] Temp files deleted
- [ ] Event listeners removed

**HIGH if missing:**
- Resource leaks on error paths
- Connections never closed

---

## Quick Severity Decision Tree

```
Is there a SECURITY vulnerability?
  → YES: CRITICAL

Is there a system-breaking bug (crash, infinite loop, race condition)?
  → YES: CRITICAL

Is authentication/authorization completely missing?
  → YES: CRITICAL

Is error handling completely absent?
  → YES: CRITICAL

Will this prevent deployment to production?
  → YES: CRITICAL

Is there an important edge case not handled?
  → YES: HIGH

Is error handling incomplete (some scenarios not covered)?
  → YES: HIGH

Is there an important best practice violation?
  → YES: HIGH

Is this a nice-to-have optimization?
  → YES: MEDIUM

Is this a monitoring/observability suggestion?
  → YES: MEDIUM

Is this an unlikely edge case?
  → YES: MEDIUM
```

---

## Validation Report Template

```
PSEUDO-CODE VALIDATION REPORT
═══════════════════════════════════════════════════════════════

SPECIFICATION TYPE: [API endpoint / Authentication / Data processing / etc.]
TECH STACK: [Node.js/Python/Go/etc. if detected]

✓ PASSED CHECKS
  [List all checks that passed]

✗ CRITICAL ISSUES (Must Fix)
  [For each issue:
    - What's wrong
    - Why it matters
    - How to fix it]

⚠ HIGH WARNINGS (Should Fix)
  [Organized by dimension]

📋 MEDIUM (Nice to Have)
  [Suggestions and optimizations]

═══════════════════════════════════════════════════════════════
DIMENSION SUMMARY

  Security:       ✓ PASSED / ⚠ ISSUES
  Completeness:   ✓ PASSED / ⚠ ISSUES
  Error Hdlg:     ✓ PASSED / ⚠ ISSUES
  Data Hdlg:      ✓ PASSED / ⚠ ISSUES
  Performance:    ✓ PASSED / ⚠ ISSUES
  Edge Cases:     ✓ PASSED / ⚠ ISSUES

OVERALL STATUS: READY / NEEDS REVIEW / BLOCKED

RECOMMENDATION: [Specific next steps]
═══════════════════════════════════════════════════════════════
```
