# Transform Pipeline Tests

Minimal tests for the 6-step transformation pipeline.

## Test Suite 1: Tech Stack Detection

### Test 1.1: Detect Node.js
```
Input: Directory with package.json (contains "express")
Expected: Tech stack = "Node.js/Express"
Target files: src/routes/, src/controllers/, src/middleware/
```

### Test 1.2: Detect Python
```
Input: Directory with pyproject.toml (contains "django" or "fastapi")
Expected: Tech stack = "Python/Django" or "Python/FastAPI"
Target files: app/views.py, app/models.py
```

### Test 1.3: Detect Go
```
Input: Directory with go.mod
Expected: Tech stack = "Go"
Target files: internal/handlers/, pkg/middleware/
```

### Test 1.4: Unknown Stack
```
Input: Directory with no recognized files
Expected: Ask user or default to Node.js
```

## Test Suite 2: Auto-Compression

### Test 2.1: Compress Verbose Requirement
```
Input: 1,500 char requirement about OAuth with repetition
Expected: Compressed to ~300 chars (80% compression)
Check: All error codes, numbers, security requirements preserved
```

### Test 2.2: Skip Compression for Concise
```
Input: 800 char requirement (already concise)
Expected: No compression, pass through as-is
```

### Test 2.3: Preserve Critical Details
```
Input: Verbose requirement with specific error codes, TTLs, constraints
Expected: All specifics preserved after compression
Check: "401", "15m", "10/hour" all in compressed output
```

## Test Suite 3: Transform to Pseudo-Code

### Test 3.1: Function Naming
```
Input: "Add OAuth authentication"
Expected: Function name = "implement_oauth_authentication"
Rule: [verb]_[subject]
```

### Test 3.2: Parameter Extraction
```
Input: "JWT tokens with 15-minute TTL, refresh tokens with 7-day TTL"
Expected: access_token_ttl="15m", refresh_token_ttl="7d"
Check: All parameters explicit (no vague values)
```

### Test 3.3: Standard Parameters Included
```
Input: Any requirement
Expected Output includes:
  - target_files=[...]
  - error_handling={...}
  - security={...}
  - timeout="5s"
  - logging=true
```

### Test 3.4: Tech-Stack Aware Paths
```
Input: "Add API endpoint" in Node.js project
Expected: target_files includes "src/app/api/[resource]/route.ts"

Input: "Add API endpoint" in Python project
Expected: target_files includes "app/views.py"
```

## Test Suite 4: Validate Completeness

### Test 4.1: Detect Missing Error Codes
```
Input: Pseudo-code with no error_handling
Expected: Flag as CRITICAL issue
Message: "No error handling defined"
```

### Test 4.2: Detect Missing Security
```
Input: Pseudo-code about authentication with no security params
Expected: Flag as CRITICAL issue
Message: "Security requirements not specified"
```

### Test 4.3: Detect Vague Requirements
```
Input: error_handling={"handle_errors": "gracefully"}
Expected: Flag as issue
Message: "Use specific HTTP status codes, not descriptions"
```

### Test 4.4: Accept Complete Specification
```
Input: Well-formed pseudo-code with all parameters
Expected: Pass completeness check
```

## Test Suite 5: Optimize with Standard Parameters

### Test 5.1: Add Missing Timeout
```
Input: Pseudo-code without timeout
Expected Output: timeout="5s" added
```

### Test 5.2: Add Retry Logic
```
Input: Pseudo-code without retry
Expected Output: retry={"max_attempts": 3, "backoff": "exponential"}
```

### Test 5.3: Preserve Existing Parameters
```
Input: Pseudo-code with timeout="10s" already specified
Expected: Keep timeout="10s", don't override
```

### Test 5.4: Complete error_handling
```
Input: error_handling with partial codes
Expected: Fill in missing standard codes (400, 401, 403, 500, 503)
```

## Test Suite 6: cc10x Bridge

### Test 6.1: Save to Specification File
```
Input: User selects "YES" to cc10x bridge
Expected: File created at .claude/cc10x/specification-reference.md
Contains: Complete pseudo-code + marker comment
```

### Test 6.2: Update Active Context
```
Input: User selects "YES" to cc10x bridge
Expected: File updated at .claude/cc10x/activeContext.md
Contains: Reference marker: <!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->
```

### Test 6.3: Skip Bridge on "NO"
```
Input: User selects "NO" to cc10x bridge
Expected: No files created/modified in .claude/cc10x/
Pseudo-code still returned to user
```

## Integration Tests

### Test I.1: Full Pipeline - OAuth Example
```
Input: "Add OAuth with Google and GitHub. JWT 15m TTL. Rate limit 10/hour."
Pipeline:
  1. Detect: Node.js ✓
  2. Compress: No compression needed (< 1000 chars) ✓
  3. Transform: implement_oauth_authentication(...) ✓
  4. Validate: All checks pass ✓
  5. Optimize: Add timeout, retry, logging ✓
  6. Bridge: Save to cc10x ✓
Expected: Complete pseudo-code with all parameters
```

### Test I.2: Full Pipeline - Complex Requirement
```
Input: 2000-char requirement about payment processing
Pipeline:
  1. Detect: Node.js ✓
  2. Compress: Down to ~400 chars ✓
  3. Transform: implement_payment_processing(...) ✓
  4. Validate: Find missing rate limiting → CRITICAL ✓
  5. Optimize: Suggest rate limit values ✓
  6. Bridge: User confirms and saves ✓
Expected: Return compressed pseudo-code with suggestions
```

## Test Data

### Simple Requirement
```
Add email/password authentication with JWT tokens.
Tokens expire after 24 hours.
Rate limit login to 5 attempts per hour.
```

### Complex Requirement
```
We need to implement a payment processing system that:
1. Accepts credit cards via Stripe
2. Validates card information before charging
3. Retries failed transactions up to 3 times
4. Logs all transactions for auditing
5. Notifies users via email of transaction status
6. Handles webhook callbacks from Stripe
7. Stores encrypted transaction data
8. Supports refunds up to 30 days after transaction
9. Has rate limiting to prevent abuse
10. Returns appropriate error codes for each failure scenario
```

### Multi-Tech Stack Example
```
Implement API rate limiting middleware.
Should work with both Node.js/Express and Python/FastAPI.
Limit to 1000 requests per hour per user.
Return 429 when exceeded.
Use Redis backend.
```

## Success Criteria

Transform is successful when:
- [ ] Function naming follows [verb]_[subject] pattern
- [ ] All parameters are explicit (no vague values)
- [ ] Standard parameters included (timeout, logging, error_handling, security)
- [ ] Tech stack detected and used for file paths
- [ ] Compression preserves all critical details
- [ ] Validation catches missing security/error handling
- [ ] Bridge saves specification file correctly

Validation is successful when:
- [ ] Checks across all 6 dimensions
- [ ] Severity levels assigned correctly
- [ ] CRITICAL issues are actual blockers
- [ ] Explanations are specific (not generic)
- [ ] Actionable suggestions provided
