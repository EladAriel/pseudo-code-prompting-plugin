---
description: Orchestrate end-to-end pseudo-code transformation with automated validation and optimization
argument-hint: [query]
---

# Complete Process Command

Orchestrate end-to-end pseudo-code transformation with automated validation and optimization.

## Command

`/complete-process` (aliases: `/complete`, `/full-transform`, `/orchestrate`)

## Description

The complete-process command provides an orchestrated workflow that automates the entire transformation pipeline. Instead of manually invoking `/transform-query`, `/validate-requirements`, and `/optimize-prompt` separately, this command handles everything in one streamlined operation.

## What's New in v1.6.1

The complete-process orchestrator has been significantly enhanced with three critical improvements:

### 1. Mandatory Skill Tool Invocation

The orchestrator now **always** uses the Skill tool for sub-skill invocations instead of handling transformations directly. This ensures:

- Consistent execution patterns
- Proper separation of concerns
- Reliable pipeline behavior

### 2. Context Window Optimization (60-80% Token Reduction)

**Major efficiency improvement** - the orchestrator now removes intermediate outputs from the conversation context:

- **Keeps**: Original query + Final optimized output
- **Removes**: All intermediate transform/validate/optimize outputs
- **Result**: 60-80% reduction in context window usage

This enables longer conversations, reduces costs, and improves performance.

### 3. Context-Aware Tree Injection

The orchestrator now automatically leverages PROJECT_TREE context when implementation keywords are detected (`implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`). This results in project-specific, architecture-aware transformations with actual file paths from your codebase.

**Learn more**: [Complete Process Orchestrator SKILL.md](../skills/complete-process-orchestrator/SKILL.md)

## Usage

### Basic Usage
```
/complete-process <your query here>
```

### With Query Argument
```
/complete-process Implement user authentication with JWT tokens
```

### Interactive Mode (No Arguments)
```
/complete-process
> Enter your query: _
```

## How It Works

### 1. Mode Selection

When invoked, you'll choose between two workflow modes:

**Quick Transform Only**
- Duration: 5-15 seconds
- Steps: Transform only
- Output: Raw pseudo-code
- Best for: Simple queries, rapid iteration

**Complete Process (Recommended)**
- Duration: 30-90 seconds
- Steps: Transform → Validate → Optimize
- Output: Fully optimized pseudo-code with validation report
- Best for: Production features, complex requirements

Your choice is saved and offered as default next time.

### 2. Input Validation

Your query is validated before processing:
- Must be 10-5000 characters
- Cannot be empty or whitespace-only
- Automatically sanitized for security

### 3. Pipeline Execution

**Quick Mode:**
```
Query → Transform → Output
```

**Complete Mode:**
```
Query → Transform → Validate → Optimize → Output
          ↓           ↓          ↓
     Step 1/3    Step 2/3   Step 3/3
```

Progress is displayed in real-time during complete mode.

### 4. Result Delivery

**Quick Mode Output:**
```
Transformed: function_name(
  param1="value1",
  param2="value2"
)
```

**Complete Mode Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Fully optimized pseudo-code with all parameters]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Validation results with checks, warnings, issues]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[List of improvements made]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration: 42s
Steps Completed: 3/3
Issues Found: 2 warnings (resolved)
```

## Examples

### Example 1: Simple Feature (Quick Mode)

**Command:**
```
/complete-process Add a dark mode toggle to settings
```

**Mode Selection:** Quick Transform Only

**Output (8 seconds):**
```
Transformed: add_dark_mode_toggle(
  location="settings",
  component="toggle_switch",
  persistence="local_storage",
  default_value="system_preference"
)
```

---

### Example 2: Authentication Feature (Complete Mode)

**Command:**
```
/complete-process Implement JWT authentication with refresh tokens
```

**Mode Selection:** Complete Process (Recommended)

**Progress:**
```
Step 1/3: 🔄 Transforming query to pseudo-code... ✓ (12s)
✓ Step 1/3 complete | Tokens: 1,234

Step 2/3: ✓ Validating requirements... ✓ (8s)
✓ Step 2/3 complete | Tokens: 2,567

Step 3/3: ⚡ Optimizing for implementation... ✓ (22s)
✓ Step 3/3 complete | Tokens: 3,891

✓ Pipeline complete! Review output below.

Total duration: 42 seconds | Total tokens: 3,891
```

**Output:**
```
Optimized: implement_jwt_authentication(
  token_type="jwt",
  access_token_ttl="15m",
  refresh_token_ttl="7d",

  endpoints={
    "login": "/api/auth/login",
    "refresh": "/api/auth/refresh",
    "logout": "/api/auth/logout"
  },

  security={
    "hashing": "bcrypt",
    "salt_rounds": 12,
    "secure_cookies": true,
    "httponly": true,
    "same_site": "strict"
  },

  validation={
    "email": "RFC5322",
    "password": "min_8_chars"
  },

  error_handling={
    "invalid_credentials": "return_401",
    "expired_token": "return_403_with_refresh",
    "rate_limit_exceeded": "return_429"
  },

  rate_limiting={
    "login_attempts": "5_per_15min",
    "lockout_duration": "15m"
  },

  storage={
    "refresh_tokens": "database",
    "blacklist": "redis"
  }
)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION REPORT: ✓ All checks passed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPROVEMENTS MADE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Security
  - Added bcrypt hashing with salt rounds
  - Added secure cookie configuration
  - Added rate limiting to prevent brute force

✓ Error Handling
  - Defined error responses for all scenarios
  - Added expired token refresh flow
  - Added rate limit handling

✓ Validation
  - Added email format validation
  - Added password strength requirements

✓ Storage
  - Specified refresh token storage (database)
  - Added token blacklist (Redis)
```

---

### Example 3: Large Query with Compression Suggestion

**Command:**
```
/complete-process [3200 character query]
```

**System Response:**
```
ℹ️ Large query detected (3247 characters)

Consider using /compress-context first for better results.
Proceed anyway? (y/N): y
```

**Continues with selected mode...**

---

## Command Options

### Mode Flags (Optional)
```
/complete-process --mode=quick <query>
/complete-process --mode=complete <query>
/complete-process --mode=auto <query>  # Uses saved preference
```

### Preference Management
```
/complete-process --show-preference    # Display saved preference
/complete-process --reset-preference   # Clear saved preference
```

### Output Format
```
/complete-process --format=json <query>     # JSON output
/complete-process --format=markdown <query> # Markdown output (default)
```

## Error Handling

### Input Validation Errors

**Empty Query:**
```
❌ Error: Query cannot be empty
Usage: /complete-process <your query>
```

**Query Too Short:**
```
❌ Error: Query must be between 10-5000 characters
Your query: 8 characters
```

**Query Too Long:**
```
❌ Error: Query exceeds maximum length (5000 characters)
Your query: 5234 characters

Suggestions:
- Use /compress-context to condense your requirements
- Break into multiple smaller queries
```

### Pipeline Errors

**Transform Failure:**
```
❌ Transformation failed: Query too ambiguous

Original query preserved. You can:
1. Rephrase with more specific details
2. Try breaking into smaller queries
3. Use quick mode for simpler transformation

Retry? (y/N): _
```

**Validation Warning (Non-Critical):**
```
⚠ Validation found 2 warnings:
- Missing error handling specification
- No timeout values defined

Continue to optimization? (Y/n): y

Step 3/3: ⚡ Optimizing for implementation... ✓

✓ Warnings addressed during optimization.
```

**Optimization Failure:**
```
❌ Optimization failed: Unable to enhance pseudo-code

Returning validated output instead.

You can:
- Use the validated output (still production-ready)
- Manually optimize with /optimize-prompt
- Retry complete process
```

**Timeout Warning:**
```
⚠ Step taking longer than expected (24s / 30s)
Processing continues... Results will be returned when complete.
```

**Timeout Exceeded:**
```
⏱️ Step timeout exceeded (30s)

Returning partial results:
✓ Transform completed
✓ Validation completed
⏸ Optimization timed out

You have:
- Transformed and validated pseudo-code (ready to use)
- Option to manually optimize with /optimize-prompt
```

## Integration

### With Other Commands

**Pre-Process Large Requirements:**
```
/compress-context <large requirements>
→ [compressed output]
→ /complete-process <use compressed output>
```

**Post-Process for Feature Development:**
```
/complete-process <feature request>
→ [optimized pseudo-code]
→ /feature-dev <implement using pseudo-code>
```

**Manual Step Execution (Alternative):**
```
/transform-query <query>
→ /validate-requirements <transformed output>
→ /optimize-prompt <validated output>

# Equivalent to /complete-process in complete mode
```

### With Hooks

**Context-Aware Transformation:**
The command automatically uses project context when available:
```
Query → Detect project → Inject structure → Transform with context
```

## Performance

### Typical Durations

**Quick Mode:**
- Simple query (< 50 words): 5-10s
- Medium query (50-200 words): 10-15s

**Complete Mode:**
- Simple query: 20-40s
- Medium query: 40-60s
- Complex query: 60-90s

### Optimization Tips

1. **Use Quick Mode for Iteration**
   - Refine your query with quick mode
   - Run complete mode on final version

2. **Compress Large Requirements**
   - Use `/compress-context` first
   - Reduces processing time by 30-50%

3. **Prefer Quick Mode for Simple Queries**
   - Faster results for well-defined requirements
   - Perfect for rapid prototyping

4. **Be Specific**
   - Clear queries process faster
   - Reduces optimization workload

## Troubleshooting

### "Query must be between 10-5000 characters"
**Solution:** Ensure query has meaningful content. For large requirements, use `/compress-context`.

### "Transformation failed: Query too ambiguous"
**Solution:** Add more specific details.
- Before: "Add notifications"
- After: "Implement email notifications for new messages using SendGrid"

### "Pipeline timeout exceeded"
**Solution:**
- Break complex queries into smaller parts
- Check network connection
- Try quick mode for faster results

### "Skill unavailable: requirement-validator"
**Solution:** Plugin may be partially loaded. Restart Claude Code or use individual commands.

### Pipeline stuck at a step
**Solution:** Wait for timeout warning. If no progress after 2 minutes, press Ctrl+C and retry.

### Mode selection not showing preference
**Solution:** Preference file may not exist. Your choice will be saved after first selection.

## Configuration

### Preference File Location
`.claude/plugin_preferences.json`

### Preference Format
```json
{
  "complete-process-orchestrator": {
    "preferred_mode": "complete",
    "show_progress": true,
    "remember_preference": true,
    "last_updated": "2026-01-18T12:00:00Z"
  }
}
```

### Metrics File Location
`.claude/plugin_metrics.json`

### Metrics Format
```json
{
  "complete-process-orchestrator": {
    "total_invocations": 42,
    "quick_mode_count": 12,
    "complete_mode_count": 30,
    "average_duration_quick": "8s",
    "average_duration_complete": "45s",
    "success_rate": 0.95,
    "last_execution": "2026-01-18T12:00:00Z"
  }
}
```

## Best Practices

### Query Writing
- ✓ Be specific about requirements
- ✓ Mention security or performance needs
- ✓ Reference integration points
- ✓ Specify constraints upfront

### Mode Selection
- ✓ Use complete mode for production features
- ✓ Use quick mode for iteration and exploration
- ✓ Let the system remember your preference
- ✓ Override when needed for specific queries

### Workflow Optimization
- ✓ Start with complete mode for new features
- ✓ Iterate with quick mode for refinements
- ✓ Review validation reports to learn patterns
- ✓ Save and reuse optimized pseudo-code

## Related Commands

- `/transform-query` - Transform only (equivalent to quick mode)
- `/validate-requirements` - Validate pseudo-code
- `/optimize-prompt` - Optimize pseudo-code
- `/compress-context` - Compress verbose requirements
- `/feature-dev` - Implement features using pseudo-code

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review [Examples](#examples) for common patterns
- Use individual commands for manual execution
- Report issues at plugin repository

## Version

Command Version: 1.0.0
Plugin Version: 1.6.0
