# Transform Query

## What It Does
Converts natural language into concise pseudo-code using function syntax. The basic transformation step - fast and lightweight.

## Goal
Structure ambiguous requirements into clear, parseable pseudo-code format. Foundation for all other commands.

## When to Use
- Quick iteration on requirements
- When you just need structure, not validation/optimization
- First step before validate/optimize
- Rapid prototyping

## How to Invoke
```
Run transform-query: implement user login with email and password
```

or

```
/transform-query implement user login with email and password
```

## Workflow

```mermaid
flowchart LR
    A[Natural<br/>Language] --> B[prompt-transformer<br/>Agent]
    B --> C[Analyze<br/>Intent]
    C --> D[Extract<br/>Parameters]
    D --> E[Create<br/>Function Syntax]
    E --> F[Pseudo-Code]

    style A fill:#FF9800
    style F fill:#4CAF50
    style B fill:#2196F3
```

### Agents Invoked
- **prompt-transformer** - Core transformation logic

### Hooks Used
- `context-aware-tree-injection` - Adds project paths (if implementation keywords detected)
- `user-prompt-submit` - Detects command

### Skills
- `prompt-structurer` - Transformation methodology (PROMPTCONVERTER)

## Output Example
```javascript
// Input: Natural language
"implement user login with email and password"

// Output: Pseudo-code
implement_user_login(
  auth_method="email_password",
  fields=["email", "password"],
  validation=true
)
```

### With Project Context
```javascript
// Input: "add authentication" (in Next.js project)
// Output includes real paths:
implement_authentication(
  target_files=["src/lib/auth.ts", "src/app/api/auth/route.ts"],
  stack="nextjs_react"
)
```

## Why Use This Command
- **Fast** - 5-10 seconds vs 30-90 for complete process
- **Eliminates ambiguity** - Clear structure from vague requests
- **Composable** - Output feeds into validate/optimize
- **Context-aware** - Uses real project paths when available
- **Simple** - Just transformation, no extra processing
