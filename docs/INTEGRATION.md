# Integration

## With Feature-Dev Workflow

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

## With Code Generation

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

## With Documentation

```bash
# Compress verbose documentation into concise specs
/compress-context [lengthy requirements document]

# Result: 60-95% token savings, 100% semantic preservation
# Use compressed version for context-efficient LLM interactions
```
