# Context-Aware Transform-Query

## Overview

The `/transform-query` command automatically includes **actual file paths from your project** when transforming natural language to pseudo-code. This happens transparently when you use implementation keywords.

**Core Benefit**: Transform queries output **specific file paths** from YOUR codebase, not generic suggestions.

## How It Works

### Automatic Activation

When you use these keywords in your query:

- `implement` - "implement user authentication"
- `create` - "create API endpoints"
- `add` - "add payment processing"
- `refactor` - "refactor auth module"
- `build` - "build dashboard"
- `generate` - "generate CRUD"
- `setup` - "setup database"
- `initialize` - "initialize project"

The system automatically:

1. **Scans** your project directory structure
2. **Detects** your technology stack (Next.js, Express, FastAPI, Go, etc.)
3. **Analyzes** your architecture patterns (MVC, feature-based, etc.)
4. **Injects** this context into `/transform-query`

### Result: Pseudo-Code with Actual Paths

Instead of generic pseudo-code, you get output with **your actual file paths**.

## Examples

### Example 1: Existing Next.js Project

**Your Project Structure:**

```text
my-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── Header.tsx
│   └── lib/
│       └── utils.ts
└── package.json
```

**Your Query:**

```bash
/transform-query "implement user authentication with JWT"
```

**Output (WITH Context-Aware):**

```javascript
Transformed: implement_authentication(
  type="jwt",
  target_files=[
    "src/lib/auth.ts",                    // ← Actual path from YOUR project
    "src/app/api/auth/[...nextauth]/route.ts",
    "src/app/providers/AuthProvider.tsx",
    "src/components/auth/LoginForm.tsx"
  ],
  modifications=[
    "src/app/layout.tsx"                  // ← File that exists in YOUR project
  ],
  stack="nextjs_react",                   // ← Detected from YOUR package.json
  architecture_pattern="app_directory",   // ← Detected from YOUR structure
  follows_existing_pattern="src/lib/utils.ts",
  integration_points=["Header.tsx:add_logout_button"],
  security=["bcrypt_hash", "jwt_token", "secure_cookies"]
)
```

**Key Features:**

- ✅ `target_files` = specific paths in YOUR project
- ✅ `modifications` = files that exist in YOUR codebase
- ✅ `stack` = detected from YOUR package.json
- ✅ `architecture_pattern` = detected from YOUR directory structure
- ✅ `follows_existing_pattern` = references YOUR existing files

---

### Example 2: Existing Express API

**Your Project Structure:**

```text
api/
├── src/
│   ├── controllers/
│   │   └── userController.js
│   ├── routes/
│   │   └── users.js
│   └── models/
│       └── User.js
└── server.js
```

**Your Query:**

```bash
/transform-query "add order management endpoints"
```

**Output (WITH Context-Aware):**

```javascript
Transformed: implement_order_management(
  target_files=[
    "src/models/Order.js",
    "src/controllers/orderController.js",
    "src/routes/orders.js"
  ],
  modifications=["server.js"],
  follows_pattern="src/controllers/userController.js",  // ← YOUR existing pattern
  stack="node_express",
  architecture="mvc",
  endpoints=["POST /orders", "GET /orders", "GET /orders/:id", "PATCH /orders/:id/status"],
  integrations=["User.js:foreign_key_userId"]
)
```

---

### Example 3: Empty Project (Virtual Skeleton)

**Your Project Structure:**

```text
empty-project/
(no files)
```

**Your Query:**

```bash
/transform-query "create FastAPI REST API for user management"
```

**Output (WITH Empty Project Detection):**

```javascript
Transformed: create_api(
  framework="fastapi",
  domain="user_management",
  recommended_structure={
    "stack": "python_fastapi",
    "files": [
      "app/api/endpoints/users.py",
      "app/core/config.py",
      "app/core/security.py",
      "app/models/user.py",
      "app/schemas/user.py",
      "app/services/user_service.py",
      "main.py",
      "requirements.txt"
    ]
  },
  endpoints=["POST /users", "GET /users", "GET /users/{id}", "PUT /users/{id}", "DELETE /users/{id}"],
  features=["crud", "validation", "authentication"],
  database="sqlalchemy"
)
```

**Note**: For empty projects, the system generates a **recommended structure** based on the detected stack.

---

### Example 4: Without Context-Aware (Generic Mode)

If you use a query WITHOUT implementation keywords:

**Your Query:**

```bash
/transform-query "add user authentication"  # ← No "implement", "create", etc.
```

**Output (Standard Mode):**

```javascript
Transformed: add_authentication(
  type="user_authentication",
  features=["login", "logout", "session"],
  security=["password_hash", "token"]
)
```

**Note**: Generic pseudo-code without specific file paths.

---

## Comparison: With vs. Without Context-Aware

| Feature | **Without Context** | **With Context** |
|---------|---------------------|------------------|
| File paths | ❌ Generic names | ✅ Actual paths from YOUR project |
| Stack detection | ❌ Not included | ✅ Auto-detected (Next.js, Express, etc.) |
| Architecture | ❌ Not analyzed | ✅ Pattern identified (MVC, app directory, etc.) |
| Existing patterns | ❌ Not referenced | ✅ References YOUR existing files |
| Integration points | ❌ Not identified | ✅ Shows how to connect to YOUR code |
| Empty projects | ❌ Generic output | ✅ Stack-specific recommended structure |

---

## Supported Technology Stacks

The system automatically detects these stacks from your project files:

### 1. Next.js / React

**Detection Indicators**: `package.json` with `next`, `.next/`, `next.config.js`

**Recommended Structure**:

- `src/app/` - Next.js 13+ app directory
- `src/components/` - React components
- `src/lib/` - Utilities
- `src/hooks/` - Custom hooks

### 2. Node.js / Express

**Detection Indicators**: `package.json` with `express`, `server.js`, `app.js`

**Recommended Structure**:

- `src/controllers/` - Route controllers
- `src/routes/` - Route definitions
- `src/models/` - Data models
- `src/middleware/` - Custom middleware

### 3. Python / FastAPI

**Detection Indicators**: `requirements.txt`, `pyproject.toml` with `fastapi`, `main.py`

**Recommended Structure**:

- `app/api/endpoints/` - API routes
- `app/core/` - Config and security
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas

### 4. Go

**Detection Indicators**: `go.mod`, `go.sum`

**Recommended Structure**:

- `cmd/` - Application entry points
- `internal/` - Private application code
- `pkg/` - Public libraries
- `api/` - API definitions

### 5. Generic

**When**: No clear stack indicators detected

**Recommended Structure**:

- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

---

## Usage Patterns

### Pattern 1: Standard Workflow

```bash
# Step 1: Transform with context
/transform-query "implement user authentication"

# Step 2: Review the pseudo-code with actual paths
# Output includes: target_files, modifications, stack, architecture_pattern

# Step 3: Use the pseudo-code to guide implementation
# You now have specific file paths to work with
```

### Pattern 2: Exploring New Features

```bash
# See what files would be created for a feature
/transform-query "add payment processing with Stripe"

# Output shows:
# - target_files: Where to create new code
# - modifications: Existing files to update
# - integrations: How to connect to existing code
```

### Pattern 3: Empty Project Initialization

```bash
# Start a new project
/transform-query "create React dashboard with authentication"

# Output shows:
# - recommended_structure: Complete directory layout
# - stack-specific best practices
# - initialization commands
```

---

## Limitations

### Performance Constraints

- **Timeout**: 15 seconds maximum for tree generation
- **File Limit**: 1000 files scanned (configurable)
- **Output Size**: 50KB maximum tree size
- **Depth Limit**: 10 directory levels deep

**Impact**: Large monorepos may hit these limits, resulting in partial trees or fallback to generic mode.

### Automatic Filtering

The tree generator excludes common directories:

- `.git`, `.svn` - Version control
- `node_modules`, `vendor` - Dependencies
- `dist`, `build`, `out`, `target` - Build output
- `__pycache__`, `.pytest_cache` - Python caches
- `.venv`, `venv` - Virtual environments
- `.idea`, `.vscode` - IDE files

**Impact**: If your project uses non-standard directory names, they might be excluded. Customize via `.gitignore`.

### Stack Detection Accuracy

Detection relies on:

1. File indicators (package.json, requirements.txt, go.mod)
2. Directory names (app/, src/, cmd/)
3. Query keywords ("FastAPI", "React", "Express")

**Impact**: Ambiguous projects (e.g., both package.json and requirements.txt) may need clarification in the query.

---

## Troubleshooting

### Issue: No Actual Paths in Output

**Symptom**: Transform-query returns generic pseudo-code without file paths

**Causes:**

1. **No implementation keyword** - Use: `implement`, `create`, `add`, `refactor`, `build`
2. **Hook not triggering** - Check that Python 3.6+ is installed
3. **Project scan failed** - Check console for errors

**Solution:**

```bash
# Ensure you use an implementation keyword
/transform-query "implement user auth"  # ✅ Good
/transform-query "add user auth"        # ✅ Good
/transform-query "user auth"            # ❌ Won't trigger context-aware
```

---

### Issue: Empty Project Structure Detected

**Symptom**: Output shows `recommended_structure` instead of `target_files`

**Causes:**

1. All files filtered (hidden, node_modules, etc.)
2. Permission errors preventing directory access
3. Directory depth exceeds 10 levels

**Solution:**

- Check for hidden files (files starting with `.`)
- Ensure read permissions on project directory
- Reduce project depth (move files closer to root)

---

### Issue: Wrong Stack Detected

**Symptom**: Output has incorrect `stack` parameter

**Causes:**

1. Ambiguous indicators (both package.json and requirements.txt)
2. Generic directory names
3. Keyword confusion in query

**Solution:**

Be explicit in your query:

```bash
# ❌ Ambiguous
/transform-query "create API endpoints"

# ✅ Explicit
/transform-query "create FastAPI endpoints"
/transform-query "create Express endpoints"
```

---

### Issue: Missing Files in Output

**Symptom**: Expected files not included in `target_files`

**Causes:**

1. File limit reached (1000 files max)
2. Files filtered by .gitignore patterns
3. Files at depth > 10

**Solution:**

- Check if files are in excluded directories
- Verify `.gitignore` patterns
- Reduce project complexity

---

## Configuration

### Adjusting Limits

Edit `hooks/get_context_tree.py`:

```python
DEFAULT_MAX_DEPTH = 10        # Maximum directory depth
DEFAULT_MAX_FILES = 1000      # Maximum files to scan
DEFAULT_TIMEOUT = 10          # Timeout in seconds
MAX_OUTPUT_BYTES = 50 * 1024  # 50KB output limit
```

### Custom Exclusions

Add patterns to `DEFAULT_EXCLUDE_DIRS`:

```python
DEFAULT_EXCLUDE_DIRS = {
    '.git', 'node_modules', 'dist', 'build',
    'your_custom_dir',  # Add custom exclusions
}
```

### Disabling Context-Aware Mode

Remove the hook entry in `hooks/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          // Remove or comment out this block:
          // {
          //   "type": "command",
          //   "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/context-aware-tree-injection.sh",
          //   ...
          // }
        ]
      }
    ]
  }
}
```

---

## Best Practices

### 1. Use Clear Implementation Keywords

```bash
# ✅ Good - triggers context-aware
/transform-query "implement user authentication"
/transform-query "create dashboard components"
/transform-query "add payment processing"

# ❌ Won't trigger context-aware
/transform-query "user authentication"
/transform-query "dashboard components"
```

### 2. Be Specific About Stack (If Ambiguous)

```bash
# ✅ Explicit stack
/transform-query "create FastAPI REST API"
/transform-query "add Next.js authentication"

# ⚠️  May guess wrong stack
/transform-query "create API"
/transform-query "add authentication"
```

### 3. Review Output Paths

Always verify the suggested file paths match your intentions:

```javascript
target_files=[
  "src/lib/auth.ts",  // ← Check: Does this location make sense?
  "src/app/api/..."   // ← Check: Follows your conventions?
]
```

### 4. Use for Both New and Existing Projects

- **Existing**: Get specific paths that match your architecture
- **Empty**: Get recommended structure for your stack

---

## Technical Details

For implementation details, architecture, and cross-platform considerations, see:

- [Tree Injection Technical Guide](TREE-INJECTION-GUIDE.md) - Complete technical implementation
- [Plugin Architecture](ARCHITECTURE.md) - Overall plugin design
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

---

## Summary

**Context-Aware `/transform-query`** automatically includes actual file paths from your project in pseudo-code output:

✅ **Detects** your stack (Next.js, Express, FastAPI, Go)

✅ **Analyzes** your architecture (MVC, app directory, feature-based)

✅ **Outputs** pseudo-code with **your actual file paths**

✅ **References** your existing files as patterns

✅ **Works** with both existing and empty projects

**Triggers automatically** when you use: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`

**No manual configuration needed** - just use implementation keywords in your queries!
