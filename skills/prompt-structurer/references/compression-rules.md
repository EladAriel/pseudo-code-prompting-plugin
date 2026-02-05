# Compression Rules

Guidelines for auto-compressing requirements from >1000 chars to 80% target.

## When to Compress

Compress if requirement is >1000 characters AND contains:
- Repetitive explanations
- Multiple examples that illustrate the same concept
- Verbose descriptions that can be condensed
- Redundant clarifications

Do NOT compress if requirement contains:
- Specific error codes or numbers (keep these!)
- Security requirements (keep these!)
- Constraint details (keep these!)
- Data structure specifications (keep these!)

## Compression Techniques

### 1. Combine Related Concepts

**Before:**
```
We need authentication. Users should be able to log in with email and password.
They should also be able to use OAuth. We support Google, GitHub, and Facebook.
Users should have JWT tokens that expire. Access tokens expire in 15 minutes.
Refresh tokens expire in 7 days.
```

**After:**
```
User authentication: email/password + OAuth (Google, GitHub, Facebook).
JWT tokens: access (15m TTL), refresh (7d TTL).
```

**Compression ratio:** 95% → 20% of original

### 2. Remove Repetitive Explanations

**Before:**
```
We want to implement a rate limiting system. Rate limiting is important for security.
It prevents brute force attacks. Each user should be limited to 10 login attempts
per hour. If a user exceeds this limit, they should get a 429 error. Rate limiting
should also apply to the password reset endpoint, which should be limited to 5
attempts per hour.
```

**After:**
```
Rate limiting: login (10/hour), password reset (5/hour). Return 429 if exceeded.
```

**Compression ratio:** 95% → 15% of original

### 3. Use Shorthand for Common Patterns

**Before:**
```
When users log in and their credentials are invalid, we should return a 401
Unauthorized status code. If users don't have permission to access a resource,
we should return a 403 Forbidden status code. If a resource doesn't exist,
return 404 Not Found.
```

**After:**
```
Error codes: invalid credentials (401), unauthorized access (403), not found (404).
```

**Compression ratio:** 85% → 20% of original

### 4. Extract Key Constraints

**Before:**
```
The API endpoint should have a timeout to prevent it from hanging indefinitely.
The timeout should be set to 5 seconds. If the timeout is exceeded, we should
return a 504 Gateway Timeout status. We should also implement retry logic with
exponential backoff, with a maximum of 3 attempts.
```

**After:**
```
Timeout: 5s (return 504). Retry: max 3 attempts with exponential backoff.
```

**Compression ratio:** 90% → 18% of original

### 5. Consolidate Data Flow

**Before:**
```
Users send their authentication request to the API. The API validates the
credentials against the user database. If valid, the API generates a JWT token
and returns it to the user. The user stores the token in local storage and uses
it to make subsequent requests. For each request, the API validates the token
before processing the request.
```

**After:**
```
Flow: user → authenticate → validate DB → generate JWT → store locally →
use for requests → validate token on each request.
```

**Compression ratio:** 90% → 30% of original

## Preservation Checklist

Keep these elements—never compress them:

- [x] Specific numbers and constraints (5s timeout, 10/hour limit, 15m TTL)
- [x] HTTP status codes (401, 403, 404, 429, 504)
- [x] Security requirements (PKCE, secure cookies, encryption)
- [x] Error scenarios (invalid credentials, not found, rate limited)
- [x] Technology choices (JWT, OAuth, Redis, PostgreSQL)
- [x] Provider names (Google, GitHub, Facebook)
- [x] File paths or module references
- [x] Data structure specifications
- [x] Behavioral constraints

## Examples from Real Requirements

### Example 1: OAuth Authentication

**Original (1,200 chars):**
```
Add OAuth authentication to our application. We want to support sign-in with Google
and GitHub. Users should be able to choose which provider they want to use. After
successful authentication, we should create or update the user record in our database.
We'll use JWT tokens for authentication. Access tokens should expire after 15 minutes.
Refresh tokens should be valid for 7 days. When an access token expires, the frontend
should use the refresh token to get a new access token. We should rate-limit login
attempts to prevent brute force attacks. The rate limit should be 10 attempts per hour.
If a user exceeds the rate limit, they should receive a 429 error. We need to log all
authentication attempts including successful and failed logins. Logging should include
the provider used, timestamp, and IP address. We should also implement a session timeout
of 24 hours. After 24 hours of inactivity, users should be automatically logged out.
```

**Compressed (250 chars, 79% compression):**
```
OAuth authentication with Google, GitHub. JWT tokens: access (15m), refresh (7d).
Rate limit: 10 login attempts/hour → 429. Log all attempts (provider, timestamp, IP).
Session timeout: 24h auto-logout. Refresh tokens renew access tokens.
```

### Example 2: API Rate Limiting

**Original (950 chars):**
```
We need to implement rate limiting for our public API endpoints. The rate limiting
should be based on the user's API key. Each user should have a limit of 1000 requests
per hour. If a user exceeds this limit, they should receive a 429 Too Many Requests
error. We're using a Node.js backend with Express. We should store the rate limit
data in Redis for performance. We should use a sliding window algorithm to track
requests. The sliding window should be reset every hour. When a request comes in, we
check if the user has exceeded their limit. If they haven't, we increment the counter
and allow the request. If they have exceeded the limit, we reject the request with a
429 error and include a Retry-After header to tell the client when they can retry.
We should log all rate limit violations for monitoring and analytics.
```

**Compressed (300 chars, 68% compression):**
```
Rate limiting: 1000 requests/hour per API key. Algorithm: sliding window (Redis).
Exceeded: return 429 with Retry-After header. Log all violations for analytics.
Tech: Node.js/Express, Redis backend.
```

## Compression Quality Metric

After compression, verify:

- [ ] **Specificity**: All numbers, error codes, constraints preserved
- [ ] **Clarity**: Core concepts still understandable
- [ ] **Completeness**: No critical information removed
- [ ] **Ratio**: Target 80% compression (±10%)

Example:
```
Original: 1,200 characters
Target: 1,200 × 0.80 = 960 characters minimum

If compressed to 250 characters:
Ratio = 250 / 1,200 = 21% of original = 79% compression ✓ (exceeds target)
```

## When Compression Fails

If you can't compress to 80% without losing critical information:

1. **Option A**: Keep original requirement (may take longer to process, but complete)
2. **Option B**: Ask user which details are most critical
3. **Option C**: Suggest user split into multiple smaller requirements

Example:
```
Requirement is 2,000 chars but contains:
- 5 different provider integrations
- 10 specific error scenarios
- 8 security requirements
- 6 performance constraints

Cannot compress to 80% without losing details.
→ Suggest: "This is complex. Should we focus on 1-2 providers first?"
```

## No Compression Needed If...

- Requirement is <1,000 characters (already concise)
- All content is specific (error codes, constraints, numbers)
- Removing anything would lose information
- Requirement is well-structured and clear

**Decision rule:** Compress if >1000 chars AND contains redundancy. Skip if concise or dense.
