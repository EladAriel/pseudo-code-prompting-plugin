# Quick Start (5 Minutes)

Get started with pseudo-code-prompting in 5 minutes.

## What This Plugin Does

Transforms fuzzy requirements like:
> "Add authentication to our API"

Into crystal-clear specifications like:
```
implement_authentication(
  method="jwt",
  token_ttl="15m",
  error_handling={401, 403, 429},
  timeout="5s",
  logging=true,
  ...
)
```

Then validates the specification across **6 critical dimensions**: Security, Completeness, Error Handling, Data Handling, Performance, Edge Cases.

## Installation

1. Copy `.claude-plugin/` to your project root
2. Or reference it from Claude Code settings

## Your First Transform

### Step 1: Say the Magic Words

Simply write:
> **Transform to pseudocode:** Add OAuth authentication with Google and GitHub. Support JWT tokens with 15-minute TTL. Rate limit login to 10 attempts per hour.

### Step 2: Get Pseudo-Code

You get back production-ready pseudo-code:

```
implement_oauth_authentication(
  providers=["google", "github"],
  token_type="jwt",
  access_token_ttl="15m",
  rate_limiting={"login_attempts": "10/1h"},
  target_files=["src/auth/oauth.ts", "src/middleware/auth.ts"],
  error_handling={...},
  security={...},
  timeout="5s",
  retry={"max_attempts": 3},
  logging=true
)
```

### Step 3: Save to cc10x (Optional)

You'll be asked if you want to save this pseudo-code to cc10x for specification-driven TDD.

**If YES**: Pseudo-code becomes your specification. When you use cc10x, it uses this as the source of truth.

**If NO**: Use pseudo-code for manual iteration.

## Your First Validation

### Step 1: Say the Magic Words

Simply write:
> **Validate my pseudocode:** implement_payment_processing( provider="stripe", amount=user_input["amount"], ...)

### Step 2: Get Validation Report

You get back a structured report:

```
✓ PASSED CHECKS
  ✓ Provider specified

✗ CRITICAL ISSUES (Must Fix)
  - No input validation
  - No error handling
  - No timeout (will hang)

⚠ HIGH WARNINGS
  - No rate limiting

OVERALL STATUS: BLOCKED
Recommendation: Add input validation, error handling, timeout before implementation
```

## Key Concepts

### 1. Pseudo-Code Format

Uses PROMPTCONVERTER function notation:
```
[verb]_[subject](
  parameter1="specific_value",
  parameter2=["list"],
  nested={
    "object": "structure"
  }
)
```

**Rule**: Every parameter explicit. No vague values like "secure", "fast", "handle".

### 2. Standard Parameters

Every pseudo-code includes:
- `timeout="5s"` - Prevents hanging
- `error_handling={...}` - Defines failure modes
- `security={...}` - Security requirements
- `logging=true` - Enables debugging
- `retry={...}` - Handles transient failures
- `target_files=[...]` - What to build

### 3. Tech Stack Awareness

Plugin detects your project type and generates appropriate file paths:

**Node.js**: `src/app/api/route.ts`, `src/middleware/`
**Python**: `app/views.py`, `app/models.py`
**Go**: `internal/handlers/`, `pkg/middleware/`

## Common Workflows

### Workflow 1: Quick Transform

```
1. "Transform to pseudocode: [your requirement]"
2. Get pseudo-code
3. Iterate if needed
```

**Use when**: You want to see how a requirement converts to specification.

### Workflow 2: Validation-First

```
1. "Transform to pseudocode: [your requirement]"
2. Review pseudo-code
3. "Validate my pseudocode: [the spec]"
4. Fix CRITICAL issues
5. Say "Yes" to save to cc10x
```

**Use when**: You want to catch issues before implementing.

### Workflow 3: Specification-Driven Development

```
1. "Transform to pseudocode: [your requirement]"
2. Fix any validation issues
3. Say "Yes" to save to cc10x
4. Optionally invoke cc10x
5. cc10x guides RED-GREEN-REFACTOR using specification
```

**Use when**: You want specification-driven TDD with cc10x.

## Tips

### ✓ Do This

```
✓ Be specific with constraints
  "Rate limit: 10/hour" not "Implement rate limiting"

✓ Include error scenarios
  "Return 401 if token expired" not "Handle token errors"

✓ Name operations clearly
  "implement_oauth" not "add_auth" or "do_authentication"

✓ Specify all data flows
  "Store in database" not "Save securely"

✓ Think about edge cases
  "Retry with exponential backoff" not "Handle failures"
```

### ✗ Avoid This

```
✗ Vague requirements
  "Add authentication" → unclear details

✗ Vague parameters
  error_handling="handle_gracefully" → what errors?

✗ Generic names
  "implement_api" → which API? What operations?

✗ Missing constraints
  No timeout, rate limit, or error codes specified

✗ Boundary conditions
  What happens on empty input? Max size?
```

## Examples

### Example 1: Email Authentication

**Requirement:**
```
Email/password authentication. Passwords stored with bcrypt.
JWT tokens valid 24 hours. Rate limit: 5 login attempts per 10 minutes.
```

**Pseudo-Code (generated):**
```
implement_email_authentication(
  method="password",
  password_hashing="bcrypt",
  token_type="jwt",
  token_ttl="24h",
  rate_limiting={"login_attempts": "5/10m"},
  error_handling={
    "invalid_credentials": 401,
    "rate_limited": 429,
    "server_error": 500
  },
  security={"validate_password_strength": true},
  timeout="5s",
  logging=true
)
```

### Example 2: Data Export

**Requirement:**
```
Export user data to CSV. Limit to 100,000 rows per export.
Require authentication. Store exports for 7 days. Log all exports.
```

**Pseudo-Code (generated):**
```
implement_data_export(
  format="csv",
  max_rows=100000,
  authentication_required=true,
  storage={
    "location": "s3",
    "retention_days": 7
  },
  target_files=["src/routes/export.ts", "src/services/export.ts"],
  error_handling={
    "unauthorized": 401,
    "too_many_rows": 400,
    "export_failed": 500
  },
  timeout="30s",
  logging={"log_all_exports": true}
)
```

## Next Steps

1. **Quick Test**: "Transform to pseudocode: [simple requirement]"
2. **Review Output**: Check pseudo-code makes sense
3. **Validate It**: "Validate my pseudocode: [the spec]" to find issues
4. **Save to cc10x**: Test the cc10x bridge (optional)
5. **Iterate**: Refine requirement and transform again

## Common Questions

**Q: What if my tech stack isn't detected?**
A: Mention it in your requirement. Plugin will adapt: "For a Django app, add user authentication..."

**Q: Can I edit the pseudo-code?**
A: Yes! Transform generates starting point. Iterate, validate, and refine until ready.

**Q: How is this different from just writing requirements?**
A: Pseudo-code is precise. Every parameter explicit. No room for "add security" or "handle errors gracefully"—you specify exactly which errors, which security checks.

**Q: What does cc10x bridge do?**
A: Saves your specification to `.claude/cc10x/specification-reference.md`. When you invoke cc10x, it uses this specification to guide TDD implementation (RED-GREEN-REFACTOR).

**Q: How long does transform take?**
A: Usually 15-30 seconds depending on requirement complexity.

**Q: Can I use this for existing code?**
A: Yes! Transform your requirement first to get specification, then validate to ensure you covered all dimensions.

## Get Help

- **README.md** - Full documentation
- **examples.md** - Real-world examples
- **cc10x-bridge.md** - How to use cc10x integration
- **skills/** - Technical deep-dives

---

**Ready to transform your first requirement?**

Simply say:
> **Transform to pseudocode:** [your requirement]

Go! 🚀
