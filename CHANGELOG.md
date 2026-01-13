# Changelog

All notable changes to the Pseudo-Code Prompting Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-01-13

### Added

#### New Skills
- `prompt-analyzer` - Analyze prompts for ambiguity, complexity, and clarity with scoring
- `prompt-optimizer` - Optimize pseudo-code for completeness and implementation readiness
- `context-compressor` - Compress verbose requirements into concise pseudo-code (60-95% reduction)
- `requirement-validator` - Validate pseudo-code requirements for completeness, security, and correctness

#### New Agents
- `requirement-validator` - Validates transformed pseudo-code, identifies gaps and security issues
- `prompt-optimizer` - Enhances pseudo-code by adding missing parameters and clarifying ambiguities
- `context-compressor` - Transforms verbose requirements into structured, compact pseudo-code

#### New Commands
- `/validate-requirements` - Validate pseudo-code for completeness and correctness
- `/optimize-prompt` - Optimize pseudo-code for implementation readiness
- `/compress-context` - Compress verbose requirements into concise pseudo-code format

#### New Hooks
- `post-transform-validation.sh` - Auto-validate transformed pseudo-code for completeness
- `context-compression-helper.sh` - Suggest context compression for verbose requirements (>100 words)

#### New Reference Files
- `validation-checklists.md` - Comprehensive checklists for different feature types (API, database, auth, etc.)
- `common-issues.md` - Pattern library for common requirement issues and solutions

#### Configuration Files
- `.claude/agent-registry.json` - Agent coordination, discovery, and workflow definitions
- `.claude/settings.json` - Hook configuration and lifecycle management

#### Project Files
- `.gitignore` - Standard ignore patterns for development
- `LICENSE` - MIT License
- `CHANGELOG.md` - Version history and changes
- `CONTRIBUTING.md` - Contribution guidelines
- `SKILL.md` - Plugin overview and quick reference

### Enhanced

#### Workflows
- `full-transformation` - Now includes requirement validation step (900 tokens)
- `optimize-and-validate` - New workflow for enhancing existing pseudo-code (700 tokens)
- `compress-transform-validate` - Complete workflow from verbose to validated (1000 tokens)

#### Plugin Metadata
- Updated version to 2.1.0
- Added keywords: validation, optimization, compression, security-validation
- Enhanced description to highlight validation and optimization capabilities

### Changed
- Increased `max_skills_per_task` in discovery to 3 (from 2)
- Updated progressive loading strategy with validation tier

## [2.0.0] - 2026-01-12

### Added

#### Core Features
- Initial release of Pseudo-Code Prompting Plugin
- PROMPTCONVERTER methodology implementation
- Progressive loading system with 4-tier architecture

#### Skills
- `prompt-structurer` - Transform natural language to pseudo-code using PROMPTCONVERTER
- `feature-dev-enhancement` - Apply structured pseudo-code across feature-dev workflow phases

#### Agents
- `prompt-analyzer` - Analyze prompts for ambiguity and complexity
- `prompt-transformer` - Transform natural language to function-like pseudo-code

#### Commands
- `/transform-query` - Transform natural language to pseudo-code

#### Hooks
- `user-prompt-submit.sh` - Detect /feature-dev and /pseudo-prompt commands

#### Documentation
- Comprehensive README.md with usage examples
- MARKETPLACE.md for Claude Code Marketplace
- PROMPTCONVERTER.md methodology guide

### Features
- Semantic skill discovery with confidence thresholds
- Token-efficient progressive loading (100-800 tokens per tier)
- Workflow automation with estimated token usage
- Integration with feature-dev workflow

## Version History

### [2.1.0] - 2026-01-13
- Added validation, optimization, and compression capabilities
- 4 new skills, 3 new agents, 3 new commands, 2 new hooks
- Enhanced workflows and quality gates

### [2.0.0] - 2026-01-12
- Initial release with transformation and analysis
- 2 skills, 2 agents, 1 command, 1 hook
- Progressive loading and semantic discovery

---

For more details, see the [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
