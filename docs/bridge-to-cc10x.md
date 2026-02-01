# Bridge to cc10x: Integrated TDD Workflow

Learn how to seamlessly integrate pseudo-code-prompting-plugin with cc10x component builder for test-driven development.

## What is the Bridge?

The bridge automatically converts your optimized pseudo-code into a detailed requirement specification that cc10x can use for TDD workflows.

**Goal:** Eliminate ambiguity between requirements and implementation. Build features correctly the first time.

## How It Works

### Step 1: Transform Your Requirement

```
Run transform: Implement JWT authentication with refresh tokens
```

Output:
```
implement_jwt_authentication(
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={"secure": true, "httponly": true, "samesite": "strict"},
  rate_limiting={"max_attempts": 5, "window": "15m"},
  error_handling={...},
  logging=true,
  timeout="5s"
)

🚀 Ready to implement? Auto-invoke cc10x? (Y/n)
```

### Step 2: Answer YES to Bridge

```
> y
```

### Step 3: Automatic Conversion

Your pseudo-code converts to a detailed cc10x specification:

```
Pseudo-code parameters:
  access_token_ttl="15m"
  refresh_token_ttl="7d"
  password_hashing="bcrypt"
  ...

        ↓ CONVERTS TO ↓

CC10X Requirement Spec:
  "Implement JWT authentication with the following constraints:

  SPECIFICATION:
  - Type: JWT tokens with bearer scheme
  - Access token TTL: 15 minutes
  - Refresh token TTL: 7 days
  - Password hashing: bcrypt with 12 salt rounds

  ENDPOINTS:
  - POST /api/auth/login
    - Accept: email, password
    - Return: access_token, refresh_token
    - Rate limit: 5 attempts per 15 minutes

  - POST /api/auth/refresh
    - Accept: refresh_token
    - Return: new access_token

  - POST /api/auth/logout
    - Invalidate tokens

  SECURITY REQUIREMENTS:
  - Password: Bcrypt hashing with 12 rounds
  - Cookies: secure, HttpOnly, SameSite=Strict
  - HTTPS only: true
  - CORS: Restrict to specific origins
  - Rate limiting: 5 login attempts per 15 minutes
  - Token refresh: Maximum 3 consecutive refreshes

  ERROR HANDLING:
  - Invalid credentials (401): "Invalid email or password"
  - Expired access token (403): "Access token expired, use refresh token"
  - Expired refresh token (403): "Session expired, login required"
  - Rate limit exceeded (429): "Too many login attempts, try again in 15 minutes"
  - Invalid token (401): "Invalid or malformed token"

  TESTING STRATEGY (TDD):
  1. RED: Write failing test for invalid credentials
  2. GREEN: Implement validation to pass test
  3. REFACTOR: Optimize error handling

  [Additional tests follow TDD pattern...]"
```

### Step 4: cc10x Takes Over

```
/cc10x:component-builder [detailed_spec]

→ Parses specification
→ Creates test file (RED phase)
→ Runs failing test
→ Implements code (GREEN phase)
→ Runs tests until passing
→ Refactors (REFACTOR phase)
→ Delivers tested, production-ready feature
```

## Bridge Conversion Examples

### Example 1: User Registration Endpoint

**Pseudo-code:**
```
create_user_endpoint(
  path="/api/users/register",
  method="POST",
  schema={
    "email": "email:required:unique",
    "password": "string:min(12):uppercase:numbers:symbols",
    "name": "string:max(100)"
  },
  auth=false,  # Registration is public
  rate_limit="10/hour",
  error_responses={400, 409, 429, 500}
)
```

**Converts to CC10X Spec:**
```
Create POST /api/users/register endpoint with the following:

SPECIFICATION:
- No authentication required (public endpoint)
- Accept: email, password, name

REQUEST VALIDATION:
- Email: Valid email format, must be unique
- Password: Minimum 12 chars, require uppercase, numbers, symbols
- Name: String, maximum 100 chars

RATE LIMITING:
- 10 requests per hour per IP

ERROR RESPONSES:
- 400: Invalid input (validation error details)
- 409: Email already registered
- 429: Rate limit exceeded
- 500: Server error

TESTING:
- Test valid registration
- Test invalid email format
- Test duplicate email
- Test weak password
- Test rate limiting
```

### Example 2: Database Query with Pagination

**Pseudo-code:**
```
query_users(
  filter={"status": "active"},
  pagination={"per_page": 20, "max": 100},
  fields=["id", "email", "name", "created_at"],
  sort={"field": "created_at", "order": "desc"},
  cache={"ttl": "5m"},
  timeout="10s"
)
```

**Converts to CC10X Spec:**
```
Create optimized user query function with:

SPECIFICATION:
- Filter: Only active users (status="active")
- Pagination: Default 20 per page, maximum 100
- Fields: Return only specified fields (id, email, name, created_at)
- Sorting: Most recent first (created_at DESC)
- Caching: 5-minute cache with invalidation on user update
- Timeout: 10 second maximum query time

TESTING:
- Test basic query returns active users only
- Test pagination (page 1, 2, etc.)
- Test field projection (no extra fields returned)
- Test sorting (newest first)
- Test cache hits
- Test cache invalidation on user update
- Test timeout on slow query
```

## Workflow Diagram

```
┌─────────────────────────┐
│  User Requirement       │
│  "Add JWT auth"         │
└────────────┬────────────┘
             │
             ├─ Step 1: Transform
             │ (Context, Compress, Transform, Validate, Optimize)
             ▼
        ┌────────────────────────────┐
        │  Optimized Pseudo-Code     │
        │  implement_jwt_auth(...)   │
        │  ✓ All checks passed       │
        └────────────┬───────────────┘
                     │
                     ├─ Bridge Offer: "Ready to implement? (Y/n)"
                     │
              ┌──────┴──────┐
              │             │
         Answer: N      Answer: Y
             │              │
             ▼              ├─ Step 2: Bridge Conversion
        Return            │ (Parameters → Detailed Spec)
        Pseudo-Code       │
                          ▼
                    ┌─────────────────────┐
                    │  CC10X Spec         │
                    │  - Endpoints        │
                    │  - Security Rules   │
                    │  - Error Handling   │
                    │  - Test Plan        │
                    └────────────┬────────┘
                                 │
                                 ├─ Step 3: cc10x TDD Workflow
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                   RED                      GREEN
                  (Test)                  (Implement)
                    │                        │
            Test fails initially    Implementation passes
                    │                        │
                    └────────────┬───────────┘
                                 │
                              REFACTOR
                            (Optimize)
                                 │
                                 ▼
                        ┌─────────────────────┐
                        │  Production Feature │
                        │  ✓ Tested           │
                        │  ✓ Documented       │
                        │  ✓ Ready to Deploy  │
                        └─────────────────────┘
```

## Benefits of Using the Bridge

### 1. **Clarity**
- Pseudo-code is precise and unambiguous
- cc10x spec leaves no room for interpretation
- Developers know exactly what to build

### 2. **Correctness**
- TDD approach: Tests written first
- Feature built to pass tests
- Edge cases covered by test cases

### 3. **Quality**
- Comprehensive test coverage from the start
- Refactoring ensures clean code
- Security constraints validated

### 4. **Speed**
- No back-and-forth clarification
- Implementation guided by spec
- Reduced rework and debugging

### 5. **Traceability**
- Requirement → Pseudo-code → Tests → Implementation
- Clear audit trail
- Easy to understand design decisions

## When to Use the Bridge

✅ **Use bridge when:**
- Building new features
- Requirements are complex
- Multiple developers involved
- Quality/testing is critical
- You want guaranteed correctness
- TDD approach preferred

❌ **Skip bridge when:**
- Simple one-line fixes
- Bugfixes without complex logic
- Refactoring existing code
- You prefer ad-hoc implementation

## When to NOT Use the Bridge

If you prefer working differently:
- Answer **NO** to "Ready to implement?" prompt
- Get pseudo-code only
- Copy/paste into tickets or documentation
- Implement manually
- Share with team for review

Bridge is optional - choose what works for you.

## Advanced: Manual Bridge Conversion

If you want to understand the conversion process:

1. **Extract pseudo-code parameters:**
   ```python
   function_name="implement_jwt_authentication"
   params = {
     "access_token_ttl": "15m",
     "refresh_token_ttl": "7d",
     "password_hashing": "bcrypt",
     ...
   }
   ```

2. **Map parameters to spec sections:**
   ```
   Tokens TTL → SPECIFICATION section
   Hashing → SECURITY REQUIREMENTS section
   Error codes → ERROR HANDLING section
   Edge cases → TESTING STRATEGY section
   ```

3. **Generate CC10X-compatible spec:**
   ```
   Create structured requirement document
   with SPECIFICATION, ENDPOINTS, SECURITY,
   ERROR HANDLING, and TESTING sections
   ```

4. **Invoke cc10x with spec:**
   ```
   /cc10x:component-builder [spec]
   ```

## Troubleshooting

### Bridge not offered?
- Ensure transform completed successfully (✓ ALL CHECKS PASSED)
- Pseudo-code must be production-ready

### "Auto-invoke not working?"
- Manually copy spec to `/cc10x:component-builder`
- Or answer YES to bridge offer and let system handle it

### "cc10x showing errors?"
- Bridge converts pseudo-code properly
- cc10x might have specific format preferences
- Run validate on pseudo-code first

## Learn More

- [Quick Start Guide](./quick-start.md) - Get started with basic commands
- [Architecture & Design](./ARCHITECTURE.md) - Deep dive into system design
- [cc10x Documentation](../../../cc10x/README.md) - TDD workflow details

## FAQ

**Q: Do I have to use the bridge?**
A: No! The bridge is optional. Answer NO to get pseudo-code only.

**Q: Will cc10x auto-generate tests?**
A: Yes, as part of the TDD workflow (RED phase).

**Q: Can I modify the specification?**
A: Yes! The spec is just text. Modify before passing to cc10x.

**Q: What if my requirement changes?**
A: Run transform again with updated requirement to get new spec.

**Q: How long does TDD workflow take?**
A: Depends on complexity. Simple feature: 5-10 minutes. Complex: 30+ minutes.

---

**Bridge integration transforms pseudo-code requirements into tested, production-ready features. No ambiguity. No misunderstanding. Just correct code.** ✅

