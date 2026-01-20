# Pseudo-Code Prompting Plugin - Quick Reference

## 🚀 One-Page Cheat Sheet

### Available Commands

| Command | What It Does | When To Use | Time |
| --- | --- | --- | --- |
| `/transform-query` | Natural language → Pseudo-code | Single transformation needed | 20-40s |
| `/validate-requirements` | Check pseudo-code completeness | After transformation | 15-30s |
| `/optimize-prompt` | Add missing parameters | After validation | 15-30s |
| `/complete-process` | Transform + Validate + Optimize | Full pipeline without Ralph | 50-100s |
| `/ralph-process` | Complete + Complexity + Ralph Loop | Automated implementation | 60-120s + Ralph |
| `/compress-context` | Verbose text → Concise pseudo-code | Long descriptions | 10-20s |

### Quick Decision Tree

```text
Do you want automated implementation with Ralph Loop?
├─ YES → Use /ralph-process
│         (includes complete-process automatically)
│
└─ NO → Do you want the full optimization pipeline?
        ├─ YES → Use /complete-process
        │         (transform → validate → optimize)
        │
        └─ NO → Use individual commands:
                ├─ /transform-query (basic transformation)
                ├─ /validate-requirements (check completeness)
                ├─ /optimize-prompt (enhance quality)
                └─ /compress-context (compress verbose text)
```

## 📊 Token Tracking

Every step shows token consumption:

```text
✓ Step N/M complete | Tokens: 1,234
```

This helps you:
- Track costs
- Identify expensive steps
- Optimize workflows
- Budget token usage

## 🔄 Complete Workflow Comparison

### Manual Workflow (Individual Commands)

```text
1. /transform-query
   Input: "Build user auth with OAuth"
   Output: implement_auth(type="oauth", ...)
   Tokens: 567

2. /validate-requirements
   Input: [pseudo-code from step 1]
   Output: Validation report (passed/warnings/critical)
   Tokens: 834

3. /optimize-prompt
   Input: [pseudo-code + validation report]
   Output: Optimized pseudo-code with all parameters
   Tokens: 623

Total: 2,024 tokens, ~90s, 3 manual steps
```

### Automated Workflow (Complete Process)

```text
1. /complete-process "Build user auth with OAuth"

   Runs automatically:
   - Transform
   - Validate
   - Optimize

   Output: Optimized pseudo-code + validation report
   Tokens: 2,024
   Time: 60s
   Manual steps: 1 ✓
```

### Fully Automated (Ralph Process)

```text
1. /ralph-process "Build user auth with OAuth"

   Runs automatically:
   - Transform → Validate → Optimize (complete-process)
   - Calculate complexity (SIMPLE/MEDIUM/COMPLEX)
   - Generate completion promise
   - Write .claude/ files
   - Launch Ralph Loop with optimized parameters

   Output: Working implementation
   Tokens: 2,500 (before Ralph) + Ralph tokens
   Time: 90s + Ralph iterations
   Manual steps: 1 ✓
```

## 🎯 Ralph Process Workflow

### The 6 Steps (Automatic)

```text
Step 1/6: Running transformation pipeline...
✓ Step 1/6 complete | Tokens: 1,234

Step 2/6: Analyzing validation metrics...
✓ Step 2/6 complete | Tokens: 156

Step 3/6: Calculating complexity score...
✓ Step 3/6 complete | Tokens: 45
  Complexity: MEDIUM (score: 42)
  Iterations: 40

Step 4/6: Generating completion criteria...
✓ Step 4/6 complete | Tokens: 89
  Promise: 'COMPLETE: Auth AND Tests passing'

Step 5/6: Writing files to .claude/ directory...
✓ Step 5/6 complete | Tokens: 234
  Files: 3 created

Step 6/6: Launching Ralph Loop...
✓ Step 6/6 complete | Tokens: 67
  Starting Ralph Loop now...
```

### Complexity Levels

| Level | Score | Iterations | Examples |
| --- | --- | --- | --- |
| SIMPLE | 0-25 | 20 | Add button, dark mode toggle, simple form |
| MEDIUM | 26-60 | 40 | User auth, REST API, basic CRUD |
| COMPLEX | 61+ | 80 | Payment processing, real-time features, multi-service |

### Complexity Calculation

```text
base = (warnings × 2) + (critical × 5) + (edge_cases × 3)
modifiers:
  + 10 if security requirements
  + 5 if error handling gaps
  - 5 if many passed checks (>8)

if score ≤ 25: SIMPLE (20 iterations)
elif score ≤ 60: MEDIUM (40 iterations)
else: COMPLEX (80 iterations)
```

## 🔧 Troubleshooting

### "Stop hook error: execvpe(/bin/bash) failed"

**Cause:** Ralph Loop plugin uses bash scripts
**Solution:** Install Git Bash or WSL
**Details:** See [WINDOWS-WSL-TROUBLESHOOTING.md](WINDOWS-WSL-TROUBLESHOOTING.md)

### "Process is stuck / no progress indicator"

**Fixed in v2.0:** Every step now shows:
```text
✓ Step N/M complete | Tokens: [N]
```

### "Pseudocode process ignored"

**Fixed in v2.0:** Simplified SKILL.md files ensure Claude follows the workflow

## 📁 File Structure

### After /ralph-process

```text
.claude/
├── ralph-prompt.local.md              (Detailed task description)
├── optimized-pseudo-code.local.md     (Optimized pseudo-code)
└── completion-promise.local.md        (Promise keyword + criteria)
```

These files tell Ralph Loop:
- What to build (ralph-prompt.local.md)
- How to build it (optimized-pseudo-code.local.md)
- When it's done (completion-promise.local.md)

## 💡 Best Practices

### ✅ DO

- Use `/ralph-process` for automated implementation
- Use `/complete-process` when you want optimized pseudo-code without Ralph
- Check token count after each step
- Review validation report before implementing
- Let Ralph iterate (don't cancel too early)

### ❌ DON'T

- Skip validation (catches critical issues)
- Skip optimization (adds missing parameters)
- Manually chain individual commands (use complete-process)
- Cancel Ralph before promise is fulfilled
- Ignore critical issues in validation report

## 🏃 Quick Start Examples

### Example 1: Simple Feature

```text
You: /ralph-process Add a logout button to the navbar

Claude: [Runs 6-step workflow]
        Complexity: SIMPLE (20 iterations)
        Ralph Loop launches...
        [20 iterations later]
        ✓ COMPLETE: Logout button added AND Functionality working
```

### Example 2: Medium Feature

```text
You: /ralph-process Build a task management API with authentication

Claude: [Runs 6-step workflow]
        Complexity: MEDIUM (40 iterations)
        Ralph Loop launches...
        [40 iterations later]
        ✓ IMPLEMENTATION COMPLETE: 4 requirements met
```

### Example 3: Complex Feature

```text
You: /ralph-process Implement payment processing with Stripe webhooks

Claude: [Runs 6-step workflow]
        Complexity: COMPLEX (80 iterations)
        Ralph Loop launches...
        [80 iterations later]
        ✓ IMPLEMENTATION COMPLETE: 6 requirements met
```

## 📈 Token Budget Planning

| Workflow | Tokens | Cost (Sonnet 4.5) | Use Case |
| --- | --- | --- | --- |
| Transform only | ~500 | $0.0015 | Quick conversion |
| Complete process | ~2,000 | $0.006 | Full pipeline |
| Ralph process (before Ralph) | ~2,500 | $0.0075 | Setup for automation |
| Ralph iteration (avg) | ~800 | $0.0024 | Per iteration |

**Example:** MEDIUM task (40 iterations)
- Setup: 2,500 tokens ($0.0075)
- Ralph: 40 × 800 = 32,000 tokens ($0.096)
- **Total: 34,500 tokens (~$0.10)**

## 🔗 Useful Links

- [Full Documentation](../README.md)
- [Windows/WSL Troubleshooting](WINDOWS-WSL-TROUBLESHOOTING.md)
- [Plugin Repository](https://github.com/EladAriel/pseudo-code-prompting-plugin)
- [Report Issues](https://github.com/EladAriel/pseudo-code-prompting-plugin/issues)

## 📝 Version

**2.0.0** - Updated for simplified workflows with token tracking

---

**Pro Tip:** Start with `/complete-process` to see the optimized pseudo-code, then decide if you want to use `/ralph-process` for automated implementation.
