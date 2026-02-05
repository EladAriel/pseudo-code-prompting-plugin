# Real-World Examples

Complete examples of transforming requirements to pseudo-code and validating them.

## Example 1: OAuth Authentication

### Original Requirement

```
Add OAuth authentication to our application. We want to support sign-in with
Google and GitHub. After successful authentication, create or update the user
in our database. Use JWT tokens with 15-minute access token TTL and 7-day
refresh tokens. Implement rate limiting for login attempts (10 per hour).
Automatically log out users after 24 hours of inactivity.
```

### Transform Process

**Step 1: Tech Stack Detection**
```
Found package.json with "next" → Detected: Next.js (Node.js)
Target structure: src/app/api/, src/lib/, src/middleware/
```

**Step 2: Auto-Compression**
```
Original: 420 chars
Already concise, no compression needed
```

**Step 3: Transform to Pseudo-Code**
```
Function name: implement + oauth + authentication
→ implement_oauth_authentication
```

**Step 4-5: Validate & Optimize**
```
Completeness: ✓ All parameters specified
Error Handling: Add missing error codes
Security: Add PKCE, secure cookie settings
Performance: Add timeout, retry logic
```

### Generated Pseudo-Code

```
implement_oauth_authentication(
  providers=["google", "github"],
  token_type="jwt",
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  session_timeout="24h",
  rate_limiting={
    "login_attempts": "10/1h",
    "token_refresh": "30/1h"
  },
  target_files=[
    "src/app/api/auth/[...auth].ts",
    "src/lib/auth.ts",
    "src/middleware/auth.ts"
  ],
  error_handling={
    "invalid_provider": 400,
    "invalid_code": 400,
    "missing_state": 400,
    "token_expired": 401,
    "invalid_refresh_token": 401,
    "insufficient_scope": 403,
    "provider_unavailable": 503,
    "rate_limit_exceeded": 429
  },
  security={
    "validate_redirect_uri": true,
    "use_pkce": true,
    "secure_cookie": true,
    "http_only": true,
    "same_site": "strict"
  },
  validation={
    "validate_email_format": true,
    "validate_provider_response": true,
    "validate_state_parameter": true
  },
  logging={
    "log_login_attempts": true,
    "log_successful_logins": true,
    "log_errors": true
  },
  timeout="5s",
  retry={"max_attempts": 3, "backoff": "exponential"},
  cache={"ttl": "5m", "key": "oauth_state"}
)
```

### Validation Report

```
✓ PASSED CHECKS
  ✓ OAuth best practices (PKCE, state parameter, nonce)
  ✓ Secure cookie settings
  ✓ Error codes for all scenarios
  ✓ Rate limiting configured
  ✓ Token TTLs specified
  ✓ Timeout and retry logic

✗ CRITICAL ISSUES: None

⚠ HIGH WARNINGS
  ⚠ Token refresh from multiple devices
    → Consider implementing token family tracking

📋 MEDIUM
  → Consider adding device fingerprinting
  → Consider adding suspicious activity alerts

OVERALL STATUS: READY
```

### Implementation Snapshot

Using this pseudo-code, cc10x would:

```
RED Phase:
  Write tests verifying:
  - OAuth login endpoint returns JWT
  - Access token expires after 15m
  - Refresh token renews access token
  - Rate limit exceeded returns 429
  - State parameter validated

GREEN Phase:
  Implement /api/auth/[...auth].ts to pass tests

REFACTOR Phase:
  Organize code, improve security comments
```

---

## Example 2: API Rate Limiting

### Original Requirement

```
Implement rate limiting for our public API. Each API key gets 1000 requests
per hour. Return 429 when exceeded. Store state in Redis. Use sliding window
algorithm. Include Retry-After header in responses.
```

### Generated Pseudo-Code

```
implement_api_rate_limiting(
  algorithm="sliding_window",
  rate_limit={
    "requests_per_hour": 1000,
    "identifier": "api_key"
  },
  target_files=[
    "src/middleware/rateLimit.ts",
    "src/lib/rateLimitStore.ts"
  ],
  storage={
    "type": "redis",
    "key_prefix": "rate_limit:",
    "ttl": "1h"
  },
  error_handling={
    "rate_limit_exceeded": 429,
    "invalid_api_key": 401,
    "redis_unavailable": 503
  },
  response_headers={
    "X-RateLimit-Limit": "1000",
    "X-RateLimit-Remaining": "[remaining]",
    "Retry-After": "[seconds]"
  },
  security={
    "validate_api_key": true,
    "protect_key_in_logs": true
  },
  logging={
    "log_limit_exceeded": true,
    "log_redis_errors": true
  },
  timeout="100ms",
  cache={"ttl": "30s"}
)
```

### Validation Report

```
✓ PASSED CHECKS
  ✓ Rate limit values specified
  ✓ Error code 429 for exceeded limits
  ✓ Backend specified (Redis)
  ✓ Response headers included
  ✓ Timeout specified (100ms)

✗ CRITICAL ISSUES: None

⚠ HIGH WARNINGS
  ⚠ No handling for Redis connection loss
    → Add fallback (deny or allow?) or circuit breaker

📋 MEDIUM
  → Consider logging top API consumers
  → Consider different limits per tier

OVERALL STATUS: NEEDS REVIEW
Recommended fix: Add Redis fallback behavior
```

---

## Example 3: Payment Processing (Complex)

### Original Requirement

```
Implement payment processing using Stripe. Accept credit card payments.
Validate card information before charging. Retry failed transactions up to
3 times. Log all transactions for auditing. Send email notifications on
success/failure. Handle webhook callbacks from Stripe. Encrypt and store
transaction data. Support refunds up to 30 days. Rate limit to prevent abuse.
Return proper error codes for each failure.
```

### Transform Process

**Compression**: Original 580 chars → compressed to ~400 chars (no critical details lost)

### Generated Pseudo-Code

```
implement_payment_processing(
  provider="stripe",
  payment_methods=["credit_card"],
  operations=["charge", "refund", "webhook"],
  charges={
    "validate_before_charging": true,
    "capture_immediately": true
  },
  refunds={
    "enabled": true,
    "window_days": 30
  },
  webhooks={
    "events": ["charge.succeeded", "charge.failed", "charge.refunded"],
    "verify_signature": true
  },
  target_files=[
    "src/services/payment.ts",
    "src/api/webhooks/stripe.ts",
    "src/models/Transaction.ts",
    "src/jobs/sendNotification.ts"
  ],
  validation={
    "validate_card_before_charge": true,
    "validate_webhook_signature": true,
    "validate_idempotency_key": true
  },
  error_handling={
    "invalid_card": 400,
    "card_declined": 402,
    "insufficient_funds": 402,
    "unauthorized": 401,
    "not_found": 404,
    "duplicate_transaction": 409,
    "stripe_error": 502,
    "stripe_timeout": 504
  },
  security={
    "encrypt_card_data": true,
    "never_log_full_card": true,
    "use_pci_compliant_service": true
  },
  notifications={
    "on_success": {"type": "email", "to": "customer"},
    "on_failure": {"type": "email", "to": "customer"},
    "on_refund": {"type": "email", "to": "customer"}
  },
  rate_limiting={
    "charges_per_minute": 10,
    "per_customer": true
  },
  storage={
    "transaction_data_encrypted": true,
    "storage_location": "database",
    "backup_strategy": "enabled"
  },
  logging={
    "log_all_transactions": true,
    "log_failures": true,
    "log_refunds": true,
    "audit_trail": true
  },
  retry={
    "max_attempts": 3,
    "backoff": "exponential",
    "max_wait_time": "5m"
  },
  timeout="10s",
  idempotency={
    "enabled": true,
    "key_source": "request_header",
    "storage": "redis",
    "ttl": "24h"
  }
)
```

### Validation Report

```
✓ PASSED CHECKS
  ✓ PCI compliance approach specified
  ✓ Webhook signature verification
  ✓ Card validation before charge
  ✓ Idempotency for retry safety
  ✓ Comprehensive error codes
  ✓ Encryption for sensitive data
  ✓ Rate limiting
  ✓ Audit logging
  ✓ Refund window specified

✗ CRITICAL ISSUES: None

⚠ HIGH WARNINGS
  ⚠ No circuit breaker for Stripe API
    → If Stripe down, all payments fail. Add fallback.
  ⚠ No timeout for webhook processing
    → Stripe webhooks may timeout. Specify timeout.

📋 MEDIUM
  → Consider reconciliation process for failed webhooks
  → Consider tracking failed charge reasons
  → Consider alerting on unusual patterns

OVERALL STATUS: NEEDS REVIEW
Recommended: Add circuit breaker and webhook timeout, then READY
```

---

## Example 4: Poor Specification (Gets Flagged)

### Original Requirement

```
Add API endpoint for user data. Make it secure. Handle errors. Use database.
```

### Generated Pseudo-Code (Before Fix)

```
implement_user_api(
  operation="read_user",
  ...
)
```

### Validation Report

```
✓ PASSED CHECKS: None

✗ CRITICAL ISSUES
  ✗ No authentication specified
    → Specify auth type (OAuth, JWT, API key)
  ✗ No input validation mentioned
    → How is user_id validated?
  ✗ No error handling defined
    → What HTTP codes for each error?
  ✗ Vague data source
    → Which database? Which table?

⚠ HIGH WARNINGS
  ⚠ No rate limiting
  ⚠ No timeout specified

OVERALL STATUS: BLOCKED
Recommendation: Requirement too vague. Provide more details:
  - What specific data does endpoint return?
  - How is user authenticated? (OAuth, JWT, API key)
  - What error scenarios? (not found, unauthorized, etc.)
  - What constraints? (timeout, rate limit)
```

### Improved Requirement

```
Add GET /api/users/:id endpoint. Require JWT authentication (Bearer token).
Return user object (id, email, name) or 404 if not found. Return 401 if no
auth token. Return 403 if user tries to access another user's data (unless admin).
Rate limit to 100 requests per minute per user. Timeout after 5 seconds.
Cache results for 5 minutes. Log all access attempts.
```

### Fixed Pseudo-Code

```
implement_user_api_get_by_id(
  method="GET",
  endpoint="/api/users/{id}",
  authentication={
    "type": "jwt",
    "scheme": "Bearer",
    "required": true
  },
  authorization={
    "check_ownership": true,
    "allow_admin_override": true
  },
  request_validation={
    "validate_user_id_format": true,
    "validate_numeric_id": true
  },
  response={
    "fields": ["id", "email", "name"],
    "exclude": ["password_hash", "secrets"]
  },
  target_files=["src/routes/users.ts"],
  error_handling={
    "invalid_user_id": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "rate_limited": 429,
    "server_error": 500
  },
  rate_limiting={
    "requests_per_minute": 100,
    "per_user": true
  },
  cache={
    "ttl": "5m",
    "key": "user:{id}",
    "invalidate_on": ["user.update", "user.delete"]
  },
  logging={
    "log_all_access": true,
    "log_authorization_failures": true
  },
  timeout="5s",
  retry={"enabled": false}
)
```

### Fixed Validation Report

```
✓ PASSED CHECKS
  ✓ JWT authentication required
  ✓ Authorization (ownership check)
  ✓ Input validation
  ✓ Error codes defined
  ✓ Rate limiting
  ✓ Cache strategy
  ✓ Timeout specified
  ✓ Logging enabled

✗ CRITICAL ISSUES: None

⚠ HIGH WARNINGS: None

OVERALL STATUS: READY
```

---

## Key Takeaways from Examples

1. **Specificity Matters**
   - "OAuth with Google, GitHub" vs. "Add authentication"
   - "10/1h rate limit" vs. "Implement rate limiting"
   - "JWT 15m TTL" vs. "Use tokens"

2. **Standard Parameters Are Essential**
   - Every pseudo-code includes timeout (prevents hanging)
   - Every pseudo-code includes error_handling (defines failure modes)
   - Every pseudo-code includes logging (enables debugging)

3. **Validation Catches Real Issues**
   - Example 3: Missing circuit breaker could lose payment data
   - Example 4: Vague requirement gets flagged as BLOCKED
   - Example 2: HIGH warning about Redis failure handling

4. **Implementation Follows Specification**
   - Pseudo-code becomes test specifications
   - Implementation validates against pseudo-code
   - Tests ensure compliance with spec

5. **Tech Stack Awareness**
   - Next.js: src/app/api/[resource]/route.ts
   - Django: app/views.py, app/models.py
   - Go: internal/handlers/, pkg/middleware/
   - Same feature, different file structures
