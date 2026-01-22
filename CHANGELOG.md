# Changelog

All notable changes to the Pseudo-Code Prompting Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.4] - 2026-01-21

### Added

#### Fully Automated Workflow System

- **Automated Agent Chaining Protocol** - Complete-process workflow now runs Transform → Validate → Optimize continuously without user intervention
- **Structured Agent Communication** - Each agent outputs workflow signals (`WORKFLOW_CONTINUES`, `NEXT_AGENT`, `CHAIN_PROGRESS`)
- **Chain Execution Loop** - Orchestrator automatically invokes next agent based on output signals
- **Automatic TODO Generation** - Implementation tasks automatically extracted from optimized pseudo-code parameters
- **TodoWrite Integration** - Orchestrator creates actual todos after optimization completes

### Changed

#### Complete-Process Orchestrator

- **BREAKING**: Workflow now fully automated - no stops between Transform/Validate/Optimize steps
- Changed agent invocation from `Skill` tool to `Task` tool for proper agent execution
- Updated orchestrator to check agent outputs for `NEXT_AGENT` signal and invoke immediately
- Final output now includes only optimized pseudo-code + generated todos (no intermediate steps)

#### Agent Output Formats

- **prompt-transformer.md** - Added `WORKFLOW_CONTINUES: YES` and `NEXT_AGENT: requirement-validator` to output
- **requirement-validator.md** - Added `WORKFLOW_CONTINUES: YES` and `NEXT_AGENT: prompt-optimizer` to output
- **prompt-optimizer.md** - Added `WORKFLOW_CONTINUES: NO`, `TODO_LIST`, and `CHAIN_COMPLETE` to output

### Enhanced

#### Documentation

- **Documentation Restructure** - Complete overhaul for user-friendliness

  **Deleted Old Documentation:**
  - Removed all 17 existing markdown files from docs/ directory
  - Removed verbose, overlapping documentation structure

  **New Command Documentation (6 files - 1-minute reads):**
  - [docs/complete-process.md](docs/complete-process.md) - Full pipeline automation
  - [docs/compress-context.md](docs/compress-context.md) - Token reduction (80-95%)
  - [docs/context-aware-transform.md](docs/context-aware-transform.md) - Architecture-aware transformation
  - [docs/optimize-prompt.md](docs/optimize-prompt.md) - Enhancement with security
  - [docs/transform-query.md](docs/transform-query.md) - Basic transformation
  - [docs/validate-requirements.md](docs/validate-requirements.md) - Quality assurance

  **Each Command Doc Includes:**
  - What it does (one sentence)
  - Goal (purpose/problem solved)
  - When to use (concrete scenarios)
  - How to invoke (natural language examples)
  - Workflow diagram (mermaid visualization)
  - Components (agents, hooks, skills)
  - Output example (before/after)
  - "Why use this command" section with compelling benefits

  **New Architecture Documentation:**
  - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete system design (2-minute read)
    - End-to-end flow diagram (mermaid)
    - Component layers (hooks → commands → agents → skills)
    - Data flow sequence diagram
    - Directory structure
    - Performance metrics
    - Design rationale

  **Updated Main README:**
  - Reduced from 384 lines to 216 lines (44% shorter)
  - Clear value proposition upfront
  - Command table with links to individual docs
  - Visual workflow diagram
  - Removed repetitive content
  - Better organization and navigation

  **New Documentation Index:**
  - [docs/README.md](docs/README.md) - Navigation guide
  - Total read time: 8 minutes for complete documentation
  - Clear navigation paths for different user needs

  **Impact:**
  - **50% shorter README** - Easier to scan and understand
  - **1-minute command docs** - Quick reference for each command
  - **Visual workflows** - Mermaid diagrams in every doc
  - **Clear value props** - "Why use this" sections to convince users
  - **Better UX** - Users can become proficient in under 10 minutes
  - **Maintainable** - Single source of truth per command

  **Rationale:**
  The previous documentation was comprehensive but difficult to navigate with 17 separate files and extensive overlap. The new structure provides:
  - Focused, digestible documentation
  - Visual workflows for better understanding
  - Clear use cases and benefits
  - Faster time to value for new users

### Technical Details

The automated workflow is inspired by the cc10x router pattern and implements:

1. **Structured Output Protocol**: Agents communicate via standardized signals
2. **Chain Enforcement**: Orchestrator ensures workflow completes to end
3. **Context Optimization**: Intermediate outputs removed, keeping only final result
4. **Todo Generation**: Parameters become actionable implementation tasks

**Migration Note**: Existing `/complete-process` usage remains the same - the automation happens transparently. The only user-visible change is the elimination of manual "continue" prompts between steps.

## [1.1.3] - 2026-01-21

### Removed

- **Legacy Shell Script Files** (Cleanup from v1.0.10 migration)

  Removed all legacy .sh hook files that were kept as reference after the Python migration in v1.0.10. These files have not been actively used since the migration to Python-based hooks.

  **Deleted Files:**
  - `hooks/compression/context-compression-helper.sh` - Legacy shell hook (replaced by .py in v1.0.10)
  - `hooks/tree/context-aware-tree-injection.sh` - Legacy shell hook (replaced by .py in v1.0.10)
  - `hooks/validation/post-transform-validation.sh` - Legacy shell hook (replaced by .py in v1.0.10)
  - `hooks/core/user-prompt-submit.sh` - Legacy shell hook (replaced by .py in v1.0.10)
  - `create-pr.sh` - Legacy shell script in root directory
  - `check-ci.sh` - Legacy shell script in root directory

  **Impact:**
  - Removes documentation/code debt from v1.0.10 Python migration
  - All hooks remain functional (Python versions already in use)
  - No breaking changes - hooks.json already references .py files only
  - Cleaner repository structure
  - Reinforces cross-platform Python-first approach

## [1.1.2] - 2026-01-21

### Removed

- **Ralph Loop Integration** (Complete removal)

  Removed all Ralph Loop integration functionality to streamline the plugin and focus on core pseudo-code transformation capabilities.

  **Impact:**
  - Commands reduced: 7 → 6 (removed `/ralph-process`)
  - Skills reduced: 9 → 8 (removed ralph-process-integration)
  - Plugin now focuses exclusively on pseudo-code transformation, validation, and optimization
  - No external dependencies on Ralph Loop plugin
  - All core functionality remains intact

## [1.1.1] - 2026-01-21

### Added

- **Session Memory Management System** (Adapted from cc10x)

  Implemented persistent memory management across all agents and skills for pattern learning, user preference retention, and quality improvement over time.

  **New Files:**
  - [skills/session-memory/SKILL.md](skills/session-memory/SKILL.md) - Core memory management skill
  - [skills/session-memory/capabilities.json](skills/session-memory/capabilities.json) - Progressive loading metadata
  - [.claude/pseudo-code-prompting/activeContext.md](.claude/pseudo-code-prompting/activeContext.md) - Current transformations, user preferences
  - [.claude/pseudo-code-prompting/patterns.md](.claude/pseudo-code-prompting/patterns.md) - Learned transformation patterns
  - [.claude/pseudo-code-prompting/progress.md](.claude/pseudo-code-prompting/progress.md) - Quality metrics

  **Updated Configuration:**
  - [plugin.json](plugin.json) - Added `session-memory` and `pattern-learning` keywords, updated to 8 skills
  - [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) - Updated descriptions to mention session memory

  **Impact:**
  - User preferences persist across sessions
  - Pattern learning improves transformation quality over time
  - Domain-specific knowledge retained and reused
  - Quality metrics track improvement
  - Context survives conversation compaction

See full CHANGELOG for complete version history.
