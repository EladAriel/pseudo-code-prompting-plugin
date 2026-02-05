# OAuth Authentication Template

Example pseudo-code transformation for OAuth with JWT tokens.

## Requirement

```
Add OAuth authentication with Google and GitHub providers.
Support JWT tokens with 15-minute access token TTL and 7-day refresh tokens.
Rate limit login to 10 attempts per hour per IP.
Auto-logout users after 24 hours of inactivity.
```

## Transformed Pseudo-Code

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
    "src/auth/oauth.ts",
    "src/auth/strategies/google.ts",
    "src/auth/strategies/github.ts",
    "src/middlewares/auth.ts",
    "src/routes/auth.ts"
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
    "same_site": "strict",
    "sign_state_token": true,
    "validate_nonce": true
  },
  validation={
    "validate_email_format": true,
    "validate_provider_response": true,
    "validate_state_parameter": true,
    "validate_code_expiry": true
  },
  logging={
    "log_login_attempts": true,
    "log_successful_logins": true,
    "log_failed_authentications": true,
    "log_token_operations": true,
    "log_rate_limit_violations": true
  },
  timeout="5s",
  retry={
    "max_attempts": 3,
    "backoff": "exponential",
    "jitter": true
  },
  cache={
    "ttl": "5m",
    "key": "oauth_state",
    "backend": "redis"
  }
)
```

## What's Included

✓ **Authentication**: OAuth with 2 providers
✓ **Tokens**: JWT with separate access/refresh TTLs
✓ **Rate Limiting**: Per-IP login attempt limiting
✓ **Session Management**: 24h auto-logout
✓ **Security**: PKCE, secure cookies, state validation, nonce verification
✓ **Error Handling**: Specific error codes for each failure scenario
✓ **Validation**: Email format, provider response, state parameter
✓ **Logging**: All important operations logged
✓ **File Paths**: Tech stack aware (Node.js/Next.js structure)
✓ **Resilience**: Timeout, retry with exponential backoff
✓ **Performance**: Caching with Redis backend

## Why Each Parameter Matters

- `providers`: Specific OAuth providers (not just "OAuth")
- `token_type="jwt"`: Stateless authentication
- `access_token_ttl="15m"`: Balance between security and UX
- `refresh_token_ttl="7d"`: Longer-lived refresh tokens
- `session_timeout="24h"`: Security boundary for long sessions
- `rate_limiting`: Prevents brute force attacks
- `validate_redirect_uri`: Prevents redirect attacks
- `use_pkce`: PKCE protection for OAuth code exchange
- `secure_cookie` + `http_only` + `same_site`: Cookie security
- `sign_state_token`: Prevents CSRF attacks
- `validate_nonce`: Prevents replay attacks
- `timeout="5s"`: Prevents hanging if provider is slow
- `retry` with backoff: Handles transient failures gracefully
- `cache`: Stores OAuth state temporarily

## Validation Checklist

When validating this pseudo-code, check:

### Security ✓
- [x] OAuth best practices (PKCE, state, nonce)
- [x] Secure cookie settings (HttpOnly, SameSite, Secure)
- [x] Input validation (email format, provider response)
- [x] Rate limiting prevents brute force
- [x] Redirect URI validation prevents open redirect

### Completeness ✓
- [x] Two providers specified
- [x] Token TTLs explicit (access vs refresh)
- [x] Session timeout specified
- [x] All file paths mentioned
- [x] Rate limit values explicit

### Error Handling ✓
- [x] HTTP status codes for all scenarios
- [x] Provider unavailability handled (503)
- [x] Rate limit exceeded handled (429)
- [x] Invalid tokens handled (401)

### Data Handling ✓
- [x] OAuth state stored temporarily
- [x] Tokens validated before use
- [x] Email extracted and validated
- [x] Cache strategy defined

### Performance ✓
- [x] Timeout specified (prevents hanging)
- [x] Cache enabled (reduces provider calls)
- [x] Rate limiting prevents abuse

### Edge Cases ✓
- [x] Multiple simultaneous login attempts
- [x] Provider downtime handled (retry)
- [x] Token expiration during operation
- [x] Concurrent token refresh

## Next Steps

1. Validate this specification with `/pseudo-code:validate`
2. Save to cc10x for specification-driven TDD
3. Implement against this specification
4. Tests pass when behavior matches pseudo-code
