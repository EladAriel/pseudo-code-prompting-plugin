# PROMPTCONVERTER Methodology

## The 5 Transformation Rules

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

## Transformation Example

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
