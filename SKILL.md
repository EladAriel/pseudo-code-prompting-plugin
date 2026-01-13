---
name: pseudo-code-prompting
description: Transform natural language into structured, validated pseudo-code
version: 2.1.0
owner: pseudo-code-prompting
license: MIT
---

# Pseudo-Code Prompting

Transform natural language requirements into structured, validated pseudo-code using the PROMPTCONVERTER methodology.

## When to Activate

- Converting verbose requirements into concise pseudo-code (60-95% compression)
- Validating requirements for completeness, security, and edge cases
- Optimizing pseudo-code for implementation readiness
- Analyzing prompts for ambiguity and complexity
- Structuring feature requests before implementation
- Ensuring requirements are unambiguous and actionable

## Key Features

### 6 Specialized Skills

| Skill | Purpose | Token Usage |
|-------|---------|-------------|
| `prompt-structurer` | Transform natural language to pseudo-code | 300-800 |
| `prompt-analyzer` | Analyze ambiguity, complexity, clarity | 200-500 |
| `prompt-optimizer` | Enhance completeness and implementation readiness | 400-700 |
| `context-compressor` | Compress verbose requirements (60-95% reduction) | 300-600 |
| `requirement-validator` | Validate security, completeness, edge cases | 500-800 |
| `feature-dev-enhancement` | Integrate with feature-dev workflow | 200-400 |

### 5 Intelligent Agents

| Agent | Purpose | Pipeline Position |
|-------|---------|-------------------|
| `prompt-analyzer` | Detect ambiguities and assess clarity | 1 (Entry) |
| `prompt-transformer` | Convert to function-like syntax | 2 (Core) |
| `context-compressor` | Compress verbose specs | 1 (Entry) |
| `prompt-optimizer` | Add missing parameters, enhance security | 3 (Enhancement) |
| `requirement-validator` | Identify gaps and security issues | 3 (Quality) |

### 4 User Commands

| Command | Usage | Example |
|---------|-------|---------|
| `/transform-query` | Transform natural language to pseudo-code | `/transform-query Add user authentication` |
| `/validate-requirements` | Validate pseudo-code completeness | `/validate-requirements create_endpoint(...)` |
| `/optimize-prompt` | Optimize for implementation | `/optimize-prompt fetch_data(url)` |
| `/compress-context` | Compress verbose requirements | `/compress-context [long specification]` |

### 3 Automated Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `user-prompt-submit` | Prompt submission | Detect /feature-dev commands, inject transformation context |
| `post-transform-validation` | After transformation | Auto-validate transformed pseudo-code |
| `context-compression-helper` | Verbose input (>100 words) | Suggest compression for efficiency |

## Quick Start

### Transform Natural Language

```bash
/transform-query Add OAuth authentication with Google and GitHub providers
```

**Output:**
```
Transformed: implement_authentication(
  type="oauth",
  providers=["google", "github"],
  scope="user_auth"
)
```

### Validate Requirements

```bash
/validate-requirements create_endpoint(path="/api/users", method="POST")
```

**Output:**
```
Requirement Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✗ CRITICAL ISSUES
- No authentication specified
- Missing request schema
- No error responses defined

⚠ WARNINGS
- No rate limiting
- Missing CORS configuration
```

### Optimize Pseudo-Code

```bash
/optimize-prompt fetch_data(url)
```

**Output:**
```
Optimized: fetch_data(
  url="string:required:url",
  timeout="5s",
  error_handling="retry",
  retries=3,
  backoff="exponential",
  logging=true
)
```

### Compress Verbose Requirements

```bash
/compress-context We need to create a REST API endpoint that accepts POST requests at /api/register. Users provide email and password. Email must be validated and unique. Password requires 12+ characters with uppercase, lowercase, numbers, and special characters. Hash with bcrypt. Return 201 on success, 409 if email taken, 400 if validation fails. Rate limit to 10 attempts per hour per IP.
```

**Output:**
```
Compressed: create_endpoint(
  path="/api/register",
  method="POST",
  request_schema={
    "email": "email:required:unique",
    "password": "string:required:min(12):requires(upper,lower,number,special)"
  },
  password_hash="bcrypt",
  response_codes={"201": "success", "409": "duplicate_email", "400": "validation_error"},
  rate_limit={"max": 10, "window": "1h", "key": "ip"}
)

Compression: 150 words → 1 line (95% reduction)
```

## Workflows

### Full Transformation (900 tokens)
```
Analyze → Transform → Validate
```
- Analyzes prompt for ambiguities
- Transforms to pseudo-code
- Validates for completeness and security

### Quick Transform (200 tokens)
```
Transform
```
- Fast transformation without deep analysis
- Best for simple, clear requirements

### Optimize and Validate (700 tokens)
```
Optimize → Validate
```
- Enhances existing pseudo-code
- Adds missing security and validation parameters
- Validates implementation readiness

### Compress, Transform, Validate (1000 tokens)
```
Compress → Transform → Validate
```
- Compresses verbose requirements
- Transforms to structured pseudo-code
- Validates completeness

## PROMPTCONVERTER Methodology

### 5 Transformation Rules

1. **Analyze Intent**: Identify core action (verb) and subject (noun)
2. **Create Function Name**: Combine into `snake_case` (e.g., `implement_authentication`)
3. **Extract Parameters**: Convert details to named parameters (e.g., `providers=["google"]`)
4. **Infer Constraints**: Detect implicit requirements (security, performance, validation)
5. **Output Format**: Single-line pseudo-code: `function_name(param="value", ...)`

### Example Transformation

**Input:**
```
Add user authentication with OAuth. Support Google and GitHub. Store tokens securely.
```

**Process:**
- **Intent**: Implement authentication (verb: implement, noun: authentication)
- **Type**: OAuth (extracted from context)
- **Providers**: Google, GitHub (explicit list)
- **Security**: Token storage (inferred constraint)

**Output:**
```
implement_authentication(
  type="oauth",
  providers=["google", "github"],
  token_storage="secure",
  session_management="jwt"
)
```

## Progressive Loading

Skills use 4-tier progressive loading for token efficiency:

| Tier | File | Tokens | When |
|------|------|--------|------|
| 1 | `capabilities.json` | 100-110 | Initial discovery and relevance matching |
| 2 | `SKILL.md` | 300-800 | Skill confirmed relevant, load methodology |
| 3 | `references/*.md` | 90-300 each | Need specific pattern or validation checklist |
| 4 | `templates/*` | 150-400 each | Generating code or structured output |

**Example Flow:**
1. User asks to "validate API endpoint requirements"
2. Load `requirement-validator/capabilities.json` (105 tokens) → Match found
3. Load `requirement-validator/SKILL.md` (650 tokens) → Understand validation process
4. Load `references/validation-checklists.md` (280 tokens) → Get API-specific checklist
5. Execute validation with focused context

**Total**: 1035 tokens (vs. 5000+ tokens loading everything upfront)

## Validation Coverage

### Security Checks
- Authentication requirements (auth, tokens, credentials)
- Authorization rules (roles, permissions)
- Input validation (sanitization, constraints)
- Sensitive data handling (encryption, logging)
- Rate limiting (APIs, exposed endpoints)

### Completeness Checks
- Required parameters present
- Data types specified
- Validation rules defined
- Error handling strategies
- Performance constraints (timeouts, caching)

### Edge Case Detection
- Empty/null input handling
- Boundary conditions
- Concurrent access scenarios
- Failure mode behaviors
- Invalid state transitions

## Integration

### With Feature-Dev Workflow
```bash
/feature-dev Add payment processing with Stripe
```
Hook auto-transforms to pseudo-code before feature development begins.

### With Code Implementation
1. Transform requirements to pseudo-code
2. Validate for completeness
3. Optimize for implementation readiness
4. Use as specification for code generation

### With Documentation
- Transform verbose specs into concise pseudo-code
- 60-95% compression while preserving semantics
- Clear, unambiguous implementation specifications

## Installation

### From Local Plugin
```bash
# Symlink to Claude Code plugins directory
ln -s $(pwd) ~/.claude/plugins/pseudo-code-prompting

# Restart Claude Code
claude-code
```

### Verify Installation
```bash
# List available commands
/help

# Should see:
# - /transform-query
# - /validate-requirements
# - /optimize-prompt
# - /compress-context
```

## Configuration

### Agent Registry
Edit `.claude/agent-registry.json` to customize:
- Agent discovery thresholds
- Workflow sequences
- Quality gates
- Token budgets

### Hook Behavior
Edit `.claude/settings.json` to enable/disable:
- Auto-validation after transformation
- Compression suggestions for verbose input
- Custom lifecycle hooks

## Examples

### API Endpoint
```
Input: Create a REST API endpoint for user registration

Transform: create_endpoint(
  path="/api/register",
  method="POST",
  auth=false,
  request_schema={
    "email": "email:required:unique",
    "password": "string:required:min(12)"
  },
  response_format={"user_id": "string", "created_at": "timestamp"},
  error_responses={"400": "validation_error", "409": "duplicate_email"},
  rate_limit={"max": 10, "window": "1h"}
)
```

### Database Query
```
Input: Query users by status and role with pagination

Transform: query_users(
  filter={"status": "enum[active,inactive,suspended]", "role": "enum[admin,user,guest]"},
  pagination={"default": 20, "max": 100},
  fields=["id", "name", "email", "status", "role"],
  sort={"field": "created_at", "order": "desc"},
  cache={"ttl": "5m"}
)
```

### File Upload
```
Input: Allow users to upload images with virus scanning

Transform: upload_file(
  file="binary:required",
  max_size="10MB",
  allowed_types=["image/jpeg", "image/png", "image/webp"],
  virus_scan=true,
  storage={"provider": "s3", "bucket": "user-uploads"},
  access_control={"auth": true, "signed_urls": true, "url_expiry": "1h"}
)
```

## Documentation

- [Full README](README.md) - Complete documentation and usage guide
- [Contributing Guide](CONTRIBUTING.md) - How to add skills, agents, commands
- [Changelog](CHANGELOG.md) - Version history and updates
- [Agent Registry](.claude/agent-registry.json) - Agent coordination and workflows

## License

MIT License - See [LICENSE](LICENSE) for details

## Version

**Current Version**: 2.1.0
**Last Updated**: 2026-01-13

**Changelog Highlights**:
- Added validation, optimization, and compression capabilities
- 4 new skills, 3 new agents, 3 new commands, 2 new hooks
- Enhanced workflows with quality gates
- Comprehensive validation checklists and common issue patterns
