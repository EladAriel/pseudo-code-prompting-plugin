# Windows/WSL Troubleshooting Guide

## Issue #1: Phantom Stop Hook Error ❌

### Symptom

```text
● Ran 1 stop hook
  ⎿  Stop hook error: Failed with non-blocking status code: <3>
     WSL (9136 - Relay) ERROR: CreateProcessCommon:735:
     execvpe(/bin/bash) failed: No such file or directory
```

### Root Cause

This error is **NOT from your pseudo-code-prompting plugin**.

Your [hooks.json:37](hooks/hooks.json#L37) correctly has:
```json
"Stop": []
```

The error comes from the **Ralph Loop plugin** trying to execute bash scripts on Windows:
```
"C:\Users\[user]\.claude\plugins\cache\claude-plugins-official\ralph-loop\96276205880a/scripts/setup-ralph-loop.sh"
```

### Why This Happens

Ralph Loop uses bash scripts (`.sh` files) which require:
- Git Bash
- WSL (Windows Subsystem for Linux)
- MSYS2
- Cygwin

On Windows, if none of these are available or properly configured, the bash script fails.

### Solution Options

#### Option 1: Install Git Bash (Recommended)

1. Install Git for Windows: https://git-scm-downloads.microsoft.com
2. During installation, select "Use Git and optional Unix tools from Command Prompt"
3. Restart Claude Code
4. Test: `bash --version` in terminal

#### Option 2: Use WSL

1. Enable WSL in PowerShell (Admin):
   ```powershell
   wsl --install
   ```
2. Restart computer
3. Set default bash to WSL:
   ```powershell
   wsl --set-default Ubuntu
   ```
4. Test: `wsl bash --version`

#### Option 3: Contact Ralph Loop Maintainers

The Ralph Loop plugin should support Python hooks (like your plugin does) instead of bash scripts on Windows.

File an issue at the Ralph Loop repository suggesting:
- Migrate hooks from bash scripts to Python scripts
- Add Windows compatibility checks
- Provide fallback for missing bash

### Workaround (Temporary)

If you cannot install bash, you can:

1. **Skip Ralph Loop integration** - Use `/complete-process` alone
2. **Manual implementation** - Use pseudo-code output without Ralph
3. **Use Python-based automation** - Build custom iteration logic

### Verification

After installing Git Bash or WSL, verify:

```bash
# Check bash is available
bash --version

# Check bash is in PATH
where bash  # Windows
which bash  # WSL/Git Bash

# Test Ralph Loop hook script
bash "C:\Users\[user]\.claude\plugins\cache\claude-plugins-official\ralph-loop\96276205880a/scripts/setup-ralph-loop.sh" --help
```

### Expected Output (Success)

```text
✓ No stop hook errors
✓ Ralph Loop launches successfully
✓ Bash scripts execute without issues
```

## Issue #2: Hook Script Permission Denied

### Symptom

```text
● Ran 1 hook
  ⎿  Hook error: Permission denied: /path/to/script.sh
```

### Solution

Make scripts executable:

```bash
# In Git Bash or WSL
chmod +x ~/.claude/plugins/*/scripts/*.sh
chmod +x ~/.claude/plugins/*/hooks/*.sh
```

## Issue #3: Python Not Found

### Symptom

```text
● Ran 1 hook
  ⎿  Hook error: python3: command not found
```

### Solution

Ensure Python 3 is installed and in PATH:

```bash
# Check Python
python3 --version
python --version

# If missing, install:
# - Windows: https://python.org/downloads
# - WSL: sudo apt install python3
```

## Issue #4: Hook Timeout

### Symptom

```text
● Ran 1 hook
  ⎿  Hook error: Command timed out after 10s
```

### Explanation

Hooks in [hooks.json](hooks/hooks.json) have timeout settings:

```json
{
  "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/core/user-prompt-submit.py",
  "timeout": 10
}
```

If your system is slow or under load, hooks may timeout.

### Solution

Increase timeout in your local settings:

1. Create `.claude/settings.local.json` in your project
2. Override timeout:
   ```json
   {
     "hooks": {
       "timeoutMultiplier": 2.0
     }
   }
   ```

## Comparison: Bash Hooks vs Python Hooks

| Feature | Bash Hooks | Python Hooks |
| --- | --- | --- |
| Windows compatibility | ❌ Requires Git Bash/WSL | ✅ Native support |
| Cross-platform | ⚠️ Limited | ✅ Excellent |
| JSON parsing | ⚠️ jq or sed/awk | ✅ Built-in json module |
| Error handling | ⚠️ Complex | ✅ Try/except |
| Maintainability | ⚠️ Shell quirks | ✅ Clean syntax |
| Performance | ✅ Fast | ✅ Fast |
| Debugging | ⚠️ Difficult | ✅ Easy |

**Recommendation:** Always use Python hooks for cross-platform plugins.

## Your Plugin's Approach ✅

Your pseudo-code-prompting plugin uses **Python hooks**, which is the correct approach:

```json
{
  "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/core/user-prompt-submit.py"
}
```

**Benefits:**
- ✅ Works on Windows without Git Bash/WSL
- ✅ Uses Python's `json` module for parsing
- ✅ Clean error handling with try/except
- ✅ Easy to debug and maintain
- ✅ Cross-platform compatible

## Testing Your Hooks

### Test Python Hook Directly

```bash
# Navigate to plugin directory
cd ~/.claude/plugins/pseudo-code-prompting/

# Test user-prompt-submit hook
python3 hooks/core/user-prompt-submit.py

# Test with sample input (requires stdin)
echo '{"userMessage": "test"}' | python3 hooks/core/user-prompt-submit.py
```

### Expected Output

```text
✓ Hook executed successfully
✓ No errors in stderr
✓ Valid JSON output (if hook produces output)
```

## Debugging Tips

### Enable Hook Debugging

Set environment variable:

```bash
# Windows PowerShell
$env:CLAUDE_DEBUG_HOOKS = "true"

# Windows CMD
set CLAUDE_DEBUG_HOOKS=true

# WSL/Git Bash
export CLAUDE_DEBUG_HOOKS=true
```

### Check Hook Logs

Hook output appears in:
- Claude Code console (View → Output → Claude Code)
- Hook execution summary in chat

### Manual Hook Testing

```bash
# Set plugin root
export CLAUDE_PLUGIN_ROOT="/path/to/plugin"

# Run hook manually
python3 $CLAUDE_PLUGIN_ROOT/hooks/core/user-prompt-submit.py
```

## Summary

| Issue | Cause | Solution |
| --- | --- | --- |
| Stop hook error | Ralph Loop uses bash scripts | Install Git Bash or WSL |
| Permission denied | Scripts not executable | `chmod +x *.sh` |
| python3 not found | Python not in PATH | Install Python, update PATH |
| Hook timeout | Slow system or hook | Increase timeout multiplier |

## Need Help?

1. **Your plugin issues:** File at https://github.com/EladAriel/pseudo-code-prompting-plugin/issues
2. **Ralph Loop issues:** File at Ralph Loop repository (bash script compatibility)
3. **Claude Code issues:** File at https://github.com/anthropics/claude-code/issues

## Version

**1.0.0** - Initial Windows/WSL troubleshooting guide
