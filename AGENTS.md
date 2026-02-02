# AGENTS.md (Pseudo-Code Prompting Orchestration - Always On)

IMPORTANT: Explore project first, then invoke the router.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: Never bypass the router. It is the system.

[Pseudo-Code Prompting v2 Orchestration Index] |root: ./
|router: hooks/{workflow-coordinator,user-prompt-submit}.py
|agents: agents/{requirement-structurer,requirement-validator}.md
|skills: skills/{prompt-structurer,requirement-validator,session-memory}/SKILL.md
|commands: commands/{transform,validate}.md

---

## Routing Decision Tree

| Command Pattern | Agent | Workflow | Output |
|-----------------|-------|----------|--------|
| `Run transform: ...` | requirement-structurer | TRANSFORM (6 steps) | Production-ready pseudo-code + bridge offer |
| `Run validate: ...` | requirement-validator | VALIDATE (2 steps) | Validation report with severity levels |
| Other (contains cc10x keywords) | None | Pass through | Allow cc10x router to proceed |

**Detection:** `workflow-coordinator.py` (priority=high) runs first, then `user-prompt-submit.py` routes command.

---

## Bridge to cc10x (Specification-Driven Handoff Protocol)

After TRANSFORM completes, pseudo-code is **automatically injected** into cc10x's activeContext:

```
AUTOMATIC INJECTION (v2.1.0+):
├─ Specification saved: .claude/pseudo-code-prompting/specification.md
├─ activeContext.md updated:
│   ├─ Current Focus: pseudo-code structure
│   ├─ References: linked to specification
│   └─ Decisions: recorded specification as guide
         ↓
🚀 Ready to implement with cc10x? (Y/n)
```

**Option A: Answer YES**
- Specification already injected into activeContext
- Automatically invokes `/cc10x:cc10x-router`
- cc10x loads memory (finds pseudo-code reference)
- component-builder receives specification as primary input
- TDD workflow starts: RED → GREEN → REFACTOR (per specification)
- **Specification persists** across sessions, compaction, handoffs
- **No ambiguity** - pseudo-code is source of truth

**Option B: Answer NO**
- Pseudo-code returned as-is
- Specification file saved for later reference
- No cc10x invocation
- Keep for documentation, tickets, or manual iteration
- Invoke cc10x separately in next message if desired (specification already in activeContext)

---

## ⚠️ CRITICAL: Prevent cc10x Hijacking

### The Problem
When users invoke pseudocode plugin in messages with cc10x keywords (build, implement, create), **cc10x router hijacks the workflow**:
- Takes over BEFORE pseudocode transform completes
- Creates its own memory files (.claude/cc10x/)
- Asks its own clarifying questions
- **IGNORES pseudocode output** ← THE BUG
- User loses the intermediate specification

### Root Cause
1. **Both plugins trigger** on development keywords
2. **No execution order** enforcement
3. **No handoff protocol** between them
4. **Broader keyword matching** in cc10x causes priority

### The Solution (v2.0.1+)

**Workflow Coordinator Hook (NEW):**
- Runs with `priority: "high"` BEFORE other hooks
- Detects "Run transform:" and "Run validate:" patterns
- Emits signals: `PSEUDOCODE_PLUGIN_ACTIVE=true`, `BLOCK_CC10X_ROUTER=true`
- Saves state to `.claude/pseudo-code-prompting/workflow-state.json`
- Allows pseudocode plugin to complete uninterrupted

**Result:**
```
User: "Run transform: Build a Project Tracker app"
           ↓
Workflow Coordinator (HIGH PRIORITY)
  ├─ Detects pattern
  ├─ Emits blocking signals
  ├─ Protects pseudocode execution
           ↓
Transform Pipeline (UNINTERRUPTED)
  ├─ 6-step pipeline completes
  ├─ Outputs pseudo-code
  ├─ Shows bridge question
           ↓
User Controls Handoff (EXPLICIT)
  ├─ Answer YES → Bridge to cc10x
  ├─ Answer NO → Keep pseudocode only
  └─ No hijacking possible
```

### User Guidance

**✅ CORRECT (Recommended):**
```bash
Run transform: Build a Project Tracker with CAP, HANA, UI5
# Wait for bridge question
# Answer: y (auto-invokes cc10x) OR n (keeps pseudocode only)
```

**✅ CORRECT (Manual Separation with Full Control):**
```bash
# Message 1:
Run transform: Build a Project Tracker
# Answer: n

# Message 2 (separate):
/cc10x:cc10x-router
[paste pseudocode]
```

**❌ ANTI-PATTERN (Now Prevented):**
```bash
# DON'T do this - blocked by workflow coordinator:
Run transform: Build a Project Tracker
/cc10x:cc10x-router
# → Hijacking PREVENTED in v2.0.1+
# → Transform completes normally
```

### Specification Injection Details (v2.1.0+)

**Injection Flow:**
1. Transform pipeline completes (6 steps)
2. Before showing bridge question, injection triggered
3. Specification saved to `.claude/pseudo-code-prompting/specification.md`
4. activeContext.md created/updated with references
5. Bridge question shown with injection confirmation
6. User answers YES/NO

**What Gets Injected into activeContext.md:**

```markdown
## Current Focus
Implementing from pseudo-code specification:

[Pseudo-code summary - first 500 chars]
... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification.

## References
- Specification: .claude/pseudo-code-prompting/specification.md

## Recent Changes
- Pseudo-code specification generated from requirements

## Decisions
- Use pseudo-code as primary specification
- Validate implementation against specification
```

**Result:** When cc10x starts, it loads activeContext and finds pseudo-code as context.

### Hook Configuration (`hooks/hooks.json`):
```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/workflow-coordinator.py",
          "statusMessage": "Coordinating workflow to prevent cc10x hijacking...",
          "timeout": 5,
          "priority": "high"  // ← RUNS FIRST
        },
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/user-prompt-submit.py",
          "statusMessage": "Checking for pseudo-code transformation commands...",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Coordination Signals:**
- `PSEUDOCODE_PLUGIN_ACTIVE=true` → Plugin is running
- `BLOCK_CC10X_ROUTER=true` → cc10x should wait/skip
- `WORKFLOW_PRIORITY=pseudocode-plugin` → Transform takes priority
- `WORKFLOW_HANDOFF_EXPECTED=true` → Bridge handoff will follow

**State File** (`.claude/pseudo-code-prompting/workflow-state.json`):
```json
{
  "workflow_active": true,
  "active_plugin": "pseudo-code-prompting",
  "command_type": "transform",
  "cc10x_blocked": true,
  "bridge_expected": true,
  "timestamp": "2026-02-02T12:34:56.789123"
}
```

### Debugging

Enable debug output:
```bash
DEBUG=1 Run transform: Your requirement
```

Check workflow state:
```bash
cat .claude/pseudo-code-prompting/workflow-state.json
```

### Changelog

See `CHANGELOG.md` for v2.0.1 release notes (workflow coordination + hijacking prevention).