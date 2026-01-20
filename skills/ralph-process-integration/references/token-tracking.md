# Token Tracking for Ralph Process Integration

## Overview

Track and display token consumption after each of the 8 steps to provide real-time cost visibility throughout the Ralph Loop integration workflow.

## Display Format

After each step completion, display token usage in this format:

```text
✓ Step N/8 complete | Tokens: X,XXX
```

## Implementation Instructions

### After Each Step

1. Check current conversation token usage
2. Display completion message with token count
3. Format numbers with comma separators (e.g., 1,234 not 1234)
4. Track cumulative token usage across all steps

### Step-by-Step Format

**Step 1/8: Complete-Process Pipeline**

```text
Step 1/8: Running complete-process pipeline...
  ✓ Transform complete
  ✓ Validation complete
  ✓ Optimization complete
  Duration: 45s
✓ Step 1/8 complete | Tokens: 2,345
```

**Step 2/8: Complexity Analysis**

```text
Step 2/8: Analyzing complexity...
  Warnings: 5
  Critical Issues: 2
  [metrics...]
  Complexity Score: 47 (MEDIUM)
  ✓ Recommended iterations: 40
✓ Step 2/8 complete | Tokens: 2,567
```

**Step 3/8: Promise Generation**

```text
Step 3/8: Generating completion criteria...
  Critical requirements identified:
    • Requirement 1
    • Requirement 2
  ✓ Promise: "IMPLEMENTATION COMPLETE: 2 requirements met"
✓ Step 3/8 complete | Tokens: 2,789
```

**Step 4/8: File Writing**

```text
Step 4/8: Writing files to .claude/ directory...
  ✓ Created .claude/ directory
  ✓ Wrote ralph-prompt.local.md (287 lines)
  ✓ Wrote optimized-pseudo-code.local.md (42 lines)
  ✓ Wrote completion-promise.local.md (15 lines)
✓ Step 4/8 complete | Tokens: 2,891
```

**Step 5/8: Promise Extraction**

```text
Step 5/8: Extracting promise keyword...
  ✓ Promise: "IMPLEMENTATION_COMPLETE"
✓ Step 5/8 complete | Tokens: 2,923
```

**Step 6/8: Task Summary**

```text
Step 6/8: Preparing Ralph Loop invocation...
  ✓ Task summary: "Implement user authentication system"
✓ Step 6/8 complete | Tokens: 2,956
```

**Step 7/8: Ralph Launch**

```text
Step 7/8: Starting Ralph Loop...
  Task: Implement user authentication system
  Iterations: 40
  Promise: "IMPLEMENTATION_COMPLETE"
  Files: .claude/ralph-prompt.local.md, .claude/optimized-pseudo-code.local.md
✓ Step 7/8 complete | Tokens: 3,012
```

**Step 8/8: Activation**

```text
Step 8/8: Ralph Loop activated
  ⚠️  Ralph Loop is now running independently
  Monitor progress via ralph-loop commands
✓ Step 8/8 complete | Tokens: 3,045
```

### Final Summary

Update the completion message to include total tokens:

```text
═══════════════════════════════════════════════════════════
✓ Ralph Loop Integration Complete
Total tokens: 3,045
═══════════════════════════════════════════════════════════
```

## Benefits

- **Real-time cost tracking**: Users see token consumption as it happens
- **Step-by-step visibility**: Track which steps consume more tokens
- **Budget planning**: Helps predict costs for complex workflows
- **Transparency**: Clear visibility into resource usage throughout the 8-step process
