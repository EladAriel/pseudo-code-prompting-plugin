---
description: Transform natural language query to code-style pseudo-code format with context-aware file paths
argument-hint: [query]
---

# Transform Query to Pseudo-Code

Transform the provided natural language query into concise, function-like pseudo-code format following PROMPTCONVERTER methodology. When project structure context is available, include actual file paths from your codebase.

## Task

User query: `$ARGUMENTS`

### Step 0: Semantic Cache Lookup

**BEFORE generating transformation, check the semantic cache**:

1. **Call semantic router**: Run `hooks/cache/find_tag.sh "$ARGUMENTS"`
2. **Evaluate result**:
   - If result is NOT "None" → **CACHE HIT**:
     - Load pattern from `.claude/prompt_cache/patterns/{tag_id}.md`
     - Display: `📦 Loaded cached pattern: {tag_id}`
     - **SKIP Steps 1-2 below** (do not generate transformation)
     - Return the cached pattern content directly
   - If result is "None" → **CACHE MISS**:
     - Log cache miss
     - Proceed with Steps 1-2 below (generate transformation)
     - Display tip: `💡 Tip: Use 'hooks/cache/cache-success.sh' to save this transformation for reuse`

**Cache hit workflow**:
```
Query → Semantic Router → Match found → Load from disk → Return cached pattern → Done
```

**Cache miss workflow**:
```
Query → Semantic Router → No match → Generate new transformation → Return result → (User can optionally cache)
```

### Step 1: Check for Context-Aware Mode

If `[CONTEXT-AWARE MODE ACTIVATED]` and `PROJECT_TREE` are present in the conversation context:
- **Mode**: Context-Aware Transformation
- **Action**: Transform query AND include actual file paths from the project structure
- **Rules**: Apply Rule A (existing project) or Rule B (empty project) based on tree content

If no context available:
- **Mode**: Standard Transformation
- **Action**: Transform to generic pseudo-code without specific paths

### Step 2: Apply PROMPTCONVERTER Transformation

1. **Analyze Intent** - Identify the core action (verb) and main subject (noun) of the query
2. **Create Function Name** - Combine into descriptive snake_case function name
3. **Extract Parameters** - Convert specific details and constraints into function arguments
4. **Detect Stack** (if PROJECT_TREE available) - Identify technology from visible files
5. **Map to Architecture** (if PROJECT_TREE available) - Reference actual file paths
6. **Output Format** - Return pseudo-code with actual paths (if available)

## Context-Aware Mode: Rule A (Existing Project)

When PROJECT_TREE shows existing files (not `<<PROJECT_EMPTY_NO_STRUCTURE>>`):

**Transform query using actual project structure**:
1. Analyze PROJECT_TREE to identify:
   - Technology stack (package.json, requirements.txt, go.mod, etc.)
   - Directory organization (src/, app/, lib/, components/, etc.)
   - Existing file patterns and naming conventions
2. Include actual file paths in pseudo-code parameters
3. Reference existing files where modifications are needed

**Output Format**:
```
Transformed: function_name(
  target_files=["actual/path/from/tree.ext", "another/real/path.ext"],
  create_files=["new/path/following/pattern.ext"],
  stack="detected_from_tree",
  ...other_params
)
```

## Context-Aware Mode: Rule B (Empty Project)

When PROJECT_TREE equals `<<PROJECT_EMPTY_NO_STRUCTURE>>`:

**Infer stack and generate virtual structure**:
1. Detect intended technology from query keywords
2. Apply stack-specific directory conventions
3. Include recommended file paths in pseudo-code

**Output Format**:
```
Transformed: function_name(
  recommended_structure={
    "stack": "inferred_stack",
    "files": ["recommended/path/based/on/stack.ext", ...],
    ...
  },
  ...other_params
)
```

## Standard Mode (No Context)

When no PROJECT_TREE available:

**Transform to generic pseudo-code**:
```
Transformed: function_name(param1="value1", param2="value2", ...)
```

## Output Format

### Context-Aware Output (with PROJECT_TREE):
```
Transformed: function_name(
  target_files=["src/lib/auth.ts", "src/app/api/auth/route.ts"],
  modifications=["src/app/layout.tsx"],
  create_files=["src/components/auth/LoginForm.tsx"],
  stack="nextjs_react",
  architecture="app_directory_pattern",
  integration_points=["existing_component:src/components/Header.tsx"],
  ...other_params
)
```

### Standard Output (no context):
```
Transformed: function_name(param1="value1", param2="value2", ...)
```

## Examples

### Example 1: Context-Aware with Existing Next.js Project

**Input Query**: "Add user authentication with JWT"

**PROJECT_TREE Available**:
```
project/
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

**Output**:
```
Transformed: implement_authentication(
  type="jwt",
  target_files=[
    "src/lib/auth.ts",
    "src/app/api/auth/[...nextauth]/route.ts",
    "src/app/providers/AuthProvider.tsx",
    "src/components/auth/LoginForm.tsx"
  ],
  modifications=["src/app/layout.tsx"],
  stack="nextjs_react",
  architecture_pattern="app_directory",
  follows_existing_pattern="src/lib/utils.ts",
  integration_points=["Header.tsx:add_logout_button"],
  security=["bcrypt_hash", "jwt_token", "secure_cookies"]
)
```

### Example 2: Context-Aware with Empty Project

**Input Query**: "Create a FastAPI REST API for user management"

**PROJECT_TREE**: `<<PROJECT_EMPTY_NO_STRUCTURE>>`

**Output**:
```
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

### Example 3: Standard Mode (No Context)

**Input Query**: "Optimize SQL query for large datasets"

**No PROJECT_TREE**

**Output**:
```
Transformed: optimize_sql_query(
  scale="large_datasets",
  metrics=["latency", "throughput"],
  techniques=["indexing", "query_plan_analysis", "caching"]
)
```

### Example 4: Context-Aware with Express API

**Input Query**: "Add order management endpoints"

**PROJECT_TREE Available**:
```
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

**Output**:
```
Transformed: implement_order_management(
  target_files=[
    "src/models/Order.js",
    "src/controllers/orderController.js",
    "src/routes/orders.js"
  ],
  modifications=["server.js"],
  follows_pattern="src/controllers/userController.js",
  stack="node_express",
  architecture="mvc",
  endpoints=["POST /orders", "GET /orders", "GET /orders/:id", "PATCH /orders/:id/status"],
  integrations=["User.js:foreign_key_userId"]
)
```

## Key Rules

**Standard Mode Rules**:
- Preserve all semantic information from the original query
- Use meaningful parameter names aligned with the task
- Include all constraints as explicit parameters
- Function name should clearly indicate the action being requested

**Context-Aware Mode Rules** (when PROJECT_TREE available):
- **ALWAYS include actual file paths** from PROJECT_TREE in parameters
- Use `target_files` for existing files to modify
- Use `create_files` for new files following project patterns
- Use `modifications` for files needing updates
- Include `stack` parameter with detected technology
- Include `architecture_pattern` parameter describing project organization
- Reference existing files as patterns (e.g., `follows_pattern="path/to/reference.ext"`)
- Add `integration_points` showing how new code connects to existing

**File Path Guidelines**:
- Use exact paths from PROJECT_TREE (case-sensitive)
- Follow existing directory structure patterns
- Match file extension conventions (.ts vs .js, .tsx vs .jsx)
- Group related files logically (features/, components/, services/)
- Reference sibling files when showing integration points

## Integration with Context-Aware Hook

This command automatically benefits from the `context-aware-tree-injection` hook:

1. When you use keywords like "implement", "create", "add" in queries
2. Hook scans project and injects PROJECT_TREE
3. This command detects the tree and applies context-aware transformation
4. Output includes actual file paths from your codebase

**Workflow**:
```
Your query: "implement user authentication"
   ↓
Hook detects "implement" → Scans project → Injects PROJECT_TREE
   ↓
transform-query command runs with context
   ↓
Output: Pseudo-code with actual file paths from your project
```

## When to Use

**Use `/transform-query` when you want**:
- Structured pseudo-code representation of your request
- Actual file paths based on your project structure (if context available)
- Clear parameter specification for implementation
- Integration with other PROMPTCONVERTER commands

**The context-aware enhancement means**:
- You get specific file paths, not generic suggestions
- Recommendations align with your existing architecture
- New files follow your project's conventions
- Integration points are explicit

## Related Commands

- `/context-aware-transform` - Direct architecture analysis (standalone)
- `/compress-context` - Compress verbose requirements before transformation
- `/validate-requirements` - Validate transformed pseudo-code
- `/optimize-prompt` - Enhance pseudo-code completeness
