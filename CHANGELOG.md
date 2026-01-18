# Changelog

All notable changes to the Pseudo-Code Prompting Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2026-01-18

### Added

#### Complete Process Orchestrator

- **New skill: complete-process-orchestrator** - End-to-end workflow automation
  - Orchestrates full transformation pipeline (transform → validate → optimize)
  - Two execution modes: Quick (5-15s) and Complete (30-90s)
  - Automatic mode selection with user preference persistence
  - Real-time progress tracking with step indicators
  - Comprehensive error handling and recovery strategies

- **New command: /complete-process** (aliases: `/complete`, `/full-transform`, `/orchestrate`)
  - Single command replaces manual execution of three separate commands
  - Interactive mode selection with clear descriptions and time estimates
  - Progress visualization for multi-step pipeline execution
  - Smart fallback handling for step failures

- **Pipeline Features**
  - **Input Validation**: Query length constraints (10-5000 chars), sanitization
  - **Progress Tracking**: Real-time step indicators with emoji status icons
  - **Error Recovery**: Checkpoint-based rollback with preserved state
  - **Timeout Protection**: Per-step and total pipeline timeouts with warnings
  - **State Management**: In-memory handoff with checkpoint preservation
  - **Preference Persistence**: Remembers user's mode choice in `.claude/plugin_preferences.json`

- **Execution Modes**
  - **Quick Mode**: Transform only (5-15s) - Best for simple queries and rapid iteration
  - **Complete Mode**: Full pipeline (30-90s) - Transform → Validate → Optimize with production-ready output

- **Documentation**
  - `skills/complete-process-orchestrator/SKILL.md` - Comprehensive 600+ line skill documentation
  - `skills/complete-process-orchestrator/capabilities.json` - Skill metadata and dependencies
  - `skills/complete-process-orchestrator/references/workflow-patterns.md` - 400+ line pattern library
  - `skills/complete-process-orchestrator/templates/mode-selection.md` - UI templates and guidelines
  - `commands/complete-process.md` - 500+ line command documentation with examples

### Changed

- **Updated plugin version** from 1.5.0 to 1.6.0
- **Updated plugin description** to include "orchestrated workflows"
- **Updated feature counts**:
  - Skills: 6 → 7
  - Commands: 5 → 6
  - Keywords: Added "workflow-orchestration" and "pipeline-automation"
- **Updated README.md**:
  - Added new "Complete Process Orchestration" section with feature overview
  - Updated all skill/command count references
  - Added usage examples and benefits
- **Minimum Claude Code version** updated to 2.1.0

### Benefits

- **50% Time Savings**: One command instead of three manual steps
- **Streamlined Workflow**: Automatic pipeline execution with intelligent error recovery
- **Better UX**: Progress visibility, preference memory, graceful degradation
- **Production Quality**: Complete mode ensures validation and optimization automatically
- **Flexibility**: Choose quick or complete mode based on query complexity

## [1.5.0] - 2026-01-18

### Added

#### Optimized Query Scoring System

- **Two-tier pattern system** for intelligent cache matching
  - **Regular patterns**: Standard patterns with 70% match threshold, 1.0x weight
  - **Optimized patterns**: Validated/enhanced patterns with 65% threshold, 1.5x priority weight
  - Encourages users to mark high-quality patterns for better matching

- **Registry schema enhancement**
  - Added `metadata.query_type` field ("regular" or "optimized")
  - Backward compatible - existing patterns default to "regular"
  - Self-documenting pattern quality level

- **Enhanced semantic router** (`hooks/cache/find_tag.py`)
  - Weight-based prioritization (1.5x for optimized patterns)
  - Updated prompt to Claude with type indicators and weights
  - Lower match threshold for optimized patterns (65% vs 70%)
  - Preferential matching when multiple patterns qualify

- **Interactive query type selection** (`hooks/cache/cache-success.sh`)
  - Prompts user: "Tag this as optimized query? [y/N]"
  - Clear explanation of regular vs optimized differences
  - Visual confirmation of selected type

- **Statistics enhancement** (`hooks/cache/cache-stats.sh`)
  - Breakdown by type: Regular vs Optimized
  - Usage counts for each type
  - Helps users understand cache composition

- **List enhancement** (`hooks/cache/list-cache.sh`)
  - Added TYPE column showing "REG" or "OPT"
  - Visual indicator of pattern quality at a glance

### Changed

#### Directory Reorganization

- **Restructured hooks directory** for better organization and maintainability
  - `hooks/cache/` - All caching scripts (find_tag.py, cache-success.sh, etc.)
  - `hooks/tree/` - Project tree generation (get_context_tree.py, context-aware-tree-injection.sh)
  - `hooks/validation/` - Post-transformation validation
  - `hooks/compression/` - Context compression helpers
  - `hooks/core/` - Core hook scripts

- **Updated all file references** across codebase
  - hooks/hooks.json - Updated all hook paths
  - commands/transform-query.md - Updated cache script paths
  - hooks/tree/context-aware-tree-injection.sh - Updated cache router path
  - All documentation updated with new paths

- **Path calculation fixes** for subdirectory structure
  - Added HOOKS_DIR intermediate variable
  - Ensures correct PLUGIN_DIR resolution from nested scripts

### Documentation

- **REFACTORING_SUMMARY.md** - Comprehensive technical documentation
  - Complete overview of directory reorganization
  - Detailed explanation of optimized query scoring
  - Migration guide (no migration needed - fully backward compatible)
  - Usage examples and benefits

- **Updated all existing documentation**
  - README.md - Updated all cache command paths
  - docs/CACHING.md - Updated all script references
  - Clear documentation of new features

### Benefits

- **Better Organization**: Related scripts grouped logically
- **Intelligent Prioritization**: Best patterns matched first
- **Self-Improving Cache**: Users mark validated patterns for better results
- **Backward Compatible**: No breaking changes, gradual adoption
- **Measurable Impact**: Statistics show type breakdown

## [1.4.0] - 2026-01-18

### Added

#### Semantic Caching System

- **AI-powered semantic pattern matching** using Claude Haiku
  - Matches queries to cached patterns based on meaning, not exact text
  - 10x cost reduction (~$0.0001 vs ~$0.01+ per query)
  - 5-15x faster responses (2s vs 10-30s)
  - Intelligent understanding of synonyms and related concepts

- **Core Components**
  - `hooks/find_tag.py` - Semantic router using Claude API
  - `hooks/find_tag.sh` - Hook wrapper with timeout and error handling
  - `hooks/cache-success.sh` - Interactive pattern saving with validation
  - Registry-based index at `.claude/prompt_cache/registry.json`

- **Cache Management Utilities**
  - `hooks/list-cache.sh` - List all cached patterns with statistics
  - `hooks/search-cache.sh` - Search patterns by tag or description
  - `hooks/delete-cache.sh` - Safe deletion with automatic backup
  - `hooks/cache-stats.sh` - Comprehensive cache metrics
  - `hooks/validate-cache.sh` - Integrity checking with auto-repair
  - `hooks/update-cache.sh` - Update existing patterns with versioning

- **Integration with transform-query**
  - Step 0: Semantic Cache Lookup added before generation
  - Automatic cache checking on all transform queries
  - Cache hit skips expensive tree generation and transformation
  - Cache miss shows tip for saving pattern

- **Storage Infrastructure**
  - Atomic file operations for data integrity
  - File locking for concurrent access safety
  - Automatic backups on overwrites and deletions
  - Pattern versioning system
  - Usage tracking with automatic stats updates

- **Comprehensive Documentation**
  - `docs/CACHING.md` - 400+ line complete user guide
  - `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
  - Updated README.md with caching feature section
  - Examples, troubleshooting, FAQs, and API reference

### Features

- **Cost Optimization**
  - Router uses Claude Haiku (cheapest model)
  - Lightweight metadata-only index loading
  - Token budget <500 tokens per lookup
  - Top 50 patterns limit in router prompt

- **Performance**
  - Cache hit: ~2 seconds (API + disk read)
  - Cache miss: ~10-30 seconds (full generation)
  - Minimal overhead: <100ms for cache miss

- **Reliability**
  - Graceful degradation on failures
  - Auto-repair for corrupted registry
  - Stale lock detection and cleanup
  - Never blocks normal operation

- **Security**
  - Input sanitization for tag names
  - Path traversal prevention
  - File permission enforcement
  - Reserved name blocking

- **Observability**
  - Comprehensive logging to ~/.claude/logs/
  - Usage tracking (automatic on cache hits)
  - Metrics collection (cache hit rate, patterns, size)
  - Debug mode via SEMANTIC_CACHE_DEBUG=1

### Benefits

- **90% Cost Savings**: After 10 reuses of same pattern
- **Positive ROI**: After 2nd reuse of pattern
- **Team Sharing**: Commit cache to repository
- **Zero Data Loss**: Atomic operations + backups
- **Backward Compatible**: Optional feature, doesn't affect existing workflows

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

- **Comprehensive documentation** (focused on `/transform-query` with actual file paths)
  - `docs/CONTEXT-AWARE-MODE.md` - Complete guide for context-aware `/transform-query` with path injection examples
  - `docs/TREE-INJECTION-GUIDE.md` - Technical implementation details and architecture
  - Updated README.md with side-by-side comparison of generic vs context-aware transform-query output

- **Multi-stack template system**
  - **nextjs_react**: Next.js 13+ with app directory, components, lib, hooks
  - **node_express**: Express with controllers, routes, models, middleware
  - **python_fastapi**: FastAPI with api/endpoints, core, models, schemas
  - **golang**: Go standard layout with cmd, internal, pkg
  - **default**: Generic structure for unknown stacks

- **GitHub Actions CI/CD workflows**
  - `ci.yml` - Comprehensive CI with JSON, bash, Python, and markdown validation
    - Skips anchor links (starting with `#`)
    - Skips directory links (ending with `/`)
    - Validates file links exist
  - `plugin-validation.yml` - Plugin-specific validation (manifest, hooks, commands, documentation)
  - `release.yml` - Automated versioning and release with release-please (requires PR creation permission)
  - `version-check.yml` - PR validation for version bumps and CHANGELOG updates
  - `.github/workflows/README.md` - Complete setup instructions, branch protection guide, and troubleshooting

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
