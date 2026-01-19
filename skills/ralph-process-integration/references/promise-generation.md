# Promise Generation Reference

## Overview

The promise generation algorithm extracts critical requirements from the validation report and formats them as a specific, testable completion promise for Ralph Loop.

## Purpose

A good completion promise:
1. **Specific:** References actual requirements from validation
2. **Testable:** Can be verified by checking code/tests/behavior
3. **Truthful:** Can only be output when genuinely complete
4. **Concise:** Short enough to be practical (< 100 chars preferred)

## Extraction Strategy

### Step 1: Identify Critical Requirements

**Source 1: Critical Issues Section**
```
✗ CRITICAL ISSUES (Must Fix)
- [Issue 1]
- [Issue 2]
- [Issue 3]
```

Extract top 3-4 most important issues.

**Source 2: Edge Cases Section** (if needed to reach 3-4 requirements)
```
📋 EDGE CASES TO CONSIDER
- [Edge case 1]
- [Edge case 2]
```

Extract top 1-2 edge cases.

### Step 2: Convert to Positive Requirements

Transform negative statements (problems) into positive statements (solutions).

**Conversion Patterns:**

| Negative Statement (Issue) | Positive Requirement |
|----------------------------|---------------------|
| "Missing [X]" | "[X] added" or "[X] implemented" |
| "No [X] specified" | "[X] defined" or "[X] configured" |
| "[X] not defined" | "[X] implemented" |
| "Unclear [X]" | "[X] clarified and implemented" |
| "Need [X]" | "[X] complete" |

**Examples:**

```
Issue: "Missing authentication requirement"
→ Requirement: "Authentication implemented"

Issue: "No error responses specified"
→ Requirement: "Error responses defined"

Issue: "Input validation not defined"
→ Requirement: "Input validation added"

Issue: "Rate limiting not specified"
→ Requirement: "Rate limiting configured"

Issue: "Missing test coverage"
→ Requirement: "Tests passing"

Issue: "Unclear data model"
→ Requirement: "Data model implemented"
```

### Step 3: Format Promise

**Format depends on number and complexity of requirements:**

#### Option 1: Specific Promise (1-3 requirements)

```
"COMPLETE: [req1] AND [req2] AND [req3]"
```

**Example:**
```
"COMPLETE: Authentication implemented AND Error handling added AND Tests passing"
```

**Best for:** Simple to medium tasks with clear, distinct requirements

#### Option 2: Count-Based Promise (4-6 requirements)

```
"IMPLEMENTATION COMPLETE: [N] requirements met"
```

**Example:**
```
"IMPLEMENTATION COMPLETE: 5 requirements met"
```

**Best for:** Medium to complex tasks with many requirements

#### Option 3: Generic Fallback (unclear requirements)

```
"IMPLEMENTATION COMPLETE AND VERIFIED"
```

**Best for:** When specific requirements cannot be extracted

### Step 4: Length Check

If promise exceeds 100 characters, simplify:

```
if len(promise) > 100:
    # Simplify to high-level
    promise = f"COMPLETE: {len(requirements)} critical requirements met"
```

**Example:**
```
Original (112 chars):
"COMPLETE: Authentication flow implemented AND Email validation added AND Password hashing configured AND Error responses defined"

Simplified (52 chars):
"COMPLETE: 4 critical requirements met"
```

## Promise Generation Algorithm

### Pseudocode Implementation

```python
def generate_promise(validation_report):
    requirements = []

    # Step 1: Extract critical issues
    critical_section = extract_section(validation_report, "✗ CRITICAL ISSUES")
    for issue in critical_section[:4]:  # Max 4
        req = convert_to_positive(issue)
        if req:
            requirements.append(req)

    # Step 2: Add edge cases if needed
    if len(requirements) < 3:
        edge_cases_section = extract_section(validation_report, "📋 EDGE CASES")
        needed = 3 - len(requirements)
        for edge_case in edge_cases_section[:needed]:
            req = convert_to_positive(edge_case)
            if req:
                requirements.append(req)

    # Step 3: Format based on count
    if len(requirements) == 0:
        # Fallback: no specific requirements found
        return "IMPLEMENTATION COMPLETE AND VERIFIED"

    elif len(requirements) <= 3:
        # Specific promise
        promise = "COMPLETE: " + " AND ".join(requirements)

    elif len(requirements) <= 6:
        # Count-based promise
        promise = f"IMPLEMENTATION COMPLETE: {len(requirements)} requirements met"

    else:
        # Too many, simplify
        promise = f"IMPLEMENTATION COMPLETE: {len(requirements)} requirements met"

    # Step 4: Length check
    if len(promise) > 100:
        if len(requirements) <= 3:
            # Try abbreviating
            promise = "COMPLETE: " + " + ".join([abbrev(r) for r in requirements])

        if len(promise) > 100:
            # Still too long, use count
            promise = f"COMPLETE: {len(requirements)} critical requirements met"

    return promise

def convert_to_positive(issue_text):
    """Convert negative issue statement to positive requirement"""

    # Remove list marker
    text = issue_text.strip().lstrip('- ')

    # Patterns for conversion
    if "missing" in text.lower():
        # "Missing authentication" → "Authentication added"
        thing = text.lower().replace("missing", "").strip()
        return f"{thing.capitalize()} added"

    if "no " in text.lower() or "not defined" in text.lower():
        # "No error handling" → "Error handling implemented"
        thing = text.lower().replace("no ", "").replace("not defined", "").strip()
        return f"{thing.capitalize()} implemented"

    if "unclear" in text.lower():
        # "Unclear requirements" → "Requirements clarified"
        thing = text.lower().replace("unclear", "").strip()
        return f"{thing.capitalize()} clarified"

    if "need" in text.lower():
        # "Need validation" → "Validation complete"
        thing = text.lower().replace("need", "").strip()
        return f"{thing.capitalize()} complete"

    # Default: try to infer positive form
    # "Handle token expiration" → "Token expiration handled"
    if text.startswith("Handle"):
        return f"{text[7:]} handled"

    # Fallback: append "resolved"
    return f"{text} resolved"
```

## Examples by Feature Category

### API Development

**Validation Report:**
```
✗ CRITICAL ISSUES
- Missing endpoint specification
- No request body schema defined
- Error response format not specified
- Authentication not required

📋 EDGE CASES
- Handle malformed JSON
- Rate limiting edge cases
```

**Extracted Requirements:**
1. "Endpoint specification added"
2. "Request schema defined"
3. "Error responses specified"
4. "Authentication required"

**Generated Promise:**
```
"IMPLEMENTATION COMPLETE: 4 requirements met"
```

**Rationale:** 4 requirements, medium complexity, use count-based format.

---

### UI Component

**Validation Report:**
```
✗ CRITICAL ISSUES
- Component structure not defined
- No state management approach

📋 EDGE CASES
- Handle loading states
- Error boundary handling
- Accessibility considerations
```

**Extracted Requirements:**
1. "Component structure defined"
2. "State management implemented"
3. "Loading states handled"

**Generated Promise:**
```
"COMPLETE: Component implemented AND State management added AND Loading handled"
```

**Rationale:** 3 clear requirements, use specific format.

---

### Data Processing

**Validation Report:**
```
✗ CRITICAL ISSUES
- Missing data validation rules
- No error handling for invalid data
- Output format not specified
- No performance considerations

📋 EDGE CASES
- Handle empty datasets
- Large file processing
- Invalid data format handling
- Memory constraints
```

**Extracted Requirements:**
1. "Data validation implemented"
2. "Error handling added"
3. "Output format defined"
4. "Performance optimized"

**Generated Promise:**
```
"IMPLEMENTATION COMPLETE: 4 requirements met"
```

**Rationale:** 4 distinct requirements, use count-based format.

---

### Security Feature

**Validation Report:**
```
✗ CRITICAL ISSUES
- Password hashing not specified
- No session management defined
- Token expiration not handled
- CSRF protection missing

📋 EDGE CASES
- Handle concurrent sessions
- Token refresh scenarios
- Account lockout logic
```

**Extracted Requirements:**
1. "Password hashing configured"
2. "Session management implemented"
3. "Token expiration handled"
4. "CSRF protection added"

**Generated Promise:**
```
"IMPLEMENTATION COMPLETE: 4 requirements met"
```

**Rationale:** Security-critical, 4 requirements, use count-based for safety.

---

### Database Migration

**Validation Report:**
```
✗ CRITICAL ISSUES
- Migration strategy not defined
- No rollback plan
- Data integrity not addressed
- No backup strategy

📋 EDGE CASES
- Handle partial failures
- Large dataset migration
- Concurrent access during migration
```

**Extracted Requirements:**
1. "Migration strategy defined"
2. "Rollback plan implemented"
3. "Data integrity ensured"
4. "Backup strategy configured"

**Generated Promise:**
```
"IMPLEMENTATION COMPLETE: 4 requirements met"
```

**Rationale:** High-stakes operation, use count-based for completeness.

## Testability Criteria

A good promise should be verifiable through:

### Code Inspection
- Files exist in expected locations
- Functions/classes are implemented
- Configuration is present

### Test Execution
- Unit tests pass
- Integration tests pass
- End-to-end tests pass

### Behavior Verification
- Feature works as described
- Edge cases are handled
- Errors are handled gracefully

### Documentation Check
- README updated
- API docs complete
- Comments in code

## Promise Quality Levels

### Excellent Promise (Specific + Testable)

```
"COMPLETE: Authentication working AND Tests passing AND Docs updated"
```

**Why excellent:**
- 3 distinct, testable requirements
- Each can be verified independently
- Clear success criteria

### Good Promise (Count-Based)

```
"IMPLEMENTATION COMPLETE: 5 requirements met"
```

**Why good:**
- Clear number of requirements
- Implies all validation issues resolved
- Testable through checklist

### Acceptable Promise (Generic)

```
"IMPLEMENTATION COMPLETE AND VERIFIED"
```

**Why acceptable:**
- Better than no promise
- Requires manual verification
- Use when specific requirements unclear

### Poor Promise (Vague)

```
"DONE"
```

**Why poor:**
- No context
- Not verifiable
- Easy to fake
- Doesn't reflect actual completion criteria

## Edge Cases in Promise Generation

### No Critical Issues Found

**Scenario:** Validation report has only warnings and passed checks

**Strategy:**
- Look at top warnings instead
- Convert warnings to requirements
- Use generic fallback if no warnings either

**Example:**
```
⚠ WARNINGS
- Consider adding tests
- Add error handling

Promise: "COMPLETE: Tests added AND Error handling implemented"
```

### Very Long Requirements List

**Scenario:** 10+ critical issues identified

**Strategy:**
- Take top 4-6 most critical
- Use count-based promise
- Don't try to list all in promise text

**Example:**
```
Promise: "IMPLEMENTATION COMPLETE: 10 requirements met"
```

### Ambiguous Issue Text

**Scenario:** Issue text is unclear or hard to convert

**Strategy:**
- Use best-effort conversion
- Keep it simple
- Fallback to "Issue resolved" if needed

**Example:**
```
Issue: "Unclear about the thing"
→ Requirement: "Thing clarified and implemented"
```

### Single Critical Issue

**Scenario:** Only one critical issue identified

**Strategy:**
- Extract it, but add edge cases to reach 2-3 requirements
- Use specific promise format
- Better to have 2-3 requirements than just 1

**Example:**
```
Issue: "Missing authentication"
Edge Case: "Handle token expiration"

Promise: "COMPLETE: Authentication added AND Token handling implemented"
```

## Integration with Ralph Loop

### Promise Output Format

Ralph Loop expects the promise in XML tags:

```xml
<promise>EXACT_PROMISE_TEXT</promise>
```

**Critical:** The text must match EXACTLY (case-sensitive, whitespace-sensitive)

### Promise in Ralph Prompt

Include clear instructions in the Ralph prompt:

```markdown
## Completion Signal

When you have completed ALL requirements and verified everything works:

Output this EXACT text:
<promise>[GENERATED_PROMISE_TEXT]</promise>

IMPORTANT:
- Match the text exactly (including capitalization)
- Only output when genuinely complete
- Do not lie to exit the loop
- Verify each requirement before claiming completion
```

### Multiple Verification Points

Encourage Ralph to verify multiple aspects:

```markdown
Verify before outputting promise:
1. [Requirement 1] - Check: [how to verify]
2. [Requirement 2] - Check: [how to verify]
3. [Requirement 3] - Check: [how to verify]
4. All tests pass
5. No errors in console/logs
```

## Common Mistakes to Avoid

### Mistake 1: Promises Too Specific

**Bad:**
```
"COMPLETE: UserAuthenticationController.authenticateUser() returns JWT token with HS256 signing"
```

**Why bad:** Too implementation-specific, brittle

**Better:**
```
"COMPLETE: Authentication working AND JWT tokens generated"
```

### Mistake 2: Promises Too Vague

**Bad:**
```
"STUFF DONE"
```

**Why bad:** Not testable, no clear criteria

**Better:**
```
"COMPLETE: Auth implemented AND Tests passing"
```

### Mistake 3: Promises Too Long

**Bad:**
```
"COMPLETE: Authentication fully implemented with JWT tokens AND Email validation working properly AND Password hashing configured with bcrypt AND Error handling for all edge cases AND Rate limiting in place AND Tests passing AND Documentation updated"
```

**Why bad:** 182 chars, hard to match exactly

**Better:**
```
"IMPLEMENTATION COMPLETE: 7 requirements met"
```

### Mistake 4: Including Implementation Details

**Bad:**
```
"COMPLETE: Implemented using bcrypt with 12 rounds"
```

**Why bad:** Specifies how, not what

**Better:**
```
"COMPLETE: Password hashing configured"
```

### Mistake 5: Conditional Promises

**Bad:**
```
"COMPLETE: Authentication added (if required)"
```

**Why bad:** Ambiguous, hard to verify

**Better:**
```
"COMPLETE: Authentication implemented"
```

## Version History

**1.0.0** - Initial promise generation patterns and examples
