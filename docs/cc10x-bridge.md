# cc10x Integration Bridge

How the pseudo-code-prompting plugin connects with cc10x for specification-driven TDD development.

## Overview

After transforming requirements to pseudo-code, the plugin offers to save your specification to cc10x. This creates a single source of truth that cc10x uses to guide implementation via TDD workflow.

```
Transform Requirement
         ↓
    Generate Pseudo-Code
         ↓
    Offer cc10x Bridge
         ↓
    User: Save to cc10x? → YES
         ↓
    Specification Saved → `.claude/cc10x/specification-reference.md`
    activeContext Updated → `.claude/cc10x/activeContext.md`
         ↓
    User: Invoke cc10x
         ↓
    cc10x Loads Specification
         ↓
    RED: Write tests based on spec
    GREEN: Implement to pass tests
    REFACTOR: Improve while spec-compliant
         ↓
    Implementation Complete & Spec-Verified
```

## Bridge Architecture

### Storage Location

Pseudo-code is saved to:
```
.claude/cc10x/specification-reference.md
```

This file is the single source of truth. cc10x loads it as context when you invoke it.

### Context Injection

The plugin updates `.claude/cc10x/activeContext.md` to reference the specification:

```markdown
# cc10x Active Context

<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->

## Specification Reference

See `specification-reference.md` for the current requirement pseudo-code.

This pseudo-code is the single source of truth for what to build. All implementation
must satisfy the specification.
```

### Marker Comments

The specification includes a marker comment:
```markdown
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->
```

This helps preserve the context even if cc10x's session memory modifies the file.

## How It Works

### When You Say "YES" to cc10x Bridge

1. **Generate Specification File**
   ```
   .claude/cc10x/specification-reference.md
   ```
   Contains:
   - Complete pseudo-code
   - Explanation of each parameter
   - Implementation hints
   - Validation criteria

2. **Update Active Context**
   ```
   .claude/cc10x/activeContext.md
   ```
   Gets reference to specification and marker comment

3. **Prepare cc10x Session**
   Display message:
   ```
   ✓ Specification saved to .claude/cc10x/specification-reference.md

   Next steps:
   1. Invoke cc10x: /cc10x:router
   2. cc10x will load your specification
   3. Follow TDD workflow:
      - RED: Write tests based on pseudo-code
      - GREEN: Implement to pass tests
      - REFACTOR: Improve while staying spec-compliant
   ```

## Specification File Format

`specification-reference.md` contains:

```markdown
# Pseudo-Code Specification

<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->

**Generated**: [date/time]
**Original Requirement**: [user's original requirement]

## Specification

[Complete pseudo-code]

## Implementation Guide

### What to Build

[Summary of what the pseudo-code specifies]

### Key Parameters

[Explanation of each parameter and why it matters]

### Error Scenarios

[All error codes and how to handle them]

### Testing Strategy

[How to verify implementation against spec]

### Files to Create/Modify

[List of target files from pseudo-code]

## Validation Criteria

[What makes implementation "correct" relative to spec]

- [ ] All parameters implemented as specified
- [ ] All error codes handled with correct HTTP status
- [ ] All security requirements enforced
- [ ] All logging enabled
- [ ] Timeout specified at 5s
- [ ] Retry logic with exponential backoff
```

## cc10x Workflow with Specification

When you invoke cc10x with a specification present:

### 1. Context Loading
```
cc10x reads .claude/cc10x/activeContext.md
Finds reference to specification-reference.md
Loads pseudo-code specification
```

### 2. RED Phase (Write Tests)
```
cc10x uses pseudo-code to guide test writing:

"Based on specification, write tests that verify:
- implement_oauth_authentication() accepts providers=["google", "github"]
- Returns JWT access token with 15m TTL
- Returns 401 if token expired
- Returns 429 if rate limit exceeded
- All operations logged"
```

### 3. GREEN Phase (Implement)
```
cc10x guides implementation:

"Implement implement_oauth_authentication() to pass tests.
Remember:
- target_files: ["src/auth/oauth.ts", ...]
- error_handling: {invalid_provider: 400, token_expired: 401, ...}
- security: {use_pkce: true, secure_cookie: true, ...}
- timeout: 5s, retry with backoff"
```

### 4. REFACTOR Phase (Improve)
```
cc10x suggests refactoring while keeping tests passing:

"Tests pass. Now refactor for:
- Code clarity (functions under 25 lines)
- Remove duplication
- Improve error messages
- Add performance comments"
```

## Key Benefits

1. **Specification-Driven Development**
   - Specification is source of truth
   - Implementation validates against spec
   - No ambiguity about requirements

2. **Persistent Context**
   - Specification survives session changes
   - cc10x can reference it across sessions
   - Team alignment on what to build

3. **Quality Assurance**
   - Pseudo-code validated before implementation
   - cc10x checks implementation against spec
   - Tests verify compliance

4. **Knowledge Transfer**
   - New team members see specification first
   - Know exactly what to build before coding
   - Specification includes error scenarios and constraints

## Troubleshooting Bridge

### Specification Not Found

If cc10x can't find the specification:

1. Check that `.claude/cc10x/` directory exists
2. Verify `specification-reference.md` was created
3. Verify `activeContext.md` has the reference marker
4. Try running transform again to regenerate specification

### Context Lost

If specification reference disappears from `activeContext.md`:

1. The marker comment `<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->` may have been removed
2. Check `specification-reference.md` still exists
3. Manually restore reference in `activeContext.md`:
   ```
   <!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->
   See specification-reference.md for current requirements.
   ```

### Multiple Specifications

If you transform multiple requirements:

1. Each `transform` updates `specification-reference.md`
2. Previous specification is overwritten
3. To keep multiple: manually rename old specifications or create branches

**Best practice**: One specification at a time. Implement it with cc10x, then transform next requirement.

## Example Workflow

### Step 1: Transform Requirement

```
User: /pseudo-code:transform

Enter requirement:
Add OAuth with Google and GitHub. JWT 15m TTL. Rate limit 10/hour.
```

Plugin outputs:
```
✓ Generated pseudo-code...

Save to cc10x for specification-driven TDD?
→ Yes: Save and prepare for cc10x
→ No: Just show pseudo-code
```

### Step 2: User Says YES

```
✓ Specification saved to .claude/cc10x/specification-reference.md
✓ Context updated

Next: Invoke cc10x
  /cc10x:router

cc10x will load your specification and guide TDD implementation.
```

### Step 3: User Invokes cc10x

```
User: /cc10x:router

cc10x loads specification, finds:
- implement_oauth_authentication(...)
- Target files: src/auth/oauth.ts, ...
- Error handling: 401, 429, etc.
- Security: PKCE, secure cookies

cc10x: "Ready for RED phase. Write tests that verify:"
  1. OAuth login returns 200 + JWT token
  2. Expired token returns 401
  3. Rate limit exceeded returns 429
  [... more test scenarios ...]
```

### Step 4: User Implements

```
User follows RED-GREEN-REFACTOR:

RED:   Write tests against spec ✓
GREEN: Implement to pass tests ✓
REFACTOR: Improve code ✓

All tests pass, implementation matches pseudo-code spec.
```

## Configuration

Optional configuration in `.claude/pseudo-code-prompting.local.md`:

```yaml
---
cc10x_bridge_auto_save: false
cc10x_bridge_auto_open: false
---
```

- `cc10x_bridge_auto_save: true` - Save without prompting
- `cc10x_bridge_auto_open: true` - Auto-invoke cc10x after saving

Default (false for both) requires user confirmation and manual cc10x invocation.

## Best Practices

1. **One Specification at a Time**
   - Complete implementation before transforming next
   - Keeps context focused and clear

2. **Validate Before Saving**
   - Use `/pseudo-code:validate` before saving to cc10x
   - Fix CRITICAL issues first
   - Agreed specification = better implementation

3. **Reference Specification in Comments**
   - When implementing, reference pseudo-code parameter
   - Include error code mappings in comments
   - Link back to specification

4. **Keep Specification Stable**
   - Don't edit `.claude/cc10x/specification-reference.md` manually
   - If changes needed, run transform again
   - New transform overwrites specification

5. **Team Communication**
   - Share specification before implementation
   - Discuss in code review: "Does implementation match spec?"
   - Use specification for requirements traceability

## Integration with Version Control

Recommended `.gitignore`:

```
.claude/
.claude-plugin/
```

Or if tracking context:

```
# Track specification but not other context
!.claude/cc10x/specification-reference.md
```

This keeps:
- Specification versioned and trackable
- Session memory private per developer
- Context compaction doesn't affect team
