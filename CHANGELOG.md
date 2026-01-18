# Changelog

All notable changes to the Pseudo-Code Prompting Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-01-18

### Added

#### Context-Aware Tree Injection Module

- **Python tree generator** (`hooks/get_context_tree.py`) - Intelligent project structure scanning
  - Recursive directory scanning with configurable depth (default: 10 levels) and file limits (default: 1000 files)
  - Smart filtering with .gitignore support and default exclusions (node_modules, .git, dist, build, __pycache__, venv, etc.)
  - Cross-platform timeout handling (Windows: threading.Timer, Unix: signal.alarm)
  - Graceful error handling for permissions, symlinks, encoding issues
  - Output truncation at 50KB with informative statistics
  - Empty project detection with `<<PROJECT_EMPTY_NO_STRUCTURE>>` flag
  - ASCII tree formatting with file and directory counts

- **Bash hook orchestrator** (`hooks/context-aware-tree-injection.sh`) - Automatic context injection
  - Keyword detection for implementation tasks: implement, create, add, refactor, build, generate, setup, initialize
  - Python executable detection (python3 → python → graceful skip)
  - 15-second timeout with graceful degradation on failure
  - Context injection with formatted project structure
  - Integration with Claude Code hook system via hooks.json

- **Context-aware transform command** (`/context-aware-transform`)
  - **Rule A (Map Mode)**: Analyzes existing project structure and suggests architecture-aligned changes
    - Stack detection from file indicators (package.json, requirements.txt, go.mod, etc.)
    - Architecture pattern identification (MVC, feature-based, layered)
    - Specific file path recommendations based on existing conventions
    - Integration point identification
  - **Rule B (Skeleton Mode)**: Generates virtual project structure for empty projects
    - Technology stack inference from keywords
    - Five predefined templates: Next.js/React, Node/Express, Python/FastAPI, Go, Generic
    - Complete directory structure with purpose annotations
    - Stack-specific initialization steps

- **Comprehensive documentation**
  - `docs/CONTEXT-AWARE-MODE.md` - User-facing guide with examples and troubleshooting
  - `docs/TREE-INJECTION-GUIDE.md` - Technical implementation details and architecture
  - Updated README.md with Context-Aware Mode section

- **Multi-stack template system**
  - **nextjs_react**: Next.js 13+ with app directory, components, lib, hooks
  - **node_express**: Express with controllers, routes, models, middleware
  - **python_fastapi**: FastAPI with api/endpoints, core, models, schemas
  - **golang**: Go standard layout with cmd, internal, pkg
  - **default**: Generic structure for unknown stacks

- **GitHub Actions CI/CD workflows**
  - `ci.yml` - Comprehensive CI with JSON, bash, Python, and markdown validation
  - `plugin-validation.yml` - Plugin-specific validation (manifest, hooks, commands, documentation)
  - `release.yml` - Automated versioning and release with release-please
  - `version-check.yml` - PR validation for version bumps and CHANGELOG updates

### Changed

- **Enhanced `/transform-query` command** - Now integrates with context-aware tree injection
  - Automatically includes actual file paths from PROJECT_TREE when available
  - Applies Rule A (map to existing) or Rule B (generate skeleton) based on project state
  - Three modes: Context-Aware (with paths), Empty Project (with recommendations), Standard (generic)
  - Output includes `target_files`, `create_files`, `modifications`, `stack`, `architecture_pattern` parameters
- Updated plugin version from 1.2.0 to 1.3.0
- Updated hook count from 3 to 4 in documentation
- Updated command count from 4 to 5 in documentation
- Enhanced plugin description to mention context-aware capabilities
- Updated README.md with new Context-Aware Mode feature section
- Renamed documentation files to uppercase convention (CONTEXT-AWARE-MODE.md, TREE-INJECTION-GUIDE.md)

### Technical Details

- **Performance**: Tree generation completes in <2s for most projects, with hard timeout at 15s
- **Limits**: max_depth=10, max_files=1000, max_output=50KB (all configurable)
- **Dependencies**: Python 3.6+ stdlib only (no external dependencies)
- **Cross-platform**: Tested on Windows and Unix-like systems
- **Error handling**: Graceful degradation on all failures (Python missing, timeout, permissions, etc.)

## [1.2.0] - 2026-01-14

### Changed

#### Plugin Structure Refactoring

- **BREAKING**: Restructured plugin to follow official Claude Code plugin patterns
- Moved from `.claude/` folder structure to official auto-discovery layout
- Skills now in `skills/*/` with progressive loading (capabilities.json → SKILL.md → references → templates)
- Agents now in `agents/*.md` with YAML frontmatter
- Commands now in `commands/*.md` with markdown format
- Hooks now registered via `hooks/hooks.json` with bash scripts

#### Hook System Overhaul

- Created `hooks/hooks.json` for proper hook registration
- Updated all hook scripts to use `${CLAUDE_PLUGIN_ROOT}` for portable paths
- Added `set -euo pipefail` for better error handling
- Split hooks by event type: UserPromptSubmit and PostToolUse
- Hooks now use interactive approval mode with `permissionDecision: "ask"`

#### Documentation Updates

- Updated README.md with "Plugin Architecture" section
- Updated `.claude-plugin/README.md` (marketplace documentation)
- Removed outdated `.claude/` folder references
- Added progressive loading architecture documentation
- Updated troubleshooting to reflect new structure

### Removed

- Removed root `SKILL.md` (skills now have individual `skills/*/SKILL.md` files)
- Removed `.claude/agent-registry.json` (Claude Code uses auto-discovery)
- Removed `.claude/settings.json` (hooks now in `hooks/hooks.json`)

## [1.1.0] - 2026-01-13

### Added - Skills

- `prompt-analyzer` - Analyze prompts for ambiguity, complexity, and clarity with scoring
- `prompt-optimizer` - Optimize pseudo-code for completeness and implementation readiness
- `context-compressor` - Compress verbose requirements into concise pseudo-code (60-95% reduction)
- `requirement-validator` - Validate pseudo-code requirements for completeness, security, and correctness

### Added - Agents

- `requirement-validator` - Validates transformed pseudo-code, identifies gaps and security issues
- `prompt-optimizer` - Enhances pseudo-code by adding missing parameters and clarifying ambiguities
- `context-compressor` - Transforms verbose requirements into structured, compact pseudo-code

### Added - Commands

- `/validate-requirements` - Validate pseudo-code for completeness and correctness
- `/optimize-prompt` - Optimize pseudo-code for implementation readiness
- `/compress-context` - Compress verbose requirements into concise pseudo-code format

### Added - Hooks

- `post-transform-validation.sh` - Auto-validate transformed pseudo-code for completeness
- `context-compression-helper.sh` - Suggest context compression for verbose requirements (>100 words)

### Added - Reference Files

- `validation-checklists.md` - Comprehensive checklists for different feature types (API, database, auth, etc.)
- `common-issues.md` - Pattern library for common requirement issues and solutions

### Added - Project Files

- `.gitignore` - Standard ignore patterns for development
- `LICENSE` - MIT License
- `CHANGELOG.md` - Version history and changes
- `CONTRIBUTING.md` - Contribution guidelines

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

## [1.0.0] - 2026-01-12

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

### [1.1.0] - 2026-01-13
- Added validation, optimization, and compression capabilities
- 4 new skills, 3 new agents, 3 new commands, 2 new hooks
- Enhanced workflows and quality gates

### [1.0.0] - 2026-01-12
- Initial release with transformation and analysis
- 2 skills, 2 agents, 1 command, 1 hook
- Progressive loading and semantic discovery

---

For more details, see the [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
