---
name: Transform Requirements to Pseudo-Code
description: Convert fuzzy requirements into crystal-clear PROMPTCONVERTER-style pseudo-code with repo-aware file paths and production-ready specifications
arguments:
  - name: query
    description: Optional label or description for your requirement (plugin will prompt for full requirement)
    required: false
when-to-use: |
  - When you have vague requirements that need crystal-clear specifications
  - When requirements miss error handling, security, or edge cases
  - Before implementation—to get everyone aligned on what to build
  - When you need architecture-aware pseudo-code for your tech stack
examples:
  - "Transform requirements for user authentication"
  - "Transform API endpoint requirements"
---

# Transform Requirements to Pseudo-Code

This command runs a 6-step pipeline:

1. **Detect Tech Stack** - Identifies your project type (Node.js, Python, Go, Rust, Java)
2. **Compress (if needed)** - Auto-compresses verbose requirements to 80% while preserving technical details
3. **Transform to Pseudo-Code** - Converts natural language to PROMPTCONVERTER-style function notation
4. **Validate Completeness** - Checks for missing security, error handling, timeouts, logging
5. **Optimize** - Adds standard parameters (timeouts, retry logic, error mappings, logging)
6. **Bridge to cc10x** - Saves pseudo-code to specification and offers TDD integration

## Usage

Simply say:
> **Transform to pseudocode:** Add OAuth with Google and GitHub providers. Users should be able to log in via OAuth, have tokens automatically refresh, be logged out after 24 hours, and get rate limited to 10 login attempts per hour.

## What You Get

✓ Production-ready pseudo-code with all parameters specified
✓ Architecture-aware file paths for your tech stack
✓ Complete error handling defined
✓ Security requirements called out
✓ Timeouts, retry logic, caching all included
✓ Option to auto-inject into cc10x for TDD workflow

## Output Example

```
implement_oauth_authentication(
  providers=["google", "github"],
  token_type="jwt",
  access_token_ttl="15m",
  refresh_token_enabled=true,
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
    "insufficient_scope": 403
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
    "validate_provider_response": true
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

Then you'll be offered:
```
Would you like to save this to cc10x for specification-driven TDD?
→ Yes: Saves to .claude/cc10x/specification-reference.md and injects into cc10x context
→ No: Returns pseudo-code for manual iteration
```

## Tips

- **Be specific about constraints**: Include timeouts, rate limits, TTLs, not just "make it fast"
- **Name error scenarios**: Don't say "handle errors"—specify actual error codes
- **Think about edge cases**: Concurrent requests, failures, recovery
- **Include security upfront**: Authentication, authorization, validation, secure storage
- **Specify file paths**: Where should code live in your project?

## See Also

- **Validate my pseudocode:** - Validate existing pseudo-code across 6 dimensions
- **Explain my project:** - Generate project explanations
- Documentation: `docs/examples.md` for real-world examples
- Integration: `docs/cc10x-bridge.md` for cc10x setup
