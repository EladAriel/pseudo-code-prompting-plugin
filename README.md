# Pseudo-Code-Prompting Plugin v2

**Simplified pseudo-code transformation engine: 70% less complexity, 50% faster, built-in cc10x bridge.**

Transform natural language requirements into production-ready pseudo-code with automatic context detection, validation, optimization, and seamless integration with cc10x TDD workflow.

## Installation

```bash
# From Marketplace
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin
/plugin install pseudo-code-prompting-plugin-v2

# From Github
## 1. Clone repo
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin
cd pseudo-code-prompting-plugin

## 2. Install to Claude Code
cp -r . ~/.claude/plugins/pseudo-code-prompting
```

## Quick Start

```bash
# Transform a requirement into pseudo-code
Run transform: Implement JWT authentication with refresh tokens

# Validate existing pseudo-code
Run validate: implement_jwt_authentication(type="jwt", ttl="15m", ...)
```

## What's New in v2

| Feature | v1 | v2 | Improvement |
|---------|----|----|-------------|
| Commands | 7 | 2 | 71% reduction |
| Agents | 6 | 2 | 67% reduction |
| Skills | 10+ | 3 | 70% reduction |
| Hooks | 5+ | 1 | 80%+ reduction |
| Execution Time | 30-90s | 15-45s | 50% faster |
| Token Usage | 2000-4000 | 600-1200 | 70% savings |
| Code Complexity | Very High | Low | 75% reduction |

**Key improvement:** Everything merged into 2 core commands with ruthless simplification.

## Features

### ✨ Transform Command
Transform natural language requirements into production-ready pseudo-code:

```
Run transform: your requirement here
```

**6-step pipeline:**
1. 🔍 Context Detection - Detects tech stack (Node.js, Python, Next.js, etc.)
2. 🗜️ Auto-Compression - Compresses verbose requirements (>1000 chars)
3. 🔄 Transform - Converts to PROMPTCONVERTER pseudo-code format
4. ✅ Validation - Checks for missing security/completeness
5. ⚙️ Optimization - Adds standard production parameters
6. 🚀 Bridge Offer - Auto-invoke cc10x for TDD workflow

**Output:** Production-ready pseudo-code + cc10x bridge option

### ✨ Validate Command
Check pseudo-code for completeness and production readiness:

```
Run validate: your_pseudo_code_here
```

**Validation dimensions:**
- 🔒 Security (auth, validation, data protection)
- ✅ Completeness (all required parameters)
- ⚠️ Error Handling (error scenarios, fallbacks)
- 📊 Data Handling (data flow, validation)
- ⚡ Performance (scalability, timeouts)
- 🎯 Edge Cases (boundary conditions, failures)

**Output:** Structured validation report with severity levels (CRITICAL, HIGH, MEDIUM, LOW)


## Examples

### Example 1: Simple Transform
```
Input:  Run transform: Add user authentication with OAuth
Output: implement_authentication(
          type="oauth",
          providers=["google", "github"],
          error_handling={"invalid_token": 401, "expired": 403},
          logging=true
        )

        🚀 Ready to implement? Auto-invoke cc10x? (Y/n)
```

### Example 2: Complex Requirement
```
Input:  Run transform: Implement JWT authentication with refresh tokens, secure
        cookies, bcrypt hashing, 15-minute access token TTL, 7-day refresh token
        TTL, rate limiting on login (5 per 15 min), and error handling

Output: implement_jwt_authentication(
          access_token_ttl="15m",
          refresh_token_ttl="7d",
          password_hashing="bcrypt",
          cookies={"secure": true, "httponly": true, "samesite": "strict"},
          rate_limiting={"max_attempts": 5, "window": "15m"},
          error_handling={401, 403, 429},
          logging=true,
          timeout="5s"
        )

        OPTIMIZATION SUMMARY
        ✓ Context detected: Node.js + Express
        ✓ Validation: ALL CHECKS PASSED
        ✓ Parameters added: 3 (error_handling, logging, timeout)

        🚀 Ready to implement? Auto-invoke cc10x? (Y/n)
```

### Example 3: Validation
```
Input:  Run validate: create_endpoint(path="/api/users", method="POST")

Output: REQUIREMENT VALIDATION REPORT

        ✗ CRITICAL ISSUES
        - Missing authentication
        - No request body schema
        - No error response codes

        ⚠ WARNINGS
        - No rate limiting

        📋 EDGE CASES
        - Duplicate user creation (409)
        - Invalid email format (400)

        OVERALL STATUS: BLOCKED
        Address critical issues before implementation.
```

## Architecture

```
User Input
   ↓
Hook (Auto-detect "Run {command}:")
   ↓
Command Router
   ├─ Run transform: → requirement-structurer agent (6-step pipeline)
   └─ Run validate:  → requirement-validator agent (validation checks)
        ↓
   Bridge Offer (cc10x integration)
   ├─ YES → /cc10x:component-builder (TDD workflow)
   └─ NO  → Return pseudo-code only
```

## When to Use

### Transform Command ✓
- Starting a new feature
- Clarifying vague requirements
- Breaking down complex tasks
- Preparing for cc10x TDD workflow
- Creating specification documents

### Validate Command ✓
- Checking existing pseudo-code
- Getting pre-implementation review
- Security validation
- Completeness verification
- Team review/approval

## Configuration

Edit `.claude-plugin/plugin.json` to customize:

```json
{
  "name": "pseudo-code-prompting-plugin",
  "version": "2.0.0",
  "description": "...",
  "keywords": ["pseudo-code", "validation", ...]
}
```

## CLI Integration

The plugin auto-detects command patterns via hooks:

```bash
# Transform
Run transform: build user authentication system

# Validate
Run validate: implement_jwt_authentication(type="jwt", ...)
```

No need to prefix with `/pseudo-code:` - simpler invocation!

## Performance Benchmarks

| Operation | Time | Token Usage |
|-----------|------|-------------|
| Simple transform | 15-25s | 600-800 |
| Complex transform | 25-40s | 900-1200 |
| Validation | 10-15s | 300-500 |
| Bridge to cc10x | <2s | minimal |
| **Total (worst case)** | **~45s** | **~1500** |

Compared to v1: **50% faster, 70% fewer tokens**

## Integration with cc10x

After transformation, pseudo-code is automatically injected into cc10x's activeContext:

```
Your pseudo-code transforms to detailed requirement spec
         ↓
AUTOMATIC INJECTION into .claude/cc10x/activeContext.md
  ├─ Specification saved to: .claude/pseudo-code-prompting/specification.md
  ├─ Current Focus updated with pseudo-code structure
  ├─ References section linked to specification
         ↓
Bridge Question: Ready to implement with cc10x?
         ↓
If YES:
  ├─ cc10x router loads memory (finds pseudo-code reference)
  ├─ component-builder receives specification as primary input
  ├─ TDD Workflow: RED → GREEN → REFACTOR
  └─ Feature built with specification as acceptance criteria
         ↓
Feature built with clear, unambiguous requirements
```

**Benefit:** Specification-driven development. Pseudo-code becomes the source of truth for implementation, persists across sessions, and guides all TDD cycles.

### What Gets Injected

When you choose YES to the bridge question:
1. **Specification File** → `.claude/pseudo-code-prompting/specification.md`
   - Full pseudo-code output
   - Timestamp and original requirement

2. **activeContext.md Updates**:
   - `## Current Focus`: Pseudo-code summary + implementation guidance
   - `## References`: Link to specification file
   - `## Recent Changes`: Logs specification generation
   - `## Decisions`: Records to use pseudo-code as guide

3. **cc10x Workflow**:
   - component-builder reads activeContext on startup
   - Uses specification as primary acceptance criteria
   - TDD cycles validate against specification
   - Memory persists across sessions

## Advanced Usage

### Architecture-Aware Pseudo-Code
The transform command automatically detects your tech stack:

```
Input:  Run transform: Add user profile endpoint

Output: create_user_endpoint(
          path="/api/users/:id",
          method="GET",
          target_files=["src/app/api/users/[id]/route.ts"],  ← Next.js specific!
          cache={"ttl": "5m"},
          ...
        )
```

### Custom Validation
Add domain-specific validation by editing agent requirements.

### Session Memory (Optional)
To preserve transformation patterns and user preferences across sessions, use the session-memory skill at the start of your workflow.

Invoke it with `skill: "pseudo-code-prompting:session-memory"` or access it through `/skill session-memory`.

This loads learned patterns, user preferences, and transformation history from `.claude/pseudo-code-prompting/`, enabling consistent and context-aware transformations. Session memory is optional and can be disabled by not invoking it; when disabled, each session starts fresh without historical context.

### Ask for project explanation (Optional)

Request a comprehensive explanation of your project structure, architecture, and design decisions by creating an `EXPLAIN.md` file.
This is useful for understanding how the codebase is organized, learning from design patterns, and documenting lessons learned.

Simply ask **"Can you explain this project?"** and Claude will generate detailed documentation covering technical architecture, codebase structure, technology decisions, and best practices discovered during development.

## Troubleshooting

### "Command not detected"
Ensure you use exact format: `Run transform: ...` or `Run validate: ...`

### "Transform taking too long"
Complex requirements may take longer. Consider breaking into smaller pieces.

### "Validation too strict"
Adjust severity levels in agent configuration, or ignore low-priority warnings.

## Migration from v1

v2 is a complete rewrite emphasizing simplicity:

**Removed:**
- 5 of 7 commands (consolidated into 2)
- 4 of 6 agents (merged logic)
- 6+ of 10 skills (kept only essential)
- 4 of 5 hooks (kept only command detection)

**Added:**
- Built-in cc10x bridge
- Auto-detection in hook (simpler invocation)
- Context-aware optimization
- Performance improvements (50% faster)

**Compatibility:** Not backward compatible with v1 skill invocations, but achieves same end results more efficiently.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for detailed version history.

## Documentation

- [Quick Start Guide](./docs/quick-start.md) - Get started in 2 minutes
- [Bridge to cc10x Guide](./docs/bridge-to-cc10x.md) - Integrate with TDD workflow
- [Architecture & Design](./docs/ARCHITECTURE.md) - Deep dive into how it works

## Support

- Issues: [GitHub Issues](https://github.com/EladAriel/pseudo-code-prompting-plugin/issues)
- Discussions: [GitHub Discussions](https://github.com/EladAriel/pseudo-code-prompting-plugin/discussions)

## License

MIT - See [LICENSE](./LICENSE) for details

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**Built with ❤️ for cleaner, simpler, more effective pseudo-code workflows.**

Made v2 possible through ruthless simplification + user feedback integration.
