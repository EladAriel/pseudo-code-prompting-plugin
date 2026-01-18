# Context-Aware Mode

## Overview

Context-Aware Mode is an intelligent feature that automatically analyzes your project structure and provides architecture-aligned implementation suggestions. Instead of generic advice, Claude understands your codebase organization and recommends changes that fit your existing patterns.

## How It Works

### Automatic Activation

Context-Aware Mode activates automatically when you use implementation keywords in your prompts:

- `implement` - "implement user authentication"
- `create` - "create a new API endpoint"
- `add` - "add payment processing"
- `refactor` - "refactor the auth module"
- `build` - "build a dashboard component"
- `generate` - "generate CRUD operations"
- `setup` - "setup database migrations"
- `initialize` - "initialize the project structure"

When triggered, the plugin:
1. Scans your project directory structure
2. Generates an ASCII tree representation
3. Injects this context into Claude's understanding
4. Applies intelligent transformation rules

### Two Operating Modes

#### Rule A: Map to Existing Structure

**When**: Your project has existing files and directories

**What happens**: Claude analyzes your structure and:
- Detects your technology stack (Next.js, Express, FastAPI, Go, etc.)
- Identifies architectural patterns (MVC, feature-based, etc.)
- References specific existing files
- Suggests file placements that match your conventions
- Follows your naming patterns

**Example**:
```
Your project:
api/
├── src/
│   ├── controllers/
│   │   └── userController.js
│   ├── routes/
│   │   └── users.js
│   └── models/
│       └── User.js

Your prompt: "implement order management"

Claude's response:
[CONTEXT-AWARE ANALYSIS]
Detected Stack: Node.js with Express
Project Pattern: MVC architecture

Implementation Plan:
1. Create Order model in src/models/Order.js
   - Follows existing User.js pattern
2. Create order controller in src/controllers/orderController.js
   - Mirrors userController.js structure
3. Create order routes in src/routes/orders.js
   - Follows users.js routing pattern
...
```

#### Rule B: Generate Virtual Skeleton

**When**: Your project is empty or has no clear structure

**What happens**: Claude infers your intended stack and:
- Detects technology from keywords (FastAPI, React, Go, etc.)
- Generates a complete recommended directory structure
- Provides stack-specific best practices
- Creates a foundation to build on

**Example**:
```
Empty project directory

Your prompt: "create a FastAPI REST API for user management"

Claude's response:
[VIRTUAL SKELETON GENERATION]
Inferred Stack: python_fastapi
Detection Reason: "FastAPI" keyword

Recommended Structure:
app/
├── api/
│   └── endpoints/
│       └── users.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
│   └── user.py
...

Implementation Plan:
1. Install dependencies: pip install fastapi uvicorn sqlalchemy
2. Create directory structure
3. Implement user endpoints...
```

## Supported Stacks

### Next.js / React
**Indicators**: `package.json`, `.next/`, `next.config.js`, keywords: "React", "Next.js"

**Template Structure**:
- `src/app/` - Next.js 13+ app directory
- `src/components/` - React components
- `src/lib/` - Utilities
- `src/hooks/` - Custom hooks

### Node.js / Express
**Indicators**: `package.json` with Express, keywords: "Express", "Node"

**Template Structure**:
- `src/controllers/` - Route controllers
- `src/routes/` - Route definitions
- `src/models/` - Data models
- `src/middleware/` - Custom middleware

### Python / FastAPI
**Indicators**: `requirements.txt`, `pyproject.toml`, keywords: "FastAPI", "Python API"

**Template Structure**:
- `app/api/endpoints/` - API routes
- `app/core/` - Config and security
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas

### Go
**Indicators**: `go.mod`, `go.sum`, keywords: "Go", "Golang"

**Template Structure**:
- `cmd/` - Application entry points
- `internal/` - Private application code
- `pkg/` - Public libraries
- `tests/` - Test files

### Generic / Default
**When**: No clear stack indicators

**Template Structure**:
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

## Usage Examples

### Example 1: Existing Next.js App

**Scenario**: You have a Next.js project with some components

```bash
Your prompt: "implement user authentication with JWT"
```

**What happens**:
1. Hook detects "implement" keyword
2. Scans your project directory
3. Finds `src/app/`, `package.json`, `next.config.js`
4. Identifies: Next.js 13+ with TypeScript
5. Analyzes: App directory structure, existing component patterns
6. Suggests: Specific files (`src/lib/auth.ts`, `src/app/api/auth/route.ts`) that match your conventions

### Example 2: Empty Python Project

**Scenario**: You just created an empty directory

```bash
Your prompt: "create a FastAPI microservice for order processing"
```

**What happens**:
1. Hook detects "create" keyword
2. Scans directory (finds it empty)
3. Returns `<<PROJECT_EMPTY_NO_STRUCTURE>>` flag
4. Analyzes keywords: "FastAPI", "microservice"
5. Infers: python_fastapi template
6. Generates: Complete directory structure with FastAPI best practices

### Example 3: Manual Command Usage

You can explicitly trigger context-aware mode:

```bash
/context-aware-transform add real-time notifications with WebSockets
```

This bypasses automatic keyword detection and forces the analysis.

## Benefits

### 1. Architecture Consistency
- New code matches existing patterns
- No mixing of conventions (e.g., consistent file extensions)
- Proper module organization

### 2. Faster Onboarding
- Works with unfamiliar codebases
- Understands structure without extensive explanation
- Identifies patterns automatically

### 3. Better File Placement
- Suggests exact paths based on existing structure
- Groups related functionality correctly
- Follows your project's organizational logic

### 4. Stack-Appropriate Suggestions
- Recommendations fit your technology stack
- Uses framework-specific best practices
- Considers tooling conventions (TypeScript vs JavaScript, etc.)

### 5. Reduced Ambiguity
- Concrete file paths instead of vague suggestions
- References existing files as patterns
- Clear integration points

## Limitations

### Performance Constraints
- **Timeout**: 15 seconds maximum for tree generation
- **File Limit**: 1000 files scanned (configurable)
- **Output Size**: 50KB maximum tree size
- **Depth Limit**: 10 directory levels deep

Large monorepos may hit these limits, resulting in partial trees or graceful degradation.

### Automatic Filtering
The tree generator excludes common directories:
- `.git`, `.svn` - Version control
- `node_modules`, `vendor` - Dependencies
- `dist`, `build`, `out`, `target` - Build output
- `__pycache__`, `.pytest_cache` - Python caches
- `.venv`, `venv` - Virtual environments
- `.idea`, `.vscode` - IDE files

If your project uses non-standard directory names, they might be excluded. Use `.gitignore` to customize filtering.

### Inference Accuracy
Stack detection relies on:
1. File indicators (package.json, requirements.txt, etc.)
2. Directory names (app/, src/, cmd/)
3. Request keywords ("FastAPI", "React")

Ambiguous projects may need clarification.

## Troubleshooting

### Hook Not Triggering

**Symptom**: No context-aware analysis appears

**Causes**:
1. Keywords not detected - Use: implement, create, add, refactor, build, generate, setup, initialize
2. Python not installed - Install Python 3.6+
3. Script execution error - Check console for errors

**Solution**: Try explicit invocation with `/context-aware-transform [request]`

### Empty Tree (PROJECT_EMPTY_NO_STRUCTURE)

**Symptom**: Claude generates skeleton despite having files

**Causes**:
1. All files filtered (hidden, node_modules, etc.)
2. Permission errors preventing directory access
3. Directory depth exceeds limit (10 levels)

**Solution**: Check for hidden files, ensure read permissions, reduce project depth

### Wrong Stack Detected

**Symptom**: Claude uses incorrect template

**Causes**:
1. Ambiguous indicators (both package.json and requirements.txt)
2. Generic directory names
3. Keyword confusion

**Solution**: Be explicit in your prompt: "using FastAPI" or "in this Next.js project"

### Partial Tree / Truncation

**Symptom**: Tree shows "[TRUNCATED]" message

**Causes**:
1. More than 1000 files
2. Output exceeds 50KB

**Solution**: This is expected for large projects. The partial tree still provides useful context.

### Timeout

**Symptom**: No tree appears, graceful fallback to normal mode

**Causes**:
1. Very large directory (>10,000 files)
2. Slow file system
3. Network-mounted directories

**Solution**: Increase timeout in `get_context_tree.py` or use manual command

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

Add patterns to `DEFAULT_EXCLUDE_DIRS` or `DEFAULT_EXCLUDE_PATTERNS`:

```python
DEFAULT_EXCLUDE_DIRS = {
    '.git', 'node_modules', 'dist', 'build',
    'your_custom_dir',  # Add custom exclusions
}
```

### Disabling Context-Aware Mode

Remove or comment out the hook entry in `hooks/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          // ... other hooks ...
          // Comment out or remove this block:
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

## Best Practices

### 1. Use Clear Keywords
Instead of: "I need authentication"
Use: "implement user authentication"

### 2. Be Specific About Stack
If ambiguous: "create a FastAPI REST API" not just "create an API"

### 3. Reference Existing Patterns
"Add orders like the existing products module"

### 4. Review Suggested Paths
Always verify Claude's file paths match your intentions

### 5. Iterate If Needed
If the first suggestion doesn't fit, clarify: "actually, place it in lib/ not utils/"

## Integration with Other Features

Context-Aware Mode works alongside:
- **/transform-query** - Convert requests to pseudo-code before analysis
- **/compress-context** - Compress verbose requirements before implementation
- **/validate-requirements** - Validate pseudo-code completeness

**Workflow Example**:
1. `/transform-query create user authentication` → Get pseudo-code
2. `implement [pseudo-code]` → Triggers context-aware mode
3. Claude provides architecture-aligned implementation

## Technical Details

For technical implementation details, see [TREE-INJECTION-GUIDE.md](TREE-INJECTION-GUIDE.md).

## Feedback and Issues

If you encounter issues or have suggestions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review logs in `hooks/context_tree.log` (if logging enabled)
3. Report issues with example prompts and project structure

## Related Documentation

- [Tree Injection Technical Guide](TREE-INJECTION-GUIDE.md) - Implementation details
- [QUICK_START.md](QUICK_START.md) - Getting started with the plugin
- [ARCHITECTURE.md](ARCHITECTURE.md) - Plugin architecture overview
