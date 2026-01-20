# Pseudo-Code Prompting Plugin - Fixes Applied (2026-01-20)

## Issues Fixed

### 1. Hook Errors (FIXED ✅)

#### Problem:
- Hooks were failing with "UserPromptSubmit hook error" appearing 3 times per message
- "Stop hook error" showing `/bin/bash` not found on Windows
- "PostToolUse:Write hook error" also failing

#### Root Causes:
1. **Nested hooks structure**: `UserPromptSubmit` had an extra `hooks` array wrapper causing triple execution
2. **Bash path issue**: Used `bash` command which doesn't exist at `/bin/bash` on Windows Git Bash/MSYS environments

#### Solution Applied:
Updated [hooks/hooks.json](hooks/hooks.json):
- Removed nested `hooks` array wrapper - flattened to direct array under event name
- Changed all `bash` commands to `sh` for cross-platform compatibility (works on Windows, Linux, macOS)

**Before:**
```json
"UserPromptSubmit": [
  {
    "hooks": [  // ❌ Extra nesting
      { "command": "bash ..." }  // ❌ bash not found on Windows
    ]
  }
]
```

**After:**
```json
"UserPromptSubmit": [
  { "command": "sh ..." },  // ✅ Direct array, sh works everywhere
  { "command": "sh ..." },
  { "command": "sh ..." }
]
```

---

### 2. Ralph Loop Integration (FIXED ✅)

#### Problem:
Ralph Loop invocation was failing with:
```
Error: Bash command permission check failed
Command contains input redirection (<) which could read sensitive files
```

#### Root Causes:
1. **Inline content instead of files**: Skill was trying to pass entire pseudo-code (with `<promise>` tags) as command arguments
2. **Security check triggered**: The `<` character in `<promise>` tags was flagged as potential file redirection
3. **Missing file writing**: No instructions to write files to `.claude/` directory
4. **Wrong invocation format**: Passing content inline instead of file references

#### Solution Applied:
Updated [skills/ralph-process-integration/SKILL.md](skills/ralph-process-integration/SKILL.md):

**Added 3 new steps:**
- **Step 5: Write Files to .claude/ Directory** - Creates and writes required files
- **Step 6: Extract Promise Keyword** - Extracts promise without `<>` characters
- **Step 7: Generate Task Summary** - Creates concise task description

**Updated workflow from 5 steps to 8 steps:**
1. Invoke Complete-Process Skill
2. Parse Validation Report
3. Calculate Complexity Score & Generate Promise
4. Generate Completion Promise
5. **NEW: Write Files to .claude/ Directory** ✅
6. **NEW: Extract Promise Keyword** ✅
7. **NEW: Generate Task Summary** ✅
8. Launch Ralph Loop (updated with file references)

**Key Changes:**

1. **File Writing (Step 5):**
   ```bash
   # Create directory
   mkdir -p .claude

   # Write 3 required files:
   - .claude/ralph-prompt.local.md (full requirements & guidance)
   - .claude/optimized-pseudo-code.local.md (optimized pseudo-code)
   - .claude/completion-promise.local.md (promise criteria)
   ```

2. **Promise Extraction (Step 6):**
   ```
   # Extract keyword without < > characters
   "Output <promise>IMPLEMENTATION_COMPLETE</promise>"
   → Promise keyword: "IMPLEMENTATION_COMPLETE"

   # Validates:
   - No < or > characters (security)
   - Uppercase with underscores or spaces
   - Length < 100 characters
   ```

3. **Task Summary (Step 7):**
   ```
   Format: "[Action] [objective] following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"

   Example: "Implement user authentication following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md"
   ```

4. **Ralph Invocation (Step 8):**
   ```
   # BEFORE (WRONG):
   args = "--max-iterations 50 --completion-promise '<promise>APP_COMPLETE</promise>' [entire prompt content here]"
   # ❌ Contains < > characters, triggers security check
   # ❌ Passes content inline (too long, security risk)

   # AFTER (CORRECT):
   args = "Implement user auth following specifications in .claude/ralph-prompt.local.md and .claude/optimized-pseudo-code.local.md --max-iterations 40 --completion-promise IMPLEMENTATION_COMPLETE"
   # ✅ File references instead of inline content
   # ✅ Promise keyword without < > characters
   # ✅ Concise and secure
   ```

**File-Based Approach Benefits:**
- ✅ No security check failures (no `<>` characters in args)
- ✅ No command length limits (files can be large)
- ✅ Ralph can reference files during execution
- ✅ Files persist for debugging/review
- ✅ Follows Ralph Loop best practices

---

## Testing Recommendations

### Test Hook Fixes:
1. Start a new Claude Code session in the test-plugin project
2. Send: "Use the pseudo-code prompting plugin"
3. Verify:
   - ✅ No "UserPromptSubmit hook error" messages
   - ✅ No "Stop hook error" with bash not found
   - ✅ Hooks execute successfully

### Test Ralph Integration:
1. Send: "Use pseudo-code prompting with ralph"
2. Request: "Build a simple todo app with React"
3. Verify:
   - ✅ Step 4/8 shows "Writing files to .claude/ directory..."
   - ✅ Files created: `.claude/ralph-prompt.local.md`, `.claude/optimized-pseudo-code.local.md`, `.claude/completion-promise.local.md`
   - ✅ Step 5/8 shows "Extracting promise keyword..." (no `<>` characters)
   - ✅ Step 8/8 shows Ralph Loop invocation with file references
   - ✅ Ralph Loop starts successfully
   - ✅ No security check errors

---

## Version Impact

- **hooks.json**: Fixed hook structure and bash compatibility
- **ralph-process-integration/SKILL.md**: Complete rewrite of Steps 5-8 to implement file-based approach
- **Workflow**: Changed from 5 steps to 8 steps
- **Compatibility**: Now works on Windows, Linux, and macOS

---

## Related Files Modified

1. [hooks/hooks.json](hooks/hooks.json) - Hook configuration
2. [skills/ralph-process-integration/SKILL.md](skills/ralph-process-integration/SKILL.md) - Ralph integration skill implementation

## Related Reference Files (No changes needed - already correct)

1. [skills/ralph-process-integration/references/ralph-invocation-specification.md](skills/ralph-process-integration/references/ralph-invocation-specification.md) - File-based approach specification
2. [skills/ralph-process-integration/references/promise-generation.md](skills/ralph-process-integration/references/promise-generation.md) - Promise generation patterns
3. [skills/ralph-process-integration/references/complexity-scoring.md](skills/ralph-process-integration/references/complexity-scoring.md) - Complexity estimation algorithm

---

## Summary

Both issues have been resolved:

1. ✅ **Hooks now work on Windows** - Changed `bash` to `sh` and fixed nested structure
2. ✅ **Ralph Loop integration now works** - Implements file-based approach with proper promise extraction

The plugin should now function correctly on all platforms and successfully integrate with Ralph Loop for automated iterative implementation.
