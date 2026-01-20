# Pseudo-Code Prompting Plugin

Transform natural language requirements into structured, validated pseudo-code for optimal LLM responses and implementation clarity.

[![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A52.1.0-blue.svg)](https://claude.ai/code)
[![Last Updated](https://img.shields.io/badge/updated-2026--01--20-brightgreen.svg)](CHANGELOG.md)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
- [Why Pseudo-Code Prompting?](#why-pseudo-code-prompting)
- [Key Features](#key-features)
- [Complete Process Orchestration](#complete-process-orchestration)
- [Ralph Loop Integration](#ralph-loop-integration)
- [PROMPTCONVERTER Methodology](#promptconverter-methodology)
- [Workflows](#workflows)
- [Validation Coverage](#validation-coverage)
- [Real-World Examples](#real-world-examples)
- [Integration](#integration)
- [Configuration](#configuration)
- [Performance Metrics](#performance-metrics)
- [Plugin Architecture](#plugin-architecture)
- [Troubleshooting](#troubleshooting)
- [Q&A](#qa)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Overview

The Pseudo-Code Prompting Plugin enhances Claude Code with automated conversion, validation, and optimization of natural language requirements into concise, function-like pseudo-code. This structured approach eliminates ambiguity, ensures completeness, and accelerates development.

**Architecture:** Utilizes Claude Code's auto-discovery system - all skills, agents, and commands are automatically loaded based on your project context. No manual configuration required.

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

### 💡 Don't Like Commands? Just Talk to Claude!

If you prefer not to use slash commands, simply say:
- **"Use pseudo-code prompting plugin"** - Claude will guide you through the transformation process
- **"Use pseudo-code prompting plugin with Ralph"** - Claude will orchestrate the complete workflow with Ralph Loop for automated implementation
- **Use pseudo-code prompting {{command}} to {{task}}** - Claude will invoke the plugin's command.
The commands: `complete process`, `compress context`, `context aware transform`, `optimize prompt`, `ralph process`, `transform query`, `validate requirements`

Claude will understand your intent and invoke the appropriate skills automatically.

---

See [docs/QUICK_START.md](docs/QUICK_START.md) for a comprehensive guide on using the plugin, including:

- How skills are automatically invoked
- Transforming natural language to pseudo-code
- Validating requirements
- Optimizing pseudo-code
- Compressing verbose requirements

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

### 🎯 8 Specialized Skills

| Skill | Purpose | Token Efficiency |
|-------|---------|------------------|
| **prompt-structurer** | Transform natural language → pseudo-code | 300-800 tokens |
| **prompt-analyzer** | Detect ambiguities, assess clarity | 200-500 tokens |
| **context-compressor** | Compress verbose requirements | 300-600 tokens |
| **prompt-optimizer** | Add missing parameters, enhance security | 400-700 tokens |
| **requirement-validator** | Validate completeness, security, edge cases | 500-800 tokens |
| **feature-dev-enhancement** | Integrate with feature-dev workflow | 200-400 tokens |
| **complete-process-orchestrator** | End-to-end workflow automation (transform → validate → optimize) | 1000-2000 tokens |
| **ralph-process-integration** | Automated iterative implementation with Ralph Loop (complexity estimation + promise generation) | 60-120s setup + Ralph iterations |

### 🤖 5 Intelligent Agents

| Agent | Specialization | Pipeline Position |
|-------|----------------|-------------------|
| **prompt-analyzer** | Ambiguity detection, complexity scoring | Entry (Tier 1) |
| **context-compressor** | Verbose requirement compression (60-95%) | Entry (Tier 1) |
| **prompt-transformer** | Natural language → function syntax | Core (Tier 2) |
| **prompt-optimizer** | Security, validation, completeness enhancement | Enhancement (Tier 3) |
| **requirement-validator** | Gap identification, security audit, edge cases | Quality (Tier 3) |

### 🎮 8 Skills (Auto-Invoked)

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
| **ralph-process-integration** | "/ralph-process" | Integrate pseudo-code processing with Ralph Loop for automated implementation |

### ⚡ 4 Automated Hooks

All hooks are implemented in Python 3 for robust JSON parsing and cross-platform compatibility.

| Hook | Trigger | Purpose |
|------|---------|---------|
| **user-prompt-submit** | User input | Detect /feature-dev commands, inject transformation |
| **post-transform-validation** | After transformation | Auto-validate output |
| **context-compression-helper** | Verbose input (>100 words) | Suggest compression |
| **context-aware-tree-injection** | Implementation keywords | Analyze project structure for architecture-aware suggestions |

**Note:** As of v1.0.10, all hooks use Python 3 with `json.load()` for reliable JSON parsing, ensuring proper handling of escaped characters, nested JSON, and complex strings across all platforms (Windows, WSL, Linux, macOS).

### 🌳 Context-Aware `/transform-query`

The `/transform-query` command automatically includes **actual file paths** from your project when transforming natural language to pseudo-code. When you use implementation keywords (`implement`, `create`, `add`, `refactor`, `build`), the hook automatically scans your project structure and outputs pseudo-code with actual paths from your codebase.

**Example**:

```javascript
/transform-query "implement user authentication"
// Outputs: actual file paths, detected stack, architecture pattern
```

**Learn more**: [Context-Aware Transform-Query Guide](docs/CONTEXT-AWARE-MODE.md) | [Technical Details](docs/TREE-INJECTION-GUIDE.md)


## Complete Process Orchestration

See [docs/COMPLETE-PROCESS-ORCHESTRATION.md](docs/COMPLETE-PROCESS-ORCHESTRATION.md) for comprehensive guide on the complete-process orchestrator, including:

- Automated pipeline (transform → validate → optimize)
- Workflow modes (Quick vs Complete)
- Context window optimization (60-80% token reduction)
- Context-aware tree injection
- Progress tracking and error recovery
- Mode selection and preference persistence

## Ralph Loop Integration

See [docs/RALPH-LOOP-INTEGRATION.md](docs/RALPH-LOOP-INTEGRATION.md) for comprehensive guide on automated iterative implementatio, including:

- End-to-end workflow with Ralph Loop
- Automatic complexity estimation
- Promise generation from validation requirements
- Iteration planning (Simple: 20, Medium: 40, Complex: 80)
- Usage examples and best practices
- Troubleshooting and advanced usage

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
