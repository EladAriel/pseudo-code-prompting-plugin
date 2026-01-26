# Learned Patterns - Pseudo-Code Prompting

## Authentication Patterns

### JWT Authentication
User prefers comprehensive security features including:
- Dual token system (access + refresh tokens)
- Password hashing with bcrypt
- Session management with database storage
- Rate limiting for login/register endpoints
- Audit logging for security events
- Email verification for new accounts
- Account lockout after failed attempts

Example transformation:
```
implement_user_authentication(
  token_type="jwt",
  framework="fastapi",
  features=["access_token", "refresh_token", "password_hashing", "email_verification", "session_management", "rate_limiting", "audit_logging", "account_lockout"],
  algorithm="HS256",
  password_scheme="bcrypt",
  database="sqlalchemy",
  token_storage="database_sessions"
)
```

Apply next time when: User requests authentication, JWT, or security-related implementations

### Production Authentication Optimization Pattern
When optimizing authentication pseudo-code, ALWAYS add these missing parameters:

**Security Essentials:**
- secret_key with validation (min_length=32, env_var, production_warning)
- password_policy with comprehensive rules (min_length, require_uppercase, require_numbers, require_special_chars, regex)
- token_blacklist mechanism with cleanup strategy
- security_headers (X-Content-Type-Options, X-Frame-Options, HSTS, CSP)
- input_sanitization to prevent injection attacks

**Token Configuration:**
- access_token_expiry with specific duration (default: 15 minutes)
- refresh_token_expiry with specific duration (default: 7 days)
- token_rotation strategy for refresh tokens
- token_storage schema with complete fields

**Database Specifications:**
- connection_pool settings (min_size, max_size, timeout, pool_pre_ping)
- Complete model schemas with fields, types, relationships, indexes
- Cleanup strategies for temporary data (failed_attempts, audit_logs)

**Redis/Cache:**
- redis_url, connection_timeout, max_connections
- Specific use cases (rate_limiting, session_cache, token_blacklist_cache)

**Email Service:**
- provider configuration (SendGrid/etc)
- api_key with validation
- template specifications for each email type
- expiry times and cooldown periods

**Rate Limiting:**
- Endpoint-specific limits (login=5/min, register=3/min, password_reset=3/hour)
- Global limits (per_ip, per_user)
- Storage backend (Redis)

**RBAC:**
- Default roles with descriptions and permissions
- Assignment strategy (user_roles table)
- Permission check mechanism

**Account Lockout:**
- max_attempts, lockout_duration_minutes
- Tracking storage and cleanup policy
- Notification configuration

**Audit Logging:**
- List of specific events to track (12+ security events)
- Retention policy in days
- Fields to capture (user_id, event_type, ip_address, user_agent, details, timestamp)
- Index configuration

Example: Session 2026-01-25 added 50+ parameters to bare authentication pseudo-code

Apply next time when: User provides authentication pseudo-code that needs optimization

## Python/FastAPI Patterns

### Naming Conventions
- Files: snake_case (auth_utils.py, email_service.py)
- Functions: snake_case (create_access_token, verify_password)
- Classes: PascalCase (TokenManager, PasswordManager, User)
- Parameters: snake_case with type hints (user_id: str, expires_delta: Optional[timedelta])

### Project Structure
- Routes in routes/ directory
- Utility classes in *_utils.py files
- Models in models.py
- Schemas in schemas.py
- Configuration in config.py

Apply next time when: Working with Python/FastAPI projects

## General Transformation Patterns

### Security/Auth Domain
When transforming security-related requests:
1. Always include authentication method (oauth, jwt, saml, etc.)
2. Specify password hashing scheme if applicable
3. Include session management strategy
4. Add security features as array parameter
5. Specify token types and expiration strategies

### Parameter Organization
- Core requirement: First parameters (type, framework, method)
- Features list: Mid-section as array
- Technical details: Later parameters (algorithm, scheme, storage)
- Configuration: Final parameters (timeouts, limits, etc.)

## Optimization Parameter Categories

### Category 1: Security (Highest Priority)
Always add: secret_key, password_policy, token_blacklist, security_headers, input_sanitization, CORS, RBAC

### Category 2: Configuration
Always add: token_expiry (access + refresh), database_pool, redis_config, email_service_config

### Category 3: Operational
Always add: rate_limiting (with specific limits), audit_logging (with events list), account_lockout (with thresholds)

### Category 4: Integration
Always add: middleware stack, lifecycle hooks, health_checks, error_handlers

### Category 5: Data Models
Always add: complete schemas with fields, types, relationships, indexes, constraints
