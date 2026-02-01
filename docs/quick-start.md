# Quick Start Guide

Get started with pseudo-code-prompting-plugin in 5 minutes.

## Installation

```bash
# From Marketplace
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin
/plugin install pseudo-code-prompting

# From Github
## 1. Clone repo
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin
cd pseudo-code-prompting-plugin

## 2. Install to Claude Code
cp -r . ~/.claude/plugins/pseudo-code-prompting
```

## Your First Transform

### Step 1: Write Your Requirement

Think of a feature you want to implement:

> "Add user authentication with email/password and email verification"

### Step 2: Use the Transform Command

```
Run transform: Add user authentication with email/password and email verification
```

### Step 3: Review the Output

You'll get:

```
TRANSFORMED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

implement_authentication(
  method="email_password",
  email_verification=true,
  password_hashing="bcrypt",
  verification_link_ttl="24h",
  endpoints={
    "register": "/api/auth/register",
    "verify": "/api/auth/verify",
    "login": "/api/auth/login"
  },
  error_handling={
    "invalid_email": 400,
    "password_weak": 400,
    "email_unverified": 403,
    "credentials_invalid": 401
  },
  logging=true,
  timeout="5s"
)

OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Context detected: Node.js + Express
✓ Validation: ALL CHECKS PASSED
✓ Parameters added: 3 (error_handling, logging, timeout)

🚀 READY TO IMPLEMENT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Auto-invoke cc10x component-builder with this specification? (Y/n)
```

### Step 4: Choose Your Path

**Option A: Use cc10x Bridge**
```
Answer: y (or yes)

→ Pseudo-code converts to detailed requirement spec
→ /cc10x:component-builder auto-invoked
→ TDD workflow starts: RED → GREEN → REFACTOR
→ Feature built with clear requirements
```

**Option B: Copy Pseudo-Code**
```
Answer: n (or no)

→ Pseudo-code returned
→ Copy to your tickets, documentation, or iterate
→ Implement manually when ready
```

## Your First Validation

### Step 1: Have Some Pseudo-Code

```
create_user_endpoint(path="/api/users", method="POST")
```

### Step 2: Run Validation

```
Run validate: create_user_endpoint(path="/api/users", method="POST")
```

### Step 3: Review the Report

You'll get:

```
REQUIREMENT VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ PASSED CHECKS
- Path and method specified

✗ CRITICAL ISSUES
- Missing authentication
  → Required Action: Add auth=true, define roles/permissions
- No error response codes
  → Required Action: Specify error_responses={400, 401, 403, 500}

⚠ WARNINGS
- No rate limiting
  → Suggestion: Add rate_limit="100/hour"

OVERALL STATUS: BLOCKED
Address critical issues before implementation.
```

### Step 4: Fix Issues

Add the missing critical items:

```
create_user_endpoint(
  path="/api/users",
  method="POST",
  auth=true,
  roles=["admin"],
  schema={
    "email": "email:required:unique",
    "name": "string:max(100)"
  },
  error_responses={400, 401, 403, 500},
  rate_limit="100/hour"
)
```

### Step 5: Validate Again

```
Run validate: create_user_endpoint(path="/api/users", method="POST", auth=true, ...)
```

Result: Status changes to **READY** ✓

## Common Patterns

### API Endpoint

```
Run transform: Create POST endpoint for user registration with email validation and password requirements
```

### Database Query

```
Run transform: Query active users with pagination, field projection, and 5-minute cache
```

### Cache Layer

```
Run transform: Add Redis caching for user profiles with TTL and cache invalidation on updates
```

### Error Handling

```
Run transform: Add comprehensive error handling for API calls with retry logic and circuit breaker
```

### Authentication

```
Run transform: Implement OAuth authentication with multiple providers (Google, GitHub) and token refresh
```

## Tips for Best Results

### ✨ Be Specific

Instead of:
```
Run transform: Add authentication
```

Use:
```
Run transform: Add JWT authentication with 15-minute access token TTL and 7-day refresh token TTL
```

### ✨ Include Constraints

Instead of:
```
Run transform: Create user endpoint
```

Use:
```
Run transform: Create user endpoint with rate limiting (100/hour) and CORS support for specific origins
```

### ✨ Mention Security

Instead of:
```
Run transform: Add login
```

Use:
```
Run transform: Add login with bcrypt password hashing, secure HttpOnly cookies, and CSRF protection
```

## Troubleshooting

### "Run transform: not recognized"

Make sure you use the exact format:
```
Run transform: your requirement
```

Not:
```
Run transform your requirement
/transform: your requirement
```

### "Validation is too strict"

Validation defaults to high standards (production-ready). Warnings are informational - you can proceed even with warnings. Only **CRITICAL** issues must be fixed before implementation.

### "Pseudo-code doesn't match my tech stack"

The plugin auto-detects tech stack from your project:
- `package.json` → Node.js/Next.js
- `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust

If detection fails, specify in requirement:
```
Run transform: For Next.js app - Create API route for user profiles
```

## What's Next?

1. **Learn more:** Read [Bridge to cc10x Guide](./bridge-to-cc10x.md)
2. **Understand architecture:** Read [Architecture & Design](./ARCHITECTURE.md)
3. **Transform & validate:** Use commands to structure your own requirements
4. **Integrate with cc10x:** Use bridge for TDD workflows

## One-Minute Summary

| Task | Command |
|------|---------|
| Transform requirement to pseudo-code | `Run transform: your requirement` |
| Validate pseudo-code | `Run validate: your_pseudo_code` |
| Use bridge to cc10x | Answer `y` when asked "Ready to implement?" |

That's it! You're ready to use pseudo-code-prompting-plugin-v2. 🚀

