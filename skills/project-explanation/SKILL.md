# Project Explanation Skill

Generates engaging technical explanations of projects that preserve architectural wisdom and lessons learned.

## What This Skill Does

Provides patterns, templates, and best practices for creating comprehensive technical documentation that:
- Explains complex systems clearly with analogies
- Justifies technology decisions
- Captures lessons learned and pitfalls
- Reads like an engaging essay, not boring documentation
- Preserves architectural knowledge for future engineers

## When to Use

- Creating technical documentation for team onboarding
- Explaining project architecture to stakeholders
- Documenting technology decisions and trade-offs
- Preserving lessons learned from building a system
- Analyzing unfamiliar codebases

## Core Principles

### 1. Clarity Through Analogy

Complex systems become understandable through comparison to familiar concepts.

**Pattern:**
```
"Think of [system] like [familiar thing]. [Familiar thing] does X, Y, Z.
Similarly, [system] does A, B, C to solve [problem]."
```

**Examples:**
- "Think of our cache like a store's back room. Items in the back room are
  grabbed quickly, but eventually expire and need restocking."
- "Our rate limiter is like a traffic light. It lets requests through quickly
  most of the time, but when traffic gets heavy, it queues them up."
- "Message queues are like mailboxes. You drop a letter in, the mailman
  delivers it eventually. You don't wait around for the delivery."

### 2. Lessons Through Anecdotes

People remember stories better than facts. Share how lessons were learned.

**Pattern:**
```
Lesson: [What was learned]
Story: "We discovered this when [situation]. [What happened].
        [How we fixed it]."
Takeaway: [How to apply in future]
```

**Example:**
```
Lesson: Database Migrations Need Careful Planning

Story: "We had a production database with 10 million user records. We wanted
to add a new column with a NOT NULL constraint. We didn't think to make it
nullable first, then backfill. We locked the entire table for 2 hours.
Customers couldn't log in. 😱"

Takeaway: For large tables, always backfill with nullable columns first,
then add constraints. Test on production volume in staging first.
```

### 3. Concrete Examples Over Abstractions

Specific details are more memorable and useful than general principles.

**❌ Avoid:**
> "The system implements error handling best practices"

**✓ Use:**
> "Every HTTP handler catches specific errors and returns appropriate status codes:
> 400 for validation, 401 for auth, 403 for permissions, 500 for server errors.
> We log errors with context (user ID, request ID) to debug production issues."

### 4. Architecture as Story

Explain architecture by describing how data and control flow through the system.

**Pattern:**
```
User → [Component A] → [Component B] → Storage
  ↓                                        ↑
  └─── Response ←─────────────────────────┘

[Component A] receives requests and validates them.
[Component B] processes business logic.
Storage persists results.
Response returns to user.

Key insight: [Why this design matters]
```

### 5. Trade-offs Honestly

Every architecture involves trade-offs. Acknowledge them.

**Pattern:**
```
We chose [Option A] over [Option B] because [reason].
Trade-off: [What we gave up] vs [What we gained].
Constraint: [What made this choice necessary].
Alternative: If [constraint changed], we would [different approach].
```

**Example:**
```
We chose PostgreSQL over MongoDB because transaction support was critical
for payment data integrity.
Trade-off: More complex queries vs guaranteed data consistency.
Constraint: Financial data must never be corrupted, even in edge cases.
Alternative: If we had simple key-value data with no relationships,
we'd use DynamoDB for infinite scalability.
```

## EXPLAIN Document Structure

### Part 1: What This Project Actually Is

**Goal**: 1-2 paragraph overview using an analogy

**Template:**
```markdown
Imagine [familiar analogy]. [System] is similar. It [core purpose] by
[key mechanism]. Just like [analogy detail], [system] [parallel detail].

In practical terms: [concrete example of what it does]
```

**Length**: 200-300 words

### Part 2: Architecture Deep Dive

**Goal**: Explain system design and component interaction

**Template:**
```markdown
## Architecture Overview

The system consists of [N] main components:

1. [Component A] - Role and responsibility
2. [Component B] - Role and responsibility
3. [Component C] - Role and responsibility

## Data Flow

[ASCII diagram or text flow]

User requests → A → B → Storage → Response

Each component has a specific job:
- [Component A] does [X]
- [Component B] does [Y]
- [Component C] does [Z]

## Why This Design

We separated concerns into layers because [reason]:
- Easier to test each layer independently
- Clear responsibilities
- Can replace components without affecting others
```

**Length**: 800-1200 words

### Part 3: Technology Decisions & Why

**Goal**: Justify major technology choices

**Template:**
```markdown
## [Technology Name]

### The Choice
We use [Technology] for [purpose].

### Why We Chose It
1. [Reason 1]: [Explanation with example]
2. [Reason 2]: [Explanation with example]
3. [Reason 3]: [Explanation with example]

### Alternatives Considered
- [Alternative 1]: [Why we didn't choose it]
- [Alternative 2]: [Why we didn't choose it]

### Lesson We Learned
[Anecdote about discovering why this was the right choice]

Example: "We initially considered [other tech], but in production discovered
that [problem]. Switching to [chosen tech] fixed [issue]."
```

**Repeat for each major technology**

**Length**: 1000-1500 words

### Part 4: Codebase Structure

**Goal**: Explain how files/modules are organized

**Template:**
```markdown
## Directory Structure

```
src/
  ├── handlers/
  ├── services/
  ├── models/
  ├── middleware/
  └── utils/
```

## Folder Purposes

### handlers/
Receives HTTP requests and routes them. Handles:
- Input validation
- Calling services
- Formatting responses

Example: `handlers/users.ts` handles GET /users/:id

### services/
Business logic and rules. Handles:
- User validation
- Database queries
- External service calls

Example: `services/UserService.ts` validates and creates users

### models/
Data structures and schema. Defines:
- TypeScript types
- Database schemas
- Validation rules

Example: `models/User.ts` defines user data structure

## Why This Structure

This layered architecture keeps concerns separate:
- Handlers: HTTP concerns
- Services: Business logic
- Models: Data definitions

Each layer can be tested independently.
```

**Length**: 600-900 words

### Part 5: Key Lessons & Pitfalls

**Goal**: Share wisdom learned through building system

**Template:**
```markdown
## Lesson 1: [Title]

### The Problem
[What went wrong, when we discovered it, impact]

### How We Fixed It
[What we changed, how it solved the problem]

### Takeaway
[How to avoid this, apply the lesson to future projects]

---

## Lesson 2: [Title]

[Same structure...]
```

**Include 3-5 major lessons**

**Length**: 800-1200 words

### Part 6: Why This Architecture?

**Goal**: Explain the constraints that shaped design

**Template:**
```markdown
## Constraints That Shaped This Design

### Consistency Over Performance
We chose PostgreSQL with transactions over eventually-consistent NoSQL
because losing money data is worse than slightly slower queries.
Constraint: Financial systems must never have data corruption.

### Latency Over Throughput
We process payments synchronously (user waits for response) instead of
async because users need to know immediately if their payment succeeded.
Constraint: Users expect <500ms response time for payment confirmation.

### Simplicity Over Flexibility
We use a monolith instead of microservices because the added complexity
of distributed systems wasn't justified by our scale.
Constraint: 5 engineers, not 500. Operational simplicity matters.

## If Constraints Changed...

If we didn't care about response time, we'd process payments asynchronously.
If we had 10x the volume, we'd split into microservices.
If we had less important data, we'd use cheaper but riskier datastores.

Architecture is shaped by constraints. When constraints change, architecture should too.
```

**Length**: 400-600 words

### Conclusion

**Goal**: Summarize key insights

**Template:**
```markdown
## What We Learned

[Project] succeeds because:
1. [Key insight 1]
2. [Key insight 2]
3. [Key insight 3]

## For Future Engineers

When maintaining or extending this system, remember:
- [Critical principle]
- [Important constraint]
- [Lesson we learned the hard way]

## Questions?

This explanation covers the major architecture and decisions. For specific
implementation details, see:
- [Architecture ADRs](./docs/adr/)
- [Setup Guide](./SETUP.md)
- [Contributing Guide](./CONTRIBUTING.md)
```

## Examples of Good Explanations

See `templates/` directory for complete example EXPLAIN files:
- `EXPLAIN_oauth_system.md` - Authentication system explanation
- `EXPLAIN_payment_system.md` - Payment processing system
- `EXPLAIN_message_queue.md` - Async job system

## Writing Tips

### Make It Engaging
- Start with a story, not abstractions
- Use "we" - makes it personal
- Share failures and how they were fixed
- Use emojis occasionally (😅 for failures, 🚀 for successes)
- Use short paragraphs and white space

### Be Specific
- Show actual code snippets
- Name actual files and functions
- Include actual metrics (latency, throughput)
- Reference actual bugs and fixes
- Use real examples, not hypotheticals

### Tell the Story
- How the project started and why
- What problems it solved
- What mistakes were made and how they were fixed
- What we'd do differently
- What future engineers should know

### Make It Useful
- Teach someone unfamiliar with the project
- Help future engineers avoid your mistakes
- Justify architectural decisions
- Explain why code is structured this way
- Provide context for maintenance and extensions

## Template Structure

This skill provides:
- EXPLAIN document template (structure and sections)
- Analogy patterns (how to explain concepts clearly)
- Anecdote patterns (how to share lessons memorably)
- Technology decision patterns (how to justify choices)
- Lesson/pitfall patterns (how to preserve wisdom)
- Complete example files

## Success Criteria

A good EXPLAIN file:
- [ ] Can be understood by engineers unfamiliar with project
- [ ] Explains architecture and design decisions clearly
- [ ] Includes lessons learned with specific examples
- [ ] Uses analogies to make concepts memorable
- [ ] Uses anecdotes to make lessons stick
- [ ] Reads like an engaging essay, not documentation
- [ ] Preserves architectural wisdom for future
- [ ] Justifies technology choices honestly
- [ ] Acknowledges trade-offs and constraints
- [ ] Provides context for maintenance and extension

## See Also

- `templates/EXPLAIN_*.md` - Example explanations
- `/pseudo-code:explain_my_project` - User command to generate EXPLAIN files
- `project-explainer` agent - Generates EXPLAIN files autonomously
