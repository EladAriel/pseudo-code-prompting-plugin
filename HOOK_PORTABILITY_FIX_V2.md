# Hook Portability Fix v2

## Issue Discovered

After the initial fix changing shebangs to `#!/usr/bin/env sh`, the CI failed with shellcheck warnings because the hook scripts use **bash-specific features**:

- `[[ ]]` - Extended test syntax (bash only)
- `BASH_REMATCH` - Regex capture array (bash only)
- `set -o pipefail` - Pipeline failure handling (bash only)
- `=~` - Regex matching operator (bash only)
- `&>` - Combined stdout/stderr redirect (bash only)

## Solution

Changed shebang from `sh` to `bash`, using `#!/usr/bin/env bash` for portability:

### Before (Original - Not Portable)
```bash
#!/bin/bash  # Hardcoded path - fails if bash is in /usr/local/bin or elsewhere
```

### After Fix v1 (Incorrect - POSIX sh can't handle bash features)
```bash
#!/usr/bin/env sh  # Uses PATH to find sh, but scripts need bash features!
```

### After Fix v2 (Correct - Portable bash)
```bash
#!/usr/bin/env bash  # Uses PATH to find bash wherever it's installed
```

## Files Fixed

All hook scripts updated with correct shebang:
- `hooks/core/user-prompt-submit.sh`
- `hooks/compression/context-compression-helper.sh`
- `hooks/tree/context-aware-tree-injection.sh`
- `hooks/validation/post-transform-validation.sh`

All hook commands in `hooks/hooks.json` updated:
```json
{
  "command": "/usr/bin/env bash ${CLAUDE_PLUGIN_ROOT}/hooks/core/user-prompt-submit.sh"
}
```

## Why This Works

- **Portable**: `#!/usr/bin/env bash` finds bash wherever it's installed (PATH lookup)
- **Compatible**: bash is available on all major platforms (Windows Git Bash, macOS, Linux)
- **Correct**: Scripts actually require bash features, so using bash is appropriate
- **CI Passes**: Shellcheck validates bash syntax when shebang specifies bash

## Lesson Learned

When porting scripts to be more portable:
1. Check if scripts use shell-specific features (bash vs POSIX sh)
2. If bash features are needed, use `#!/usr/bin/env bash` (not `#!/bin/bash` or `#!/usr/bin/env sh`)
3. Run shellcheck to validate compatibility

## Testing

```bash
# Verify all shebangs are correct
head -1 hooks/**/*.sh

# Expected output:
#!/usr/bin/env bash
```

```bash
# Run shellcheck (should pass now with bash shebang)
shellcheck hooks/**/*.sh
```
