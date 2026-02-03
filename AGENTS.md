# AGENTS.md - Pseudo-Code Prompting Orchestration

**IMPORTANT:** Never bypass the router. It is the system.

[Index] |root: ./
|routing: hooks/{workflow-coordinator,user-prompt-submit}.py
|context-protection: hooks/{post-tool-use,context-merger,post-cc10x-context-write}.py
|agents: agents/{requirement-structurer,requirement-validator}.md
|skills: skills/{prompt-structurer,requirement-validator,session-memory}
|commands: commands/{transform,validate}.md

---

## Routing Decision Tree

| Command Pattern | Agent | Workflow | Output |
|---|---|---|---|
| `Run transform: ...` | requirement-structurer | 6-step transform | Production pseudo-code + bridge |
| `Run validate: ...` | requirement-validator | Validation | Report with severity |
| Other | None | Pass through | Allow cc10x |

---

## Context Protection System (v2.1.3)

**Three-layer protection prevents specification loss when cc10x writes to activeContext.md:**

**Layer 1: Markers** - `post-tool-use.py` adds `## Specification` section with `PSEUDO-CODE-CONTEXT` preservation markers

**Layer 2: Merging** - `context-merger.py` intelligently merges cc10x and pseudo-code contexts

**Layer 3: Recovery** - `post-cc10x-context-write.py` detects and restores lost specifications

**Hook execution:** `post-tool-use.py` (high priority) → `post-cc10x-context-write.py` (normal priority)

---

## Bridge to cc10x (Handoff Protocol)

After transform:
1. PostToolUse hook saves `specification.md`
2. Updates `activeContext.md` with specification reference
3. Bridge question shown: "Ready to implement with cc10x?"

**Answer YES:**
- cc10x loads specification from activeContext
- component-builder uses spec as primary input
- TDD workflow: RED → GREEN → REFACTOR
- Specification persists across sessions ✓

**Answer NO:**
- Keep pseudo-code only
- Specification saved for later use

---

## Workflow Coordination (Prevent cc10x Hijacking)

**Problem:** cc10x router could hijack before pseudocode completes.

**Solution:** `workflow-coordinator.py` runs with `priority=high`:
- Detects "Run transform:" and "Run validate:" patterns
- Emits `PSEUDOCODE_PLUGIN_ACTIVE=true` and `BLOCK_CC10X_ROUTER=true`
- Protects pseudocode execution until completion
- Saves state to `.claude/pseudo-code-prompting/workflow-state.json`

**Result:** Transform completes uninterrupted. User controls bridge via YES/NO answer.

---

## Files

**Hooks:**
- `workflow-coordinator.py` - Detect transform/validate commands (UserPromptSubmit)
- `user-prompt-submit.py` - Route to correct agent
- `post-tool-use.py` - Save spec + add markers (PostToolUse)
- `post-cc10x-context-write.py` - Recover lost specs (PostToolUse)
- `context-merger.py` - Utility for context merging

**Output Files:**
- `.claude/pseudo-code-prompting/specification.md` - Persisted specification
- `.claude/pseudo-code-prompting/workflow-state.json` - Coordination state
- `.claude/cc10x/activeContext.md` - Context with spec reference

---

## Debugging

```bash
DEBUG=1 Run transform: Your requirement

# Check workflow state
cat .claude/pseudo-code-prompting/workflow-state.json

# Check specification
cat .claude/pseudo-code-prompting/specification.md

# Check context
cat .claude/cc10x/activeContext.md
```

See `CHANGELOG.md` for version history and `docs/bridge-to-cc10x.md` for detailed docs.
