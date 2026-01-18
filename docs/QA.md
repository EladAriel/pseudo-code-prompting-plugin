# Q&A

## How does the plugin gather context?

The plugin uses a sophisticated **progressive loading system** that loads context incrementally based on relevance, dramatically reducing token usage while maintaining full functionality.

### 1. Auto-Discovery & Semantic Matching

When you make a request, Claude Code:

1. **Scans all skills** by reading their `capabilities.json` files (Tier 1)
2. **Matches triggers** against your request using keywords and regex patterns
3. **Scores relevance** to determine which skills are needed
4. **Loads only relevant skills** for your specific task

**Example:**

```text
Your request: "Validate this API endpoint specification"

Scanning:
  - prompt-structurer/capabilities.json (110 tokens) → Score: 30% (transform != validate)
  - requirement-validator/capabilities.json (108 tokens) → Score: 95% (validate, API, endpoint match!)
  - context-compressor/capabilities.json (95 tokens) → Score: 10% (compress != validate)

Decision: Load requirement-validator skill only
```

### 2. Progressive Loading (4-Tier Architecture)

Once a skill is selected, context loads in stages:

**Tier 1: Discovery** (`capabilities.json` - ~100 tokens)

```json
{
  "skill_id": "requirement-validator",
  "triggers": {
    "keywords": ["validate", "verify", "check", "review"],
    "patterns": ["validate.*requirements", "check.*completeness"]
  },
  "provides": ["validation_report", "security_audit", "completeness_check"]
}
```

**Tier 2: Overview** (`SKILL.md` - ~400 tokens)

```markdown
# Requirement Validator

Validates pseudo-code requirements for completeness, security, and edge cases.

## Process
1. Parse pseudo-code structure
2. Check for critical issues (auth, validation, errors)
3. Identify warnings (rate limiting, CORS)
4. Detect edge cases (nulls, concurrency)
5. Generate structured report with recommendations
```

**Tier 3: Specific Patterns** (`references/*.md` - ~280 tokens each, loaded on-demand)

```markdown
# API Endpoint Validation Checklist

## Critical Requirements
- [ ] Authentication specified (auth, roles, permissions)
- [ ] Request schema defined (required fields, types, validation)
- [ ] Error response codes (400, 401, 403, 404, 500)

## Security Requirements
- [ ] Rate limiting (prevent abuse)
- [ ] Input sanitization (prevent injection attacks)
...
```

**Tier 4: Templates** (`templates/*.md` - loaded only for generation)

- Only loaded when generating structured output
- Not needed for validation tasks

### 3. Example: Full Workflow Token Usage

**Scenario:** Transform verbose requirements → Validate → Optimize

**Without Progressive Loading (Traditional Approach):**

```text
Load all skills upfront:
  - prompt-structurer: 800 tokens
  - prompt-analyzer: 650 tokens
  - requirement-validator: 800 tokens
  - prompt-optimizer: 700 tokens
  - context-compressor: 600 tokens
  - feature-dev-enhancement: 450 tokens
  + All references: ~2,000 tokens
Total: ~6,000 tokens loaded before even starting!
```

**With Progressive Loading (Plugin Approach):**

```text
Step 1: Transform (200 tokens)
  - Load: prompt-structurer/capabilities.json (110 tokens)
  - Load: prompt-structurer/SKILL.md (400 tokens)
  - Load: references/common-patterns.md (280 tokens on-demand)
  Subtotal: 790 tokens

Step 2: Validate (700 tokens)
  - Load: requirement-validator/capabilities.json (108 tokens)
  - Load: requirement-validator/SKILL.md (650 tokens)
  - Load: references/validation-checklists.md (280 tokens)
  Subtotal: 1,038 tokens

Step 3: Optimize (400 tokens)
  - Load: prompt-optimizer/capabilities.json (95 tokens)
  - Load: prompt-optimizer/SKILL.md (700 tokens)
  Subtotal: 795 tokens

Total: ~2,130 tokens (64% savings vs 6,000 tokens)
```

### 4. How Hooks Inject Context

Hooks add context dynamically based on events:

**UserPromptSubmit Hook:**

```bash
# When you type: "Create user authentication"

Hook detects keywords → Injects:
```

```text
🔍 Detected transformation request
Loading prompt-structurer skill...
Applying PROMPTCONVERTER methodology
```

**PostToolUse Hook:**

```bash
# After you transform requirements

Hook detects Write/Edit tool → Injects:
```

```text
✓ Transformation complete
Running validation...
[Validation results appear automatically]
```

### 5. Smart Reference Loading

References are loaded **just-in-time** based on what's needed:

#### Example: Validating different feature types

```text
API Endpoint validation:
  → Loads: references/validation-checklists.md (API section)
  → Skips: Database, Authentication, Frontend sections

Database Schema validation:
  → Loads: references/validation-checklists.md (Database section)
  → Skips: API, Authentication, Frontend sections

Authentication System validation:
  → Loads: references/validation-checklists.md (Auth section)
  → Loads: references/common-issues.md (Security patterns)
  → Skips: API, Database, Frontend sections
```

### 6. Token Efficiency Comparison

| Scenario                                                   | Traditional  | Progressive  | Savings |
| ---------------------------------------------------------- | ------------ | ------------ | ------- |
| Simple transform                                           | 3,000 tokens | 790 tokens   | 74%     |
| Transform + validate                                       | 5,500 tokens | 1,828 tokens | 67%     |
| Full workflow (compress + transform + validate + optimize) | 8,000 tokens | 2,918 tokens | 64%     |
| Just validation                                            | 3,000 tokens | 1,038 tokens | 65%     |

### 7. How Skills Reference Each Other

Skills can reference other skills for composition:

**Example: `prompt-optimizer` referencing `requirement-validator`**

```markdown
# In prompt-optimizer/SKILL.md:

After optimization, consider using the `requirement-validator` skill
to ensure all added parameters meet security and completeness standards.
```

When this happens:
1. Claude sees the reference to `requirement-validator`
2. Loads its `capabilities.json` (108 tokens)
3. Loads its `SKILL.md` (650 tokens)
4. Applies validation to optimized output

**Total additional cost:** 758 tokens (only when cross-skill validation is needed)

---

**Key Takeaway:** Progressive loading means you only pay (in tokens) for what you actually use, when you use it. This makes the plugin extremely efficient while maintaining comprehensive functionality.
