# Complete Process Orchestrator

Orchestrate end-to-end pseudo-code transformation workflows with automated validation and optimization.

## Purpose

The Complete Process Orchestrator skill provides an automated pipeline that combines transformation, validation, and optimization into a seamless workflow. Instead of invoking each step separately, users can choose between a quick transformation or a complete process that handles everything automatically.

## CRITICAL IMPLEMENTATION REQUIREMENTS

### 1. Always Use Skill Tool for Sub-Skills

**MANDATORY**: When executing transformation, validation, or optimization steps, you MUST use the Skill tool to invoke the respective skills. NEVER handle these directly or inline.

```text
❌ WRONG: Directly transforming the query yourself
✅ CORRECT: Use Skill tool with skill="pseudo-code-prompting:prompt-structurer"

❌ WRONG: Directly validating yourself
✅ CORRECT: Use Skill tool with skill="pseudo-code-prompting:requirement-validator"

❌ WRONG: Directly optimizing yourself
✅ CORRECT: Use Skill tool with skill="pseudo-code-prompting:prompt-optimizer"
```

### 2. Context Window Optimization (MANDATORY)

To minimize token usage, you MUST remove intermediate outputs from the conversation flow:

**Keep Only**:

- Original user query (input)
- Final optimized output

**Remove/Don't Store**:

- Transform step output (intermediate)
- Validate step input (redundant with transform output)
- Validate step output (intermediate)
- Optimize step input (redundant with validate output)

**Implementation**: After each step completes, extract only the essential result and pass it to the next step WITHOUT including full tool outputs in subsequent messages.

### 3. Context-Aware Tree Injection (MANDATORY)

Before invoking the transform step, you MUST ensure the context-aware tree injection occurs:

**Process**:

1. Check if user query contains implementation keywords: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`
2. If keywords detected, the UserPromptSubmit hook should have already injected PROJECT_TREE context
3. When invoking prompt-structurer skill, include any PROJECT_TREE context that was injected
4. This enables context-aware transformation with actual file paths from the project

**Why This Matters**: Without PROJECT_TREE context, transformations will be generic instead of project-specific.

## Execution Workflow

### Quick Mode Execution

1. **Validate Input**: Check query length (10-5000 characters)
2. **Invoke Transform Skill**:
   - Use: `Skill tool with skill="pseudo-code-prompting:prompt-structurer" args="[user query]"`
   - Extract ONLY the transformed output
3. **Return Result**: Output the transformed pseudo-code
4. **Clean Up**: Do NOT keep the transform tool output in context

### Complete Mode Execution

1. **Validate Input**: Check query length (10-5000 characters)
2. **Step 1/3: Transform**
   - Use: `Skill tool with skill="pseudo-code-prompting:prompt-structurer" args="[user query]"`
   - Extract: `transformed_output` (single variable)
   - Clean: Remove full tool output from context
3. **Step 2/3: Validate**
   - Use: `Skill tool with skill="pseudo-code-prompting:requirement-validator" args="[transformed_output]"`
   - Extract: `validation_report` (single variable)
   - Clean: Remove full tool output AND transformed_output from context
4. **Step 3/3: Optimize**
   - Use: `Skill tool with skill="pseudo-code-prompting:prompt-optimizer" args="[transformed_output]"`
   - Extract: `optimized_output` (final result)
   - Clean: Remove full tool output from context
5. **Return Result**: Output optimized pseudo-code + validation report + optimization summary
6. **Final Context**: Keep ONLY original query + final outputs

**Token Savings**: By removing intermediate outputs, you save approximately 60-80% of context window usage.

## Context-Aware Detection and Tree Injection

### Automatic Hook Execution

Before this skill executes, the **UserPromptSubmit** hook automatically runs and checks the user's query for implementation keywords:

**Keywords**: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`

If ANY of these keywords are detected, the hook:

1. Generates a project structure tree using `get_context_tree.py`
2. Injects the tree into the conversation context with `[CONTEXT-AWARE MODE ACTIVATED]` marker
3. Provides guidance on using the project structure for transformation

### Checking for Context Injection

At the start of execution, check if the conversation context contains:

```text
[CONTEXT-AWARE MODE ACTIVATED]

Project Structure:
```
(project tree)
```

Use this project structure as context for the request: "..."
```

**If Found**: The PROJECT_TREE context is available. Pass this context when invoking the prompt-structurer skill.

**If Not Found**: Either:

- Query didn't contain implementation keywords (no tree needed)
- Hook failed to execute (graceful degradation)
- Project is empty (tree generation skipped)

### Using Context During Transformation

When PROJECT_TREE context is available, you MUST pass it to the transform skill:

```text
Skill tool with skill="pseudo-code-prompting:prompt-structurer"
args="[user query]

PROJECT_TREE:
[tree structure from context]
"
```

This ensures the transformation includes project-specific file paths and architecture-aware suggestions.

### Context-Aware Troubleshooting

**Context not appearing?**

1. Check if query contains implementation keywords
2. Verify hook is configured in `hooks/hooks.json`
3. Check if Python is installed (`python3 --version`)
4. Verify script exists: `hooks/tree/get_context_tree.py`

**Empty project tree?**

The hook gracefully skips tree injection for empty projects and returns `<<PROJECT_EMPTY_NO_STRUCTURE>>`.

## When to Use

Use this skill when:
- You want an end-to-end workflow from natural language to optimized pseudo-code
- You need production-ready pseudo-code with validation and optimization
- You want to streamline repetitive transform → validate → optimize cycles
- You prefer automated workflows over manual step execution
- You're implementing complex features that benefit from full validation

## Workflow Modes

### Quick Mode (Fast)
**Duration**: 5-15 seconds
**Steps**: Transform only
**Output**: Raw pseudo-code

**Best For**:
- Simple queries and rapid prototyping
- Exploratory work and experimentation
- When you already know the requirements are clear
- Quick syntax conversion without validation

**Example Use Cases**:
- "Add a logout button"
- "Create a helper function for date formatting"
- "Update button color to blue"

### Complete Mode (Recommended)
**Duration**: 30-90 seconds
**Steps**: Transform → Validate → Optimize
**Output**: Optimized pseudo-code with validation report

**Best For**:
- Production feature implementation
- Complex requirements with multiple parameters
- When you need comprehensive validation
- Features requiring security, error handling, or edge case coverage
- Team environments where quality standards matter

**Example Use Cases**:
- "Implement user authentication with OAuth"
- "Create a payment processing endpoint"
- "Add file upload with validation and virus scanning"
- "Build a real-time notification system"

## How It Works

### Mode Selection
When you invoke the orchestrator, you'll be prompted:

```
Choose transformation workflow:

○ Quick Transform Only
  Transform to pseudo-code only (5-15s, best for simple queries)

● Complete Process (Recommended)
  Transform → Validate → Optimize (30-90s, production-ready output)
```

Your preference is remembered for future invocations but can always be changed.

### Pipeline Execution

#### Quick Mode Flow
```
User Query → Input Validation → Transform → Output
```

#### Complete Mode Flow

```text
User Query → Input Validation → Transform → Validate → Optimize → Output
                                     ↓          ↓          ↓
                              Progress     Progress    Progress
                              Step 1/3     Step 2/3    Step 3/3
```

**Important**: The UserPromptSubmit hook automatically injects PROJECT_TREE context BEFORE this skill executes if the query contains implementation keywords (`implement`, `create`, `add`, etc.). This context is available during the Transform step for context-aware pseudo-code generation.

### Progress Tracking

During complete mode execution, you'll see real-time progress:

```
Step 1/3: 🔄 Transforming query to pseudo-code...
Step 2/3: ✓ Validating requirements...
Step 3/3: ⚡ Optimizing for implementation...

✓ Pipeline complete! Review output below.
```

## Features

### Input Validation
- Validates query length (10-5000 characters)
- Rejects empty or whitespace-only queries
- Sanitizes input for security
- Provides clear error messages for invalid input

### Error Handling & Recovery
- **Graceful Degradation**: If validation fails, you can skip to optimization
- **Rollback Support**: Failed steps preserve previous successful output
- **Checkpoint Recovery**: Resume from failure point
- **Partial Results**: Get what completed successfully even if pipeline fails

### State Management
- Preserves intermediate results between steps
- Allows step retry without re-running entire pipeline
- Maintains context across failure and recovery

### Preference Persistence
- Remembers your last mode choice
- Shows your preferred mode on next invocation
- Stores preferences globally in `.claude/plugin_preferences.json`
- Can override saved preference at any time

### Timeout Protection
- Transform step: 30 seconds
- Validate step: 15 seconds
- Optimize step: 45 seconds
- Total pipeline: 120 seconds (2 minutes)
- Warns at 80% of timeout threshold
- Returns partial results on timeout

## Output Format

### Quick Mode Output
```
Transformed: function_name(
  param1="value1",
  param2="value2",
  ...
)
```

### Complete Mode Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

implement_feature(
  // Fully optimized parameters with validation,
  // error handling, security, and edge cases
  ...
)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ PASSED CHECKS
- [checks that passed]

⚠ WARNINGS
- [warnings found]

✗ CRITICAL ISSUES (if any)
- [critical issues]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Improvements Made:
✓ Security
  - [security enhancements]
✓ Error Handling
  - [error handling added]
✓ Performance
  - [performance optimizations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration: 42s
Steps Completed: 3/3
Issues Found: 2 warnings (resolved)
```

## Examples

### Example 1: Simple Feature (Quick Mode)

**Input Query**:
```
Add a dark mode toggle to the settings page
```

**Mode Selection**: Quick Transform Only

**Output** (5 seconds):
```
Transformed: add_dark_mode_toggle(
  location="settings_page",
  component_type="toggle_switch",
  persistence="local_storage"
)
```

---

### Example 2: Complex Feature (Complete Mode)

**Input Query**:
```
Implement user authentication with JWT tokens
```

**Mode Selection**: Complete Process (Recommended)

**Progress**:
```
Step 1/3: 🔄 Transforming query to pseudo-code...
Step 2/3: ✓ Validating requirements...
Step 3/3: ⚡ Optimizing for implementation...
```

**Output** (45 seconds):
```
Optimized: implement_authentication(
  type="jwt",
  token_ttl="1h",
  refresh_token=true,
  refresh_token_ttl="30d",
  hashing="bcrypt",
  auth_endpoint="/api/auth/login",
  refresh_endpoint="/api/auth/refresh",
  logout_endpoint="/api/auth/logout",

  request_schema={
    "email": "email:required",
    "password": "string:required:min(8)"
  },

  response_format={
    "access_token": "jwt",
    "refresh_token": "string",
    "expires_in": "number",
    "user": {"id": "string", "email": "string"}
  },

  security={
    "rate_limiting": "5_attempts_per_15min",
    "lockout_duration": "15m",
    "secure_cookies": true,
    "httponly": true,
    "same_site": "strict"
  },

  error_handling={
    "invalid_credentials": "return_401",
    "expired_token": "return_403_with_refresh_prompt",
    "server_error": "log_and_return_500"
  },

  validation={
    "email_format": "RFC5322",
    "password_strength": "min_8_chars_with_requirements"
  }
)

Validation Report: ✓ All checks passed
Optimization Summary: Added security, error handling, and validation
```

---

### Example 3: Pipeline Recovery

**Scenario**: Validation fails but user wants to continue

```
Step 1/3: 🔄 Transforming query to pseudo-code... ✓
Step 2/3: ✓ Validating requirements... ⚠ Issues found

Validation found 3 warnings:
- Missing error handling specification
- No timeout values defined
- Performance constraints not specified

Continue to optimization anyway? (Y/n): y

Step 3/3: ⚡ Optimizing for implementation... ✓

✓ Pipeline complete! Warnings were addressed during optimization.
```

## Error Handling

### Transform Failure
```
❌ Transformation failed: Query too ambiguous

Original query preserved. Suggestions:
- Rephrase with more specific details
- Try breaking into smaller queries
- Switch to quick mode and iterate
```

### Validation Failure (Non-Critical)
```
⚠ Validation found issues

You can:
1. Continue to optimization (recommended - may fix issues)
2. Return validation report and revise query
3. Return transformed pseudo-code as-is

Choice: _
```

### Optimization Failure
```
❌ Optimization failed: Unable to enhance pseudo-code

Returning validated pseudo-code instead. You can:
- Use the validated output (still production-ready)
- Manually optimize using /optimize-prompt command
- Retry the complete process
```

### Timeout Warning
```
⚠ Step taking longer than expected (24s / 30s)
Processing continues... Results will be returned when complete.
```

## Edge Cases Handled

### Concurrent Invocations
If you invoke the orchestrator while another is running, new requests are queued automatically.

### Very Large Queries
Queries over 3000 characters trigger a suggestion:
```
ℹ️ Large query detected (3547 characters)

Consider using /compress-context first for better results.
Proceed anyway? (y/N): _
```

### Partial Skill Availability
If dependent skills are unavailable:
```
⚠ requirement-validator skill unavailable

Falling back to: Transform → Optimize (validation skipped)
Continue? (Y/n): _
```

### User Cancellation
Press Ctrl+C to cancel during execution:
```
⚠ Pipeline cancelled by user

Progress saved:
✓ Transform completed
✓ Validation completed
⏸ Optimization not started

Resume later with /resume-pipeline? (saved to .claude/pipeline_state.json)
```

## Integration with Other Skills

### Used By Complete Process Orchestrator
- **prompt-structurer**: Performs transformation step
- **requirement-validator**: Performs validation step
- **prompt-optimizer**: Performs optimization step

### Complements
- **compress-context**: Use before orchestrator for large requirements
- **feature-dev-enhancement**: Use orchestrator output with /feature-dev
- **context-aware-transform**: Orchestrator leverages project context automatically

### Semantic Cache Integration
The orchestrator integrates with the semantic cache system:
- Quick mode checks cache before transformation
- Complete mode caches final optimized output
- Cache hits skip entire pipeline (< 1 second)

## Best Practices

### When to Choose Quick Mode
✓ Simple, well-defined queries
✓ Rapid prototyping and iteration
✓ Non-critical features
✓ Learning and experimentation

### When to Choose Complete Mode
✓ Production features
✓ Security-sensitive implementations
✓ Complex multi-parameter features
✓ Features requiring validation/testing
✓ Team environments with quality standards

### Workflow Tips
1. **Start with Complete Mode** for important features - it catches issues early
2. **Use Quick Mode for iteration** - refine your query quickly
3. **Review validation reports** - they teach you what makes good pseudo-code
4. **Save preferences** - let the orchestrator remember your preference
5. **Leverage cache** - repeated queries return instantly

### Query Writing Tips
- **Be specific**: "Add OAuth authentication" → "Implement OAuth 2.0 authentication with Google provider"
- **Include constraints**: Mention performance, security, or scale requirements
- **Specify integration points**: Name files, components, or services to integrate with
- **Provide context**: Reference existing patterns or architectures

## Troubleshooting

### "Query must be between 10-5000 characters"
**Solution**: Ensure query has meaningful content, not just spaces. For very large requirements, use `/compress-context` first.

### "Transformation failed: Query too ambiguous"
**Solution**: Add more specific details. Example:
- Before: "Add notifications"
- After: "Implement email and push notifications for new messages with SendGrid"

### "Pipeline timeout exceeded"
**Solution**:
- Break complex queries into smaller parts
- Use `/compress-context` for verbose requirements
- Check network connection

### "Skill unavailable: requirement-validator"
**Solution**: Plugin may be partially loaded. Restart Claude Code or use individual commands (`/transform-query`, `/validate-requirements`, `/optimize-prompt`).

### Pipeline stuck at a step
**Solution**: Wait for timeout warning. If no progress after 2 minutes, cancel (Ctrl+C) and retry with quick mode.

## Configuration

### Preference Storage
Preferences are stored in `.claude/plugin_preferences.json`:

```json
{
  "complete-process-orchestrator": {
    "preferred_mode": "complete",
    "show_progress": true,
    "auto_optimize": true,
    "last_updated": "2026-01-18T12:00:00Z"
  }
}
```

### Metrics Collection
Anonymous metrics are collected in `.claude/plugin_metrics.json`:

```json
{
  "complete-process-orchestrator": {
    "total_invocations": 42,
    "quick_mode_count": 12,
    "complete_mode_count": 30,
    "average_duration_quick": "8s",
    "average_duration_complete": "45s",
    "success_rate": 0.95
  }
}
```

## Command Aliases

You can invoke the orchestrator using any of these commands:
- `/complete-process` (primary)
- `/complete`
- `/full-transform`
- `/orchestrate`

## Technical Details

### Pipeline Architecture
```
┌─────────────────────────────────────────┐
│         Mode Selection (UI)             │
│   AskUserQuestion with preference hint  │
└────────────┬────────────────────────────┘
             │
             ├─→ Quick Mode
             │   └─→ Transform → Output
             │
             └─→ Complete Mode
                 └─→ Transform
                     ├─→ Checkpoint
                     └─→ Validate
                         ├─→ Checkpoint
                         └─→ Optimize
                             ├─→ Checkpoint
                             └─→ Output
```

### State Management
- **In-Memory**: Intermediate results passed directly between steps
- **Checkpoints**: Saved after each successful step
- **Recovery**: Can resume from last checkpoint on failure

### Dependency Graph
```
complete-process-orchestrator
    ├── prompt-structurer (transform step)
    ├── requirement-validator (validate step)
    └── prompt-optimizer (optimize step)
```

## Success Criteria

A successful orchestration includes:
- ✓ Valid input query accepted
- ✓ Mode selected (or preference loaded)
- ✓ All selected steps completed
- ✓ Progress tracked and displayed
- ✓ Output returned in expected format
- ✓ Preference saved for next time
- ✓ Metrics recorded

## Version History

- **1.0.0** (2026-01-18): Initial release with quick and complete modes

## Related Commands

- `/transform-query` - Transform only (equivalent to quick mode)
- `/validate-requirements` - Validate pseudo-code
- `/optimize-prompt` - Optimize pseudo-code
- `/compress-context` - Compress verbose requirements before orchestration
- `/feature-dev` - Use orchestrator output for feature development

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review [Examples](#examples) for common patterns
- See related commands for manual step execution
- Report issues at plugin repository
