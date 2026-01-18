# Plugin Architecture

## Directory Structure

This plugin follows Claude Code's official plugin structure with auto-discovery:

```
pseudo-code-prompting-plugin/
├── plugin.json                 # Plugin manifest (minimal)
├── skills/                     # 6 skills with progressive loading
│   ├── context-compressor/
│   │   ├── capabilities.json   # Tier 1: Discovery (90-110 tokens)
│   │   ├── SKILL.md           # Tier 2: Overview (300-800 tokens)
│   │   └── references/         # Tier 3: Specific patterns (90-300 tokens)
│   ├── prompt-structurer/
│   ├── prompt-analyzer/
│   ├── prompt-optimizer/
│   ├── requirement-validator/
│   └── feature-dev-enhancement/
├── agents/                     # 5 agent definitions
│   ├── prompt-analyzer.md
│   ├── context-compressor.md
│   ├── prompt-transformer.md
│   ├── prompt-optimizer.md
│   └── requirement-validator.md
├── commands/                   # 4 command definitions
│   ├── transform-query.md
│   ├── validate-requirements.md
│   ├── optimize-prompt.md
│   └── compress-context.md
└── hooks/                      # 3 event hooks
    ├── hooks.json             # Hook registration
    ├── user-prompt-submit.sh
    ├── context-compression-helper.sh
    └── post-transform-validation.sh
```

## Progressive Loading System

Skills use a 4-tier progressive loading architecture for token efficiency:

**Tier 1: Discovery** (`capabilities.json`) - 90-110 tokens
- Quick relevance check
- Trigger patterns and keywords
- Loaded for every skill search

**Tier 2: Overview** (`SKILL.md`) - 300-800 tokens
- Methodology and process steps
- Loaded when skill is confirmed relevant

**Tier 3: Specific** (`references/*.md`) - 90-300 tokens each
- Domain-specific patterns and checklists
- Loaded on-demand when needed

**Tier 4: Generation** (`templates/*.md`) - 150-400 tokens each
- Boilerplate and format examples
- Loaded when generating structured output

**Token Efficiency**: 788 tokens (progressive) vs 5,000+ tokens (full load) = 84% savings

## Hook System

Hooks are event-driven automation scripts registered in `hooks/hooks.json`:

**UserPromptSubmit Hooks** (run when user submits input):
- `user-prompt-submit.sh` - Detects transformation keywords, injects context
- `context-compression-helper.sh` - Suggests compression for verbose input (>100 words)

**PostToolUse Hooks** (run after Write/Edit tools):
- `post-transform-validation.sh` - Auto-validates transformed pseudo-code

All hooks use:
- Interactive approval mode (`permissionDecision: "ask"`)
- `${CLAUDE_PLUGIN_ROOT}` for portable paths
- Proper error handling (`set -euo pipefail`)
