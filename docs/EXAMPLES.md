# Real-World Examples

## Example 1: E-Commerce Checkout

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

## Example 2: Real-Time Dashboard

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

## Example 3: Machine Learning Pipeline

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

## Example 4: LangChain Guardrails Documentation Compression

**Verbose Input (~4,200 tokens - LangChain documentation):**
```
Full documentation covering guardrails implementation, including safety checks, content filtering, PII detection strategies (redact/mask/hash/block), human-in-the-loop workflows, custom middleware patterns, before/after agent hooks, layered protection architecture, deterministic vs model-based approaches, code examples in both class and decorator syntax, configuration parameters, and resource links.
```

**Compressed Output (~850 tokens):**
```javascript
// Core Concept
guardrails(
  purpose="validate_and_filter_content_at_execution_points",
  intercept_at=["before_agent", "after_agent", "model_calls", "tool_calls"],
  use_cases=["prevent_pii_leakage", "block_prompt_injection",
             "block_harmful_content", "enforce_compliance",
             "validate_output_quality"]
)

// Guardrail Types
guardrail_approaches(
  deterministic={
    "method": "rule_based_logic",
    "patterns": ["regex", "keyword_matching", "explicit_checks"],
    "pros": ["fast", "predictable", "cost_effective"],
    "cons": ["may_miss_nuanced_violations"]
  },
  model_based={
    "method": "llm_or_classifier_evaluation",
    "capabilities": ["semantic_understanding", "catch_subtle_issues"],
    "pros": ["nuanced_detection"],
    "cons": ["slower", "more_expensive"]
  }
)

// Built-in PII Detection
PIIMiddleware(
  supported_types=["email", "credit_card", "ip", "mac_address", "url"],
  strategies={
    "redact": "replace_with_[REDACTED_{TYPE}]",
    "mask": "partial_obscure_last4",
    "hash": "deterministic_hash",
    "block": "raise_exception"
  },
  config_params={
    "pii_type": "required",
    "strategy": "default=redact",
    "apply_to_input": "default=true",
    "apply_to_output": "default=false"
  }
)

// Human-in-the-Loop
HumanInTheLoopMiddleware(
  purpose="require_human_approval_for_sensitive_ops",
  use_cases=["financial_transactions", "delete_production_data",
             "external_communications"],
  requirements=["checkpointer", "thread_id"],
  workflow=[
    "agent.invoke(messages, config={'thread_id': 'id'})",
    "agent_pauses_for_approval()",
    "agent.invoke(Command(resume={'decisions': [{'type': 'approve'}]}), config=same_thread)"
  ]
)

// Custom Guardrails
before_agent_guardrail(
  timing="once_at_start_of_invocation",
  use_cases=["session_level_checks", "authentication",
             "rate_limiting", "block_inappropriate_requests"],
  pattern="@hook_config(can_jump_to=['end'])"
)

after_agent_guardrail(
  timing="once_before_returning_to_user",
  use_cases=["model_based_safety_checks", "quality_validation",
             "compliance_scans", "output_filtering"],
  pattern="@hook_config(can_jump_to=['end'])"
)

// Layered Protection
multi_layer_guardrails(
  execution_order="sequential_in_middleware_array",
  layers=[
    "ContentFilterMiddleware (deterministic_input)",
    "PIIMiddleware (pii_protection_input_output)",
    "HumanInTheLoopMiddleware (approval_for_sensitive_tools)",
    "SafetyGuardrailMiddleware (model_based_output_check)"
  ]
)


// Architecture Decisions
decisions([
  {"id": "GUARD-001", "pattern": "middleware_interception",
   "execution_points": ["before_agent", "after_agent", "model_calls", "tool_calls"]},
  {"id": "GUARD-002", "pattern": "dual_approach",
   "types": ["deterministic", "model_based"]},
  {"id": "GUARD-003", "pattern": "layered_protection",
   "execution": "sequential_middleware_array"}
])
```

**Result:** 4,200 tokens → 850 tokens (80% reduction), 95%+ information retention

**Key Achievements:**

- Preserved all critical concepts, patterns, and examples
- Compressed verbose explanations into function parameters
- Converted long code examples into essential syntax patterns
- Maintained technical accuracy and all configuration options
- Created quick-reference format for implementation

## Usage Examples from Repository

Real-world usage examples are available in the [examples/](../examples/) folder:

- **[create-auth-api-example](../examples/create-auth-api-example/)** - Authentication API endpoint design
  - Demonstrates natural language → pseudo-code transformation
  - Shows validation and optimization in action
  - Complete API specification with security requirements

See [examples/README.md](../examples/README.md) for more details and how to add your own examples.
