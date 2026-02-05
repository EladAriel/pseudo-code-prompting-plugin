# Pseudo-Code Prompting Plugin

Transform vague requirements into crystal-clear pseudo-code specifications and validate them for production readiness.

## What It Does

**Transform** fuzzy requirements like:
> "Add OAuth with Google and GitHub"

Into **production-ready specifications** like:
```
implement_oauth_authentication(
  providers=["google", "github"],
  token_type="jwt",
  access_token_ttl="15m",
  error_handling={401, 403, 429},
  security={use_pkce: true, secure_cookie: true},
  timeout="5s",
  logging=true
)
```

**Validate** across **6 critical dimensions**:
- Security (auth, authorization, data protection)
- Completeness (all parameters specified, no vague terms)
- Error Handling (status codes, retry, fallback)
- Data Handling (sources, validation, storage)
- Performance (timeouts, caching, scalability)
- Edge Cases (concurrency, failures, cleanup)

## Key Features

✓ **3 Core Commands**
- `/pseudo-code:transform` - Requirements → Production-Ready Pseudo-Code
- `/pseudo-code:validate` - Validate across 6 critical dimensions
- `/pseudo-code:explain_my_project` - Generate engaging project documentation

✓ **6-Step Transformation Pipeline**
- Detects your tech stack (Node.js, Python, Go, Rust, Java)
- Auto-compresses verbose requirements (70-80% efficient)
- Converts to PROMPTCONVERTER-style pseudo-code
- Validates completeness
- Adds standard production parameters
- Offers cc10x bridge for TDD

✓ **Production-Ready Specifications**
- Every spec includes timeouts, error handling, logging, security
- Architecture-aware file paths per tech stack
- Explicit parameters (no vague values)
- Comprehensive error code mappings

✓ **6-Dimension Validation**
- Checks security, completeness, error handling, data handling, performance, edge cases
- Severity levels: CRITICAL (must fix) / HIGH (should fix) / MEDIUM (nice-to-have)
- Structured reports with recommendations

✓ **Engaging Project Explanations (EXPLAIN Files)**
- Technical architecture with analogies
- Codebase structure and component connections
- Technology decisions and trade-offs
- Lessons learned and pitfalls to avoid
- Written as engaging essays, not boring documentation
- Perfect for team onboarding and knowledge preservation

✓ **Tech Stack Detection**
- Node.js/Express/Next.js → src/app/api/, src/routes/
- Python/Django/FastAPI → app/views.py, app/models.py
- Go → internal/handlers/, pkg/middleware/
- Rust → src/handlers/, src/services/
- Java/Maven → src/main/java/

✓ **cc10x Integration**
- Specification-driven TDD workflow
- Saves to `.claude/cc10x/specification-reference.md`
- cc10x loads specification as single source of truth

## Usage

### Transform Requirements to Pseudo-Code

```
/pseudo-code:transform

Enter your requirement:
Add OAuth with Google and GitHub. JWT tokens 15m TTL. Rate limit 10/hour.

Get back:
implement_oauth_authentication(...)  ✓
```

### Validate Pseudo-Code

```
/pseudo-code:validate

Paste pseudo-code:
implement_oauth_authentication(...)

Get report:
✓ PASSED CHECKS
✗ CRITICAL ISSUES
⚠ WARNINGS
OVERALL STATUS: READY
```

### Explain Your Project

```
/pseudo-code:explain_my_project

Describe your project:
Payment processing system with Stripe integration, webhooks, and refund handling.

Get back:
EXPLAIN_payment_system.md ✓

With:
- Technical architecture explanation (with analogies)
- Codebase structure and how parts connect
- Technology decisions and why they were made
- Lessons learned and pitfalls to avoid
- Engaging essay-style documentation (not boring tech docs)
```

### Specification-Driven TDD with cc10x

```
1. /pseudo-code:transform
2. Validate if needed
3. Say "Yes" to save to cc10x
4. /cc10x:router
5. Follow RED-GREEN-REFACTOR using specification
```

## Installation

### From Marketplace (Recommended)

```
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin
/plugin install pseudo-code-prompting-plugin
```

### Manual Installation

1. Clone repository: `git clone https://github.com/EladAriel/pseudo-code-prompting-plugin.git`
2. Copy `.claude-plugin/` to your project
3. Or reference from Claude Code settings

## Documentation

- **[Getting Started](./QUICK_START.md)** - 5-minute quick start guide
- **[Examples](./docs/examples.md)** - 4 real-world workflows
- **[cc10x Integration](./docs/cc10x-bridge.md)** - TDD integration guide
- **[Architecture Guide](./docs/architecture.md)** - How it all works

## Real-World Examples

### Example 1: OAuth Authentication
Transform: "Add OAuth with Google, GitHub. JWT 15m TTL. Rate limit 10/hour."
→ Production-ready pseudo-code with all parameters, error codes, security

### Example 2: API Rate Limiting
Transform: "Rate limit API to 1000 req/hour per user. Return 429 when exceeded."
→ Detailed specification with Redis backend, sliding window, retry headers

### Example 3: Payment Processing
Transform: "Stripe payments. Validate before charging. Retry 3x. Support refunds."
→ Complete spec with error handling, webhook validation, idempotency

## Who Should Use This

- **Engineers** who want crystal-clear specifications before implementation
- **Teams** that need to align on requirements
- **Architects** who want to ensure production readiness
- **QA/Reviewers** who need to validate specifications
- **Anyone using cc10x** for specification-driven TDD

## Key Benefits

1. **Eliminates Ambiguity** - "Add auth" → precise specification
2. **Catches Issues Early** - Validation finds security gaps before implementation
3. **Improves Quality** - Standard parameters in every spec (timeout, logging, retry)
4. **Guides Implementation** - Pseudo-code becomes test specification
5. **Enables Collaboration** - Shared specs create team alignment
6. **Reduces Rework** - Implementation errors caught because they violate spec
7. **Tech Stack Aware** - Generates appropriate file paths and patterns

## Best Practices

✓ **Be Specific**
- "Rate limit: 10/hour" not "implement rate limiting"
- "Return 401 if expired" not "handle token errors"

✓ **Include Error Scenarios**
- List specific HTTP status codes
- Define retry and fallback strategies

✓ **Name Operations Clearly**
- `implement_oauth` not `add_auth`

✓ **Think About Edge Cases**
- Concurrent requests, failures, boundary conditions

## Troubleshooting

**Plugin not loading after install?**
- Restart Claude Code
- Check `.claude-plugin/` directory exists

**Transform command not found?**
- Verify marketplace installation completed
- Check `/help` for available commands

**Can't install from marketplace?**
- Verify marketplace.claude.dev is accessible
- Try manual installation (see options above)

## Support

- **GitHub Issues**: https://github.com/EladAriel/pseudo-code-prompting-plugin/issues
- **GitHub Discussions**: https://github.com/EladAriel/pseudo-code-prompting-plugin/discussions

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See GitHub for contribution guidelines.

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Version

**v3.0.0** - Production-ready release
- 6-step transformation pipeline
- 6-dimension validation
- Tech stack detection (5+ languages)
- Auto-compression for requirements
- cc10x integration
- ~2,500 lines of documentation
- 60+ test specifications

---

**Transform vague requirements into production-ready specifications.**

[Get Started →](./QUICK_START.md)
