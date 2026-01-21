# Optimize Prompt

## What It Does
Enhances pseudo-code by adding missing security, validation, error handling, and performance parameters. Turns basic pseudo-code into production-ready specifications.

## Goal
Ensure completeness by automatically adding commonly-needed parameters that were omitted from initial transformation.

## When to Use
- After transforming basic requirements
- When pseudo-code lacks security/validation details
- Before implementation to catch missing requirements
- To enhance quick transformations

## How to Invoke
```
Run optimize-prompt: create_endpoint(path="/api/users", method="POST")
```

or

```
/optimize-prompt create_endpoint(path="/api/users", method="POST")
```

## Workflow

```mermaid
flowchart LR
    A[Basic<br/>Pseudo-Code] --> B[prompt-optimizer<br/>Agent]
    B --> C[Add<br/>Security]
    C --> D[Add<br/>Validation]
    D --> E[Add Error<br/>Handling]
    E --> F[Add<br/>Performance]
    F --> G[Production-Ready<br/>Pseudo-Code]

    style A fill:#FFC107
    style G fill:#4CAF50
    style B fill:#2196F3
```

### Agents Invoked
- **prompt-optimizer** - Applies optimization patterns

### Hooks Used
- `post-transform-validation` - Auto-triggers after transformation (optional)

### Skills
- `prompt-optimizer` - Enhancement patterns for security, validation, performance

## Output Example
```javascript
// Input: Basic pseudo-code
create_endpoint(path="/api/users", method="POST")

// Output: Optimized with all enhancements
create_endpoint(
  path="/api/users",
  method="POST",
  auth=true,                                    // ← Added security
  roles=["admin"],                              // ← Added authorization
  request_schema={                              // ← Added validation
    "name": "string:required:max(100)",
    "email": "email:required:unique"
  },
  response_format={                             // ← Added response spec
    "user_id": "string",
    "created_at": "timestamp"
  },
  error_responses={                             // ← Added error handling
    "400": "invalid_input",
    "409": "duplicate_email"
  },
  rate_limit="100/hour"                         // ← Added performance
)

Improvements Made:
✓ Security - Auth + role-based access
✓ Validation - Request schema with constraints
✓ Error Handling - Specific error codes
✓ Performance - Rate limiting
```

## Why Use This Command
- **Prevents security gaps** - Adds auth, validation automatically
- **Catches missing requirements** - Adds commonly-needed parameters
- **Production-ready output** - No need to manually add error handling
- **Learns patterns** - Understands what parameters go together
- **Time saver** - Don't manually think through every constraint
