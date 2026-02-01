# Memory Migration: v1 to v2

Reference guide for understanding how session memory architecture evolved from v1 to v2.

## Key Architecture Changes

### Agent Consolidation (6 Agents → 2 Agents)

| v1 | v2 | Approach |
|----|----|----------|
| 6 specialized agents | 2 focused agents | Agents still memory-aware, but consolidated |
| prompt-analyzer | requirement-structurer (steps 1-2) | Context detection + compression merged into structurer |
| context-compressor | requirement-structurer (step 2) | Auto-compression is step 2 of structurer |
| prompt-transformer | requirement-structurer (step 3) | Transformation is step 3 of structurer |
| prompt-optimizer | requirement-structurer (steps 5-6) | Optimization + bridge is steps 5-6 of structurer |
| requirement-validator | requirement-validator | Unchanged - still validates comprehensively |
| smart-router | Simple hook | Simplified to pattern detection only |

### Memory Integration Point Changes

| v1 | v2 |
|----|----|
| Memory loaded at hook level | Memory loaded at command level |
| 5+ hooks checking memory | 1 hook for pattern detection |
| Complex orchestration logic | Direct command → agent routing |
| Memory updates in multiple places | Centralized updates at command END |

### Hook Distribution vs Command Routing

**v1:** Memory checks distributed across 5+ hooks
```
Hook 1 (auto-detect) → Load memory
Hook 2 (analyze) → Use memory
Hook 3 (transform) → Use memory
Hook 4 (optimize) → Use memory
Hook 5 (finalize) → Update memory
```

**v2:** Single hook for detection, commands handle memory
```
Hook (user-prompt-submit.py) → Detect pattern
                              → Route to command
Command (transform.md) → Load memory
                       → Call agent
                       → Update memory
```

## Memory File Compatibility

**Good News:** v1 and v2 use the SAME memory file schemas.

### activeContext.md
- v1 schema: Preserved ✓
- v2 usage: Same structure, read by all commands
- Migration: No changes needed

### patterns.md
- v1 schema: Preserved ✓
- v2 usage: Same structure, more aggressively used for pattern matching
- Migration: No changes needed

### progress.md
- v1 schema: Preserved ✓
- v2 usage: Same structure, used for validation learnings + optimization
- Migration: No changes needed

**Result:** v1 memory files work seamlessly with v2 agents. No migration script needed.

## Integration Point Migration

### v1 Memory Integration

v1 agents had deep memory awareness:
```
requirement-analyzer:
  - Load patterns for known ambiguities
  - Update patterns with new ambiguities

prompt-transformer:
  - Load user preferences for naming
  - Load patterns for domain patterns
  - Update patterns with discovered patterns

prompt-optimizer:
  - Load patterns for security patterns
  - Load progress for optimization history
  - Update progress with optimization results

requirement-validator:
  - Load patterns for validation patterns
  - Load progress for validation history
  - Update progress with validation learnings
```

### v2 Memory Integration

v2 consolidates into 2 agents with clearer integration:

**requirement-structurer:**
- Step 1-6: Load and apply memory at each step
- Single update cycle at END (all 3 files)
- Clear phase: Load → Transform → Update

**requirement-validator:**
- Step 1-2: Load patterns + progress
- Update cycle at END (patterns + progress primarily, activeContext secondarily)
- Clear validation: Proactive checks + report

## What v2 Does Better With Memory

### 1. Proactive Issue Detection

v2 memory learns validation failures and catches them earlier:

```
v1: Issue detected in validation phase
v2: Issue detected proactively in optimization phase (using learned patterns)
    → Earlier feedback to user
```

### 2. Compression Preference Tracking

v2 learns user's compression style:

```
v1: Compression preferences optional, context-compressor aware
v2: Compression preferences tracked in activeContext, applied in step 2
    → More consistent compression across sessions
```

### 3. Context Auto-Reset on Project Switch

v2 automatically detects project changes:

```
v1: User has to manually clear context when switching projects
v2: Hook detects project path change → auto-reset activeContext
    → Prevents stale preferences from other projects
```

### 4. Unified Memory Updates

v2 updates all memory files in one coordinated step:

```
v1: Each agent updates memory independently
    → Potential inconsistencies
v2: Command orchestrates single update cycle
    → All 3 files updated consistently
```

## Migration Checklist

If upgrading from v1 to v2:

- [ ] v1 memory files (activeContext.md, patterns.md, progress.md) automatically work with v2
- [ ] No schema changes needed
- [ ] No migration script required
- [ ] v2 SKILL.md documentation references v2 agents (requirement-structurer, requirement-validator)
- [ ] v2 commands (transform.md, validate.md) have memory sections
- [ ] v2 ARCHITECTURE.md explains unified memory integration

## No Breaking Changes

**Important:** v1 → v2 memory migration is **completely backwards compatible**.

- Existing memory files work unchanged
- Same 3-file schema
- Same file locations (`.claude/pseudo-code-prompting/`)
- Same permission-free operations (Read/Edit/Write only)
- Same project context auto-reset strategy

**What happens:**
1. v2 commands read existing v1 memory files
2. v1 patterns applied to v2 transformations
3. v1 validation learnings used by v2 validator
4. New v2 learnings added to same memory files
5. Both versions can read the same memory

## Reference: v1 Agent Purposes (Historical)

For understanding what v1 agents did (all now consolidated into v2):

### prompt-analyzer (v1)
- Analyzed requirement for ambiguities
- Identified missing specifications
- Extracted key intent and parameters

### context-compressor (v1)
- Compressed verbose requirements
- Preserved technical details
- Removed redundant explanations

### prompt-transformer (v1)
- Converted to PROMPTCONVERTER format
- Applied naming conventions
- Extracted constraints as parameters

### prompt-optimizer (v1)
- Added standard parameters (timeout, retry, cache)
- Applied tech stack conventions
- Included error handling

### requirement-validator (v1)
- Validated pseudo-code for completeness
- Checked security requirements
- Identified missing parameters

### smart-router (v1)
- Routed user input to correct skill
- Complex orchestration logic
- Multiple decision points

## Why v2 Simplified Architecture

### Problem v1 Had
- 5+ hooks running sequentially
- Complex state management across hooks
- Multiple agents doing overlapping work
- Hard to maintain and debug

### Solution v2 Provides
- 1 hook for pattern detection
- Direct command → agent routing
- Consolidated agents (6 → 2)
- Clear responsibility boundaries
- 60-70% less code

### Memory Benefit
v2's simplified architecture makes memory integration clearer and more reliable:
- Single load/update cycle (not distributed)
- Clear phase boundaries (Load → Process → Update)
- Consistent memory state across pipeline
- Easier to add new commands with memory support

## Lessons from v1 → v2 Evolution

### What Worked Well in v1 Memory
- 3-file structure (perfect)
- Project context auto-reset strategy (excellent)
- Permission-free operations pattern (excellent)
- Schema design (works unchanged in v2)

### What v2 Improved
- Simplified memory loading (command-level vs hook-level)
- Clearer agent consolidation
- Proactive issue detection from learned patterns
- Consistent update cycle

### Key Principles Preserved
- Memory is optional but valuable
- Memory files permission-free (Read/Edit/Write)
- Memory survives conversation compaction
- Memory learnings accumulate over time

---

**Migration Status:** ✓ Complete. v1 memory files work with v2 agents out of the box.
