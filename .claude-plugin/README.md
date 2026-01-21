# Pseudo-Code Prompting Plugin Installation

## Quick Start

### Requirements

- Claude Code v2.1.0 or higher

### From Marketplace

```bash
# Step 1: Add the marketplace
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin

# Step 2: Install the plugin
/plugin install pseudo-code-prompting
```

All features (8 skills, 5 agents, 6 commands, 4 hooks) are automatically available after installation.

### From GitHub (Manual)

```bash
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin ~/.claude/plugins/pseudo-code-prompting
```

### Local Development

```bash
# Clone and symlink for development
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin
cd ~/.claude/plugins
ln -s /path/to/pseudo-code-prompting-plugin pseudo-code-prompting
```

## What It Does

Converts verbose natural language into concise, production-ready pseudo-code:

**Before (158 words):**
```
We need to create a REST API endpoint that handles user registration. The endpoint should
accept POST requests at the /api/register path. Users need to provide their email address,
which must be validated to ensure it's a proper email format and not already in use...
```

**After (1 line, 95% reduction):**
```javascript
create_endpoint(
  path="/api/register",
  method="POST",
  request_schema={"email": "email:required:unique", "password": "string:required:min(12)"},
  password_hash="bcrypt",
  response_codes={"201": {"user_id": "string"}, "400": "validation_error", "409": "duplicate_email"},
  rate_limit={"max": 10, "window": "1h", "key": "ip"}
)
```

## Features

### 8 Specialized Skills
- **prompt-structurer** - Transform natural language to pseudo-code
- **requirement-validator** - Validate completeness and security
- **prompt-optimizer** - Add missing parameters
- **context-compressor** - Reduce verbosity by 80-95%
- **feature-dev-enhancement** - Integrate with feature-dev workflow
- **complete-process-orchestrator** - Full pipeline automation
- **session-memory** - Pattern learning and preference retention
- **prompt-analyzer** - Ambiguity detection and complexity scoring

### 6 Commands
- `/complete-process` - Full pipeline: transform → validate → optimize
- `/transform-query` - Basic transformation to pseudo-code
- `/compress-context` - Reduce verbose requirements
- `/validate-requirements` - Check completeness and security
- `/optimize-prompt` - Add security, validation, error handling
- `/context-aware-transform` - Architecture-aware with real file paths

### 5 Specialized Agents
- **prompt-transformer** - Natural language → function syntax
- **requirement-validator** - Security audit and gap detection
- **prompt-optimizer** - Enhancement with missing parameters
- **context-compressor** - Token reduction (60-95%)
- **prompt-analyzer** - Ambiguity and complexity analysis

### 4 Automated Hooks
- **user-prompt-submit** - Detects commands and keywords
- **context-aware-tree-injection** - Scans project structure automatically
- **context-compression-helper** - Suggests compression for large inputs
- **post-transform-validation** - Auto-validates output

## Key Benefits

✅ **60-95% Token Reduction** - Compress verbose requirements while preserving 100% semantics

✅ **Context-Aware** - Automatically scans your project and includes real file paths

✅ **Security Validation** - Checks auth, input sanitization, OWASP compliance

✅ **Session Memory** - Learns your preferences and patterns across sessions

✅ **Production-Ready** - Adds validation, error handling, performance constraints

## Usage

Just talk to Claude naturally:
```
Run complete-process: implement JWT authentication with refresh tokens
```

Or use slash commands:
```
/complete-process implement JWT authentication with refresh tokens
```

## Documentation

- **[Main README](../README.md)** - Complete overview and examples
- **[Command Docs](../docs/)** - Individual 1-minute guides for each command
- **[ARCHITECTURE](../docs/ARCHITECTURE.md)** - System design with diagrams
- **[CHANGELOG](../CHANGELOG.md)** - Version history

**Total read time: 10 minutes to become proficient!**

## Plugin Architecture

```
User Request → Hooks (auto-inject context) → Commands → Agents → Skills → Output
```

- **Progressive Loading**: Skills use capabilities.json for token-efficient discovery
- **Auto-Discovery**: All commands, skills, and hooks are automatically loaded
- **Context-Aware**: Automatically analyzes your project structure

## PROMPTCONVERTER Methodology

The plugin uses the PROMPTCONVERTER methodology with 5 transformation rules:

1. **Analyze Intent**: Identify core action (verb) and subject (noun)
2. **Create Function Name**: Combine into `snake_case` (e.g., `implement_authentication`)
3. **Extract Parameters**: Convert details to named parameters (e.g., `providers=["google"]`)
4. **Infer Constraints**: Detect implicit requirements (security, performance, validation)
5. **Output Format**: Single-line pseudo-code: `function_name(param="value", ...)`

## Performance Metrics

| Metric | Result |
|--------|--------|
| Token reduction | 60-95% |
| Processing time (transform) | 5-15 seconds |
| Processing time (complete) | 30-90 seconds |
| Validation accuracy | 95%+ |

## Version

**Current Version:** 1.1.4
**Last Updated:** 2026-01-21

## Support

- **Issues:** [GitHub Issues](https://github.com/EladAriel/pseudo-code-prompting/issues)
- **Discussions:** [GitHub Discussions](https://github.com/EladAriel/pseudo-code-prompting/discussions)
