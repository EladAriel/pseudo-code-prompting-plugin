# Smart Router Skill

Intelligent command routing skill for executing any pseudo-code-prompting command with automatic context detection and cached tree reuse for token efficiency.

## Skill Metadata

```json
{
  "skill_id": "smart-router",
  "tier": "orchestration",
  "name": "Smart Router",
  "tokens_estimate": 250,
  "triggers": {
    "keywords": ["smart", "router", "intelligent", "route"],
    "patterns": ["/smart [command]", "smart router"],
    "contexts": ["user invokes smart router", "multi-command workflow"]
  },
  "capabilities": [
    "intelligent-routing",
    "context-detection",
    "tree-caching",
    "token-optimization",
    "sub-command-orchestration"
  ]
}
```

## Purpose

The smart router skill provides intelligent routing of `/smart` commands to any pseudo-code-prompting sub-command with:
- Automatic context-aware mode detection
- Cached PROJECT_TREE reuse (no re-scanning)
- Token efficiency (60-80% savings across multiple commands)
- Transparent pass-through of sub-command results

## Supported Sub-Commands

| Command | Description | Input | Output |
|---------|-------------|-------|--------|
| transform-query | Convert natural language to pseudo-code | Query string | Transformed pseudo-code |
| validate-requirements | Validate pseudo-code completeness | Pseudo-code | Validation report |
| optimize-prompt | Enhance pseudo-code | Pseudo-code | Optimized pseudo-code |
| complete-process | Full Transform → Validate → Optimize | Query string | Optimized output + TODOs |
| compress-context | Reduce verbose text | Large text | Compressed text |

## Capabilities

### 1. Command Routing
- Parse `/smart [command] [arguments]` format
- Identify which sub-command to execute
- Validate command name against supported list
- Return error for unknown commands

### 2. Context Detection
- Check for `[CONTEXT-AWARE MODE ACTIVATED]` in context
- Detect if PROJECT_TREE is available in context
- Determine context-aware vs standard mode
- Pass context to sub-command appropriately

### 3. Tree Caching (Option B: Read-Only)
- Reuse cached PROJECT_TREE for all read-only commands
- No re-scanning project within workflow
- 60-80% token savings across multiple commands
- Handles staleness: Not an issue (all commands read-only)

### 4. Sub-Command Invocation
- Use Skill tool to invoke appropriate sub-command
- Pass arguments without modification
- Include PROJECT_TREE if context-aware mode
- Return sub-command output directly

### 5. Error Handling
- Validate sub-command name
- Check for required arguments
- Propagate sub-command errors with context
- Provide helpful error messages

## Integration Points

### With Hooks

**context-aware-tree-injection hook:**
- Detects implementation keywords (implement, create, add, build)
- Scans project and injects PROJECT_TREE into context
- Smart router skill reuses cached tree for all subsequent commands

**user-prompt-submit hook:**
- Detects `/smart` command invocation
- Prepares routing context
- Activates smart-router skill

### With Skills (Sub-Command Routing)

```
smart-router skill
  ├─ Routes to pseudo-code-prompting:transform-query
  ├─ Routes to pseudo-code-prompting:validate-requirements
  ├─ Routes to pseudo-code-prompting:optimize-prompt
  ├─ Routes to pseudo-code-prompting:complete-process
  └─ Routes to pseudo-code-prompting:compress-context
```

### With Agent

**smart-router agent:**
- Parses command and arguments
- Detects context-aware mode
- Routes to sub-command skill
- Manages memory updates
- Handles errors

## Token Efficiency Strategy

### Scenario: Multiple Commands in One Session

**Without smart (re-scan per command):**
```
1. /transform-query + tree scan:  2000 + 1500 = 3500 tokens
2. /validate + tree scan:         2000 + 1200 = 3200 tokens
3. /optimize + tree scan:         2000 + 1800 = 3800 tokens
Total: 10,500 tokens
```

**With smart (cached tree reuse):**
```
Initial: Tree captured by hooks:      0 tokens (automatic)
1. /smart transform-query:             1500 tokens (no scan)
2. /smart validate-requirements:       1200 tokens (reuse tree)
3. /smart optimize-prompt:             1800 tokens (reuse tree)
Total: 4,500 tokens (57% savings)
```

### Why Option B Works (Read-Only Commands)

All pseudo-code-prompting commands are **read-only**:
- Transform-query: Reads tree → generates code (no modification)
- Validate-requirements: Analyzes code → returns report (no modification)
- Optimize-prompt: Enhances code → returns optimized (no modification)
- Complete-process: Full pipeline → returns output (no modification)
- Compress-context: Reduces text → returns compressed (no modification)

**Actual project writes happen outside this workflow** (via `/feature-dev` or manual implementation)

**Result:** Tree staleness is not a concern. Cached tree is safe for all commands.

## Workflow Integration

### Standard Workflow

```
1. User types: /smart transform-query [query]
   ↓
2. Hook detects [CONTEXT-AWARE MODE ACTIVATED] + PROJECT_TREE
   ↓
3. smart-router agent routes to transform-query skill
   ↓
4. Sub-command skill uses cached PROJECT_TREE
   ↓
5. Returns transformed pseudo-code with file paths
   ↓
6. User gets result in 2-3 seconds (no tree re-scan)
```

### Multi-Command Session

```
Command 1: /smart transform-query [query]
  └─ Caches PROJECT_TREE from hooks

Command 2: /smart validate-requirements [code]
  └─ Reuses cached tree

Command 3: /smart optimize-prompt [code]
  └─ Reuses cached tree

Total time: ~10 seconds (vs 20+ with re-scans)
Total tokens: ~4500 (vs 10500 with re-scans)
```

## Performance Characteristics

### Routing Latency
- Command parsing: <50ms
- Context detection: <50ms
- Sub-command invocation: 100-200ms
- **Total overhead: <500ms (negligible)**

### Command Execution Time (with cached tree)
- transform-query: 2-5 seconds
- validate-requirements: 2-5 seconds
- optimize-prompt: 5-10 seconds
- complete-process: 20-40 seconds
- compress-context: 2-5 seconds

### Token Consumption
- routing overhead: ~100 tokens
- cached tree reuse: 60-80% savings
- per-command cost: Depends on sub-command

## Error Scenarios

### Unknown Sub-Command
```
Input: /smart validate [pseudo-code]
Output: ❌ Unknown command "validate"
        Use "validate-requirements" instead
```

### Missing Arguments
```
Input: /smart transform-query
Output: ❌ Missing arguments for transform-query
        Usage: /smart transform-query [query]
```

### Sub-Command Failure
```
Input: /smart transform-query [ambiguous query]
Output: ❌ transform-query failed: Query too ambiguous
        Suggestion: Add more specific details
```

### Context Error
```
Input: /smart [command] (in completely different project)
Output: ⚠️ Project context changed
        Clearing cached tree
        Running in standard mode
```

## Usage Examples

### Example 1: Transform with Cached Tree
```
Command: /smart transform-query Implement OAuth2 authentication
Flow: Detect cached tree → Pass to transform-query → Output with file paths
Result: Transformed pseudo-code with actual paths from project
```

### Example 2: Validate Pseudo-Code
```
Command: /smart validate-requirements implement_oauth(...)
Flow: Parse pseudo-code → Route to validate-requirements → Return report
Result: Validation report with issues and severity
```

### Example 3: Complete Pipeline
```
Command: /smart complete-process Build REST API with PostgreSQL
Flow: Mode selection → Route to complete-process → Full pipeline → Return TODOs
Result: Optimized pseudo-code + validation + TODOs
```

### Example 4: Compress Requirements
```
Command: /smart compress-context [3000 char requirements]
Flow: Route to compress-context → Reduce by 60-95% → Return
Result: Compressed requirements
```

## Implementation Requirements

1. **Use Skill tool for sub-command invocation** (never inline execution)
2. **Pass context directly** to sub-command (preserve PROJECT_TREE)
3. **Return output as-is** (no wrapping or modification)
4. **Handle errors gracefully** (user-friendly messages)
5. **Update memory** (track routing history)
6. **Maintain compatibility** (with all sub-commands)

## References

- **Command File:** `commands/smart.md`
- **Agent:** `agents/smart-router.md`
- **Related Skills:**
  - `skills/prompt-structurer/SKILL.md` (for transform-query routing)
  - `skills/requirement-validator/SKILL.md` (for validate-requirements routing)
  - `skills/prompt-optimizer/SKILL.md` (for optimize-prompt routing)
  - `skills/complete-process-orchestrator/SKILL.md` (for complete-process routing)
  - `skills/context-compressor/SKILL.md` (for compress-context routing)

## Version

Skill Version: 1.0.0
Plugin Version: 1.1.6
