# Quick Start Guide

## How It Works

**Skills are automatically invoked by Claude** when you use relevant keywords. You don't call them directly - just describe what you need naturally.

## 1. Transform Natural Language

**You say:**
```
Transform this to pseudo-code: Add OAuth authentication with Google and GitHub providers
```

**Claude automatically invokes the `prompt-structurer` skill and responds:**
```javascript
implement_authentication(
  type="oauth",
  providers=["google", "github"],
  scope="user_auth",
  token_ttl="1h",
  refresh_token=true
)
```

## 2. Validate Requirements

**You say:**
```
Validate this requirement: create_endpoint(path="/api/users", method="POST")
```

**Claude automatically invokes the `requirement-validator` skill and responds:**

**Output:**
```
Requirement Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Function: create_endpoint(path="/api/users", method="POST")

✗ CRITICAL ISSUES (Must Fix)
- No authentication requirement specified
  → Required Action: Add auth=true, specify roles
- Missing request body schema
  → Required Action: Define request_schema with validation
- No error response codes defined
  → Required Action: Specify error_responses for 400, 401, 403, 500

⚠ WARNINGS (Medium Priority)
- No rate limiting specified
  → Suggestion: Add rate_limit="100/hour" to prevent abuse
- Missing CORS configuration
  → Suggestion: Add cors=["allowed-origins"] if needed

📋 EDGE CASES TO CONSIDER
- Duplicate user creation (409 conflict)
- Invalid data format (400 bad request)
- Database connection failure (500 server error)

Overall Status: BLOCKED (Critical issues must be resolved)
```

## 3. Optimize Pseudo-Code

```bash
/optimize-prompt fetch_data(url)
```

**Output:**
```javascript
Original:
fetch_data(url)

Optimized:
fetch_data(
  url="string:required:url",
  timeout="5s",
  error_handling="retry",
  retries=3,
  backoff="exponential",
  fallback="return_cached",
  circuit_breaker=true,
  logging=true
)

Improvements Made:
✓ Security
  - Added URL validation
✓ Error Handling
  - Retry strategy with exponential backoff
  - Circuit breaker for fault tolerance
  - Fallback to cached data
✓ Performance
  - Timeout specified to prevent hanging
✓ Observability
  - Logging enabled for debugging
```

## 4. Compress Verbose Requirements

```bash
/compress-context We need to implement a notification system that can send messages to users through multiple channels. Users should be able to receive notifications via email, SMS, and push notifications. When sending emails, use SendGrid. For SMS, use Twilio. Push notifications should go through Firebase Cloud Messaging. Users should be able to configure their preferences. The system should retry failed deliveries up to 3 times with exponential backoff. Track all delivery statuses and log all notification attempts.
```

**Output:**
```javascript
Original Length: 115 words
Compressed Length: 1 function call (~30 words)
Compression Ratio: 3.83:1 (74% reduction)

Compressed Pseudo-Code:
implement_notifications(
  channels={
    "email": {"provider": "SendGrid", "config": "env:SENDGRID_API_KEY"},
    "sms": {"provider": "Twilio", "config": "env:TWILIO_CREDENTIALS"},
    "push": {"provider": "FCM", "platforms": ["ios", "android"]}
  },
  user_preferences=true,
  retry_strategy={"attempts": 3, "backoff": "exponential"},
  delivery_tracking=true,
  audit_logging=true
)

Information Preserved:
✓ Multi-channel delivery: email, SMS, push
✓ Provider specifications: SendGrid, Twilio, FCM
✓ User preference management
✓ Retry logic with exponential backoff
✓ Delivery tracking and audit logging
```
