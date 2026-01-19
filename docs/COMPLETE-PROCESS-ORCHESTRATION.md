# Complete Process Orchestration

Automate the entire transformation pipeline with a single command. Instead of manually running transform → validate → optimize, the Complete Process Orchestrator handles everything automatically with intelligent error recovery and progress tracking.

## Overview

The Complete Process Orchestrator (introduced in v1.6.0, enhanced in v1.6.1) streamlines the pseudo-code transformation workflow by automating all steps in a single command.

**The Problem**: Running `/transform-query`, `/validate-requirements`, and `/optimize-prompt` separately is tedious and error-prone.

**The Solution**: One command that orchestrates the entire workflow with two modes.

## Workflow Modes

### Quick Mode (5-15s)

- **Transform only**
- Best for simple queries and rapid iteration
- Perfect for prototyping
- Minimal validation

### Complete Mode (30-90s) - Recommended

- **Transform → Validate → Optimize**
- Production-ready output with full validation
- Includes error handling, security, and edge cases
- Comprehensive quality assurance

## Usage Example

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

## Key Features (v1.6.1)

### 1. Mandatory Skill Tool Invocation

The orchestrator now **enforces** proper skill invocation patterns:

- ✅ Always uses Skill tool for sub-skill invocations (`prompt-structurer`, `requirement-validator`, `prompt-optimizer`)
- ✅ Prevents direct handling of transformations for consistency
- ✅ Ensures proper separation of concerns in the pipeline
- ✅ Clear examples of correct vs incorrect patterns in documentation

### 2. Context Window Optimization (60-80% Token Reduction)

**Massive efficiency improvement** - the orchestrator now intelligently removes intermediate outputs:

**Before (v1.6.0)**:

```
User Query (500 tokens)
→ Transform Output (800 tokens) ← KEPT
→ Validate Input (800 tokens) ← KEPT (duplicate)
→ Validate Output (600 tokens) ← KEPT
→ Optimize Input (600 tokens) ← KEPT (duplicate)
→ Optimize Output (900 tokens) ← KEPT

Total Context: 4,200 tokens
```

**After (v1.6.1)**:

```
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

### 3. Context-Aware Tree Injection Integration

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

## Core Features

### Mode Selection

Choose quick or complete based on your needs:
- Quick mode for rapid prototyping
- Complete mode for production-ready output

### Progress Tracking

Real-time visibility into pipeline execution:
- Step-by-step progress indicators
- Duration tracking for each step
- Clear completion status

### Error Recovery

Automatic rollback and checkpoint recovery:
- Preserves work on failures
- Easy retry from checkpoints
- Graceful degradation

### Preference Persistence

Remembers your mode choice:
- Saves preference to `.claude/plugin_preferences.json`
- Auto-selects your preferred mode next time
- Can be changed anytime

### Timeout Protection

Graceful handling with partial results:
- Configurable timeouts per step
- Returns partial results if timeout occurs
- Prevents hanging on slow operations

### State Management

Preserves work on failures:
- Checkpoint system for recovery
- State file in `.claude/` directory
- Easy resume from last successful step

## Benefits

- ✅ **Streamlined Workflow**: One command instead of three
- ✅ **Intelligent Automation**: Full validation and optimization automatically
- ✅ **Error Resilience**: Recovers from failures gracefully
- ✅ **Time Savings**: 50% faster than manual steps
- ✅ **Quality Assurance**: Complete mode ensures production-ready output
- ✅ **Context Efficiency**: 60-80% reduction in token usage (v1.6.1)
- ✅ **Project-Aware**: Automatically includes actual file paths (v1.6.1)

## Available Commands

The orchestrator can be invoked with multiple aliases:

- `/complete-process` (primary)
- `/complete` (alias)
- `/full-transform` (alias)
- `/orchestrate` (alias)

## Technical Details

### Version History

- **v1.0.0**: Initial release with basic orchestration
- **v1.1.0** (Plugin v1.6.1): Added context window optimization, mandatory skill invocation, context-aware tree injection

### Location

- **Skill**: [skills/complete-process-orchestrator/SKILL.md](../skills/complete-process-orchestrator/SKILL.md)
- **Capabilities**: [skills/complete-process-orchestrator/capabilities.json](../skills/complete-process-orchestrator/capabilities.json)

### Features Provided

- `workflow_orchestration`
- `mode_selection`
- `progress_tracking`
- `error_recovery`
- `preference_persistence`
- `context_window_optimization` (v1.1.0)
- `context_aware_tree_injection` (v1.1.0)
- `mandatory_skill_tool_invocation` (v1.1.0)

## Usage Patterns

### For Quick Iteration

```bash
/complete-process "add dark mode toggle"
# Select: Quick Transform Only
# Duration: ~8 seconds
# Output: Basic pseudo-code transformation
```

### For Production Features

```bash
/complete-process "implement payment processing with Stripe"
# Select: Complete Process (Recommended)
# Duration: ~45 seconds
# Output: Validated, optimized, production-ready pseudo-code
```

### For Context-Aware Results

```bash
# Use implementation keywords
/complete-process "implement user authentication"
# Automatically activates context-aware mode
# Output includes actual file paths from your project
```

## Related Documentation

- [Context-Aware Mode Guide](CONTEXT-AWARE-MODE.md) - Project structure analysis
- [Tree Injection Technical Guide](TREE-INJECTION-GUIDE.md) - How PROJECT_TREE works
- [Complete Process Skill Documentation](../skills/complete-process-orchestrator/SKILL.md) - Detailed implementation
- [Ralph Loop Integration](RALPH-LOOP-INTEGRATION.md) - Automated implementation with Ralph

## Support

For issues or questions:
- Check the [main plugin README](../README.md)
- Review the [PROMPTCONVERTER documentation](../../PROMPTCONVERTER.md)
- See the [skill documentation](../skills/complete-process-orchestrator/SKILL.md)
