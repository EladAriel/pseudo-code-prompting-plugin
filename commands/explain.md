---
name: Explain My Project
description: Generate a comprehensive technical explanation of your project including architecture, structure, technologies, decisions, and lessons learned. Perfect for documentation, onboarding, and knowledge sharing.
arguments:
  - name: project
    description: Optional project name or description (plugin will prompt if not provided)
    required: false
when-to-use: |
  - When you want to document your project for team onboarding
  - When you need to explain your project to stakeholders or other teams
  - When you want to preserve architectural knowledge and lessons learned
  - When you need to create engaging technical documentation
  - When analyzing a codebase you're unfamiliar with
examples:
  - "Explain my project: payment processing system"
  - "Generate EXPLAIN.md for the authentication module"
  - "I need to document our API architecture"
---

# Explain My Project

Generates a comprehensive, engaging technical explanation of your project that covers architecture, structure, technologies, decisions, and lessons learned.

## What You Get

✓ **Technical Architecture** - How your system is designed and why
✓ **Codebase Structure** - How files/modules connect and relate
✓ **Technology Decisions** - Why you chose each technology
✓ **Lessons Learned** - Bugs fixed, pitfalls avoided, best practices
✓ **Engaging Writing** - Uses analogies and anecdotes, not boring docs

## Output Format

A file: `EXPLAIN_{project_name}.md`

```markdown
# EXPLAIN: [Project Name]

> An engaging technical explanation covering architecture, structure,
> technologies, decisions, and lessons learned.

## Part 1: What This Project Actually Is
[Clear explanation with analogies]

## Part 2: Architecture Deep Dive
[Technical architecture with examples]

## Part 3: Technology Decisions & Why
[Decision rationale with lessons]

## Part 4: Codebase Structure
[How files/modules connect]

## Part 5: Key Lessons & Pitfalls
[Bugs encountered, fixes, best practices]

## Part 6: Why This Architecture?
[Design justification]

## Conclusion
[Summary and key takeaways]
```

## Usage

Simply say:
> **Explain my project**

Or optionally be more specific:
> **Explain my project:** Payment processing system that handles Stripe integration, webhook callbacks, transaction storage, and refund management. Focus on webhook handling and error recovery.

Get back:
```
EXPLAIN_payment_processing.md ✓
With comprehensive technical explanation
```

## Key Features

### Comprehensive Analysis
- **Architecture**: System design, components, data flow
- **Structure**: Codebase organization, module relationships
- **Technologies**: Why each choice was made
- **Decisions**: Technical tradeoffs and alternatives considered
- **Lessons**: Bugs fixed, pitfalls avoided, best practices discovered

### Engaging Writing Style
- Uses analogies to explain complex concepts
- Includes anecdotes and real examples
- Tells the story of why decisions were made
- Not boring technical documentation
- Memorable and educational

### Perfect For
- Team onboarding (new developers learn context)
- Knowledge preservation (capture architectural wisdom)
- Design reviews (explain decisions to stakeholders)
- Internal documentation (share knowledge across teams)
- Project retrospectives (document lessons learned)

## Typical Sections Included

### What This Project Actually Is
Clear, accessible explanation of project purpose and scope. Uses analogies.

Example: "Think of our payment system like a bank branch. It accepts
deposits (charges), manages accounts, processes withdrawals (refunds),
and keeps a ledger (audit trail)."

### Architecture Deep Dive
Technical architecture with diagrams described in text. Shows how components interact.

Example: API Gateway → Processing Engine → Storage → Webhook Handler

### Technology Decisions
Why specific technologies were chosen. Alternative approaches considered.

Example: "We chose PostgreSQL over MongoDB because transactions and
ACID guarantees were critical for payment data integrity."

### Codebase Structure
How the project is organized. Why files are structured this way.

Example: `/handlers` for API endpoints, `/services` for business logic,
`/models` for data structures.

### Lessons & Pitfalls
Bugs encountered, how they were fixed, how to avoid them.

Example: "We initially didn't handle webhook retries properly. This taught us
to implement idempotency keys. Now every payment operation is idempotent."

### Best Practices Discovered
Patterns that worked well. Anti-patterns to avoid.

Example: "Don't process payments synchronously. Use async queues.
We learned this the hard way during Black Friday 😅"

## Tips for Great Explanations

**Be Specific**
- Concrete examples, not abstract generalities
- Actual code structure, not theoretical diagrams
- Real bugs and fixes, not hypothetical problems

**Use Analogies**
- Explain complex systems simply
- "Like a..." comparisons help understanding
- Makes concepts memorable

**Include Anecdotes**
- How you discovered a bug in production
- Why a particular decision seemed good but wasn't
- How a technology choice saved the day
- Makes documentation engaging and relatable

**Preserve Wisdom**
- Lessons that took weeks/months to learn
- Pitfalls that wasted engineering time
- Best practices that improved quality
- Future-proofs the project against repeated mistakes

## Example Output

See `skills/project-explanation/` for technical writing patterns and templates.

## See Also

- **Transform to pseudocode:** - Convert requirements to pseudo-code
- **Validate my pseudocode:** - Validate specifications
- `skills/project-explanation/SKILL.md` - Technical writing patterns
