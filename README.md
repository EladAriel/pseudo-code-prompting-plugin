# Pseudo-Code Prompting Plugin

Transform natural language requirements into structured, validated pseudo-code for optimal LLM responses and implementation clarity.

[![Version](https://img.shields.io/badge/version-1.6.1-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A52.1.0-blue.svg)](https://claude.ai/code)

## Overview

The Pseudo-Code Prompting Plugin enhances Claude Code with automated conversion, validation, and optimization of natural language requirements into concise, function-like pseudo-code. This structured approach eliminates ambiguity, ensures completeness, and accelerates development.

**Architecture:** Utilizes Claude Code's auto-discovery system - all skills, agents, and commands are automatically loaded based on your project context. No manual configuration required.

## Why Pseudo-Code Prompting?

### The Problem
- **Verbose requirements** consume excessive tokens (80-95% waste)
- **Ambiguous specifications** lead to incomplete implementations
- **Missing constraints** cause security vulnerabilities and edge case bugs
- **Unclear intent** results in clarification cycles and delays

### The Solution
Transform this:
```
We need to create a REST API endpoint that handles user registration. The endpoint should accept POST requests at the /api/register path. Users need to provide their email address, which must be validated to ensure it's a proper email format and not already in use. They also need to provide a password that meets our security requirements: at least 12 characters, including uppercase, lowercase, numbers, and special characters. The system should hash the password using bcrypt before storing it. If registration is successful, return a 201 status with the new user ID. If the email is already taken, return a 409 error. If validation fails, return a 400 error with details about what went wrong. We should also rate limit this endpoint to prevent abuse, allowing maximum 10 registration attempts per hour from the same IP address.
```

Into this:
```javascript
create_endpoint(
  path="/api/register",
  method="POST",
  request_schema={
    "email": "email:required:unique",
    "password": "string:required:min(12):requires(upper,lower,number,special)"
  },
  password_hash="bcrypt",
  response_codes={
    "201": {"user_id": "string", "created_at": "timestamp"},
    "400": "validation_error",
    "409": "duplicate_email"
  },
  rate_limit={"max": 10, "window": "1h", "key": "ip"},
  audit_log=true
)
```

**Result**: 95% reduction (158 words → 1 structured call), 100% semantic preservation, implementation-ready

## Key Features

### 🎯 7 Specialized Skills

| Skill | Purpose | Token Efficiency |
|-------|---------|------------------|
| **prompt-structurer** | Transform natural language → pseudo-code | 300-800 tokens |
| **prompt-analyzer** | Detect ambiguities, assess clarity | 200-500 tokens |
| **context-compressor** | Compress verbose requirements | 300-600 tokens |
| **prompt-optimizer** | Add missing parameters, enhance security | 400-700 tokens |
| **requirement-validator** | Validate completeness, security, edge cases | 500-800 tokens |
| **feature-dev-enhancement** | Integrate with feature-dev workflow | 200-400 tokens |
| **complete-process-orchestrator** | End-to-end workflow automation (transform → validate → optimize) | 1000-2000 tokens |

### 🤖 5 Intelligent Agents

| Agent | Specialization | Pipeline Position |
|-------|----------------|-------------------|
| **prompt-analyzer** | Ambiguity detection, complexity scoring | Entry (Tier 1) |
| **context-compressor** | Verbose requirement compression (60-95%) | Entry (Tier 1) |
| **prompt-transformer** | Natural language → function syntax | Core (Tier 2) |
| **prompt-optimizer** | Security, validation, completeness enhancement | Enhancement (Tier 3) |
| **requirement-validator** | Gap identification, security audit, edge cases | Quality (Tier 3) |

### 🎮 7 Skills (Auto-Invoked)

Skills are automatically invoked by Claude when relevant keywords/patterns are detected:

| Skill | Triggers | Purpose |
|-------|----------|---------|
| **prompt-structurer** | "transform", "structure", "pseudo-code" | Transform natural language to pseudo-code |
| **prompt-analyzer** | "analyze", "complexity", "ambiguity" | Analyze prompts for clarity |
| **requirement-validator** | "validate", "verify", "check" | Validate completeness & security |
| **prompt-optimizer** | "optimize", "enhance", "improve" | Add missing parameters |
| **context-compressor** | "compress", "reduce", "simplify" | Compress verbose requirements |
| **feature-dev-enhancement** | "feature-dev", "workflow" | Integrate with feature-dev |
| **complete-process-orchestrator** | "/complete-process", "/complete", "full workflow" | Orchestrate complete transformation pipeline |

### ⚡ 4 Automated Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| **user-prompt-submit** | User input | Detect /feature-dev commands, inject transformation |
| **post-transform-validation** | After transformation | Auto-validate output |
| **context-compression-helper** | Verbose input (>100 words) | Suggest compression |
| **context-aware-tree-injection** | Implementation keywords | Analyze project structure for architecture-aware suggestions |

### 🌳 Context-Aware `/transform-query` (NEW in v1.3.0)

The `/transform-query` command now automatically includes **actual file paths** from your project when transforming natural language to pseudo-code.

**How it works**:

1. You use implementation keywords: `implement`, `create`, `add`, `refactor`, `build`
2. Hook automatically scans your project structure
3. `/transform-query` outputs pseudo-code **with actual file paths** from your codebase

**Without Context-Aware** (Generic):

```javascript
/transform-query "add user authentication"

Output:
implement_authentication(
  type="jwt",
  features=["login", "logout", "session"],
  security=["bcrypt", "token"]
)
```

**With Context-Aware** (Actual Paths):

```javascript
/transform-query "implement user authentication"

Output:
implement_authentication(
  type="jwt",
  target_files=[
    "src/lib/auth.ts",              // ← Actual file from YOUR project
    "src/app/api/auth/route.ts"     // ← Follows YOUR architecture
  ],
  modifications=["src/app/layout.tsx"],
  create_files=["src/components/auth/LoginForm.tsx"],
  stack="nextjs_react",             // ← Detected from YOUR package.json
  architecture_pattern="app_directory"
)
```

**Key Benefits**:

- ✅ Outputs include **specific file paths** from your project
- ✅ Follows **your existing architecture** patterns
- ✅ Detects **your stack** automatically (Next.js, Express, FastAPI, Go)
- ✅ Works with **empty projects** too (generates recommended structure)

**Learn more**: [Context-Aware Transform-Query Guide](docs/CONTEXT-AWARE-MODE.md) | [Technical Details](docs/TREE-INJECTION-GUIDE.md)

### 💾 Semantic Caching System (v1.4.0) + Optimized Query Scoring (v1.5.0)

Dramatically reduce API costs and response times by intelligently reusing previously-generated patterns through AI-powered semantic matching.

**The Problem**: Generating pseudo-code patterns requires expensive API calls and takes 10-30 seconds each time.

**The Solution**: Semantic caching understands the **meaning** of your query and matches it to similar patterns, even with different wording.

**Example**:

```bash
# First time (generates pattern)
/transform-query implement Google OAuth authentication
# → Takes 15 seconds, costs $0.01

# Later (semantically similar query)
/transform-query add Google login with OAuth 2.0
# 📦 Loaded cached pattern: auth_google_oauth
# → Takes 2 seconds, costs $0.0001 (100x cheaper!)
```

**Key Benefits**:

- **10x Cost Reduction**: Cache hits use Claude Haiku (~$0.0001) vs full generation (~$0.01+)
- **5-15x Faster**: Load from disk (2s) vs full generation (10-30s)
- **Intelligent Matching**: Semantic understanding, not exact text matching
- **Team Sharing**: Commit cached patterns to share with your team
- **Auto-Optimized**: Most-used patterns prioritized for faster lookups

**How It Works**:

```text
Your Query
    ↓
Semantic Router (Claude Haiku) ← Lightweight, fast
    ↓
  Match?
    ↓
Yes → Load from Cache → Done! (2 seconds)
No  → Generate Pattern → Optionally Save (10-30 seconds)
```

**Quick Start**:

```bash
# 1. Install Python package
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY="your-key"

# 3. Generate a pattern
/transform-query implement JWT authentication

# 4. Save it for reuse
./hooks/cache/cache-success.sh
# Tag: auth_jwt
# Description: JWT authentication with access tokens

# 5. Later, benefit from semantic matching
/transform-query add JWT-based user login
# 📦 Loaded cached pattern: auth_jwt ← Instant!
```

**Cache Management Commands**:

```bash
./hooks/cache/list-cache.sh          # List all cached patterns
./hooks/cache/search-cache.sh oauth  # Search by keyword
./hooks/cache/cache-stats.sh         # View statistics
./hooks/cache/validate-cache.sh      # Check integrity
./hooks/cache/delete-cache.sh <tag>  # Remove pattern
./hooks/cache/update-cache.sh <tag>  # Update pattern
```

**Cost Example** (10 authentication requests):

- **Without Cache**: 10 × $0.01 = **$0.10**
- **With Cache**: $0.01 + (9 × $0.0001) = **$0.0109** (~90% savings)

**Learn more**: [Semantic Caching Documentation](docs/CACHING.md)

### 🎯 Enhanced Cache Control & Context Injection (NEW in v1.6.1)

Version 1.6.1 introduces three major improvements to the caching system for better user control and cross-project reusability:

#### 1. ✅ User Confirmation Before Cache Operations

Never be surprised by cached results again. The system now asks for your confirmation before using a cached pattern:

```text
╔════════════════════════════════════════════════════════════════╗
║                    Cached Pattern Found                        ║
╚════════════════════════════════════════════════════════════════╝

Tag ID:           auth_jwt
Type:             optimized
Description:      JWT authentication with refresh tokens
Similarity:       87%
Usage Count:      12
Last Used:        2026-01-18
File Size:        3.2KB

Preview:
────────────────────────────────────────────────────────────────
implement_jwt_authentication(
  token_type="jwt",
  access_token_ttl="15m",
  ...
────────────────────────────────────────────────────────────────

💡 Tip: Cache hits save ~90% cost and 5-15x faster than generation

Would you like to use this cached pattern? [Y]es / [N]o / [V]iew full / [C]ancel:
```

**Features**:

- Interactive preview with metadata (similarity score, usage stats, pattern type)
- View full pattern before accepting
- 30-second timeout with countdown (defaults to "yes")
- Non-interactive mode for CI/CD (auto-confirms)
- Environment variable override: `export CACHE_AUTO_CONFIRM=yes`

#### 2. 🔄 Context-Aware Path Injection

Cached patterns are now **project-agnostic** - they work across different codebases by adapting to your current project structure:

**How It Works**:

- ✅ Cache matching based on **intent**, NOT file paths
- ✅ Automatic detection of current project structure
- ✅ Technology stack identification (Node.js, Python, Go, Rust, Java)
- ✅ Intelligent path mapping from cached pattern to your project

**Example**:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 CACHED PATTERN LOADED: auth_jwt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  CONTEXT-AWARE MODE: This pattern is being adapted to your current project

Current Project Root: /your/project
Project Stack:
  📦 Node.js/JavaScript project (package.json found)

Current Project Structure:
src/
├── lib/
│   └── auth.ts
├── app/
│   └── api/
└── components/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CACHED PATTERN BELOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When applying this pattern:
1. Map the cached file paths to your current project structure shown above
2. Preserve the relative directory relationships from the pattern
3. Adapt file names/paths to match your current technology stack
4. If a suggested file/directory doesn't exist, create it or use the closest match

[Original cached pattern with context for adaptation...]
```

**Benefits**:

- Same cached pattern works across Next.js, Express, FastAPI, Go projects
- No brittle path replacement - intelligent semantic mapping
- Claude understands how to adapt paths to your project
- Preserves relative directory relationships

#### 3. 🛠️ Fixed Permission Pattern Syntax

Resolved configuration file syntax errors that could block cache operations:

- Fixed `:*` wildcard patterns to use proper `*` syntax
- Updated `.claude/settings.local.json` for compatibility
- All permission patterns now follow correct format

**Technical Details**:

- **Confirmation Script**: [hooks/cache/confirm-cache-use.sh](hooks/cache/confirm-cache-use.sh)
- **Path Injection Script**: [hooks/cache/inject-context-paths.sh](hooks/cache/inject-context-paths.sh)
- **Integration Point**: [hooks/tree/context-aware-tree-injection.sh](hooks/tree/context-aware-tree-injection.sh)
- **Updated Documentation**: [commands/transform-query.md](commands/transform-query.md)

#### 4. 🚀 Complete Process Orchestrator Improvements (ALSO NEW in v1.6.1)

The `/complete-process` orchestrator has been significantly enhanced with three critical improvements for efficiency and accuracy:

##### **Mandatory Skill Tool Invocation**

The orchestrator now **enforces** proper skill invocation patterns:

- ✅ Always uses Skill tool for sub-skill invocations (`prompt-structurer`, `requirement-validator`, `prompt-optimizer`)
- ✅ Prevents direct handling of transformations for consistency
- ✅ Ensures proper separation of concerns in the pipeline
- ✅ Clear examples of correct vs incorrect patterns in documentation

##### **Context Window Optimization (60-80% Token Reduction)** 🎯

**Massive efficiency improvement** - the orchestrator now intelligently removes intermediate outputs:

**Before (v1.6.0)**:

```text
User Query (500 tokens)
→ Transform Output (800 tokens) ← KEPT
→ Validate Input (800 tokens) ← KEPT (duplicate)
→ Validate Output (600 tokens) ← KEPT
→ Optimize Input (600 tokens) ← KEPT (duplicate)
→ Optimize Output (900 tokens) ← KEPT

Total Context: 4,200 tokens
```

**After (v1.6.1)**:

```text
User Query (500 tokens) ← KEPT
→ Transform Output → extracted, not kept
→ Validate Input → not kept (duplicate)
→ Validate Output → extracted, not kept
→ Optimize Input → not kept (duplicate)
→ Final Optimized Output (900 tokens) ← KEPT

Total Context: 1,400 tokens (66% reduction!)
```

**Benefits**:

- 60-80% reduction in context window usage
- Enables longer conversations without hitting token limits
- Reduces costs significantly
- Improves performance

**Implementation**: The orchestrator extracts only essential results and passes them to the next step WITHOUT including full tool outputs in subsequent messages.

##### **Context-Aware Tree Injection Integration** 🌳

The orchestrator now automatically leverages PROJECT_TREE context from the UserPromptSubmit hook:

**How It Works**:

1. User query contains implementation keywords: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`
2. Hook automatically injects `[CONTEXT-AWARE MODE ACTIVATED]` with project structure
3. Orchestrator checks for this marker and passes PROJECT_TREE context to transform skill
4. Results in **project-specific, architecture-aware** transformations

**Without Context-Aware**:

```javascript
implement_authentication(
  type="jwt",
  features=["login", "logout"]
)
```

**With Context-Aware**:

```javascript
implement_authentication(
  type="jwt",
  target_files=["src/lib/auth.ts", "src/app/api/auth/route.ts"],
  stack="nextjs_react",
  architecture_pattern="app_directory"
)
```

**Troubleshooting**: The orchestrator documentation now includes guidance for checking context injection and resolving issues.

**Technical Details**:

- **Updated SKILL**: [skills/complete-process-orchestrator/SKILL.md](skills/complete-process-orchestrator/SKILL.md)
- **Updated Capabilities**: [skills/complete-process-orchestrator/capabilities.json](skills/complete-process-orchestrator/capabilities.json)
- **Skill Version**: Updated from 1.0.0 to 1.1.0
- **New Features**: `context_window_optimization`, `context_aware_tree_injection`, `mandatory_skill_tool_invocation`

### 🔄 Complete Process Orchestration (NEW in v1.6.0)

Automate the entire transformation pipeline with a single command. Instead of manually running transform → validate → optimize, the Complete Process Orchestrator handles everything automatically with intelligent error recovery and progress tracking.

**The Problem**: Running `/transform-query`, `/validate-requirements`, and `/optimize-prompt` separately is tedious and error-prone.

**The Solution**: One command that orchestrates the entire workflow with two modes:

**Quick Mode** (5-15s):

- Transform only
- Best for simple queries and rapid iteration
- Perfect for prototyping

**Complete Mode** (30-90s):

- Transform → Validate → Optimize
- Production-ready output with full validation
- Includes error handling, security, and edge cases

**Example**:

```bash
# Invoke the orchestrator
/complete-process Implement JWT authentication with refresh tokens

# Choose your workflow mode:
○ Quick Transform Only (5-15s)
● Complete Process (Recommended) (30-90s)

# Complete mode shows progress:
Step 1/3: 🔄 Transforming query to pseudo-code... ✓ (12s)
Step 2/3: ✓ Validating requirements... ✓ (8s)
Step 3/3: ⚡ Optimizing for implementation... ✓ (22s)

✓ Pipeline complete! Review output below.
```

**Key Features**:

- **Mode Selection**: Choose quick or complete based on your needs
- **Progress Tracking**: Real-time visibility into pipeline execution
- **Error Recovery**: Automatic rollback and checkpoint recovery
- **Preference Persistence**: Remembers your mode choice for next time
- **Timeout Protection**: Graceful handling with partial results
- **State Management**: Preserves work on failures for easy retry

**Benefits**:

- ✅ **Streamlined Workflow**: One command instead of three
- ✅ **Intelligent Automation**: Full validation and optimization automatically
- ✅ **Error Resilience**: Recovers from failures gracefully
- ✅ **Time Savings**: 50% faster than manual steps
- ✅ **Quality Assurance**: Complete mode ensures production-ready output

**Available Commands**:

- `/complete-process` (primary)
- `/complete` (alias)
- `/full-transform` (alias)
- `/orchestrate` (alias)

**Learn more**: [Complete Process Documentation](skills/complete-process-orchestrator/SKILL.md)

## Installation

### Requirements

- Claude Code v2.1.0 or higher

### From Marketplace

```bash
# Step 1: Add the marketplace
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin

# Step 2: Install the plugin
/plugin install pseudo-code-prompting
```

### From GitHub (Manual)

```bash
# Clone to your Claude plugins directory
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin ~/.claude/plugins/pseudo-code-prompting
```

### Project-Scoped Installation

```bash
# Copy plugin to your project
cp -r pseudo-code-prompting-plugin/.claude your-project/.claude
```

### Verify Installation

After installation, verify the plugin is loaded:

```bash
/plugin list
```

You should see `pseudo-code-prompting` in the installed plugins list.

**Note:** This plugin uses **auto-invoked skills**, not slash commands. Skills are automatically triggered by Claude when you use relevant keywords in your requests.

## Quick Start Guide

See [docs/QUICK_START.md](docs/QUICK_START.md) for a comprehensive guide on using the plugin, including:

- How skills are automatically invoked
- Transforming natural language to pseudo-code
- Validating requirements
- Optimizing pseudo-code
- Compressing verbose requirements

## PROMPTCONVERTER Methodology

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for detailed information on the 5 transformation rules and methodology, including:

- Analyzing intent
- Creating function names
- Extracting parameters
- Inferring constraints
- Output formatting

## Workflows

See [docs/WORKFLOWS.md](docs/WORKFLOWS.md) for information on different workflow patterns, including:

- Full transformation workflow
- Quick transform
- Optimize and validate
- Compress, transform, validate
- Progressive loading architecture

## Validation Coverage

See [docs/VALIDATION.md](docs/VALIDATION.md) for comprehensive information on validation features, including:

- Security validation checks
- Completeness checks
- Edge case detection

## Real-World Examples

See [docs/EXAMPLES.md](docs/EXAMPLES.md) for detailed real-world examples, including:

- E-Commerce checkout implementation (94% reduction)
- Real-time dashboard (92% reduction)
- Machine learning pipeline (93% reduction)
- LangChain Guardrails documentation compression (80% reduction, 4,200 → 850 tokens)
- Usage examples from repository

## Integration

See [docs/INTEGRATION.md](docs/INTEGRATION.md) for information on integrating with other workflows, including:

- Feature-dev workflow integration
- Code generation integration
- Documentation integration

## Configuration

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for configuration options, including:

- Customizing hook behavior
- Customizing skills
- Extending skills with custom patterns
- Advanced usage

## Performance Metrics

See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for performance statistics, including:

- Token efficiency
- Compression ratios
- Validation coverage metrics

## Plugin Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for architectural details, including:

- Directory structure
- Progressive loading system
- Hook system

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues and solutions, including:

- Commands not working
- Hooks not triggering
- Skills not auto-invoked
- Validation too strict

## Q&A

See [docs/QA.md](docs/QA.md) for frequently asked questions, including:

- How the plugin gathers context
- Auto-discovery and semantic matching
- Progressive loading architecture
- Hook context injection
- Smart reference loading
- Token efficiency comparisons

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new skills
- How to create custom agents
- How to write hooks
- Code quality guidelines
- Pull request process

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following [CONTRIBUTING.md](CONTRIBUTING.md)
4. Test thoroughly with Claude Code
5. Submit a pull request

## Documentation

- **[README.md](README.md)** - This file - Complete plugin documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed contribution guidelines
- **[examples/](examples/)** - Real-world usage examples
- **[LICENSE](LICENSE)** - MIT License details

## License

MIT License - See [LICENSE](LICENSE) for full details.

Copyright (c) 2026 Pseudo-Code Prompting Contributors

## Support

- **Issues:** [GitHub Issues](https://github.com/EladAriel/pseudo-code-prompting/issues)
- **Discussions:** [GitHub Discussions](https://github.com/EladAriel/pseudo-code-prompting/discussions)

## Acknowledgments

- Built for [Claude Code](https://claude.com/code)

## Version

**Current Version:** 1.6.0
**Last Updated:** 2026-01-18
**Minimum Claude Code Version:** 2.1.0