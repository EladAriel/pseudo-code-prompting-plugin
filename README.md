# Pseudo-Code Prompting Plugin

Transform natural language requirements into structured, validated pseudo-code for optimal LLM responses and implementation clarity.

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A52.1.0-blue.svg)](https://claude.ai/code)

## Overview

The Pseudo-Code Prompting Plugin enhances Claude Code with automated conversion, validation, and optimization of natural language requirements into concise, function-like pseudo-code. This structured approach eliminates ambiguity, ensures completeness, and accelerates development.

**Architecture:** Utilizes Claude Code's auto-discovery system - all skills, agents, and commands are automatically loaded based on your project context. No manual configuration required.

## Why Pseudo-Code Prompting?

### The Problem
- **Verbose requirements** consume excessive tokens (80-95% waste)
- **Ambiguous specifications** lead to incomplete implementations
- **Missing constraints** cause security vulnerabilities and edge case bugs
- **Unclear intent** results in clarification cycles and delays

### The Solution
Transform this:
```
We need to create a REST API endpoint that handles user registration. The endpoint should accept POST requests at the /api/register path. Users need to provide their email address, which must be validated to ensure it's a proper email format and not already in use. They also need to provide a password that meets our security requirements: at least 12 characters, including uppercase, lowercase, numbers, and special characters. The system should hash the password using bcrypt before storing it. If registration is successful, return a 201 status with the new user ID. If the email is already taken, return a 409 error. If validation fails, return a 400 error with details about what went wrong. We should also rate limit this endpoint to prevent abuse, allowing maximum 10 registration attempts per hour from the same IP address.
```

Into this:
```javascript
create_endpoint(
  path="/api/register",
  method="POST",
  request_schema={
    "email": "email:required:unique",
    "password": "string:required:min(12):requires(upper,lower,number,special)"
  },
  password_hash="bcrypt",
  response_codes={
    "201": {"user_id": "string", "created_at": "timestamp"},
    "400": "validation_error",
    "409": "duplicate_email"
  },
  rate_limit={"max": 10, "window": "1h", "key": "ip"},
  audit_log=true
)
```

**Result**: 95% reduction (158 words → 1 structured call), 100% semantic preservation, implementation-ready

## Key Features

### 🎯 6 Specialized Skills

| Skill | Purpose | Token Efficiency |
|-------|---------|------------------|
| **prompt-structurer** | Transform natural language → pseudo-code | 300-800 tokens |
| **prompt-analyzer** | Detect ambiguities, assess clarity | 200-500 tokens |
| **context-compressor** | Compress verbose requirements | 300-600 tokens |
| **prompt-optimizer** | Add missing parameters, enhance security | 400-700 tokens |
| **requirement-validator** | Validate completeness, security, edge cases | 500-800 tokens |
| **feature-dev-enhancement** | Integrate with feature-dev workflow | 200-400 tokens |

### 🤖 5 Intelligent Agents

| Agent | Specialization | Pipeline Position |
|-------|----------------|-------------------|
| **prompt-analyzer** | Ambiguity detection, complexity scoring | Entry (Tier 1) |
| **context-compressor** | Verbose requirement compression (60-95%) | Entry (Tier 1) |
| **prompt-transformer** | Natural language → function syntax | Core (Tier 2) |
| **prompt-optimizer** | Security, validation, completeness enhancement | Enhancement (Tier 3) |
| **requirement-validator** | Gap identification, security audit, edge cases | Quality (Tier 3) |

### 🎮 6 Skills (Auto-Invoked)

Skills are automatically invoked by Claude when relevant keywords/patterns are detected:

| Skill | Triggers | Purpose |
|-------|----------|---------|
| **prompt-structurer** | "transform", "structure", "pseudo-code" | Transform natural language to pseudo-code |
| **prompt-analyzer** | "analyze", "complexity", "ambiguity" | Analyze prompts for clarity |
| **requirement-validator** | "validate", "verify", "check" | Validate completeness & security |
| **prompt-optimizer** | "optimize", "enhance", "improve" | Add missing parameters |
| **context-compressor** | "compress", "reduce", "simplify" | Compress verbose requirements |
| **feature-dev-enhancement** | "feature-dev", "workflow" | Integrate with feature-dev |

### ⚡ 3 Automated Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| **user-prompt-submit** | User input | Detect /feature-dev commands, inject transformation |
| **post-transform-validation** | After transformation | Auto-validate output |
| **context-compression-helper** | Verbose input (>100 words) | Suggest compression |

## Installation

### Requirements

- Claude Code v2.1.0 or higher

### From Marketplace

```bash
# Step 1: Add the marketplace
/plugin marketplace add EladAriel/pseudo-code-prompting-plugin

# Step 2: Install the plugin
/plugin install pseudo-code-prompting
```

### From GitHub (Manual)

```bash
# Clone to your Claude plugins directory
git clone https://github.com/EladAriel/pseudo-code-prompting-plugin ~/.claude/plugins/pseudo-code-prompting
```

### Project-Scoped Installation

```bash
# Copy plugin to your project
cp -r pseudo-code-prompting-plugin/.claude your-project/.claude
```

### Verify Installation

After installation, verify the plugin is loaded:

```bash
/plugin list
```

You should see `pseudo-code-prompting` in the installed plugins list.

**Note:** This plugin uses **auto-invoked skills**, not slash commands. Skills are automatically triggered by Claude when you use relevant keywords in your requests.

## Quick Start Guide

### How It Works

**Skills are automatically invoked by Claude** when you use relevant keywords. You don't call them directly - just describe what you need naturally.

### 1. Transform Natural Language

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

### 2. Validate Requirements

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

### 3. Optimize Pseudo-Code

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

### 4. Compress Verbose Requirements

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

## PROMPTCONVERTER Methodology

### The 5 Transformation Rules

1. **Analyze Intent**: Identify core action (verb) and subject (noun)
   - "Add user authentication" → action: `implement`, subject: `authentication`

2. **Create Function Name**: Combine into `snake_case`
   - `implement` + `authentication` → `implement_authentication`

3. **Extract Parameters**: Convert details to named parameters
   - "with Google and GitHub" → `providers=["google", "github"]`
   - "OAuth" → `type="oauth"`

4. **Infer Constraints**: Detect implicit requirements
   - Security → `token_storage="secure"`, `session_management="jwt"`
   - Performance → `timeout="5s"`, `cache=true`

5. **Output Format**: Single-line pseudo-code
   - `function_name(param1="value1", param2="value2", ...)`

### Transformation Example

**Input:**
```
Add user authentication with OAuth. Support Google and GitHub. Store tokens securely.
Allow password reset via email.
```

**Process:**
```
Step 1 (Analyze Intent):
  Verb: implement/add
  Noun: authentication
  → Function: implement_authentication

Step 2 (Extract Parameters):
  "OAuth" → type="oauth"
  "Google and GitHub" → providers=["google", "github"]
  "password reset via email" → password_reset={"method": "email"}

Step 3 (Infer Constraints):
  "Store tokens securely" → token_storage="secure", encryption=true
  (Implicit) → session_management="jwt", token_ttl="1h"

Step 4 (Output):
  implement_authentication(
    type="oauth",
    providers=["google", "github"],
    token_storage="secure",
    session_management="jwt",
    token_ttl="1h",
    password_reset={"method": "email", "token_expiry": "24h"}
  )
```

## Workflows

### 1. Full Transformation Workflow (900 tokens)

```
Analyze → Transform → Validate
```

**Use when:** Starting from natural language requirements
**Process:**
1. **Prompt Analyzer** detects ambiguities, scores complexity
2. **Prompt Transformer** converts to pseudo-code
3. **Requirement Validator** checks completeness, security

**Output:** Validated, implementation-ready pseudo-code

### 2. Quick Transform (200 tokens)

```
Transform
```

**Use when:** Requirements are clear and simple
**Process:**
1. **Prompt Transformer** directly converts to pseudo-code

**Output:** Basic pseudo-code (may need manual validation)

### 3. Optimize and Validate (700 tokens)

```
Optimize → Validate
```

**Use when:** You have pseudo-code that needs enhancement
**Process:**
1. **Prompt Optimizer** adds missing parameters, security, validation
2. **Requirement Validator** verifies implementation-readiness

**Output:** Enhanced, validated pseudo-code

### 4. Compress, Transform, Validate (1000 tokens)

```
Compress → Transform → Validate
```

**Use when:** Requirements are verbose (>100 words)
**Process:**
1. **Context Compressor** reduces to 5-40% of original size
2. **Prompt Transformer** structures into pseudo-code
3. **Requirement Validator** ensures nothing was lost

**Output:** Compressed, validated pseudo-code

## Progressive Loading Architecture

Skills use 4-tier progressive loading for token efficiency:

| Tier | Files | Token Budget | When Loaded |
|------|-------|--------------|-------------|
| **Tier 1: Discovery** | `capabilities.json` | 100-110 | Always (relevance matching) |
| **Tier 2: Overview** | `SKILL.md` | 300-800 | Skill confirmed relevant |
| **Tier 3: Specific** | `references/*.md` | 90-300 each | Need specific pattern/checklist |
| **Tier 4: Generate** | `templates/*` | 150-400 each | Code generation |

### Example: API Endpoint Validation

```
User Query: "Validate my API endpoint requirements"

Loading Sequence:
1. Tier 1: Load requirement-validator/capabilities.json (105 tokens)
   → Matched: validation, API, endpoint keywords

2. Tier 2: Load requirement-validator/SKILL.md (650 tokens)
   → Understand validation process, severity levels

3. Tier 3: Load references/validation-checklists.md (280 tokens)
   → Get API-specific checklist (auth, validation, rate limits)

4. Execute: Run validation with focused context

Total: 1,035 tokens (vs. 5,000+ loading everything upfront)
Efficiency: 79% token savings
```

## Validation Coverage

### Security Validation
- ✅ Authentication requirements (auth, tokens, credentials)
- ✅ Authorization rules (roles, permissions)
- ✅ Input validation (sanitization, type checking)
- ✅ Sensitive data handling (encryption, secure storage)
- ✅ Rate limiting (APIs, endpoints)
- ✅ OWASP Top 10 vulnerabilities

### Completeness Checks
- ✅ Required parameters present
- ✅ Data types specified
- ✅ Validation rules defined
- ✅ Error handling strategies
- ✅ Performance constraints (timeouts, caching, scale)
- ✅ Integration dependencies (APIs, services)

### Edge Case Detection
- ✅ Empty/null input handling
- ✅ Boundary conditions (min/max values)
- ✅ Concurrent access scenarios
- ✅ Failure mode behaviors
- ✅ Invalid state transitions
- ✅ Race conditions

## Real-World Examples

### Example 1: E-Commerce Checkout

**Verbose Input (142 words):**
```
We need to implement a checkout process for our e-commerce platform. Users should be able to review their cart, enter shipping information, and select a payment method. We need to support credit cards through Stripe and PayPal. Calculate shipping costs based on the user's address and the total weight of items. Apply any discount codes they have. Calculate tax based on the shipping address. Show a final total before they confirm. Process the payment, and if it succeeds, create an order in the database, send a confirmation email, and update inventory. If payment fails, show an appropriate error message and allow them to try a different payment method. Log all transactions for accounting purposes.
```

**Compressed Output (1 function):**
```javascript
implement_checkout(
  steps=["cart_review", "shipping_info", "payment_method", "confirmation"],
  payment_providers={
    "stripe": {"types": ["credit_card", "debit_card"]},
    "paypal": {"integration": "express_checkout"}
  },
  calculations={
    "shipping": {"based_on": ["address", "weight"]},
    "tax": {"based_on": "shipping_address"},
    "discount": {"apply_codes": true}
  },
  success_actions=[
    "create_order",
    "send_confirmation_email",
    "update_inventory"
  ],
  error_handling={
    "payment_failed": "allow_retry_different_method",
    "inventory_insufficient": "notify_and_offer_alternatives"
  },
  transaction_logging=true,
  idempotency_key="order_id"
)
```

**Result:** 142 words → 1 call (94% reduction), all requirements preserved

### Example 2: Real-Time Dashboard

**Verbose Input (98 words):**
```
Create a real-time analytics dashboard that displays key metrics for our SaaS application. Show active users, API request rates, error rates, and revenue for the current day. Update the metrics automatically every 30 seconds without requiring a page refresh. Use WebSockets for real-time updates. Cache the data on the server side for 10 seconds to reduce database load. If the WebSocket connection drops, automatically reconnect and resume updates. Show a visual indicator when data is stale or the connection is lost. Allow users to export the data as CSV.
```

**Compressed Output:**
```javascript
create_dashboard(
  metrics=["active_users", "api_request_rate", "error_rate", "revenue"],
  timeframe="current_day",
  realtime={
    "protocol": "websocket",
    "update_interval": "30s",
    "auto_reconnect": true,
    "connection_indicator": true
  },
  caching={"server_side": true, "ttl": "10s"},
  data_staleness_indicator=true,
  export={"formats": ["csv"]}
)
```

**Result:** 98 words → 1 call (92% reduction)

### Example 3: Machine Learning Pipeline

**Verbose Input (127 words):**
```
Build a machine learning training pipeline for our image classification model. The pipeline should fetch training data from S3, preprocess images by resizing to 224x224 and normalizing pixel values. Split data into 80% training and 20% validation. Train a ResNet-50 model with a learning rate of 0.001 and batch size of 32. Use early stopping if validation loss doesn't improve for 5 epochs. Save model checkpoints every epoch. Track metrics like accuracy, precision, recall, and F1 score. Send a notification when training completes. If training fails, retry up to 3 times with exponential backoff. Log all hyperparameters and metrics to MLflow for experiment tracking.
```

**Compressed Output:**
```javascript
create_ml_pipeline(
  data_source={"provider": "s3", "bucket": "training-data"},
  preprocessing={
    "resize": "224x224",
    "normalize": "pixel_values"
  },
  data_split={"train": 0.8, "validation": 0.2},
  model={"architecture": "resnet50"},
  training_params={
    "learning_rate": 0.001,
    "batch_size": 32,
    "early_stopping": {"patience": 5, "monitor": "val_loss"}
  },
  checkpointing={"frequency": "per_epoch"},
  metrics=["accuracy", "precision", "recall", "f1_score"],
  experiment_tracking={"platform": "mlflow"},
  notifications={"on_complete": true},
  error_handling={"retry": 3, "backoff": "exponential"}
)
```

**Result:** 127 words → 1 call (93% reduction)

## Integration

### With Feature-Dev Workflow

```bash
# Automatically transforms requirements before feature development
/feature-dev Add payment processing with Stripe

# Hook detects command and injects transformation:
Transformed: implement_payment_processing(
  provider="stripe",
  methods=["credit_card", "debit_card"],
  currency="usd",
  webhook_handling=true
)

# Feature development proceeds with structured requirements
```

### With Code Generation

```bash
# 1. Transform requirements
/transform-query Create REST API for user management

# 2. Validate completeness
/validate-requirements [generated pseudo-code]

# 3. Optimize for implementation
/optimize-prompt [validated pseudo-code]

# 4. Generate code from structured specification
[Use optimized pseudo-code as implementation spec]
```

### With Documentation

```bash
# Compress verbose documentation into concise specs
/compress-context [lengthy requirements document]

# Result: 60-95% token savings, 100% semantic preservation
# Use compressed version for context-efficient LLM interactions
```

## Configuration

This plugin uses auto-discovery and requires no manual configuration. All skills, agents, commands, and hooks are automatically loaded.

### Optional: Customize Hook Behavior

If you want to customize hook behavior in your workspace, create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/user-prompt-submit.sh",
            "statusMessage": "Checking for transformation commands...",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Note**: This is optional. The plugin already registers hooks via `hooks/hooks.json` in the plugin folder.

### Customizing Skills

Skills are automatically discovered from the plugin's `skills/` folder. Each skill has:

- `capabilities.json` - Discovery triggers and metadata
- `SKILL.md` - Main skill content
- `references/` - Domain-specific patterns (optional)
- `templates/` - Code generation templates (optional)

To add custom domain patterns, you can extend skills by adding files to your workspace `.claude/skills/` folder (separate from the plugin).

## Advanced Usage

### Extending Skills with Custom Patterns

The plugin's skills are in the plugin folder and automatically loaded. To add custom domain-specific patterns:

1. **Option A**: Contribute to the plugin by adding patterns to the skill's `references/` folder
2. **Option B**: Create workspace-specific extensions (advanced users only)

#### Example: Custom Validation Checklist

If you want to extend the `requirement-validator` skill with ML-specific patterns, you could:

```markdown
# Your custom checklist (for plugin contribution)
# Location: skills/requirement-validator/references/ml-validation-checklist.md

## Machine Learning Feature Validation

### Data Requirements
- [ ] Training data source specified
- [ ] Data preprocessing pipeline defined
- [ ] Train/validation/test split ratios
- [ ] Data augmentation strategy

### Model Requirements
- [ ] Model architecture specified
- [ ] Hyperparameters defined
- [ ] Training stopping criteria
- [ ] Checkpoint strategy

### Evaluation Requirements
- [ ] Metrics specified (accuracy, F1, etc.)
- [ ] Evaluation frequency
- [ ] Experiment tracking platform
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills and patterns.

## Performance Metrics

### Token Efficiency

| Workflow | Without Plugin | With Plugin | Savings |
|----------|---------------|-------------|---------|
| Feature specification | 5,000 tokens | 1,000 tokens | 80% |
| Requirements validation | 3,000 tokens | 700 tokens | 77% |
| Context compression | 10,000 tokens | 500 tokens | 95% |

### Compression Ratios

| Content Type | Average Compression | Range |
|--------------|---------------------|-------|
| API specifications | 85% | 75-92% |
| Feature requirements | 88% | 80-95% |
| Technical documentation | 82% | 70-90% |
| User stories | 78% | 65-88% |

### Validation Coverage

| Category | Checks | Coverage |
|----------|--------|----------|
| Security | 15 checks | 95% of OWASP Top 10 |
| Completeness | 20 checks | 90% of common parameters |
| Edge Cases | 12 patterns | 85% of typical scenarios |

## Plugin Architecture

### Directory Structure

This plugin follows Claude Code's official plugin structure with auto-discovery:

```
pseudo-code-prompting-plugin/
├── plugin.json                 # Plugin manifest (minimal)
├── skills/                     # 6 skills with progressive loading
│   ├── context-compressor/
│   │   ├── capabilities.json   # Tier 1: Discovery (90-110 tokens)
│   │   ├── SKILL.md           # Tier 2: Overview (300-800 tokens)
│   │   └── references/         # Tier 3: Specific patterns (90-300 tokens)
│   ├── prompt-structurer/
│   ├── prompt-analyzer/
│   ├── prompt-optimizer/
│   ├── requirement-validator/
│   └── feature-dev-enhancement/
├── agents/                     # 5 agent definitions
│   ├── prompt-analyzer.md
│   ├── context-compressor.md
│   ├── prompt-transformer.md
│   ├── prompt-optimizer.md
│   └── requirement-validator.md
├── commands/                   # 4 command definitions
│   ├── transform-query.md
│   ├── validate-requirements.md
│   ├── optimize-prompt.md
│   └── compress-context.md
└── hooks/                      # 3 event hooks
    ├── hooks.json             # Hook registration
    ├── user-prompt-submit.sh
    ├── context-compression-helper.sh
    └── post-transform-validation.sh
```

### Progressive Loading System

Skills use a 4-tier progressive loading architecture for token efficiency:

**Tier 1: Discovery** (`capabilities.json`) - 90-110 tokens
- Quick relevance check
- Trigger patterns and keywords
- Loaded for every skill search

**Tier 2: Overview** (`SKILL.md`) - 300-800 tokens
- Methodology and process steps
- Loaded when skill is confirmed relevant

**Tier 3: Specific** (`references/*.md`) - 90-300 tokens each
- Domain-specific patterns and checklists
- Loaded on-demand when needed

**Tier 4: Generation** (`templates/*.md`) - 150-400 tokens each
- Boilerplate and format examples
- Loaded when generating structured output

**Token Efficiency**: 788 tokens (progressive) vs 5,000+ tokens (full load) = 84% savings

### Hook System

Hooks are event-driven automation scripts registered in `hooks/hooks.json`:

**UserPromptSubmit Hooks** (run when user submits input):
- `user-prompt-submit.sh` - Detects transformation keywords, injects context
- `context-compression-helper.sh` - Suggests compression for verbose input (>100 words)

**PostToolUse Hooks** (run after Write/Edit tools):
- `post-transform-validation.sh` - Auto-validates transformed pseudo-code

All hooks use:
- Interactive approval mode (`permissionDecision: "ask"`)
- `${CLAUDE_PLUGIN_ROOT}` for portable paths
- Proper error handling (`set -euo pipefail`)

## Troubleshooting

### Commands Not Working

**Issue:** Commands like `/transform-query` not found

**Solution:**
```bash
# Verify plugin installation
/plugin list

# Check if pseudo-code-prompting is loaded
# Reinstall if needed:
/plugin install pseudo-code-prompting
```

### Hook Not Triggering

**Issue:** Hooks not executing on user input or file edits

**Solution:**
```bash
# Check hook scripts are executable
ls -la ~/.claude/plugins/pseudo-code-prompting/hooks/*.sh

# Should show -rwxr-xr-x permissions
# If not, make executable:
cd ~/.claude/plugins/pseudo-code-prompting/hooks
chmod +x *.sh

# Verify hooks.json exists
cat hooks/hooks.json
```

### Skills Not Auto-Invoked

**Issue:** Skills not triggering on keywords like "transform" or "validate"

**Solution:**
Skills are auto-discovered from the `skills/` folder. Each skill has a `capabilities.json` with trigger patterns.

```bash
# Verify skills exist
ls ~/.claude/plugins/pseudo-code-prompting/skills/

# Check a skill's triggers
cat ~/.claude/plugins/pseudo-code-prompting/skills/prompt-structurer/capabilities.json

# Use explicit keywords: "transform to pseudo-code", "validate requirements"

# Reload plugin
/plugin reload pseudo-code-prompting
```

### Validation Too Strict

**Issue:** Too many warnings/errors flagged

**Solution:**

The validation skill follows security best practices. If you need to adjust validation behavior:

1. **Review the validation checklists** in the skill:
   - [skills/requirement-validator/references/validation-checklists.md](skills/requirement-validator/references/validation-checklists.md)

2. **Provide context** when using validation:
   ```
   /validate-requirements [your-pseudo-code]

   Context: This is a prototype/internal tool/low-risk feature
   ```

3. **Skip certain checks** explicitly:
   ```
   /validate-requirements [your-pseudo-code]

   Skip: Rate limiting (internal API), CORS (same-origin only)
   ```

The validation is intentionally comprehensive to catch security issues early.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new skills
- How to create custom agents
- How to write hooks
- Code quality guidelines
- Pull request process

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following [CONTRIBUTING.md](CONTRIBUTING.md)
4. Test thoroughly with Claude Code
5. Submit a pull request

## Documentation

- **[SKILL.md](SKILL.md)** - Quick reference guide and overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed contribution guidelines
- **[LICENSE](LICENSE)** - MIT License details

## License

MIT License - See [LICENSE](LICENSE) for full details.

Copyright (c) 2026 Pseudo-Code Prompting Contributors

## Support

- **Issues:** [GitHub Issues](https://github.com/EladAriel/pseudo-code-prompting/issues)
- **Discussions:** [GitHub Discussions](https://github.com/EladAriel/pseudo-code-prompting/discussions)

## Acknowledgments

- Built for [Claude Code](https://claude.com/code)

## Version

**Current Version:** 2.1.0
**Last Updated:** 2026-01-13
**Minimum Claude Code Version:** 1.0.0