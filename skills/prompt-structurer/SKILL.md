# Prompt Structurer Skill

Converts natural language requirements into PROMPTCONVERTER-style pseudo-code through intelligent transformation and compression.

## What This Skill Does

Transforms vague requirements like "Add authentication to our API" into precise pseudo-code:

```
implement_authentication(
  methods=["jwt", "oauth"],
  providers=["google", "github"],
  token_ttl="15m",
  refresh_enabled=true,
  rate_limiting="10/1h",
  target_files=["src/auth/handler.ts", "src/middleware/auth.ts"],
  error_handling={...},
  security={...}
)
```

Key features:
- **Compression**: Auto-compresses verbose requirements to 80% while preserving technical details
- **Standardization**: Converts to function-like format with explicit parameters
- **Architecture-aware**: Includes file paths based on detected tech stack
- **Production-ready**: Adds standard parameters (timeouts, logging, error handling)

## When to Use

- User provides a vague or verbose requirement
- Need to convert natural language to actionable specification
- Requirement is >1000 characters and needs compression
- Output needs to be in PROMPTCONVERTER function format

## How It Works

### Phase 1: Compression (if needed)

If requirement is >1000 characters:
1. Identify key technical details (error codes, constraints, specific values)
2. Remove repetitive explanations
3. Combine related concepts
4. Target 80% compression (1000 chars → 800 chars)

Example:
```
BEFORE (1200 chars):
"We need to add user authentication to our API. Users should be able to log in with
their email and password. We also want to support OAuth authentication with Google.
Users should have access tokens that expire after 15 minutes. Refresh tokens should
be used to get new access tokens. We need to implement rate limiting to prevent
brute force attacks. The rate limit should be 10 login attempts per hour per IP..."

AFTER (300 chars):
"User authentication: email/password + OAuth Google. Access tokens (JWT, 15m TTL).
Refresh tokens for renewal. Rate limit: 10 login attempts/hour/IP. Logout after 24h inactivity."
```

### Phase 2: Parameter Extraction

Extract technical parameters from requirement:
- Authentication methods (email/password, OAuth, JWT, etc.)
- External providers (Google, GitHub, Facebook, etc.)
- Rate limits (attempts, timeframes)
- Token TTLs and refresh strategies
- Data sources and storage
- Error scenarios
- Security requirements

### Phase 3: PROMPTCONVERTER Transformation

Convert to function format:

**Name formula**: `[verb]_[subject]`
- Verb: action to perform (implement, validate, process, handle)
- Subject: what's being acted upon (authentication, payment, caching, etc.)

Examples:
- "Add OAuth" → `implement_oauth_authentication`
- "Create payment flow" → `implement_payment_processing`
- "Handle API caching" → `implement_api_caching`
- "Validate user input" → `validate_user_input`

**Parameter structure**:
```python
function_name(
  # Core parameters (explicit, typed)
  param1="specific_value",
  param2=["list", "of", "values"],

  # Nested objects (when complexity requires)
  complex_param={
    "nested_key": "value",
    "another": 123
  },

  # Standard production parameters (always included)
  target_files=["path/to/file.ts"],
  error_handling={...},
  security={...},
  timeout="5s",
  logging=true
)
```

### Phase 4: Architecture-Aware File Paths

Include target_files based on detected tech stack.

**Node.js/Next.js:**
```
target_files=[
  "src/app/api/[resource]/route.ts",
  "src/lib/services/[service].ts",
  "src/middleware/[middleware].ts"
]
```

**Python/Django:**
```
target_files=[
  "app/views.py",
  "app/models.py",
  "app/middleware.py",
  "app/forms.py"
]
```

**Go:**
```
target_files=[
  "internal/handlers/[handler].go",
  "internal/services/[service].go",
  "pkg/middleware/[middleware].go"
]
```

**Rust:**
```
target_files=[
  "src/handlers/mod.rs",
  "src/services/mod.rs",
  "src/middleware/mod.rs"
]
```

## Standard Parameters

Every pseudo-code includes these production-ready parameters:

### error_handling
```python
error_handling={
  "invalid_input": 400,
  "unauthorized": 401,
  "forbidden": 403,
  "not_found": 404,
  "conflict": 409,
  "rate_limited": 429,
  "server_error": 500,
  "service_unavailable": 503
}
```

### security
```python
security={
  "validate_input": true,
  "validate_authorization": true,
  "encrypt_sensitive_data": true,
  "use_secure_cookies": true,
  "enforce_https": true,
  "rate_limiting_enabled": true,
  "use_pkce": true,  # if OAuth
  "secure_cookie_settings": {
    "http_only": true,
    "same_site": "strict",
    "secure": true
  }
}
```

### timeout
```python
timeout="5s"  # Prevents hanging indefinitely
```

### retry
```python
retry={
  "max_attempts": 3,
  "backoff": "exponential",
  "jitter": true
}
```

### cache (if applicable)
```python
cache={
  "ttl": "5m",
  "key_strategy": "resource_id",
  "invalidation": "on_update"
}
```

### logging
```python
logging=true  # All operations logged
```

## Examples

### Example 1: OAuth Authentication

INPUT:
```
Add OAuth authentication with Google and GitHub. Support JWT tokens with 15-minute
access token TTL and 7-day refresh token TTL. Rate limit login to 10 attempts per hour.
Auto-logout users after 24 hours of inactivity.
```

OUTPUT:
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
  target_files=["src/auth/oauth.ts", "src/auth/strategies/", "src/middlewares/auth.ts"],
  error_handling={
    "invalid_provider": 400,
    "invalid_code": 400,
    "token_expired": 401,
    "invalid_refresh_token": 401,
    "insufficient_scope": 403,
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
    "log_token_operations": true,
    "log_errors": true
  },
  timeout="5s",
  retry={"max_attempts": 3, "backoff": "exponential"},
  cache={"ttl": "5m", "key": "oauth_state"}
)
```

### Example 2: API Rate Limiting

INPUT:
```
Implement rate limiting for our public API. Should limit to 1000 requests per hour
per user. Return 429 status when exceeded. Use sliding window algorithm.
```

OUTPUT:
```
implement_api_rate_limiting(
  algorithm="sliding_window",
  request_limit={
    "per_user": 1000,
    "time_window": "1h"
  },
  enforcement="per_user_id",
  target_files=["src/middleware/rateLimiter.ts", "src/services/rateLimitStore.ts"],
  error_handling={
    "rate_limit_exceeded": 429,
    "invalid_api_key": 401,
    "malformed_request": 400
  },
  security={
    "validate_api_key": true,
    "validate_user_identity": true
  },
  storage={
    "type": "redis",
    "ttl": "1h"
  },
  logging={
    "log_limit_exceeded": true,
    "log_suspicious_patterns": true
  },
  timeout="100ms",
  cache={"ttl": "30s"}
)
```

## Tips for Usage

1. **Be specific**: Replace vague terms with concrete values
   - ❌ "make it secure" → ✓ "validate_input: true, use_https: true, encrypt_passwords"
   - ❌ "handle errors" → ✓ "error_handling: {invalid_input: 400, server_error: 500}"

2. **Include constraints**: Numbers, timeouts, limits
   - "Rate limit to 10 attempts per hour"
   - "Token TTL 15 minutes"
   - "Timeout after 5 seconds"

3. **Name operations clearly**: Verb + subject
   - ✓ implement_oauth, validate_request, process_payment
   - ❌ do_auth, handle_thing, manage_stuff

4. **Specify error scenarios**: Not just "handle errors"
   - Which HTTP status codes?
   - What recovery strategy?
   - Should it retry?

5. **Think about data flow**: Where does it come from? Where does it go?
   - Input source (user, database, API)
   - Storage location
   - Output format

## See Also

- `requirement-validator/` - Validation patterns
- `/pseudo-code:transform` command - User-facing transformation
- `/pseudo-code:validate` command - Validation across 6 dimensions
