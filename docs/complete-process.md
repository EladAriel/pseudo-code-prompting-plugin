# Complete Process

## What It Does
Runs the full transformation pipeline automatically: transforms natural language → validates requirements → optimizes pseudo-code. One command replaces three manual steps.

## Goal
Save time and ensure quality by automating the complete workflow instead of running transform/validate/optimize separately.

## When to Use
- Production features requiring validation and optimization
- Complex requirements needing thorough analysis
- When you want best-quality output without manual orchestration

## How to Invoke
```
Run complete-process: implement JWT authentication with refresh tokens
```

or

```
/complete-process implement JWT authentication with refresh tokens
```

## Workflow

```mermaid
flowchart TD
    A[Your Query] --> B{Mode Selection}
    B -->|Quick| C[Transform Only]
    B -->|Complete| D[Transform]
    D --> E[Validate]
    E --> F[Optimize]
    C --> G[Output: Pseudo-Code]
    F --> H[Output: Validated + Optimized]

    style D fill:#4CAF50
    style E fill:#2196F3
    style F fill:#FF9800
    style H fill:#4CAF50
```

### Agents Invoked
1. **prompt-transformer** - Converts natural language to pseudo-code
2. **requirement-validator** - Checks completeness and security
3. **prompt-optimizer** - Enhances with missing parameters

### Hooks Used
- `user-prompt-submit` - Detects command invocation
- `context-aware-tree-injection` - Injects project structure (if available)
- `context-compression-helper` - Suggests compression for large inputs

### Skills
- `prompt-structurer` - Core transformation logic
- `requirement-validator` - Validation rules
- `prompt-optimizer` - Optimization patterns

## Output Example
```javascript
// Input: "implement user login"
// Output after complete process:
implement_user_login(
  auth_method="email_password",
  endpoints={
    "login": "/api/auth/login",
    "logout": "/api/auth/logout"
  },
  security={
    "hashing": "bcrypt",
    "session": "jwt",
    "csrf_protection": true
  },
  rate_limiting="5_attempts_per_15min",
  error_handling={
    "invalid_credentials": "return_401",
    "account_locked": "return_423"
  }
)
```

## Why Use This Command
- **60-80% token reduction** - Removes intermediate outputs from context
- **Consistent quality** - Automated validation catches issues
- **Saves time** - One command vs three manual steps
- **Production-ready** - Output includes security, validation, error handling
- **Context-aware** - Uses your actual project structure
