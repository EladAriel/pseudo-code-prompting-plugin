---
description: Integrate pseudo-code processing with Ralph Loop for automated implementation
argument-hint: [query]
---

# Ralph Process Command

Analyzes query complexity, runs complete-process pipeline, generates completion criteria, and launches Ralph Loop with optimized parameters for automated iterative implementation.

## Usage

```bash
/ralph-process <your implementation request>
```

## What This Command Does

1. **Runs complete-process pipeline** (transform → validate → optimize)
2. **Analyzes complexity** from validation report
3. **Estimates iterations** needed (20/40/80 based on complexity)
4. **Generates completion promise** from critical requirements
5. **Launches Ralph Loop** with optimized prompt and parameters

The Ralph Loop will then iterate on implementation until the completion promise is fulfilled or maximum iterations are reached.

## Examples

### Simple Task
```bash
/ralph-process "Add a dark mode toggle to the settings page"
```
Expected: ~20 iterations

### Medium Task
```bash
/ralph-process "Implement user registration with email validation"
```
Expected: ~40 iterations

### Complex Task
```bash
/ralph-process "Build a payment processing endpoint with Stripe integration"
```
Expected: ~80 iterations

## When to Use

**Use /ralph-process when:**
- You want end-to-end automated implementation
- Task requires multiple refinement cycles
- You want automatic complexity-based planning
- You need completion criteria generated automatically

**Use /complete-process instead when:**
- You only need query optimization
- You want to review before implementing
- You plan to implement manually

**Use /ralph-loop directly when:**
- You already have an optimized query
- You know exact iteration count needed
- You have specific completion criteria ready

## Technical Details

This command invokes the `ralph-process-integration` skill which orchestrates:
- **complete-process-orchestrator** skill for query optimization
- **ralph-loop** plugin for iterative implementation

The skill uses a rule-based complexity scoring algorithm:
- **Simple (0-25 points):** 20 iterations
- **Medium (26-60 points):** 40 iterations
- **Complex (61+ points):** 80 iterations

Scoring factors: warnings (×2), critical issues (×5), edge cases (×3), security (+10), error handling (+5)

## Notes

- Ralph Loop will run continuously until promise fulfilled or max iterations reached
- You can cancel anytime with `/cancel-ralph`
- The completion promise is generated from critical requirements in validation report
- All progress is visible in the output with step-by-step status updates
