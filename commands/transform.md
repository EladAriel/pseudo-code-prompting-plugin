---
name: "transform"
description: "Transform requirements to production-ready pseudo-code"
---

# Transform: Requirement to Production-Ready Pseudo-Code

Transform natural language requirements into production-ready pseudo-code with automatic context detection, compression, validation, optimization, and cc10x bridge integration.

## Usage

```
Run transform: your requirement here
```

## Quick Examples

### Simple Feature
```
Run transform: Add user authentication with OAuth
```

### Complex Requirement
```
Run transform: Implement JWT authentication with refresh tokens, secure cookies, bcrypt password hashing, 15-minute access token TTL, 7-day refresh token TTL, rate limiting on login attempts (5 per 15 minutes), and comprehensive error handling for invalid credentials, expired tokens, and rate limit scenarios.
```

### Database Feature
```
Run transform: Create optimized user query with pagination, field projection, and caching
```

## What This Command Does

Your requirement goes through a **6-step pipeline**:

### 1️⃣ Context Detection
- Detects your project's tech stack (Node.js, Python, Go, Rust, Next.js, etc.)
- Reads project structure to understand conventions
- Makes pseudo-code architecture-aware from the start

### 2️⃣ Auto-Compression
- If your requirement is verbose (>1000 chars), intelligently compresses it
- Preserves all technical requirements
- Removes redundant explanations
- Result: Focused, concise specification

### 3️⃣ Transform to Pseudo-Code
- Converts requirement into function-like pseudo-code format
- Extracts intent, parameters, and constraints
- Follows PROMPTCONVERTER methodology
- Result: Machine-readable, architecture-aware specification

### 4️⃣ Validate Completeness
- Checks for missing security requirements (auth, validation, error handling)
- Verifies all parameters are specified
- Identifies edge cases
- Result: Validation report or issues to fix

### 5️⃣ Optimize with Parameters
- Adds standard parameters (timeout, retry, cache, error_handling, logging)
- Applies tech stack conventions
- Includes error response codes
- Result: Production-ready pseudo-code

### 6️⃣ Bridge to cc10x
- Offers to auto-invoke cc10x component-builder
- Converts pseudo-code to detailed requirement specification
- Enables TDD workflow: RED → GREEN → REFACTOR
- Result: Feature built with clear, unambiguous requirements

## Memory Integration (Optional)

Session memory enhances transformation quality by learning from previous sessions. This is **optional but valuable**.

### How Memory Helps

**Session 1:** You transform "Add authentication endpoint"
- Memory learns: Your naming style (snake_case), security preferences, patterns used

**Session 2:** You transform "Add user listing endpoint"
- Memory automatically:
  - Applies your naming style learned from Session 1
  - Suggests rate limiting pattern discovered in Session 1
  - Knows your preferred parameter structure
- Result: 5-10% better quality, 10-15% fewer tokens

### Enabling Memory Integration

Memory is **automatic if available**, but you can control it:

- **Automatic (default):** If `.claude/pseudo-code-prompting/` directory exists, memory loads and applies
- **Explicit:** Include project context in your requirement: "For Next.js app: Add authentication"
- **Disable if needed:** Include "ignore memory" in requirement if you want fresh transformation

### What Gets Remembered

Memory learns and recalls:

| What | Where | How It Helps |
|------|-------|--------------|
| Naming conventions (snake_case, camelCase, etc.) | activeContext.md | Consistent naming across transformations |
| Tech stack patterns | patterns.md | Stack-specific parameter suggestions |
| Security patterns | patterns.md | Auto-includes security requirements |
| Transformation history | progress.md | Learns from what worked before |
| Common mistakes | progress.md | Avoids repeated issues |
| User preferences | activeContext.md | Personalized transformation style |

### Memory Transparency

View your memory files anytime:
```
.claude/pseudo-code-prompting/
├── activeContext.md   # Current session state + user preferences
├── patterns.md        # Learned patterns from all transformations
└── progress.md        # Quality metrics and history
```

These files are permission-free to read and plain text for easy viewing.

### Resetting Memory

If you want to start fresh or switch projects:
- Delete `.claude/pseudo-code-prompting/` directory
- Memory auto-resets if you switch projects (detected automatically)
- On project switch, only activeContext resets; patterns and progress carry over to new project (useful for learning domain patterns)

## Example: JWT Authentication

### Input
```
Run transform: Implement JWT authentication with refresh tokens, secure cookies, and bcrypt password hashing. Include 15-minute access token TTL, 7-day refresh token TTL, rate limiting on login attempts (5 per 15 minutes), and comprehensive error handling.
```

### Output

```
TRANSFORMED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

implement_jwt_authentication(
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={
    "secure": true,
    "httponly": true,
    "samesite": "strict"
  },
  rate_limiting={
    "max_attempts": 5,
    "window": "15m"
  },
  error_handling={
    "invalid_credentials": 401,
    "expired_token": 403,
    "rate_limit_exceeded": 429
  },
  logging=true,
  timeout="5s"
)

OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Context detected: Node.js + Express project
✓ Validation: ALL CHECKS PASSED
  - Security: JWT + bcrypt + secure cookies ✓
  - Rate limiting: Configured ✓
  - Error handling: Comprehensive ✓
✓ Parameters added: error_handling, logging, timeout
✓ Production ready: Yes

🚀 READY TO IMPLEMENT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your pseudo-code is production-ready.

Auto-invoke cc10x component-builder with this specification? (Y/n)

If YES:
  - Pseudo-code converts to detailed requirement spec
  - /cc10x:component-builder starts with clear, unambiguous requirements
  - Runs TDD workflow: RED → GREEN → REFACTOR
  - Feature built correctly first time

If NO:
  - Pseudo-code returned as-is
  - Copy/paste into tickets, documentation, or iterate manually
  - You control when to implement
```

## Common Use Cases

### 1. New API Endpoint
```
Run transform: Create POST /api/users endpoint with email/password validation, user creation, and error handling for duplicate users
```

### 2. Database Query
```
Run transform: Optimize query to fetch active users with pagination, field projection, sorting by creation date, and caching
```

### 3. Feature Flag System
```
Run transform: Implement feature flags with A/B testing, rollout percentage, and user targeting
```

### 4. Error Monitoring
```
Run transform: Add error tracking with Sentry, include stack traces, user context, and rate limiting to prevent log spam
```

### 5. Cache Layer
```
Run transform: Add Redis caching layer for user profiles with 5-minute TTL, cache invalidation on update, and fallback to database
```

## When to Use Transform

✅ **Use this command when:**
- Starting a new feature from scratch
- Clarifying vague requirements
- Breaking down complex tasks
- Documenting specifications
- Preparing for implementation
- Need bridge to cc10x for TDD workflow

❌ **Don't use if:**
- You already have pseudo-code (use `Run validate:` instead)
- Your requirement is a single line (just implement directly)
- You're debugging existing code (use regular cc10x workflows)

## Tips for Best Results

### ✨ Be Specific
- **Good:** "Add JWT authentication with bcrypt hashing and 15-minute token expiry"
- **Bad:** "Add authentication"

### ✨ Include Constraints
- **Good:** "Create endpoint with rate limiting (100/hour) and CORS for specific origins"
- **Bad:** "Create endpoint"

### ✨ Mention Security Requirements
- **Good:** "Add secure session management with HttpOnly cookies and CSRF protection"
- **Bad:** "Add sessions"

### ✨ Specify Tech Stack (Optional)
- **Good:** "For Next.js app: Add API route for user profile with caching"
- **Bad:** "Add user profile endpoint"

## Output Options

### Option 1: Use Auto-Invoke Bridge
After transformation, choose **YES** to auto-invoke cc10x:
```
Your pseudo-code converts to detailed requirement spec
→ /cc10x:component-builder auto-invoked
→ TDD workflow starts immediately
→ Feature built with clear requirements
```

### Option 2: Copy Pseudo-Code Only
Choose **NO** to get pseudo-code only:
```
Pseudo-code returned
→ Copy to tickets, documentation, or iterate
→ Implement manually later
→ Share with team for review
```

## Validation Report (If Issues Found)

If validation finds critical issues:

```
⚠ VALIDATION ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✗ CRITICAL: No authentication specified
  → Required Action: Add auth=true, specify roles/permissions

✗ CRITICAL: No error handling defined
  → Required Action: Specify error responses (400, 401, 403, 500)

⚠ WARNING: No rate limiting for login endpoint
  → Suggestion: Add rate_limit="5/15m" to prevent brute force

OVERALL STATUS: NEEDS REVIEW

Pseudo-code can proceed to implementation, but address critical issues first.
```

## Performance

- **Simple transform:** 15-25 seconds
- **Complex transform:** 25-40 seconds
- **With compression:** +5-10 seconds (if needed)
- **Bridge to cc10x:** <2 seconds

## Next Steps

### After Successful Transform

1. **Review pseudo-code** - Ensure it matches your intent
2. **Check validation** - Address any critical issues
3. **Choose bridge option:**
   - **YES:** Auto-invoke cc10x for immediate TDD workflow
   - **NO:** Copy pseudo-code for manual iteration

4. **If using cc10x bridge:**
   - Feature built via RED → GREEN → REFACTOR
   - Tests written first (TDD approach)
   - Implementation guided by spec
   - No ambiguity or misunderstanding

5. **If not using bridge:**
   - Iterate on pseudo-code manually
   - Share with team for review
   - Update tickets/documentation
   - Implement when ready

## Learn More

- [Quick Start Guide](../docs/quick-start.md)
- [Bridge to cc10x Guide](../docs/bridge-to-cc10x.md)
- [Architecture & Design](../docs/ARCHITECTURE.md)
- [Validate Command](./validate.md)
