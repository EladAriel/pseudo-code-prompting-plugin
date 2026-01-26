# Complete-Process Hook Orchestration

This document describes the three-stage hook system for the complete-process command, which monitors and filters outputs across the entire transformation pipeline.

## Overview

The complete-process command orchestrates a three-stage transformation pipeline:
1. **Transform** - Convert natural language to pseudo-code
2. **Validate** - Check completeness and security
3. **Optimize** - Add missing parameters and improvements

To maximize clarity while preserving context, three specialized hooks monitor this pipeline:

- **Pre-Execution**: Inject project context before pipeline starts
- **In-Process**: Filter outputs based on stage-specific requirements
- **Post-Execution**: Clean intermediate messages and format final output

## Architecture

```
User: /complete-process "Implement JWT authentication"
    ↓
[UserPromptSubmit Hook]
    ├→ user-prompt-submit.py (detects /complete-process)
    └→ complete-process-tree-injection.py (injects PROJECT_TREE context)
    ↓
Claude invokes: Skill(prompt-transformer) with context
    ↓
Agent returns: pseudo_code + WORKFLOW_CONTINUES: YES
    ↓
[PostToolUse Hook - Stage 1: TRANSFORM]
    └→ complete-process-orchestrator.py
        • Detects: WORKFLOW_CONTINUES: YES, NEXT_AGENT: requirement-validator
        • Action: Extract ONLY pseudo-code function
        • Output: "[TRANSFORM_COMPLETE]\n{function}\n[PROCEEDING_TO_VALIDATION]"
    ↓
Claude invokes: Skill(requirement-validator)
    ↓
Agent returns: validation_report + WORKFLOW_CONTINUES: YES
    ↓
[PostToolUse Hook - Stage 2: VALIDATE]
    └→ complete-process-orchestrator.py
        • Detects: NEXT_AGENT: prompt-optimizer
        • Action: Keep FULL validation report
        • Output: "[VALIDATE_COMPLETE]\n{full_report}\n[PROCEEDING_TO_OPTIMIZATION]"
    ↓
Claude invokes: Skill(prompt-optimizer)
    ↓
Agent returns: optimized_code + TODO_LIST + WORKFLOW_CONTINUES: NO
    ↓
[PostToolUse Hook - Stage 3: OPTIMIZE]
    └→ complete-process-orchestrator.py
        • Detects: WORKFLOW_CONTINUES: NO
        • Action: Extract optimized code + TODOs
        • Output: "[OPTIMIZE_COMPLETE]\n{code}\n[TODOS]\n{list}"
    ↓
[PostToolUse Hook - CLEANUP]
    └→ complete-process-cleanup.py
        • Detects: Pipeline completion
        • Action: Remove intermediate outputs, format final message
        • Output: Clean presentation with code + improvements + TODOs
    ↓
Final Output: Ready for /feature-dev implementation
```

## Hook Files

### 1. Pre-Execution: `complete-process-tree-injection.py`

**Trigger**: `UserPromptSubmit` when `/complete-process` command detected

**Purpose**: Inject project structure context before the pipeline starts

**Detection Patterns**:
```python
patterns = [
    r'/complete-process\s+',
    r'/complete\s+',
    r'/full-transform\s+',
    r'/orchestrate\s+'
]
```

**Output Marker**:
```
[COMPLETE_PROCESS_CONTEXT_INJECTION]
...
[COMPLETE_PROCESS_CONTEXT_START]
<project tree structure>
[COMPLETE_PROCESS_CONTEXT_END]
```

**Benefits**:
- Claude understands project organization before transformation
- Makes intelligent decisions about file placement
- Considers existing patterns and conventions

### 2. In-Process: `complete-process-orchestrator.py`

**Trigger**: `PostToolUse` with matcher: `Skill.*complete-process|Skill.*transform-query|Skill.*validate-requirements|Skill.*optimize-prompt`

**Purpose**: Monitor each pipeline stage and filter outputs for clarity

**Stage Detection** (via workflow markers):
```
Stage 1 (TRANSFORM):
- Marker: WORKFLOW_CONTINUES: "YES" + NEXT_AGENT: "requirement-validator"
- Filter: Extract ONLY pseudo-code function
- Removes: Verbose explanations, reasoning, examples

Stage 2 (VALIDATE):
- Marker: WORKFLOW_CONTINUES: "YES" + NEXT_AGENT: "prompt-optimizer"
- Filter: Keep FULL validation report
- Keeps: All checks, warnings, recommendations

Stage 3 (OPTIMIZE):
- Marker: WORKFLOW_CONTINUES: "NO" (pipeline complete)
- Filter: Extract optimized code + TODO list
- Removes: Intermediate optimization steps, explanations
```

**Output Format**:
```
[STAGE_COMPLETE]
<filtered content>
[PROCEEDING_TO_NEXT_STAGE]
```

**Pipeline State Tracking**:
- Saves to: `.claude/pseudo-code-prompting/pipeline-state.json`
- Tracks: Which stages completed, outputs from each stage
- Used by: Cleanup hook to know what to remove

### 3. Post-Execution: `complete-process-cleanup.py`

**Trigger**: `PostToolUse` with matcher: `WORKFLOW_CONTINUES.*NO|CHAIN_COMPLETE`

**Purpose**: Clean intermediate messages and format final output

**Actions**:
1. Extract final optimized pseudo-code
2. Extract TODO items for implementation
3. Extract improvements applied by optimizer
4. Detect validation status
5. Remove intermediate transform/validate outputs
6. Format clean final message

**Output Template**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ COMPLETE-PROCESS PIPELINE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTIMIZED PSEUDO-CODE:
{optimized_code}

IMPROVEMENTS APPLIED:
✓ Security: Added JWT validation
✓ Error handling: Added retry logic
✓ Performance: Added rate limiting

READY FOR IMPLEMENTATION - TODOs:
1. Implement OAuth provider configuration
2. Add token refresh logic
3. Set up rate limiting

→ Ready for implementation! Use /feature-dev with the optimized pseudo-code above.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Stage-Output-Filter Utility

**Location**: `hooks/orchestration/stage-output-filter.py`

**Purpose**: Provides reusable extraction patterns and formatters for each stage

**Key Methods**:

### `detect_stage(output: str) -> Optional[str]`
Identifies which stage just completed based on workflow markers.

```python
# Returns: 'transform', 'validate', 'optimize', or None
stage = StageOutputFilter.detect_stage(agent_output)
```

### `filter_transform_output(output: str) -> str`
Extracts ONLY the pseudo-code function from transform output.

```python
filtered = StageOutputFilter.filter_transform_output(output)
# Before: "Let me structure that for you. Transformed: function(...) More context..."
# After: "[TRANSFORM_COMPLETE]\nfunction(...)\n[PROCEEDING_TO_VALIDATION]"
```

### `filter_validate_output(output: str) -> str`
Keeps FULL validation report (all checks preserved).

```python
filtered = StageOutputFilter.filter_validate_output(output)
# Includes: All validation checks, warnings, pass/fail status
```

### `filter_optimize_output(output: str) -> str`
Extracts ONLY optimized code and TODO list.

```python
filtered = StageOutputFilter.filter_optimize_output(output)
# Before: "Optimizing... Applied security... Added error handling... optimized_function(...) TODOs: [...]"
# After: "[OPTIMIZE_COMPLETE]\noptimized_function(...)\n[TODOS]\n[...]"
```

### `extract_todos(output: str) -> List[str]`
Extracts TODO items in multiple formats:

```python
todos = StageOutputFilter.extract_todos(output)
# Supports: JSON array, markdown lists, numbered items, quoted strings
```

### `is_pipeline_complete(output: str) -> bool`
Detects if pipeline is complete.

```python
if StageOutputFilter.is_pipeline_complete(output):
    # Run cleanup hook
```

## Configuration

### hooks.json Registration

```json
{
  "UserPromptSubmit": [
    {
      "matcher": "complete-process|/complete |/full-transform|/orchestrate",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/orchestration/complete-process-tree-injection.py",
          "statusMessage": "Preparing project context for complete-process pipeline...",
          "timeout": 15
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Skill.*complete-process|Skill.*transform-query|Skill.*validate-requirements|Skill.*optimize-prompt",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/orchestration/complete-process-orchestrator.py",
          "statusMessage": "Processing complete-process pipeline stage...",
          "timeout": 12
        }
      ]
    },
    {
      "matcher": "WORKFLOW_CONTINUES.*NO|CHAIN_COMPLETE",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/orchestration/complete-process-cleanup.py",
          "statusMessage": "Finalizing complete-process output...",
          "timeout": 10
        }
      ]
    }
  ]
}
```

## How It Works

### Example: Implementing JWT Authentication

**Input**:
```
/complete-process Implement JWT authentication with refresh tokens and rate limiting
```

**Stage 1 - Transform** (5-10s):
```
Raw output: "Let me break this down into components. Transformed:
implement_jwt_auth(
  token_type="jwt",
  refresh_enabled=true,
  rate_limit={"attempts": 5}
)
The transformer considers security implications..."

Filtered output:
implement_jwt_auth(
  token_type="jwt",
  refresh_enabled=true,
  rate_limit={"attempts": 5}
)
[PROCEEDING_TO_VALIDATION]
```

**Stage 2 - Validate** (5-10s):
```
Raw output: "Validation Report:
✓ Security: Requires HTTPS configuration
✓ Parameters: Access token TTL missing
✓ Error Handling: Not specified..."

Filtered output:
Validation Report:
✓ Security: Requires HTTPS configuration
✓ Parameters: Access token TTL missing
✓ Error Handling: Not specified
[PROCEEDING_TO_OPTIMIZATION]
```

**Stage 3 - Optimize** (10-20s):
```
Raw output: "Optimizing the specification by applying enterprise patterns...
Added security enhancements...
Optimized: implement_jwt_auth(
  token_type="jwt",
  refresh_enabled=true,
  rate_limit={"attempts": 5},
  security={"https_required": true},
  token_ttl={"access": "15m", "refresh": "7d"}
)
TODO_LIST: ["Configure HTTPS", "Set up token storage", "Implement rate limiting"]"

Filtered output:
[OPTIMIZE_COMPLETE]
implement_jwt_auth(
  token_type="jwt",
  refresh_enabled=true,
  rate_limit={"attempts": 5},
  security={"https_required": true},
  token_ttl={"access": "15m", "refresh": "7d"}
)
[TODOS]
["Configure HTTPS", "Set up token storage", "Implement rate limiting"]
```

**Stage 4 - Cleanup**:
```
Final formatted output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ COMPLETE-PROCESS PIPELINE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTIMIZED PSEUDO-CODE:
implement_jwt_auth(
  token_type="jwt",
  refresh_enabled=true,
  rate_limit={"attempts": 5},
  security={"https_required": true},
  token_ttl={"access": "15m", "refresh": "7d"}
)

IMPROVEMENTS APPLIED:
✓ Security: Added HTTPS requirement and token TTL configuration
✓ Error handling: Integrated rate limiting
✓ Performance: Specified token refresh window

READY FOR IMPLEMENTATION - TODOs:
1. Configure HTTPS
2. Set up token storage
3. Implement rate limiting

→ Ready for implementation! Use /feature-dev with the optimized pseudo-code above.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

### Hook Failure Modes

**Graceful Degradation**: If any hook fails, it:
1. Logs error to stderr (doesn't interrupt)
2. Exits with code 0 (success)
3. Outputs nothing (passes through unchanged)
4. Pipeline continues unaffected

### Pipeline State Recovery

If hooks miss a stage:
1. State file (`pipeline-state.json`) tracks completed stages
2. Missing stages can be re-run manually
3. Cleanup hook verifies completion before formatting

### Timeout Handling

- Pre-execution: 15s timeout (includes tree generation)
- In-process: 12s timeout per stage
- Post-execution: 10s timeout

If timeout exceeded, hook exits silently and output passes through.

## Memory Files

### Pipeline State: `.claude/pseudo-code-prompting/pipeline-state.json`

```json
{
  "current_stage": "optimize",
  "stages_completed": ["transform", "validate", "optimize"],
  "status": "complete",
  "outputs": {
    "transform": "[TRANSFORM_COMPLETE]\n...",
    "validate": "[VALIDATE_COMPLETE]\n...",
    "optimize": "[OPTIMIZE_COMPLETE]\n..."
  },
  "final_code": "implement_jwt_auth(...)",
  "todos": ["Configure HTTPS", "Set up token storage"]
}
```

**Used by**: Cleanup hook, future analysis, context preservation

## Performance Impact

### Token Usage

**Without hooks** (raw pipeline output):
- Transform: 500 tokens
- Validate: 300 tokens
- Optimize: 400 tokens
- **Total: 1,200 tokens in context**

**With hooks** (filtered outputs):
- Transform: 50 tokens (just code)
- Validate: 200 tokens (full report kept)
- Optimize: 100 tokens (code + TODOs)
- **Total: 350 tokens in context**
- **Savings: 71%**

### Execution Time

- Pre-execution hook: +2-5s (tree generation)
- In-process hooks: <500ms per stage
- Post-execution hook: <500ms
- **Total overhead: 2-5.5s** (minimal compared to agent execution)

## Development & Testing

### Running Hooks Manually

```bash
# Test pre-execution hook
echo '{"prompt": "/complete-process implement auth", "cwd": "/project"}' | \
  python3 hooks/orchestration/complete-process-tree-injection.py

# Test orchestrator
echo '{"prompt": "WORKFLOW_CONTINUES: YES\nNEXT_AGENT: validator", "tool_name": "Skill"}' | \
  python3 hooks/orchestration/complete-process-orchestrator.py

# Test cleanup
echo '{"prompt": "WORKFLOW_CONTINUES: NO\nOptimized: func(...)"}' | \
  python3 hooks/orchestration/complete-process-cleanup.py
```

### Running Test Suite

```bash
pytest tests/test_hooks/test_complete_process_orchestration.py -v

# Run specific test
pytest tests/test_hooks/test_complete_process_orchestration.py::TestStageOutputFilter::test_detect_transform_stage -v

# Run with markers
pytest -m "hook or integration" tests/test_hooks/test_complete_process_orchestration.py
```

## Troubleshooting

### Hook Not Triggering

**Problem**: Hook files not executing

**Solutions**:
1. Verify Python path: `which python3`
2. Check file permissions: `chmod +x hooks/orchestration/*.py`
3. Verify hooks.json matcher patterns
4. Check Claude Code hook logs

### Output Not Filtered

**Problem**: Seeing verbose output despite hooks

**Solutions**:
1. Verify stage detection: Check for `WORKFLOW_CONTINUES` marker
2. Verify hook input format: Should be JSON via stdin
3. Check pipeline state: `.claude/pseudo-code-prompting/pipeline-state.json`
4. Verify timeout didn't expire

### Stage Transition Failed

**Problem**: Pipeline stuck at one stage

**Solutions**:
1. Wait for timeout (10-15s) - hook will pass through
2. Manually run next command: `/validate-requirements <output>`
3. Check error logs in `.claude/` directory
4. Restart Claude Code

## Future Enhancements

Potential improvements:
- Real-time progress indicators
- Persistent pipeline history
- Advanced output caching
- Custom filtering patterns
- Hook composition (pre/post for other commands)
