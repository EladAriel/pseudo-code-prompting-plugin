# Validation Tests

Minimal tests for 6-dimension validation pipeline.

## Test Suite 1: Security Dimension

### Test 1.1: Detect Missing Authentication
```
Input:
  implement_user_registration(
    name=user_input["name"],
    email=user_input["email"],
    ...
  )
  (no authentication mentioned)

Expected: CRITICAL issue
Message: "Authentication not specified"
```

### Test 1.2: Accept Proper Security
```
Input:
  implement_oauth_authentication(
    providers=["google"],
    security={
      "validate_input": true,
      "use_pkce": true,
      "secure_cookie": true
    },
    ...
  )

Expected: ✓ Security check passed
```

### Test 1.3: Detect Missing Rate Limiting on Public Endpoint
```
Input:
  implement_login(
    username=user_input,
    password=user_input,
    ...
  )
  (no rate limiting)

Expected: HIGH warning
Message: "No rate limiting on public endpoint"
```

### Test 1.4: Accept Rate Limiting
```
Input:
  implement_login(
    rate_limiting={"login_attempts": "10/1h"},
    ...
  )

Expected: ✓ Rate limiting check passed
```

## Test Suite 2: Completeness Dimension

### Test 2.1: Detect Vague Parameters
```
Input:
  implement_api_optimization(
    performance="optimize",
    security="make_secure",
    ...
  )

Expected: HIGH issue
Message: "Use specific values, not descriptions"
Examples: "timeout=5s" not "timeout=fast"
```

### Test 2.2: Accept Specific Parameters
```
Input:
  implement_api_caching(
    cache_ttl="5m",
    cache_backend="redis",
    max_cache_size="1GB",
    ...
  )

Expected: ✓ Completeness check passed
```

### Test 2.3: Detect Missing File Paths
```
Input:
  implement_payment_processing(
    providers=["stripe"],
    ...
  )
  (no target_files mentioned)

Expected: HIGH warning
Message: "No target files specified"
```

### Test 2.4: Detect Missing Timeout
```
Input:
  implement_external_api_call(
    endpoint="https://api.example.com",
    ...
  )
  (no timeout specified)

Expected: CRITICAL issue
Message: "No timeout specified (will hang indefinitely)"
```

## Test Suite 3: Error Handling Dimension

### Test 3.1: Detect Missing Error Codes
```
Input:
  implement_authentication(
    error_handling={}  (empty)
    ...
  )

Expected: CRITICAL issue
Message: "No error codes defined"
```

### Test 3.2: Accept Standard Error Codes
```
Input:
  implement_authentication(
    error_handling={
      "invalid_credentials": 401,
      "account_locked": 429,
      "permission_denied": 403
    },
    ...
  )

Expected: ✓ Error handling check passed
```

### Test 3.3: Detect Missing 401 for Auth Failure
```
Input:
  implement_token_validation(
    error_handling={
      "invalid_token": 400,  (should be 401)
      "expired_token": 400,  (should be 401)
      ...
    }
  )

Expected: CRITICAL or HIGH issue
Message: "Auth failures should return 401, not 400"
```

### Test 3.4: Detect Missing 429 for Rate Limit
```
Input:
  Pseudo-code mentions rate_limiting but error_handling doesn't include 429

Expected: HIGH issue
Message: "Rate limit exceeded should return 429"
```

### Test 3.5: Detect No Retry Strategy
```
Input:
  implement_external_service_call(
    endpoint="https://external-api.com",
    timeout="5s",
    error_handling={...},
    ...
  )
  (no retry logic)

Expected: HIGH warning
Message: "No retry strategy for transient failures"
```

## Test Suite 4: Data Handling Dimension

### Test 4.1: Detect No Input Validation
```
Input:
  implement_user_registration(
    email=user_input["email"],
    password=user_input["password"],
    ...
  )
  (no validation mentioned)

Expected: CRITICAL issue
Message: "No input validation specified"
```

### Test 4.2: Accept Validation Strategy
```
Input:
  implement_user_registration(
    validation={
      "validate_email_format": true,
      "validate_password_strength": true,
      "check_email_not_exists": true
    },
    ...
  )

Expected: ✓ Data handling check passed
```

### Test 4.3: Detect Plaintext Password Storage
```
Input:
  implement_authentication(
    storage={
      "password_storage": "plaintext"  or not mentioned
    }
  )

Expected: CRITICAL issue
Message: "Passwords must be hashed, not stored plaintext"
```

### Test 4.4: Detect Missing Concurrency Handling
```
Input:
  implement_payment_processing(
    (processes user payments)
    (no mention of locking, transactions, etc.)
    ...
  )

Expected: HIGH warning
Message: "Concurrent payment requests not addressed"
```

## Test Suite 5: Performance Dimension

### Test 5.1: Detect No Timeout
```
Input:
  implement_external_api_call(
    endpoint="https://external.com",
    ...
  )
  (no timeout)

Expected: CRITICAL issue
Message: "No timeout specified (can hang indefinitely)"
```

### Test 5.2: Accept Timeout
```
Input:
  implement_external_api_call(
    timeout="5s",
    retry={"max_attempts": 3},
    ...
  )

Expected: ✓ Performance check passed
```

### Test 5.3: Detect No Caching
```
Input:
  implement_user_profile_endpoint(
    (frequently accessed data)
    (no caching mentioned)
    ...
  )

Expected: MEDIUM suggestion
Message: "Consider caching user profiles (read-heavy operation)"
```

### Test 5.4: Detect Unbounded Result Set
```
Input:
  implement_list_users(
    (returns all users without pagination)
    ...
  )

Expected: HIGH issue
Message: "Unbounded result set (no pagination)"
```

## Test Suite 6: Edge Cases Dimension

### Test 6.1: Detect No Concurrency Handling
```
Input:
  implement_data_update(
    update_user_score(user_id, points),
    ...
  )
  (reads score, updates, writes - no locking)

Expected: HIGH warning
Message: "Race condition possible with concurrent updates"
```

### Test 6.2: Detect No External Service Failure Handling
```
Input:
  implement_send_notification(
    via_email_service="SendGrid",
    ...
  )
  (no fallback if SendGrid down)

Expected: HIGH warning
Message: "No handling if email service unavailable"
```

### Test 6.3: Detect Boundary Condition Issues
```
Input:
  implement_string_processing(
    split_string(user_input, delimiter),
    (doesn't handle empty string or null)
    ...
  )

Expected: MEDIUM suggestion
Message: "Consider empty string and null input handling"
```

### Test 6.4: Detect No Resource Cleanup
```
Input:
  implement_file_upload(
    save_file_to_disk(file),
    (doesn't mention cleanup on error)
    ...
  )

Expected: MEDIUM suggestion
Message: "Consider cleanup (delete temp file) on error"
```

## Integration Tests

### Test I.1: Full Validation - Good Spec
```
Input:
  implement_oauth_authentication(
    providers=["google", "github"],
    token_type="jwt",
    access_token_ttl="15m",
    rate_limiting={"login_attempts": "10/1h"},
    target_files=["src/auth/oauth.ts", ...],
    error_handling={
      "invalid_provider": 400,
      "token_expired": 401,
      "rate_limit_exceeded": 429
    },
    security={
      "validate_input": true,
      "use_pkce": true
    },
    timeout="5s",
    retry={"max_attempts": 3}
  )

Expected Output:
  ✓ PASSED CHECKS (6+)
  ✗ CRITICAL ISSUES: None
  ⚠ HIGH WARNINGS: None or 1-2
  📋 MEDIUM: 0-2 suggestions
  OVERALL: READY
```

### Test I.2: Full Validation - Needs Review
```
Input:
  implement_payment_processing(
    amount=user_input["amount"],
    currency=user_input["currency"],
    stripe_token=user_input["token"],
    ...
  )
  (minimal validation, no rate limiting, no error handling)

Expected Output:
  ✓ PASSED CHECKS: Basic structure
  ✗ CRITICAL ISSUES:
    - No input validation
    - No rate limiting
  ⚠ HIGH WARNINGS:
    - No timeout specified
    - No retry logic
  📋 MEDIUM: 2-3 suggestions
  OVERALL: NEEDS REVIEW
```

### Test I.3: Full Validation - Blocked
```
Input:
  implement_user_authentication(
    ... (no authentication specified at all, just stores in plaintext)
    ...
  )

Expected Output:
  ✓ PASSED CHECKS: None or minimal
  ✗ CRITICAL ISSUES: 5+
    - No authentication method
    - Passwords not encrypted
    - No authorization checks
    - No rate limiting
    - No input validation
  OVERALL: BLOCKED
```

## Test Data

### Example 1: Simple OAuth
```
implement_oauth_authentication(
  providers=["google"],
  token_type="jwt",
  access_token_ttl="15m",
  target_files=["src/auth/oauth.ts"],
  error_handling={
    "invalid_provider": 400,
    "token_expired": 401
  },
  security={"use_pkce": true},
  timeout="5s"
)
```

### Example 2: API Endpoint
```
implement_user_list_api(
  method="GET",
  endpoint="/api/users",
  pagination={"page_size": 20},
  target_files=["src/routes/users.ts"],
  error_handling={
    "invalid_page": 400,
    "unauthorized": 401,
    "not_found": 404
  },
  timeout="5s",
  cache={"ttl": "5m"}
)
```

### Example 3: Database Operation
```
implement_update_user_profile(
  fields=["name", "email", "bio"],
  validation={
    "validate_email_format": true,
    "check_email_unique": true
  },
  error_handling={
    "validation_failed": 400,
    "email_exists": 409,
    "not_found": 404
  },
  timeout="5s"
)
```

## Success Criteria

Validation is successful when:
- [ ] All 6 dimensions checked
- [ ] CRITICAL issues are actual blockers (security, system crashes)
- [ ] HIGH issues are important (incomplete error handling, missing rate limiting)
- [ ] MEDIUM issues are suggestions (optimizations, edge cases)
- [ ] Each issue has specific explanation and suggestion
- [ ] Severity assignments are consistent
- [ ] Non-applicable checks are skipped with reasoning
