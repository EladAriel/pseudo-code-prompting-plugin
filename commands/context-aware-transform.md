---
description: Transform requests with context-aware project structure analysis
argument-hint: [feature request or implementation query]
---

# Context-Aware Transform

Transform user requests by analyzing existing project structure (Rule A) or creating a virtual skeleton for empty projects (Rule B).

## Task

User request: `$ARGUMENTS`

This command processes requests in two modes based on project state detected by the context-aware-tree-injection hook.

### Rule A: Existing Project Structure (Map to Architecture)

When PROJECT_TREE is provided in context and not equal to `<<PROJECT_EMPTY_NO_STRUCTURE>>`:

1. **Parse Structure** - Extract directories, files, and organizational patterns from PROJECT_TREE
2. **Detect Stack** - Identify technology from visible files:
   - `package.json`, `.next/` → Next.js/React
   - `requirements.txt`, `setup.py`, `pyproject.toml` → Python
   - `go.mod`, `go.sum` → Go
   - `Cargo.toml` → Rust
   - `pom.xml`, `build.gradle` → Java
   - `composer.json` → PHP
3. **Map Architecture** - Identify existing patterns:
   - Directory structure (`src/`, `lib/`, `app/`, `components/`)
   - Test organization (`tests/`, `__tests__/`, `spec/`)
   - Configuration files (tsconfig.json, .eslintrc, etc.)
   - Naming conventions visible in existing files
4. **Generate Response** - Provide implementation that:
   - References specific existing files with exact paths
   - Follows detected architectural patterns
   - Integrates with existing conventions
   - Places new files in appropriate locations based on structure

### Rule B: Empty Project (Generate Virtual Skeleton)

When PROJECT_TREE equals `<<PROJECT_EMPTY_NO_STRUCTURE>>` or no tree provided:

1. **Infer Stack** - Detect intended technology from request keywords:
   - "React", "Next.js", "next" → nextjs_react template
   - "Express", "Node", "nodejs", "node.js" → node_express template
   - "FastAPI", "Python API", "python api" → python_fastapi template
   - "Go", "Golang" → golang template
   - Default → generic template if no clear indicators
2. **Generate Virtual Skeleton** - Create recommended structure:
   - Complete directory hierarchy for detected stack
   - Standard configuration files
   - Common organizational patterns
3. **Provide Implementation Plan** - Output:
   - Full directory structure
   - Implementation steps aligned with skeleton
   - Technology-specific best practices

## Stack Templates

### nextjs_react (Next.js 13+ with React)
```
project/
├── src/
│   ├── app/                    # Next.js 13+ app directory
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── api/                # API routes
│   ├── components/
│   │   ├── ui/                 # Reusable UI components
│   │   └── shared/             # Shared components
│   ├── lib/                    # Utilities and helpers
│   ├── hooks/                  # Custom React hooks
│   └── types/                  # TypeScript type definitions
├── public/                     # Static assets
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
├── next.config.js
└── .env.example
```

**Indicators**: `next`, `nextjs`, `react`, `tsx`, `app directory`

### node_express (Node.js with Express)
```
project/
├── src/
│   ├── controllers/            # Route controllers
│   ├── models/                 # Data models
│   ├── routes/                 # Express route definitions
│   ├── middleware/             # Custom middleware
│   ├── services/               # Business logic
│   ├── utils/                  # Helper functions
│   └── config/                 # Configuration
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── .env.example
└── server.js                   # Entry point
```

**Indicators**: `express`, `node`, `nodejs`, `api`, `rest api`

### python_fastapi (Python with FastAPI)
```
project/
├── app/
│   ├── api/
│   │   └── endpoints/          # API endpoint modules
│   │       ├── users.py
│   │       └── auth.py
│   ├── core/
│   │   ├── config.py           # Configuration
│   │   └── security.py         # Auth & security
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   └── user.py
│   └── services/               # Business logic
│       └── user_service.py
├── tests/
│   ├── test_users.py
│   └── test_auth.py
├── requirements.txt
├── pyproject.toml
├── .env.example
└── main.py                     # FastAPI app entry
```

**Indicators**: `fastapi`, `python api`, `pydantic`, `uvicorn`

### golang (Go with standard project layout)
```
project/
├── cmd/
│   └── api/
│       └── main.go             # Application entry
├── internal/
│   ├── handlers/               # HTTP handlers
│   ├── models/                 # Data models
│   ├── services/               # Business logic
│   └── config/                 # Configuration
├── pkg/                        # Public libraries
│   └── utils/
├── tests/
│   └── integration/
├── go.mod
├── go.sum
└── .env.example
```

**Indicators**: `go`, `golang`, `go.mod`

### default (Generic/Language-Agnostic)
```
project/
├── src/                        # Source code
│   ├── core/                   # Core functionality
│   ├── utils/                  # Utilities
│   └── config/                 # Configuration
├── tests/                      # Test files
│   ├── unit/
│   └── integration/
├── docs/                       # Documentation
└── README.md
```

**Indicators**: No clear stack detected or generic request

## Output Format

### For Rule A (Existing Structure - Map Mode):

```
[CONTEXT-AWARE ANALYSIS]

Detected Stack: [stack name]
Project Pattern: [pattern description]

Existing Structure Analysis:
- [Key observation about organization]
- [Pattern detected in file naming]
- [Architectural decision visible in structure]

Implementation Plan:
1. [Action] in [existing/path/to/file.ext]
   - [Specific changes needed]
   - [Integration points with existing code]
   - Rationale: [Why this location based on structure]

2. [Action] - Create [new/path/to/file.ext]
   - Follows pattern from [reference/existing/file.ext]
   - Placement rationale: [Based on structure observation]

Affected Files:
- [path/to/file1.ext] (modify)
- [path/to/file2.ext] (create)
- [path/to/file3.ext] (modify)

Architecture Alignment Notes:
- [How changes fit existing patterns]
- [Conventions followed from structure]
- [Integration strategy with current architecture]
```

### For Rule B (Empty Project - Skeleton Mode):

```
[VIRTUAL SKELETON GENERATION]

Inferred Stack: [stack name]
Detection Reason: [Keywords or indicators that led to this choice]

Recommended Structure:
[Complete directory tree with annotations]

project/
├── [dir1]/
│   ├── [subdir]/              # [Purpose]
│   └── [file]                 # [Description]
├── [dir2]/                    # [Purpose]
└── [config-file]              # [Purpose]

Implementation Plan:
1. Initialize [stack-specific setup]
   - [Command to run]
   - [Configuration needed]

2. Create directory structure
   - [Directories to create]
   - [Purpose of each]

3. Implement [feature from request]
   - [Where to place implementation]
   - [Files to create]
   - [Stack-specific patterns to follow]

Next Steps:
1. [Initialization command]
2. [Dependency installation]
3. [First implementation step]
4. [Testing setup]
```

## Examples

### Example 1: Rule A - Existing Next.js Project

**Context Provided:**
```
PROJECT_TREE:
project/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── Header.tsx
│   └── lib/
│       └── utils.ts
├── package.json
└── next.config.js
```

**Request:** `add user authentication with JWT`

**Response:**
```
[CONTEXT-AWARE ANALYSIS]

Detected Stack: Next.js 13+ (React with TypeScript)
Project Pattern: App directory structure with organized components and utilities

Existing Structure Analysis:
- Uses Next.js 13+ app directory (`src/app/`)
- TypeScript throughout (`.tsx`, `.ts` extensions)
- Utilities organized in `lib/` directory
- Components in dedicated `components/` folder

Implementation Plan:
1. Create authentication utilities in src/lib/auth.ts
   - JWT token generation and validation functions
   - Session management helpers
   - Follows existing pattern: utilities in lib/ directory

2. Create authentication API routes in src/app/api/auth/[...nextauth]/route.ts
   - Next.js API route handlers for login/logout
   - Follows Next.js 13 app directory API pattern

3. Create authentication context provider in src/app/providers/AuthProvider.tsx
   - React context for auth state management
   - Wraps application in src/app/layout.tsx

4. Create login component in src/components/auth/LoginForm.tsx
   - New subdirectory follows existing components/ pattern
   - Consistent with Header.tsx component structure

Affected Files:
- src/lib/auth.ts (create) - JWT utilities
- src/app/api/auth/[...nextauth]/route.ts (create) - API endpoints
- src/app/providers/AuthProvider.tsx (create) - Context provider
- src/app/layout.tsx (modify) - Wrap with AuthProvider
- src/components/auth/LoginForm.tsx (create) - Login UI

Architecture Alignment Notes:
- Utilities placement in lib/ matches existing utils.ts pattern
- Component organization mirrors existing Header.tsx structure
- API routes follow Next.js 13 app directory conventions
- TypeScript usage consistent throughout
```

### Example 2: Rule B - Empty Project with FastAPI Request

**Context Provided:**
```
PROJECT_TREE: <<PROJECT_EMPTY_NO_STRUCTURE>>
```

**Request:** `create a FastAPI REST API for user management with CRUD operations`

**Response:**
```
[VIRTUAL SKELETON GENERATION]

Inferred Stack: python_fastapi
Detection Reason: "FastAPI" keyword explicitly mentioned in request

Recommended Structure:
app/
├── api/
│   └── endpoints/
│       ├── __init__.py
│       └── users.py           # User CRUD endpoints
├── core/
│   ├── __init__.py
│   ├── config.py              # Settings and configuration
│   └── security.py            # Authentication & authorization
├── models/
│   ├── __init__.py
│   └── user.py                # SQLAlchemy User model
├── schemas/
│   ├── __init__.py
│   └── user.py                # Pydantic User schemas
├── services/
│   ├── __init__.py
│   └── user_service.py        # Business logic layer
└── __init__.py
tests/
├── test_users.py              # User endpoint tests
└── conftest.py                # Pytest configuration
requirements.txt               # Dependencies
pyproject.toml                 # Project metadata
.env.example                   # Environment variables template
main.py                        # FastAPI application entry point

Implementation Plan:
1. Initialize FastAPI project
   - Install dependencies: `pip install fastapi uvicorn sqlalchemy pydantic python-dotenv`
   - Create virtual environment: `python -m venv .venv`

2. Create directory structure
   - app/ - Main application package
   - app/api/endpoints/ - API route definitions
   - app/core/ - Core functionality (config, security)
   - app/models/ - Database models
   - app/schemas/ - Request/response schemas
   - app/services/ - Business logic
   - tests/ - Test files

3. Implement User CRUD in app/api/endpoints/users.py
   - POST /users - Create user
   - GET /users - List users (with pagination)
   - GET /users/{id} - Get specific user
   - PUT /users/{id} - Update user
   - DELETE /users/{id} - Delete user

4. Define data structures
   - models/user.py: SQLAlchemy User model with fields (id, email, username, created_at)
   - schemas/user.py: Pydantic schemas (UserCreate, UserUpdate, UserResponse)

5. Setup in main.py
   - FastAPI app initialization
   - CORS middleware
   - Router registration
   - Database connection setup

Next Steps:
1. `python -m venv .venv && source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
2. `pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv`
3. Create files following structure above
4. Run with: `uvicorn main:app --reload`
```

### Example 3: Rule A - Existing Express API

**Context Provided:**
```
PROJECT_TREE:
api/
├── src/
│   ├── controllers/
│   │   └── productController.js
│   ├── routes/
│   │   └── products.js
│   ├── models/
│   │   └── Product.js
│   └── middleware/
│       └── errorHandler.js
├── package.json
└── server.js
```

**Request:** `add order management endpoints`

**Response:**
```
[CONTEXT-AWARE ANALYSIS]

Detected Stack: Node.js with Express
Project Pattern: MVC architecture with separate controllers, routes, and models

Existing Structure Analysis:
- Clear MVC separation (controllers/, routes/, models/)
- Existing product management as reference pattern
- Centralized error handling via middleware/
- JavaScript (not TypeScript)

Implementation Plan:
1. Create Order model in src/models/Order.js
   - Follows existing Product.js model pattern
   - Define schema for orders (id, userId, products, total, status, createdAt)

2. Create order controller in src/controllers/orderController.js
   - Mirrors productController.js structure
   - Implement: createOrder, getOrders, getOrderById, updateOrderStatus, deleteOrder

3. Create order routes in src/routes/orders.js
   - Follow products.js routing pattern
   - Define endpoints: POST /orders, GET /orders, GET /orders/:id, PATCH /orders/:id/status, DELETE /orders/:id

4. Register routes in server.js
   - Add: `app.use('/api/orders', ordersRouter);`
   - Consistent with existing products route registration

Affected Files:
- src/models/Order.js (create) - Order data model
- src/controllers/orderController.js (create) - Order business logic
- src/routes/orders.js (create) - Order route definitions
- server.js (modify) - Register order routes

Architecture Alignment Notes:
- Model structure matches Product.js pattern
- Controller methods follow productController.js conventions
- Route organization mirrors products.js
- Error handling will use existing middleware/errorHandler.js
- Maintains MVC separation visible in current structure
```

## Key Rules

1. **Always Check PROJECT_TREE Context First**
   - If tree is provided and not empty flag → Apply Rule A (Map Mode)
   - If tree is empty flag or missing → Apply Rule B (Skeleton Mode)
   - Never guess project structure - rely on provided tree

2. **Stack Detection Priority (Rule A)**
   - File indicators > Keywords in request
   - Multiple indicators → Choose primary framework
   - Ambiguous → State both possibilities and ask for clarification

3. **Path Specificity (Rule A)**
   - Always provide exact file paths from root
   - Reference existing files when suggesting patterns
   - Explain placement rationale based on structure

4. **Architecture Alignment (Rule A)**
   - Respect existing directory organization
   - Follow visible naming conventions
   - Don't introduce conflicting patterns
   - Match existing file extension conventions (.ts vs .js, .tsx vs .jsx)

5. **Template Selection (Rule B)**
   - Match keywords to most appropriate template
   - Default template only when no clear stack indicators
   - Explain detection reasoning to user

6. **Graceful Ambiguity Handling**
   - If stack unclear → Present options and ask
   - If request conflicts with structure → Note discrepancy
   - If multiple valid approaches → Explain trade-offs

7. **Cross-Reference Integration**
   - Mention related files that will interact
   - Note configuration changes needed
   - Identify import/export points

## Integration

This command works with the context-aware-tree-injection hook:

1. **Automatic Invocation**: When hook detects keywords (implement, create, add, refactor), it injects PROJECT_TREE context
2. **Manual Invocation**: Use `/context-aware-transform [request]` to explicitly trigger
3. **Context-Free**: If no PROJECT_TREE in context, defaults to Rule B (skeleton generation)

The hook triggers on these keywords: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`
