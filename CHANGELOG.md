# Changelog

All notable changes to the Pseudo-Code Prompting Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.9] - 2026-01-19

### Added

- **Enhanced Natural Language Plugin Invocation**: Added hook support for explicit plugin invocation via natural language
  - Now recognizes "Use pseudo-code prompting plugin" patterns
  - Automatically routes to appropriate skill (complete-process or ralph-process)
  - Prevents manual implementation bypass when plugin is explicitly requested

- **UserPromptSubmit Hook Enhancement**: Updated [hooks/core/user-prompt-submit.sh](hooks/core/user-prompt-submit.sh)
  - New pattern matching for explicit plugin requests
  - Injects `<plugin-invocation-detected>` context to enforce skill usage
  - Catches variations: "Use pseudo-code prompting plugin", "Use pseudocode prompting with ralph", "Invoke pseudo-code plugin"
  - Provides clear routing instructions based on Ralph Loop mention

- **Skill Trigger Improvements**:
  - Added `triggers` section to [ralph-process-integration/capabilities.json](skills/ralph-process-integration/capabilities.json)
  - Added `triggers` section to [complete-process-orchestrator/capabilities.json](skills/complete-process-orchestrator/capabilities.json)
  - Defined keywords, patterns, and contexts for better auto-invocation
  - Added `auto_invoke_on` field to specify explicit invocation scenarios

- **Documentation Enhancements**:
  - Added Table of Contents to [README.md](README.md) for easier navigation
  - Moved Installation and Quick Start sections after Overview for better flow
  - Added "💡 Don't Like Commands? Just Talk to Claude!" section with natural language usage instructions
  - Clear guidance: "Use pseudo-code prompting plugin" or "Use pseudo-code prompting plugin with Ralph"

### Changed

- **Hook Priority**: Explicit plugin invocation check now runs before transformation keyword detection
- **User Experience**: Claude now reliably invokes skills when explicitly requested by name
- **Metadata**: Updated `complete-process-orchestrator/capabilities.json` updated date to 2026-01-19

### Fixed

- **Critical Bug**: Fixed issue where Claude would bypass plugin skills when user explicitly requested plugin usage
- **Pattern Matching**: Hook now correctly identifies natural language plugin invocation requests
- **Skill Routing**: Ensures proper skill selection based on user intent (with/without Ralph)

### Technical Details

**New Hook Pattern:**
```bash
if [[ "$PROMPT" =~ [Uu]se.*(pseudo.*code.*prompting|pseudocode.*prompting).*(plugin|with.*ralph|with.*Ralph) ]] || \
   [[ "$PROMPT" =~ [Ii]nvoke.*(pseudo|pseudocode).*(plugin|workflow) ]]; then
```

**Injected Context:**
- `<plugin-invocation-detected>` tag with CRITICAL priority
- Explicit Skill tool invocation instructions
- DO NOT bypass rules to prevent manual implementation
- Clear routing logic based on Ralph Loop mention

**Pattern Coverage:**
- "Use pseudo-code prompting plugin" → complete-process
- "Use pseudo-code prompting plugin with Ralph" → ralph-process
- "Use pseudocode prompting with ralph" → ralph-process
- "Invoke pseudo-code plugin" → complete-process
- "Invoke pseudocode workflow" → complete-process

## [1.0.8] - 2026-01-19

### Added

- **New `/ralph-process` Command**: End-to-end automated workflow that integrates pseudo-code processing with Ralph Loop for iterative implementation
  - Automatically runs complete-process pipeline (transform → validate → optimize)
  - Analyzes validation report to estimate complexity and iteration requirements
  - Generates specific completion promises from validation requirements
  - Launches Ralph Loop with optimized parameters

- **New Skill: ralph-process-integration**
  - Complexity estimation algorithm based on validation report metrics
  - Automatic promise generation from critical requirements
  - Intelligent iteration planning (20/40/80 based on complexity score)
  - Comprehensive error handling and fallback strategies
  - Detailed progress reporting at each step

- **Reference Documentation**
  - [complexity-scoring.md](pseudo-code-prompting-plugin/skills/ralph-process-integration/references/complexity-scoring.md) - Detailed scoring algorithm with calibration examples
  - [promise-generation.md](pseudo-code-prompting-plugin/skills/ralph-process-integration/references/promise-generation.md) - Promise creation patterns and best practices

- **Templates**
  - [ralph-prompt-template.md](pseudo-code-prompting-plugin/skills/ralph-process-integration/templates/ralph-prompt-template.md) - Template for constructing Ralph Loop prompts

### Changed

- **Plugin Version**: Bumped from 1.6.1 to 1.7.0
- **Skill Count**: Increased from 7 to 8 skills
- **Command Count**: Increased from 6 to 7 commands
- **Description**: Updated to mention Ralph Loop integration and automated iterative development

### Dependencies

- Now integrates with **ralph-loop** (official Claude plugin)
- Requires **complete-process-orchestrator** v1.1.0+ for query optimization

### Technical Details

**Complexity Scoring Formula:**
```
base_score = (warnings × 2) + (critical × 5) + (edge_cases × 3)
modifiers = +10 (security) + 5 (error handling) - 5 (well-defined)
```

**Classification:**
- Simple (0-25): 20 iterations
- Medium (26-60): 40 iterations
- Complex (61+): 80 iterations

**Promise Generation:**
- Extracts critical requirements from validation report
- Converts negative issues to positive requirements
- Formats as specific testable criteria
- Falls back to generic when requirements unclear

## [1.6.1] - Previous Release

### Added
- Context window optimization (60-80% token reduction)
- Mandatory skill tool invocation enforcement
- Context-aware tree injection for transform-query

### Changed
- Complete-process orchestrator improvements
- Enhanced efficiency and accuracy

---

## Future Enhancements

Potential improvements for v2.x:

### Ralph Integration Enhancements
- Adaptive iteration estimates based on historical data
- Mid-loop progress monitoring
- Partial completion detection with sub-promises
- Complexity tuning via user configuration

### Machine Learning Features
- ML-based complexity scoring
- Learning from user feedback
- Project-specific calibration
- Automatic weight adjustment

### Workflow Improvements
- Multi-phase promise support
- Integration with feature-dev phases
- Custom promise templates
- Workflow branching based on complexity

---

## Version History

| Version | Date | Major Changes |
|---------|------|---------------|
| 1.0.8 | 2026-01-19 | Ralph Loop integration, complexity estimation, promise generation |
| 1.0.7 | Previous | Context window optimization, mandatory skill invocation |
| 1.0.6 | Previous | Complete-process orchestrator |
| 1.0.5 | Previous | Progressive loading |
| 1.0.4 | Previous | Security validation |
| 1.0.3 | Previous | Context-aware transform-query |
| 1.0.2 | Previous | Hooks and automation |
| 1.0.1 | Previous | Additional skills and agents |
| 1.0.0 | Initial | Core prompt structuring functionality |

---

## Migration Guide

### From 1.0.7 to 1.0.8

**No breaking changes** - all existing functionality preserved.

**New Features Available:**
```bash
# Use the new ralph-process command
/ralph-process "Your implementation request"

# Still works - existing commands unchanged
/complete-process "Your query"
/transform-query "Your query"
```

**What's Different:**
- If you have ralph-loop installed, you can now use `/ralph-process` for automated implementation
- All existing skills and commands work exactly as before
- No configuration changes needed

**Recommended Workflow:**
1. For optimization only: Continue using `/complete-process`
2. For automated implementation: Try `/ralph-process`
3. For manual control: Use `/complete-process` then `/ralph-loop` separately

---

## Support

For issues, questions, or contributions:
- GitHub Repository: [pseudo-code-prompting-plugin](https://github.com/EladAriel/pseudo-code-prompting-plugin)
- Documentation: [PROMPTCONVERTER.md](PROMPTCONVERTER.md)
- Ralph Integration: [skills/ralph-process-integration/README.md](pseudo-code-prompting-plugin/skills/ralph-process-integration/README.md)
