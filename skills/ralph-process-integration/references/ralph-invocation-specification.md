# Ralph Loop Invocation Specification

## Overview

This document specifies how to correctly invoke Ralph Loop with optimized inputs, including automatic file management in the `.claude/` directory, promise extraction, complexity estimation, and error handling.

## Complete Pseudo-Code Specification

```javascript
optimize_ralph_invocation(
  skill_name="ralph-loop:ralph-loop",

  // CRITICAL FIX #1: Promise Extraction Algorithm
  promise_extraction={
    "patterns": [
      "regex:<promise>(.*?)</promise>",
      "regex:MUST output `<promise>(.*?)</promise>`",
      "keyword:IMPLEMENTATION_COMPLETE|TASK_COMPLETE|BUILD_SUCCESSFUL"
    ],
    "search_locations": [
      "validation_report:completion_criteria",
      "requirements:completion_section",
      "checklist:final_items"
    ],
    "extraction_strategy": "first_match_or_fallback",
    "fallback": "TASK_COMPLETE",
    "validation": "must_be_uppercase:must_be_single_word"
  },

  // CRITICAL FIX #2: Complexity Estimation Algorithm
  complexity_estimation={
    "algorithm": "scoring_matrix",
    "scoring_rules": {
      "keywords": {
        "full_stack": 30, "authentication": 15, "database": 10,
        "api": 8, "frontend": 8, "backend": 8, "integration": 15,
        "real_time": 12, "security": 10, "testing": 5, "deployment": 8
      },
      "file_count": {
        "threshold_simple": "<=3 files = 5 points",
        "threshold_medium": "4-10 files = 15 points",
        "threshold_complex": ">10 files = 30 points"
      },
      "dependencies": {
        "external_apis": 10,
        "third_party_libs": 5,
        "microservices": 20
      }
    },
    "classification": {
      "simple": {
        "score_range": "0-30",
        "iterations": 20,
        "buffer": 5
      },
      "medium": {
        "score_range": "31-60",
        "iterations": 40,
        "buffer": 10
      },
      "complex": {
        "score_range": "61+",
        "iterations": 80,
        "buffer": 20
      }
    }
  },

  // CRITICAL FIX #3: Task Summary Generation
  task_summary_generation={
    "source": "user_input_or_requirements",
    "extraction_method": "first_sentence_or_title",
    "format": {
      "structure": "imperative_verb + object + context",
      "examples": [
        "Create React app with user registration",
        "Implement JWT authentication system"
      ]
    },
    "max_length": 100,
    "validation": "must_start_with_verb:must_describe_outcome"
  },

  // CRITICAL FIX #4: Path Resolution
  path_resolution={
    "base_dir": ".claude/",
    "resolve_relative": true,
    "normalize_paths": true,
    "create_if_missing": true,
    "check_writable": true,
    "fallback_location": "./tmp/claude/"
  },

  // File Management with .local.md Extension
  file_management={
    "output_location": ".claude/",
    "ensure_directory": true,
    "naming_pattern": "*.local.md",
    "files": [
      {
        "name": "optimized-pseudo-code.local.md",
        "content": "final_optimized_pseudo_code",
        "source": "complete_process_output",
        "validation": "must_not_be_empty:min_length(50)"
      },
      {
        "name": "completion-promise.local.md",
        "content": "promise_keyword_and_criteria",
        "source": "validation_requirements:completion_section",
        "validation": "must_contain_promise_tag"
      },
      {
        "name": "ralph-prompt.local.md",
        "content": "human_readable_task_description",
        "source": "original_requirements",
        "validation": "must_not_be_empty:max_length(10000)"
      }
    ],
    "error_handling": {
      "file_write_failure": "retry_3_times",
      "permission_denied": "try_fallback_location",
      "disk_full": "cleanup_old_files"
    },
    "versioning": {
      "enabled": true,
      "keep_versions": 3,
      "strategy": "timestamp_suffix"
    },
    "concurrency_control": {
      "lock_file": ".claude/.ralph-invocation.lock",
      "max_concurrent": 1
    }
  },

  // Invocation Template
  invocation_template={
    "skill": "ralph-loop:ralph-loop",
    "args": "{task_summary} following specifications in ralph-prompt.md and optimized-pseudo-code.md --max-iterations {iterations} --completion-promise {promise}"
  },

  // Pre-Invocation Checks
  pre_invocation_checks={
    "validate_files_exist": true,
    "validate_ralph_plugin_available": true,
    "check_directory_writable": true,
    "verify_no_concurrent_ralph": true
  },

  // Post-Execution Processing
  post_execution={
    "parse_ralph_output": true,
    "extract_promise_fulfillment": true,
    "save_execution_summary": ".claude/ralph-execution-summary.json",
    "cleanup": {
      "remove_lock_file": true,
      "archive_old_runs": "after_7_days"
    }
  }
)
```

## File Structure in .claude/ Directory

```
.claude/
├── ralph-prompt.local.md              # Human-readable task description
├── optimized-pseudo-code.local.md     # Final optimized pseudo-code
├── completion-promise.local.md        # Promise keyword and criteria
├── ralph-progress.json                # Real-time progress tracking (optional)
├── ralph-execution-summary.json       # Post-execution results (optional)
└── .ralph-invocation.lock             # Concurrency control lock
```

## File Templates

### 1. ralph-prompt.local.md

```markdown
# Task: [Task Title]

## Objective
[Clear statement of what needs to be built]

## Requirements

### Functional Requirements
- Requirement 1
- Requirement 2

### Technical Requirements
- Tech stack details
- Dependencies
- Architecture patterns

### Security Requirements
- Authentication needs
- Authorization rules
- Data protection

## Success Criteria
[Specific, measurable criteria for completion]

## Completion Promise
You MUST output `<promise>PROMISE_KEYWORD</promise>` when ALL criteria are met.
```

### 2. optimized-pseudo-code.local.md

```markdown
# Optimized Pseudo-Code

## Function Call

\`\`\`javascript
function_name(
  param1="value1",
  param2="value2",
  security={...},
  validation={...},
  error_handling={...}
)
\`\`\`

## Parameters

### Security
- Authentication: [details]
- Validation: [rules]

### Implementation
- Files to create: [list]
- Integration points: [list]

## Implementation Notes
[Additional context for Ralph Loop execution]
```

### 3. completion-promise.local.md

```markdown
# Completion Promise

## Promise Keyword
`IMPLEMENTATION_COMPLETE`

## Completion Criteria

You MUST output `<promise>IMPLEMENTATION_COMPLETE</promise>` when ALL of the following are true:

1. ✅ [Criterion 1]
2. ✅ [Criterion 2]
3. ✅ [Criterion 3]

## Validation Checklist
- [ ] Feature works as specified
- [ ] Tests pass
- [ ] No errors in console
- [ ] Documentation updated
```

## Complete Workflow Integration

### Step-by-Step Process

```
Step 1: User Request
   ↓
Step 2: Run Complete Process
   → Transform query to pseudo-code
   → Validate requirements
   → Optimize for implementation
   ↓
Step 3: Extract Promise
   → Scan validation report for <promise> tags
   → Search for promise keywords in completion criteria
   → Use fallback if not found: TASK_COMPLETE
   ↓
Step 4: Estimate Complexity
   → Score based on keywords (authentication=15, database=10, etc.)
   → Score based on file count
   → Classify: simple (0-30), medium (31-60), complex (61+)
   → Set iterations: 20, 40, or 80 respectively
   → Add buffer: +5, +10, +20
   ↓
Step 5: Generate Task Summary
   → Extract from user input
   → Format: "Create X with Y following Z"
   → Max 100 characters
   → Must start with imperative verb
   ↓
Step 6: Save Files to .claude/
   → Ensure .claude/ directory exists
   → Write ralph-prompt.local.md
   → Write optimized-pseudo-code.local.md
   → Write completion-promise.local.md
   → Validate all files exist and are not empty
   ↓
Step 7: Pre-Invocation Checks
   → Verify Ralph Loop plugin installed
   → Check .claude/ directory writable
   → Verify no concurrent Ralph execution (check lock file)
   → Validate file references exist
   ↓
Step 8: Invoke Ralph Loop
   → Substitute template variables
   → Call Skill tool with:
       skill="ralph-loop:ralph-loop"
       args="{task_summary} following specifications in
             ralph-prompt.md and optimized-pseudo-code.md
             --max-iterations {iterations}
             --completion-promise {promise}"
   ↓
Step 9: Track Progress (Optional)
   → Monitor ralph-progress.json
   → Log execution events
   → Display iteration count and status
   ↓
Step 10: Parse Results
   → Extract <promise> tag from output
   → Validate promise fulfillment
   → Save execution summary
   → Cleanup lock files
```

## Example Invocation

### Good Example

```javascript
{
  "skill": "ralph-loop:ralph-loop",
  "args": "Create React app with user registration following specifications in ralph-prompt.md and optimized-pseudo-code.md --max-iterations 80 --completion-promise IMPLEMENTATION_COMPLETE"
}
```

### File References

The args should reference:
- `ralph-prompt.md` (not full path, Ralph will look in .claude/)
- `optimized-pseudo-code.md` (not full path)

The actual files are:
- `.claude/ralph-prompt.local.md`
- `.claude/optimized-pseudo-code.local.md`

Ralph Loop will automatically look in the `.claude/` directory for these files.

## Error Handling

### Error 1: Files Not Created

```
❌ Pre-invocation check failed: Required files missing
   Missing: .claude/ralph-prompt.local.md

Action taken:
- Attempted file creation
- File write failed: Permission denied
- Using fallback location: ./tmp/claude/
- Files created successfully
- Continuing with Ralph invocation...
```

### Error 2: Promise Not Found

```
⚠️  Warning: Completion promise not found in validation report

Search results:
- Pattern 1 (<promise>.*</promise>): No match
- Pattern 2 (keyword scan): No match

Action taken:
- Using fallback promise: TASK_COMPLETE
- User notified

Continuing with: --completion-promise TASK_COMPLETE
```

### Error 3: Concurrent Invocation

```
❌ Pre-invocation check failed: Lock file exists

Details:
- Lock file: .claude/.ralph-invocation.lock
- Created: 2026-01-20 10:30:00
- Age: 45 seconds

Action:
- Waiting for lock release (max 60s)...
- Lock released after 52s
- Proceeding with invocation
```

## Implementation Notes

### Promise Extraction Implementation

```
1. Search validation report for <promise>TEXT</promise> tags
2. If not found, search for "MUST output `<promise>"
3. If not found, scan for keywords: IMPLEMENTATION_COMPLETE, TASK_COMPLETE
4. If not found, use fallback: "TASK_COMPLETE"
5. Validate promise: must be uppercase, single word or underscore-separated
```

### Complexity Scoring Implementation

```
score = 0

// Keyword scoring
for keyword in ["full_stack", "authentication", "database", etc.]:
  if keyword in requirements:
    score += keyword_weight

// File count scoring
if file_count <= 3:
  score += 5
elif file_count <= 10:
  score += 15
else:
  score += 30

// Classification
if score <= 30:
  complexity = "SIMPLE", iterations = 20, buffer = 5
elif score <= 60:
  complexity = "MEDIUM", iterations = 40, buffer = 10
else:
  complexity = "COMPLEX", iterations = 80, buffer = 20

final_iterations = iterations + buffer
```

### File Management Implementation

```
1. Check if .claude/ directory exists
   - If not, create it
   - If creation fails, use fallback: ./tmp/claude/

2. For each file (ralph-prompt, pseudo-code, promise):
   - Generate content from appropriate source
   - Validate content (not empty, correct format)
   - Write to .claude/{name}.local.md
   - If write fails, retry 3 times
   - If still fails, try fallback location
   - Log all operations

3. Create lock file: .claude/.ralph-invocation.lock
   - Check if lock exists
   - If exists and < 60s old, wait
   - If exists and > 60s old, assume stale and override
   - Create new lock with timestamp

4. On completion:
   - Remove lock file
   - Archive old versions (keep 3 most recent)
   - Save execution summary
```

## Best Practices

1. **Always run complete-process first** to generate optimized pseudo-code
2. **Verify .claude/ directory exists** before invocation
3. **Check lock files** to avoid concurrent executions
4. **Use .local.md extension** for context injection files
5. **Include promise in validation report** for automatic extraction
6. **Monitor ralph-progress.json** for real-time status
7. **Review ralph-execution-summary.json** after completion

## Integration with Complete-Process

The ralph-process-integration skill should:

1. Invoke `pseudo-code-prompting:complete-process` first
2. Extract outputs: optimized pseudo-code, validation report
3. Apply promise extraction algorithm
4. Apply complexity estimation algorithm
5. Generate task summary
6. Save files to .claude/
7. Perform pre-invocation checks
8. Invoke Ralph Loop with correct args format
9. Track progress and parse results

## Version

**1.0.0** - Initial specification with optimized Ralph invocation logic
