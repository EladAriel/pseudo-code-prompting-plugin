# Workflows

## 1. Full Transformation Workflow (900 tokens)

```
Analyze → Transform → Validate
```

**Use when:** Starting from natural language requirements
**Process:**
1. **Prompt Analyzer** detects ambiguities, scores complexity
2. **Prompt Transformer** converts to pseudo-code
3. **Requirement Validator** checks completeness, security

**Output:** Validated, implementation-ready pseudo-code

## 2. Quick Transform (200 tokens)

```
Transform
```

**Use when:** Requirements are clear and simple
**Process:**
1. **Prompt Transformer** directly converts to pseudo-code

**Output:** Basic pseudo-code (may need manual validation)

## 3. Optimize and Validate (700 tokens)

```
Optimize → Validate
```

**Use when:** You have pseudo-code that needs enhancement
**Process:**
1. **Prompt Optimizer** adds missing parameters, security, validation
2. **Requirement Validator** verifies implementation-readiness

**Output:** Enhanced, validated pseudo-code

## 4. Compress, Transform, Validate (1000 tokens)

```
Compress → Transform → Validate
```

**Use when:** Requirements are verbose (>100 words)
**Process:**
1. **Context Compressor** reduces to 5-40% of original size
2. **Prompt Transformer** structures into pseudo-code
3. **Requirement Validator** ensures nothing was lost

**Output:** Compressed, validated pseudo-code

## Progressive Loading Architecture

Skills use 4-tier progressive loading for token efficiency:

| Tier | Files | Token Budget | When Loaded |
|------|-------|--------------|-------------|
| **Tier 1: Discovery** | `capabilities.json` | 100-110 | Always (relevance matching) |
| **Tier 2: Overview** | `SKILL.md` | 300-800 | Skill confirmed relevant |
| **Tier 3: Specific** | `references/*.md` | 90-300 each | Need specific pattern/checklist |
| **Tier 4: Generate** | `templates/*` | 150-400 each | Code generation |

### Example: API Endpoint Validation

```
User Query: "Validate my API endpoint requirements"

Loading Sequence:
1. Tier 1: Load requirement-validator/capabilities.json (105 tokens)
   → Matched: validation, API, endpoint keywords

2. Tier 2: Load requirement-validator/SKILL.md (650 tokens)
   → Understand validation process, severity levels

3. Tier 3: Load references/validation-checklists.md (280 tokens)
   → Get API-specific checklist (auth, validation, rate limits)

4. Execute: Run validation with focused context

Total: 1,035 tokens (vs. 5,000+ loading everything upfront)
Efficiency: 79% token savings
```
