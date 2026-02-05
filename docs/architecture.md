# Plugin Architecture Guide

This guide explains how the pseudo-code-prompting plugin works internally, how components connect, and how to understand or extend it.

## High-Level Architecture

The plugin has three main pipelines:

```
User Input
    ↓
┌───────────────────────────────────────┐
│  TRANSFORM PIPELINE                   │
│  (Requirement → Pseudo-Code)          │
│  - Tech stack detection               │
│  - Auto-compression                   │
│  - PROMPTCONVERTER formatting         │
│  - Completeness validation            │
│  - Standard parameter injection       │
│  - cc10x bridge (optional save)        │
└───────────────────────────────────────┘
    ↓
Pseudo-Code Specification
    ↓
┌───────────────────────────────────────┐
│  VALIDATION PIPELINE                  │
│  (Pseudo-Code → 6-Dimension Report)   │
│  - Security checks                    │
│  - Completeness checks                │
│  - Error handling review              │
│  - Data handling audit                │
│  - Performance constraints            │
│  - Edge case analysis                 │
└───────────────────────────────────────┘
    ↓
Validation Report (with severity)
```

## Component Architecture

### Entry Points (Commands)

**Three commands** invoke the plugin:

1. **`/pseudo-code:transform`** (commands/transform.md)
   - Takes: User requirement text
   - Invokes: `requirement-structurer` agent
   - Returns: Production-ready pseudo-code
   - Entry point for specification creation

2. **`/pseudo-code:validate`** (commands/validate.md)
   - Takes: Pseudo-code to review
   - Invokes: `requirement-validator` agent
   - Returns: Structured validation report
   - Entry point for quality assurance

3. **`/pseudo-code:explain_my_project`** (commands/explain.md)
   - Takes: Project description
   - Invokes: `project-explainer` agent
   - Returns: Engaging technical documentation
   - Entry point for project explanations

### Processing Agents

**Three agents** handle the heavy lifting:

1. **`requirement-structurer`** (agents/requirement-structurer.md)
   - 6-step transformation pipeline
   - Uses: `prompt-structurer` skill
   - Flow:
     - Step 1: Detect tech stack (Node.js, Python, Go, Rust, Java)
     - Step 2: Auto-compress verbose requirements (70-80% efficient)
     - Step 3: Convert to PROMPTCONVERTER-style pseudo-code
     - Step 4: Validate completeness
     - Step 5: Add standard production parameters
     - Step 6: Optionally save to cc10x bridge
   - Output: Function-style pseudo-code with all parameters

2. **`requirement-validator`** (agents/requirement-validator.md)
   - 6-dimension validation checker
   - Uses: `requirement-validator` skill
   - Validates across:
     - Security (auth, authorization, data protection)
     - Completeness (all parameters specified, no vague terms)
     - Error Handling (status codes, retry, fallback)
     - Data Handling (sources, validation, storage)
     - Performance (timeouts, caching, scalability)
     - Edge Cases (concurrency, failures, cleanup)
   - Output: Structured report with CRITICAL/HIGH/MEDIUM severity

3. **`project-explainer`** (agents/project-explainer.md)
   - Creates engaging technical documentation
   - Uses: `project-explanation` skill
   - Generates:
     - Technical architecture explanations
     - Codebase structure diagrams
     - Technology decisions and trade-offs
     - Lessons learned and pitfalls
   - Output: Essay-style EXPLAIN_*.md documentation

### Knowledge Skills

**Three skills** contain the domain knowledge:

1. **`prompt-structurer`** (skills/prompt-structurer/)
   - Transformation methodology
   - Files:
     - SKILL.md: Core transformation logic
     - references/compression-rules.md: Auto-compression guidelines
     - templates/oauth-example.md: Complete OAuth reference
   - Knows:
     - How to compress requirements without losing details
     - PROMPTCONVERTER naming rules (verb + subject)
     - Tech stack-specific file paths
     - Standard production parameters

2. **`requirement-validator`** (skills/requirement-validator/)
   - Validation patterns and checklists
   - Files:
     - SKILL.md: Validation methodology
     - references/validation-checklist.md: Validation reference
   - Knows:
     - 6 validation dimensions in depth
     - Severity guidelines (when to mark CRITICAL vs HIGH vs MEDIUM)
     - Tech stack-specific validation patterns
     - Non-applicable check handling

3. **`project-explanation`** (skills/project-explanation/)
   - Technical writing patterns
   - Files:
     - SKILL.md: Writing templates and best practices
   - Knows:
     - How to explain architecture with analogies
     - Codebase structure explanation techniques
     - Technology trade-off analysis
     - Essay-style technical documentation

## Data Flow

### Transform Pipeline (Detailed)

```
User Requirement Text
    ↓
[Step 1: Tech Stack Detection]
- Analyzes project structure
- Detects: Node.js, Python, Go, Rust, Java
- Output: Stack identifier + target file paths
    ↓
[Step 2: Auto-Compression]
- Removes redundancy from requirement
- Preserves critical details (error codes, constraints)
- Applies: Summarization, tokenization, parameter extraction
- Output: Compressed requirement (70-80% of original)
    ↓
[Step 3: PROMPTCONVERTER Format]
- Converts to function notation: `verb_subject(params)` where `verb` and `subject` are placeholders
- Extracts parameters from compressed requirement
- Names function clearly (e.g., implement_oauth_authentication)
- Output: Function stub with parameters identified
    ↓
[Step 4: Completeness Validation]
- Checks: All parameters have explicit values
- Finds: Vague terms like "secure", "fast", "handle"
- Output: Complete parameter set or list of missing items
    ↓
[Step 5: Standard Parameter Injection]
- Adds: timeout, error_handling, security, logging, retry
- Fills in: Architecture-aware file paths
- Merges: With parameters extracted in Step 3
- Output: Production-ready pseudo-code
    ↓
[Step 6: cc10x Bridge (Optional)]
- If user says "Yes to cc10x":
  - Saves to: .claude/cc10x/specification-reference.md
  - Format: YAML frontmatter + pseudo-code
  - When cc10x invoked: Uses this as single source of truth
- Output: Confirmation + saved file path
```

### Validation Pipeline (Detailed)

```
Pseudo-Code Specification
    ↓
[Security Dimension]
- Checks: Authentication method specified?
- Checks: Authorization rules clear?
- Checks: Data protection specified?
- Checks: Secrets handling defined?
- Severity: CRITICAL if missing auth, HIGH if incomplete
    ↓
[Completeness Dimension]
- Checks: All parameters have values (not vague)?
- Checks: No "handle gracefully" or "secure"?
- Checks: Specific error codes listed?
- Severity: CRITICAL if vague terms remain
    ↓
[Error Handling Dimension]
- Checks: Error codes specified (401, 403, 429, etc.)?
- Checks: Retry strategy defined?
- Checks: Fallback behavior clear?
- Checks: Timeout specified?
- Severity: CRITICAL if missing timeout
    ↓
[Data Handling Dimension]
- Checks: Input validation specified?
- Checks: Data sources identified?
- Checks: Storage method clear?
- Checks: Data retention defined?
- Severity: CRITICAL if no input validation
    ↓
[Performance Dimension]
- Checks: Timeout value realistic?
- Checks: Caching strategy (if applicable)?
- Checks: Rate limiting defined?
- Checks: Scalability considerations?
- Severity: HIGH if timeout too generous
    ↓
[Edge Cases Dimension]
- Checks: Concurrency handling?
- Checks: Cleanup on failure?
- Checks: Boundary conditions (empty input, max size)?
- Checks: Resource exhaustion protection?
- Severity: MEDIUM if edge cases unclear
    ↓
Structured Report
- ✓ PASSED CHECKS
- ✗ CRITICAL ISSUES (must fix before implementation)
- ⚠ HIGH WARNINGS (should fix before implementation)
- ℹ MEDIUM SUGGESTIONS (nice to have)
- OVERALL STATUS: READY / NEEDS REVIEW / BLOCKED
```

## Tech Stack Awareness

The plugin generates different file paths and patterns per tech stack:

### Node.js/Express/Next.js
```
- Route handlers: src/app/api/, src/routes/
- Middleware: src/middleware/
- Services: src/services/
- Models: src/models/
```

### Python/Django/FastAPI
```
- Views: app/views.py
- Models: app/models.py
- Serializers: app/serializers.py
- Middleware: app/middleware.py
```

### Go
```
- Handlers: internal/handlers/
- Middleware: pkg/middleware/
- Services: internal/services/
- Models: pkg/models/
```

### Rust
```
- Handlers: src/handlers/
- Middleware: src/middleware/
- Services: src/services/
- Models: src/models/
```

### Java/Maven
```
- Controllers: src/main/java/com/*/controller/
- Services: src/main/java/com/*/service/
- Models: src/main/java/com/*/model/
```

## Standard Parameters

Every pseudo-code includes these production-ready parameters:

```javascript
implement_[feature](
  // Functional parameters (from requirement)
  param1="value",
  param2=["list"],

  // File paths (tech stack specific)
  target_files=["src/path/to/file.ts", ...],

  // Error handling (status codes, retry)
  error_handling={
    "error_type": 400,
    "not_found": 404,
    "auth_error": 401,
    "rate_limit": 429
  },

  // Security requirements
  security={
    "use_pkce": true,
    "secure_cookie": true,
    "validate_input": true
  },

  // Timeout (prevents hanging)
  timeout="5s",

  // Retry strategy (for transient failures)
  retry={"max_attempts": 3, "backoff": "exponential"},

  // Logging (for debugging)
  logging=true
)
```

## Pseudo-Code Format

Uses PROMPTCONVERTER function notation for clarity:

```
function_name(
  parameter="explicit_value",  // Always explicit, never "generic"
  list_param=["item1", "item2"],
  object_param={
    "key": "value",
    "nested": {"key": "value"}
  }
)
```

**Rules:**
- Function name: verb + subject (e.g., `implement_oauth_authentication`)
- Every parameter explicit (no vague values like "secure", "fast")
- Complex structures use nested objects/arrays
- Error codes always specific (401, 403, 429)
- Timeouts always specified (prevents hanging)

## Error Handling & Severity Levels

### CRITICAL (Must Fix)
- Security vulnerability (no auth, plaintext passwords)
- Hanging risk (no timeout)
- Data loss risk (no validation)
- Performance blocking (unrealistic timeout)

### HIGH (Should Fix)
- Incomplete error handling
- Missing rate limiting
- Vague parameter values
- Incomplete security specification

### MEDIUM (Nice to Have)
- Edge case handling
- Logging completeness
- Performance optimization opportunities

## cc10x Bridge Integration

When user saves pseudo-code to cc10x:

```
.claude/cc10x/specification-reference.md
────────────────────────────────────────
---
title: Feature Specification
requirement: [original requirement]
tech_stack: [detected stack]
---

implement_<feature_name>(parameters)
```

When cc10x is invoked later:
1. cc10x loads this specification
2. Uses it as single source of truth
3. Guides RED-GREEN-REFACTOR testing
4. Ensures implementation matches spec

## Component Interactions

```
User Command
    ↓
transform.md / validate.md / explain.md (Commands)
    ↓
    ├→ requirement-structurer.md (Agent) → prompt-structurer (Skill)
    │
    ├→ requirement-validator.md (Agent) → requirement-validator (Skill)
    │
    └→ project-explainer.md (Agent) → project-explanation (Skill)
    ↓
Pseudo-Code / Report / Documentation
    ↓
[Optional] → .claude/cc10x/specification-reference.md (Bridge)
```

## File Organization

```
Plugin Root
├── commands/                    # Entry points
│   ├── transform.md            # Users invoke this
│   ├── validate.md             # Users invoke this
│   └── explain.md              # Users invoke this
│
├── agents/                      # Processing logic
│   ├── requirement-structurer.md
│   ├── requirement-validator.md
│   └── project-explainer.md
│
├── skills/                      # Domain knowledge
│   ├── prompt-structurer/       # Transformation rules
│   ├── requirement-validator/   # Validation patterns
│   └── project-explanation/     # Writing templates
│
├── docs/                        # User documentation
│   ├── architecture.md          # This file
│   ├── cc10x-bridge.md         # TDD integration
│   └── examples.md             # Real-world workflows
│
├── tests/                       # Test specifications
│   ├── test_transform_pipeline.md
│   └── test_validation.md
│
└── plugin.json                  # Manifest
```

## Key Design Decisions

1. **Three Explicit Commands** (Not Auto-Detection)
   - Clear user intent
   - Simpler mental model
   - No accidental transformations

2. **6-Step Transform Pipeline**
   - Tech stack detection (adapts to your project)
   - Auto-compression (70-80% efficient)
   - Completeness validation (no vague terms)
   - Standard parameters (production ready)
   - Optional cc10x bridge (TDD integration)

3. **6-Dimension Validation**
   - Comprehensive (covers all critical areas)
   - Severity-based (prioritize fixes)
   - Actionable (specific recommendations)

4. **Production-Ready Defaults**
   - Every spec includes timeout, error handling, logging
   - No vague values permitted
   - Architecture-aware file paths

5. **cc10x Integration** (Optional)
   - Not forced (users choose)
   - Simple storage (YAML + pseudo-code)
   - Single source of truth for TDD

## Extending the Plugin

### Add a New Command

1. Create `commands/my-command.md`
2. Define when-to-use, arguments, examples
3. Reference an agent (new or existing)
4. Add to `plugin.json` commands list

### Add a New Validation Dimension

1. Update `agents/requirement-validator.md` (add dimension)
2. Update `skills/requirement-validator/SKILL.md` (add checks)
3. Update `skills/requirement-validator/references/validation-checklist.md`

### Add Tech Stack Support

1. Update `agents/requirement-structurer.md` (detection rules)
2. Update `skills/prompt-structurer/SKILL.md` (file paths)
3. Add example templates if needed

## Performance & Limitations

- **Transform time**: 15-30 seconds (depends on requirement complexity)
- **Validation time**: 5-10 seconds (depends on pseudo-code size)
- **Compression ratio**: 70-80% (removes redundancy, keeps details)
- **Tech stacks**: 5 supported (Node.js, Python, Go, Rust, Java)
- **Max requirement size**: ~5000 characters (internal limit)

## Troubleshooting

### Transform not generating pseudo-code
- Ensure requirement includes specific constraints
- Add error codes, timeouts, rate limits
- Mention tech stack explicitly if not detected

### Validation showing too many CRITICALs
- Add missing error handling
- Specify timeout (required to prevent hanging)
- Add input validation for data operations

### cc10x bridge not saving
- Check .claude/cc10x/ directory exists
- Verify plugin has write permissions
- Check that you selected "Yes" when prompted

## Related Documentation

- **[Quick Start](../QUICK_START.md)** - 5-minute getting started
- **[Examples](./examples.md)** - Real-world workflows
- **[cc10x Bridge](./cc10x-bridge.md)** - TDD integration guide

---

**Last Updated**: 2026-02-05
**Plugin Version**: 3.0.0
