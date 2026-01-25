# Plugin Architecture

**Read time: 2 minutes**

## Overview
The plugin transforms natural language into production-ready pseudo-code through a multi-agent pipeline with context-aware project analysis.

## End-to-End Flow

```mermaid
flowchart TD
    A[User Request] --> B{Hook:<br/>user-prompt-submit}
    B -->|Implementation keywords| C[Hook:<br/>context-aware-tree-injection]
    C --> D[Scan Project<br/>Structure]
    D --> E[Inject PROJECT_TREE<br/>Context]
    B -->|Direct command| F[Command Router]
    E --> F

    F --> G{Which Command?}

    G -->|/smart| EV[Eval Router]
    G -->|/complete-process| H[Complete Pipeline]
    G -->|/transform-query| I[Transform Agent]
    G -->|/compress-context| J[Compress Agent]
    G -->|/validate-requirements| K[Validate Agent]
    G -->|/optimize-prompt| L[Optimize Agent]
    G -->|/context-aware-transform| M[Context Agent]

    EV -->|Sub-command| H
    EV -->|Sub-command| I
    EV -->|Sub-command| J
    EV -->|Sub-command| K
    EV -->|Sub-command| L

    H --> I
    I --> N[Pseudo-Code]
    H --> K
    K --> O[Validation Report]
    H --> L
    L --> P[Optimized Output]

    J --> N
    M --> N

    P --> Q{Hook:<br/>post-transform-validation}
    Q --> R[Final Output]

    style B fill:#9C27B0
    style C fill:#9C27B0
    style Q fill:#9C27B0
    style H fill:#4CAF50
    style I fill:#2196F3
    style K fill:#FF9800
    style L fill:#F44336
    style R fill:#4CAF50
```

## Component Layers

### Layer 1: Hooks (Auto-Triggered)
| Hook | Trigger | Purpose |
|------|---------|---------|
| `user-prompt-submit` | User input | Detects commands and keywords |
| `context-aware-tree-injection` | Keywords: implement, create, add | Scans project, injects structure |
| `context-compression-helper` | Input >100 words | Suggests compression |
| `post-transform-validation` | After transformation | Auto-validates output |

### Layer 2: Commands (User-Invoked)
| Command | Purpose | Agents Used | Workflow |
|---------|---------|-------------|----------|
| **`/smart`** (NEW) | **Smart router with intelligent context caching** | **smart-router** | **Routes to any sub-command, reuses cached context (40-70% token savings)** |
| `/complete-process` | Full automated pipeline | transformer → validator → optimizer | Fully automated chain with TODO generation |
| `/transform-query` | Basic transformation | transformer | Single step |
| `/compress-context` | Reduce verbosity | compressor | Single step |
| `/validate-requirements` | Quality check | validator | Single step |
| `/optimize-prompt` | Enhance specs | optimizer | Single step |
| `/context-aware-transform` | Architecture-aware | analyzer → transformer | Two-step process |

### Layer 3: Agents (Processing)
| Agent | Specialization | Input → Output |
|-------|----------------|----------------|
| **`smart-router`** (NEW) | **Meta-routing with context reuse** | **Command → Routed sub-command** |
| `prompt-transformer` | NL → pseudo-code | Text → Function syntax |
| `context-compressor` | Token reduction | Verbose → Concise |
| `requirement-validator` | Quality assurance | Pseudo-code → Report |
| `prompt-optimizer` | Enhancement | Basic → Production-ready |
| `prompt-analyzer` | Structure analysis | Project tree → Patterns |

### Layer 4: Skills (Capabilities)
| Skill | Knowledge Base | Loaded When |
|-------|----------------|-------------|
| **`smart-router`** (NEW) | **Command routing, context caching, token optimization** | **When /smart command invoked** |
| `prompt-structurer` | PROMPTCONVERTER methodology | Transform operations |
| `requirement-validator` | Security/validation checklists | Validation operations |
| `prompt-optimizer` | Enhancement patterns | Optimization operations |
| `context-compressor` | Compression techniques | Large inputs |

## Data Flow

### Example: Complete Process Command (Automated Chain)
```mermaid
sequenceDiagram
    participant U as User
    participant H as Hooks
    participant O as Orchestrator
    participant A1 as Transform Agent
    participant A2 as Validate Agent
    participant A3 as Optimize Agent
    participant S as Skills

    U->>H: "implement JWT auth"
    H->>H: Detect "implement" keyword
    H->>H: Scan project structure
    H->>O: Inject PROJECT_TREE context

    Note over O: AUTOMATED CHAIN STARTS

    O->>A1: Transform with context
    A1->>S: Load prompt-structurer
    S-->>A1: PROMPTCONVERTER rules
    A1-->>O: Pseudo-code + NEXT_AGENT: validator

    Note over O: Auto-invokes next agent (no stop)

    O->>A2: Validate pseudo-code
    A2->>S: Load requirement-validator
    S-->>A2: Validation checklists
    A2-->>O: Validation report + NEXT_AGENT: optimizer

    Note over O: Auto-invokes next agent (no stop)

    O->>A3: Optimize pseudo-code
    A3->>S: Load prompt-optimizer
    S-->>A3: Enhancement patterns
    A3-->>O: Optimized output + TODO_LIST + WORKFLOW_CONTINUES: NO

    Note over O: Chain complete

    O->>O: Generate implementation TODOs
    O->>H: Post-transform hook
    H-->>U: Optimized function + TODOs
```

## Directory Structure

```
pseudo-code-prompting-plugin/
├── agents/                      # Processing engines
│   ├── smart-router.md
│   ├── prompt-transformer.md
│   ├── requirement-validator.md
│   ├── prompt-optimizer.md
│   ├── prompt-analyzer.md
│   └── context-compressor.md
│
├── commands/                    # User-facing commands
│   ├── smart.md
│   ├── complete-process.md
│   ├── transform-query.md
│   ├── compress-context.md
│   ├── validate-requirements.md
│   ├── optimize-prompt.md
│   └── context-aware-transform.md
│
├── skills/                      # Capability definitions
│   ├── smart-router/
│   │   ├── SKILL.md
│   │   └── capabilities.json
│   ├── prompt-structurer/
│   │   ├── capabilities.json
│   │   ├── SKILL.md
│   │   └── references/         # Knowledge base
│   ├── requirement-validator/
│   ├── prompt-optimizer/
│   ├── complete-process-orchestrator/
│   ├── context-compressor/
│   ├── session-memory/
│   ├── feature-dev-enhancement/
│   └── prompt-analyzer/
│
├── hooks/                       # Auto-triggered logic
│   ├── core/
│   │   └── user-prompt-submit.py
│   ├── tree/
│   │   ├── context-aware-tree-injection.py
│   │   └── get_context_tree.py
│   ├── compression/
│   │   └── context-compression-helper.py
│   └── validation/
│       └── post-transform-validation.py
│
└── docs/                        # Documentation (you are here)
    ├── complete-process.md
    ├── transform-query.md
    └── ARCHITECTURE.md
```

## Key Architectural Patterns

### 1. Progressive Loading
Skills load on-demand based on context, not all at once. Reduces memory and token usage.

### 2. Hook-Driven Context
Hooks automatically inject project structure, user can focus on request not context gathering.

### 3. Automated Agent Chaining
Agents communicate via structured signals (`WORKFLOW_CONTINUES`, `NEXT_AGENT`) enabling fully automated pipeline execution without user intervention.

### 4. Context Window Optimization
Complete-process removes intermediate outputs, keeping only query + final result (60-80% token reduction).

### 5. Automatic TODO Generation
The optimizer extracts implementation tasks from optimized pseudo-code parameters, creating actionable TODOs via TodoWrite tool.

### 6. Memory Persistence
Session memory survives conversation compaction:
- `.claude/pseudo-code-prompting/activeContext.md` - Current transformations
- `.claude/pseudo-code-prompting/patterns.md` - Learned patterns
- `.claude/pseudo-code-prompting/progress.md` - Quality metrics

## Integration Points

### With Claude Code
- Uses Claude Code's auto-discovery system
- Skills auto-load based on capabilities.json
- Commands registered via frontmatter metadata
- Hooks execute on specified triggers

### With Other Plugins
- Integrates with `feature-dev` workflow
- Outputs compatible with code generation tools
- Can chain with other transformation plugins

## Token Efficiency

| Operation | Tokens Without Plugin | With Plugin | Savings |
|-----------|----------------------|-------------|---------|
| Verbose requirement | 4,200 | 850 | 80% |
| Transform + validate + optimize | 8,000 | 1,600 | 80% |
| Complete process (with cleanup) | 10,000 | 2,000 | 80% |
| Context-aware transform | 6,000 | 1,200 | 80% |

## Performance Characteristics

- **Transform only**: 5-15 seconds
- **Complete process**: 30-90 seconds
- **Context-aware mode**: +5-10 seconds (project scan)
- **Compression**: 10-20 seconds (60-95% size reduction)

## Why This Architecture?

1. **Separation of Concerns** - Hooks, commands, agents, skills each have clear roles
2. **Composability** - Mix and match agents for different workflows
3. **Context-Aware** - Automatic project analysis, not manual context gathering
4. **Token-Efficient** - Progressive loading, output cleanup, compression
5. **Quality-Focused** - Validation and optimization built into pipeline
6. **Developer-Friendly** - Real paths, existing patterns, integration points

## Next Steps

- See individual command docs for usage details
- Check [README.md](../README.md) for installation
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) to extend the plugin
