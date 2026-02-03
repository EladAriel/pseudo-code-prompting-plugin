# Bridge to cc10x: Integrated TDD Workflow

Learn how to seamlessly integrate pseudo-code-prompting-plugin with cc10x component builder for test-driven development.

## What's New in v2.1.3

**Stable Specification Reference & Multi-Layer Protection:** Eliminates race conditions through mandatory reference file.

- ✅ **Mandatory reference file** - specification-reference.md is cc10x's entry point (STABLE FIX)
- ✅ **Specification markers** - Special sections with preservation markers in activeContext.md
- ✅ **Context merging** - Intelligent merging prevents cc10x overwrites from losing specification
- ✅ **Recovery mechanism** - Automatic detection and restoration if specification lost
- ✅ **Prevention-first approach** - Sticky specification section survives cc10x writes
- ✅ **Backup hooks** - Multiple safety nets ensure specification never lost
- ✅ **Hybrid protection** - Combines reference entry point, prevention, merging, and recovery

### The Problem (Fixed in v2.1.3)

Before v2.1.3, when cc10x wrote to `activeContext.md`, it would **completely overwrite the file**, losing the pseudo-code specification reference that the pseudo-code plugin had injected. This caused **race conditions** where sometimes the specification was preserved and sometimes not.

**Example of the problem:**
```
Overwrite file .claude\cc10x\activeContext.md
- Line 1-77: Pseudo-code + plugin context (removed)
+ Line 1-40: CC10X's fresh context (added)
Result: Specification reference lost ❌ (unstable)
```

### The Solution (v2.1.3 - Stable)

Four-layer fix implemented:

1. **Layer 0: Mandatory Reference** - specification-reference.md acts as cc10x's entry point (NEW - eliminates race conditions)
2. **Layer 1: Specification Markers** - Pseudo-code context includes special preservation markers
3. **Layer 2: Context Merging** - Smart merging logic preserves specification when contexts update
4. **Layer 3: Recovery Hook** - Automatic detection and restoration if specification lost

See [Context Preservation (v2.1.3)](#context-preservation-v213-new) below for details.

---

## What is the Bridge?

The bridge automatically converts your optimized pseudo-code into a detailed requirement specification that cc10x can use for TDD workflows.

**Goal:** Eliminate ambiguity between requirements and implementation. Build features correctly the first time.

**NEW (v2.1.2):** Specification is automatically persisted in cc10x's memory via PostToolUse hook for guaranteed context availability.

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

---

## Specification Reference (v2.1.3 - NEW - MANDATORY ENTRY POINT)

### The Stable Solution: Mandatory Reference File

Instead of trying to preserve context through overwrites, v2.1.3 introduces a **mandatory specification reference** that cc10x reads FIRST:

**File:** `.claude/cc10x/specification-reference.md`

```markdown
<!-- MANDATORY: Load this specification before proceeding with implementation -->
<!-- CC10X Session Memory: Load .claude/pseudo-code-prompting/specification.md -->

# Specification Reference

**Status:** ACTIVE - Must load specification before creating context
**Source:** .claude/pseudo-code-prompting/specification.md
```

### How It Works

```
1. Transform creates specification.md
2. PostToolUse hook creates specification-reference.md
   ├─ Signals: "LOAD SPECIFICATION BEFORE PROCEEDING"
   └─ References: .claude/pseudo-code-prompting/specification.md
3. User answers YES to bridge
4. cc10x starts and MUST read specification-reference.md
5. cc10x MUST load .claude/pseudo-code-prompting/specification.md
6. cc10x creates activeContext.md with specification included
7. Component-builder uses specification as primary input
8. No race conditions, no unstable behavior ✅
```

### Why This Is More Stable

**Before (Race Condition):**
```
pseudo-code plugin creates activeContext with spec reference
              ↓
         (RACE CONDITION)
              ↓
cc10x creates fresh activeContext (SOMETIMES loses reference)
```

**After (Guaranteed):**
```
pseudo-code plugin creates specification-reference.md
              ↓
         (MANDATORY)
              ↓
cc10x reads specification-reference.md FIRST
              ↓
cc10x loads specification.md (guaranteed to exist)
              ↓
cc10x creates activeContext with specification included (ALWAYS)
```

### Files Created

On each transform:
- `.claude/pseudo-code-prompting/specification.md` - Full specification
- `.claude/cc10x/specification-reference.md` - Mandatory entry point (NEW)

cc10x MUST read specification-reference.md before creating context.

---

## Context Preservation (v2.1.3 - MULTI-LAYER BACKUP)

### The Problem: Context Overwriting

When pseudo-code plugin injected context into `activeContext.md`, cc10x's session-memory system would later load and **completely rewrite** the file with its own structure, losing the pseudo-code reference.

**What happened:**
```
1. Pseudo-code plugin: Injects "## Specification" section into activeContext.md
   Result: activeContext.md has specification reference ✓

2. User answers YES to bridge
3. cc10x loads activeContext.md and OVERWRITES it completely
   Result: activeContext.md loses specification reference ✗

4. cc10x component-builder runs without specification context
   Result: Implementation loses guidance from pseudo-code ✗
```

### The Solution: Three-Layer Protection

#### Layer 1: Specification Markers (Prevention)

The `## Specification` section now includes preservation markers that signal to other tools:
```markdown
## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE. Persisted specification reference. -->
<!-- This section contains critical implementation guidance and should be preserved. -->

**Source:** Pseudo-code specification
**File:** .claude/pseudo-code-prompting/specification.md
...
<!-- END PSEUDO-CODE-CONTEXT -->
```

**Benefits:**
- Clear signal that this section is critical
- Self-contained and easy to identify
- Survived across context writes

#### Layer 2: Context Merging (Smart Merge)

New `context-merger.py` utility intelligently merges contexts:
```python
merged = merge_contexts(
    cc10x_context,      # Fresh context from cc10x
    pseudo_context      # Preserved pseudo-code context
)
# Result: Both contexts preserved in one file
```

**How it works:**
1. Extract pseudo-code context before cc10x writes
2. After cc10x writes fresh context
3. Check if pseudo-context is missing
4. If missing, intelligently merge it back
5. Insert before `## Blockers` section for readability

#### Layer 3: Recovery Hook (Safety Net)

New `post-cc10x-context-write.py` hook runs after cc10x writes:
```
1. Checks if specification reference exists
2. If missing: loads specification.md
3. Rebuilds specification section
4. Injects back into activeContext.md
5. Ensures specification never lost
```

**Triggers only when needed** - if specification is already present, hook does nothing.

### How It Works End-to-End

```
1. User: "Run transform: [requirement]"
2. Transform completes, generates pseudo-code

3. PostToolUse Hook (PHASE 1):
   ├─ Saves specification to .claude/pseudo-code-prompting/specification.md
   ├─ Adds ## Specification section to activeContext.md
   └─ Marks with PSEUDO-CODE-CONTEXT preservation markers

4. User answers YES to bridge

5. cc10x starts and writes to activeContext.md

6. PostToolUse Hook (PHASE 2 - Recovery):
   ├─ Detects if specification reference was lost
   ├─ If lost: loads specification.md
   ├─ Rebuilds ## Specification section
   ├─ Injects back into activeContext.md
   └─ Ensures specification always found

7. cc10x component-builder:
   ├─ Loads activeContext.md
   ├─ Finds ## Specification section
   ├─ Loads full spec from specification.md
   ├─ Runs TDD per specification
   └─ Builds correctly ✅
```

### Files Involved

**New/Modified Files:**
- `hooks/post-tool-use.py` (MODIFIED) - Adds specification markers
- `hooks/context-merger.py` (NEW) - Utility for intelligent merging
- `hooks/post-cc10x-context-write.py` (NEW) - Recovery mechanism
- `hooks/hooks.json` (MODIFIED) - Registers recovery hook

**Specification Files:**
- `.claude/pseudo-code-prompting/specification.md` - Persistent specification
- `.claude/cc10x/activeContext.md` - Context with specification reference

### Benefits of Three-Layer Approach

| Layer | Problem | Solution | Benefit |
|-------|---------|----------|---------|
| **Prevention** | Context not marked as persistent | Specification markers added | Other tools know not to remove |
| **Merging** | Contexts overwrite each other | Smart merge logic | Both contexts preserved |
| **Recovery** | Even with prevention, might get lost | Auto-detection & restoration | Safety net catches edge cases |

### No Configuration Needed

The three-layer protection is **automatic**:
- No extra commands needed
- No manual file management
- Just answer YES to bridge offer
- Specification stays available ✅

---

## Specification Injection (v2.1.2 - PostToolUse Hook)

### What's Automatically Injected?

Your pseudo-code specification is automatically injected into cc10x's memory via **PostToolUse hook** (runs after pseudo-code generation):

**Saved Files:**
1. `.claude/pseudo-code-prompting/specification.md`
   - Your original requirement
   - Generated pseudo-code
   - Timestamp

2. `.claude/cc10x/activeContext.md` (updated with)
   - `## Current Focus`: Pseudo-code summary
   - `## References`: Link to specification.md
   - `## Recent Changes`: Logs specification generation
   - `## Decisions`: Records specification as implementation guide

### Why This Matters

**Before (v2.0.1):**
- Pseudo-code generated
- Bridge to cc10x
- cc10x had no persistent context
- Context lost on session restart or compaction

**After (v2.1.2):**
- Pseudo-code generated
- PostToolUse hook automatically extracts pseudo-code
- Specification persisted to `.claude/pseudo-code-prompting/specification.md`
- Automatic injection into cc10x's `.claude/cc10x/activeContext.md`
- cc10x loads memory (finds specification)
- component-builder uses specification as primary input
- Persists across sessions and context compaction
- **GUARANTEED:** Pseudo-code never lost, always saved by hook

### How It Works (PostToolUse Hook Flow)

```
1. User runs: "Run transform: your requirement"
2. Agent generates pseudo-code
3. Agent completes (outputs pseudo-code)
4. PostToolUse Hook (post-tool-use.py) automatically triggers
   ├─ Detects: "TRANSFORMED PSEUDO-CODE" pattern
   ├─ Checks: workflow-state.json for requirement
   ├─ Saves: .claude/pseudo-code-prompting/specification.md
   └─ Updates: .claude/cc10x/activeContext.md
5. Bridge question shown (spec already saved!)
6. User answers: YES (or answers NO to keep only pseudo-code)

If YES to bridge:
7. cc10x router starts
8. Loads: .claude/cc10x/activeContext.md
9. Reads: "## Current Focus" section
10. Finds: Pseudo-code + specification link
11. Loads full spec: .claude/pseudo-code-prompting/specification.md
12. Passes to component-builder
13. component-builder runs TDD per specification
    - RED: Write tests per specification
    - GREEN: Implement per specification
    - REFACTOR: Maintain specification adherence
14. Feature built exactly as specified ✅
```

**Key Difference (v2.1.2):** PostToolUse hook ensures specification is saved AUTOMATICALLY, whether or not user chooses to bridge to cc10x.

### Manual Specification Access

If you need to see what was saved:

```bash
# View specification
cat .claude/pseudo-code-prompting/specification.md

# View cc10x active context
cat .claude/cc10x/activeContext.md

# Manually delete if not needed
rm -rf .claude/pseudo-code-prompting/
```

### Specification Persistence

The specification is durable and will survive:
- ✅ Session restarts
- ✅ Context compaction
- ✅ Agent handoffs
- ✅ Long-running workflows
- ✅ Multiple invocations

This ensures cc10x always has access to your original pseudo-code specification.

---

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

### "Specification reference missing from activeContext?"
- Recovery hook should have restored it automatically
- Check `.claude/pseudo-code-prompting/specification.md` exists
- If missing: Re-run transform to generate specification
- If present but not in activeContext: Check hook logs with `DEBUG=1`

### "How do I verify specification was saved?"
```bash
# Check specification file exists
ls -la .claude/pseudo-code-prompting/specification.md

# Check activeContext has specification section
cat .claude/cc10x/activeContext.md | grep -A5 "## Specification"

# Verify preservation markers
cat .claude/cc10x/activeContext.md | grep "PSEUDO-CODE-CONTEXT"
```

### "Debug context preservation issues"
```bash
# Enable debug logging
export DEBUG=1

# Run transform again
# Watch for debug messages about:
# - "Added specification section"
# - "Recovered specification reference"
# - Context merger operations
```

## Learn More

- [Quick Start Guide](./quick-start.md) - Get started with basic commands
- [Architecture & Design](./ARCHITECTURE.md) - Deep dive into system design

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

