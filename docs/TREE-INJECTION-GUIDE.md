# Tree Injection Technical Guide

## Architecture Overview

The Context-Aware Tree Injection system consists of three integrated components:

```
User Prompt ("implement feature")
        ↓
┌─────────────────────────────────────────┐
│ context-aware-tree-injection.sh (Hook) │
│ - Keyword detection                     │
│ - Python script invocation              │
│ - Context formatting & injection        │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ get_context_tree.py (Generator)        │
│ - Directory scanning                    │
│ - Filtering & gitignore support         │
│ - ASCII tree formatting                 │
│ - Truncation & error handling           │
└─────────────────────────────────────────┘
        ↓
[CONTEXT-AWARE MODE] + PROJECT_TREE
        ↓
┌─────────────────────────────────────────┐
│ context-aware-transform.md (Command)    │
│ - Rule A: Map to existing structure     │
│ - Rule B: Generate virtual skeleton     │
│ - Stack detection & template application│
└─────────────────────────────────────────┘
        ↓
Architecture-Aligned Response
```

## Component 1: Python Tree Generator

**File**: `hooks/get_context_tree.py`

### Purpose
Scan project directories and generate ASCII tree representations with intelligent filtering and error handling.

### Key Features

#### 1. Cross-Platform Timeout Handling
```python
if platform.system() == 'Windows':
    timer = threading.Timer(timeout, handle_timeout, args=[generator])
    timer.daemon = True
    timer.start()
else:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
```

**Rationale**: Windows doesn't support `signal.alarm()`, so we use `threading.Timer` as a fallback.

#### 2. Intelligent Filtering

**Default Exclusions**:
- Version control: `.git`, `.svn`
- Dependencies: `node_modules`, `vendor`, `bower_components`
- Build output: `dist`, `build`, `out`, `target`
- Python caches: `__pycache__`, `.pytest_cache`, `.mypy_cache`
- Virtual environments: `venv`, `.venv`
- IDE files: `.idea`, `.vscode`

**Gitignore Support**:
```python
def load_gitignore_patterns(self) -> Set[str]:
    gitignore_path = self.root_path / '.gitignore'
    patterns = set()

    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.add(line)

    return patterns
```

**Pattern Matching** (simplified glob):
- `*.pyc` → Matches all `.pyc` files
- `node_modules/` → Matches directory
- `build` → Matches file or directory named `build`

#### 3. Performance Optimizations

**Early Termination**:
```python
if self.file_count >= self.max_files or self.timed_out:
    break
```

Stops scanning once limits are reached.

**Lazy Evaluation**:
- Processes entries incrementally
- Doesn't load entire tree into memory at once
- Yields results as they're generated

**Depth Limiting**:
```python
if current_depth >= self.max_depth:
    return []
```

Prevents excessive recursion on deeply nested projects.

#### 4. Error Handling

**Permission Errors**:
```python
try:
    entries = list(dir_path.iterdir())
except PermissionError:
    self.errors.append(f"Permission denied: {dir_path}")
    self.skipped_count += 1
    return tree  # Continue with partial results
```

**Encoding Errors**:
```python
with open(gitignore_path, 'r', encoding='utf-8', errors='replace') as f:
    # 'replace' mode substitutes invalid characters with �
```

**Symlink Detection**:
```python
if entry.is_symlink():
    continue  # Skip symlinks to avoid cycles
```

#### 5. Output Truncation

```python
def truncate_output(self, tree_string: str) -> str:
    tree_bytes = tree_string.encode('utf-8')

    if len(tree_bytes) <= MAX_OUTPUT_BYTES:
        return tree_string

    truncated_bytes = tree_bytes[:MAX_OUTPUT_BYTES - 500]
    truncated_string = truncated_bytes.decode('utf-8', errors='ignore')

    footer = f"\n\n[TRUNCATED: Output exceeded {MAX_OUTPUT_BYTES} bytes]"
    footer += f"\nShowing partial tree (scanned {self.file_count} files)"

    return truncated_string + footer
```

**Strategy**: Keep the top of the tree (most important directories) and add truncation notice.

### Configuration

**Command-Line Interface**:
```bash
python3 get_context_tree.py [path] [options]

Options:
  --max-depth N        Maximum recursion depth (default: 10)
  --max-files N        Maximum files to scan (default: 1000)
  --include-hidden     Include hidden files/directories
  --timeout N          Execution timeout in seconds (default: 10)
```

**Exit Codes**:
- `0` - Success (tree generated or empty)
- `1` - Error (directory doesn't exist, permissions, etc.)

### Example Output

**Normal Project**:
```
project/
|-- src/
|   |-- components/
|   |   |-- Header.tsx
|   |   +-- Footer.tsx
|   +-- lib/
|       +-- utils.ts
+-- package.json

Total: 4 files, 3 directories (scanned to depth 10)
```

**Empty Project**:
```
<<PROJECT_EMPTY_NO_STRUCTURE>>
```

**Error/Truncated**:
```
project/
|-- src/
... [many files] ...

[TRUNCATED: Output exceeded 51200 bytes]
Showing partial tree (scanned 1000 files, 200 directories)

Total: 1000 files (limited to 1000 files), 200 directories
Skipped: 5 items (permission denied or errors)
```

## Component 2: Bash Hook Orchestrator

**File**: `hooks/context-aware-tree-injection.sh`

### Purpose
Detect implementation keywords in user prompts, invoke the Python tree generator, and inject structured context into Claude's prompt.

### Workflow

#### 1. Stdin Parsing
```bash
INPUT=$(cat)

if [[ "$INPUT" =~ \"prompt\":[[:space:]]*\"([^\"]+)\" ]]; then
  PROMPT="${BASH_REMATCH[1]}"
else
  exit 0  # No prompt found, pass through
fi
```

**Input Format** (JSON):
```json
{
  "session_id": "abc123",
  "prompt": "implement user authentication",
  "cwd": "/path/to/project",
  "permission_mode": "ask"
}
```

#### 2. Keyword Detection
```bash
if [[ "$PROMPT" =~ (implement|create|add|refactor|build|generate|setup|initialize) ]]; then
  # Trigger tree injection
fi
```

**Trigger Keywords**:
- `implement` - "implement user auth"
- `create` - "create API endpoint"
- `add` - "add payment module"
- `refactor` - "refactor database layer"
- `build` - "build dashboard"
- `generate` - "generate CRUD"
- `setup` - "setup testing framework"
- `initialize` - "initialize project"

#### 3. Python Detection
```bash
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
  PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
  PYTHON_CMD="python"
else
  exit 0  # Python not available, graceful degradation
fi
```

**Fallback Chain**:
1. Try `python3` (preferred)
2. Try `python`
3. Exit gracefully if neither exists

#### 4. Tree Generation with Timeout
```bash
if command -v timeout &> /dev/null; then
  TREE_OUTPUT=$($PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1)
elif command -v gtimeout &> /dev/null; then
  TREE_OUTPUT=$(gtimeout 15s $PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1)
else
  TREE_OUTPUT=$($PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 10 --max-files 1000 2>&1)
fi
```

**Timeout Tools**:
- `timeout` (GNU coreutils, Linux)
- `gtimeout` (macOS with `brew install coreutils`)
- No timeout (fallback, risk of hanging)

#### 5. Error Handling
```bash
if [[ "$TREE_OUTPUT" == "[TREE_ERROR]" ]] || [[ -z "$TREE_OUTPUT" ]] || [[ "$TREE_OUTPUT" == *"[ERROR:"* ]]; then
  exit 0  # Graceful degradation
fi
```

**Error Scenarios**:
- Python script returns `[TREE_ERROR]`
- Empty output
- Output contains `[ERROR:` marker

**Recovery**: Silent pass-through, no context injection.

#### 6. Context Injection
```bash
cat <<EOF

[CONTEXT-AWARE MODE ACTIVATED]

Project Structure:
\`\`\`
$TREE_OUTPUT
\`\`\`

Use this project structure as context for the request: "$PROMPT"

When responding:
1. Reference existing files and directories from the structure above
2. Suggest modifications that align with the current architecture
3. Identify where new files should be placed based on existing patterns
4. Detect the technology stack from visible files (package.json, requirements.txt, etc.)

EOF
```

**Format**:
- Markdown code block for tree (triple backticks)
- Clear instructions for Claude
- Reference to original prompt

### Hook Registration

**File**: `hooks/hooks.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/context-aware-tree-injection.sh",
            "statusMessage": "Analyzing project structure for context-aware suggestions...",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

**Key Fields**:
- `type: "command"` - Execute as shell command
- `${CLAUDE_PLUGIN_ROOT}` - Portable path variable
- `timeout: 15` - 15 second limit (Python: 10s + overhead: 5s)
- `statusMessage` - User feedback during execution

### Performance Characteristics

**Typical Execution Times**:
- Small project (<100 files): 50-200ms
- Medium project (100-500 files): 200-500ms
- Large project (500-1000 files): 500ms-2s
- Very large (>1000 files): 2-10s (hits file limit)

**Memory Usage**:
- Python process: 10-50MB typically
- Peak: ~100MB for large projects

**Network Mounted Directories**:
- Can be 5-10x slower due to I/O latency
- May trigger timeout on large projects

## Component 3: Context-Aware Transform Command

**File**: `commands/context-aware-transform.md`

### Purpose
Process user requests using one of two strategies based on whether project structure is available.

### Rule A: Map to Existing Structure

**Trigger**: `PROJECT_TREE` is present in context and not `<<PROJECT_EMPTY_NO_STRUCTURE>>`

**Process**:
1. **Parse Tree** - Extract directories, files, patterns
2. **Detect Stack** - Identify technology from indicators:
   - `package.json` + `next.config.js` → Next.js
   - `requirements.txt` + `app/` → FastAPI
   - `go.mod` + `cmd/` → Go
3. **Analyze Architecture** - Identify patterns:
   - MVC (controllers/, models/, views/)
   - Feature-based (features/auth/, features/orders/)
   - Layered (api/, services/, data/)
4. **Generate Response** - Provide:
   - Specific file paths from tree
   - Pattern matching rationale
   - Integration points

**Example Output**:
```
[CONTEXT-AWARE ANALYSIS]

Detected Stack: Next.js 13+ (React with TypeScript)
Project Pattern: App directory with feature organization

Implementation Plan:
1. Create src/lib/auth.ts
   - Follows existing lib/ utilities pattern
2. Create src/app/api/auth/route.ts
   - Next.js 13 app directory API route
...
```

### Rule B: Generate Virtual Skeleton

**Trigger**: `PROJECT_TREE` equals `<<PROJECT_EMPTY_NO_STRUCTURE>>` or not present

**Process**:
1. **Infer Stack** - Detect from request keywords:
   - "FastAPI" → python_fastapi
   - "Next.js", "React" → nextjs_react
   - "Express", "Node" → node_express
   - "Go", "Golang" → golang
   - No indicators → default
2. **Select Template** - Load predefined structure for stack
3. **Generate Skeleton** - Output complete directory tree
4. **Provide Steps** - Include initialization commands

**Example Output**:
```
[VIRTUAL SKELETON GENERATION]

Inferred Stack: python_fastapi
Detection Reason: "FastAPI" keyword in request

Recommended Structure:
app/
├── api/
│   └── endpoints/
│       └── users.py
├── core/
│   ├── config.py
│   └── security.py
...

Implementation Plan:
1. pip install fastapi uvicorn sqlalchemy
2. Create directory structure
3. Implement user endpoints
...
```

### Stack Templates

**Defined Templates**:
1. **nextjs_react** - Next.js 13+ with React
2. **node_express** - Node.js with Express
3. **python_fastapi** - Python with FastAPI
4. **golang** - Go with standard layout
5. **default** - Generic structure

**Template Structure**:
```markdown
### nextjs_react
\`\`\`
project/
├── src/
│   ├── app/                    # Next.js app directory
│   ├── components/             # React components
│   ├── lib/                    # Utilities
│   └── hooks/                  # Custom hooks
...
\`\`\`

**Indicators**: next, nextjs, react, app directory
```

### Integration

**Hook → Command Flow**:
```
1. Hook detects "implement" keyword
2. Hook generates PROJECT_TREE
3. Hook injects: [CONTEXT-AWARE MODE] + PROJECT_TREE
4. Claude sees context-aware-transform.md instructions
5. Claude checks if PROJECT_TREE present:
   - If yes → Apply Rule A
   - If no or empty flag → Apply Rule B
6. Claude generates response following selected rule
```

## Error Handling & Graceful Degradation

### Error Hierarchy (Most to Least Graceful)

#### 1. Silent Pass-Through (Preferred)
**Scenarios**:
- Python not installed
- Script not found
- Timeout exceeded
- No keywords detected

**Behavior**: Hook exits with code 0, no context injection, Claude operates normally.

#### 2. Partial Success (Acceptable)
**Scenarios**:
- Permission errors on some directories
- Output truncation (>50KB)
- .gitignore parse error

**Behavior**: Returns partial tree with warnings in footer, Claude works with available context.

#### 3. Visible Error (Rare)
**Scenarios**:
- Script syntax error
- Critical file system error

**Behavior**: Returns `[ERROR: ...]` message, logged for debugging.

### Error Messages

**Permission Denied**:
```
pseudo-code-prompting-plugin/
|-- src/
...

Total: 50 files, 10 directories
Skipped: 3 items (permission denied or errors)

Warnings:
- Permission denied: /path/to/protected
```

**Timeout**:
```
[No tree appears, graceful fallback to normal mode]
```

**Empty Project**:
```
<<PROJECT_EMPTY_NO_STRUCTURE>>
```

## Performance Tuning

### Adjusting Limits

**In get_context_tree.py**:
```python
DEFAULT_MAX_DEPTH = 10        # Increase for deeper projects
DEFAULT_MAX_FILES = 1000      # Increase for larger projects
DEFAULT_TIMEOUT = 10          # Increase for slow file systems
MAX_OUTPUT_BYTES = 50 * 1024  # Increase for more context
```

**In context-aware-tree-injection.sh**:
```bash
$PYTHON_CMD "$PYTHON_SCRIPT" "$CWD" --max-depth 15 --max-files 2000 --timeout 20
```

**Trade-offs**:
- Higher limits → More context, slower execution
- Lower limits → Faster, less context

### Hook Timeout

**In hooks/hooks.json**:
```json
{
  "timeout": 15  // Increase if tree generation is slow
}
```

**Recommendation**: Python timeout + 5 seconds overhead

### Custom Exclusions

**Add to get_context_tree.py**:
```python
DEFAULT_EXCLUDE_DIRS = {
    '.git', 'node_modules',
    'my_custom_cache_dir',  # Add custom exclusions
}

DEFAULT_EXCLUDE_PATTERNS = {
    '*.pyc', '*.log',
    '*.tmp',  # Add custom patterns
}
```

## Security Considerations

### Path Traversal Prevention
```python
self.root_path = Path(root_path).resolve()
# resolve() normalizes paths and prevents ../ traversal
```

### Command Injection Prevention
```bash
$PYTHON_CMD "$PYTHON_SCRIPT" "$CWD"  # Quoted variables
```

### Resource Limits
- Max execution time: 15s
- Max files: 1000
- Max output: 50KB
- Max depth: 10 levels

### Symlink Handling
```python
if entry.is_symlink():
    continue  # Don't follow to prevent access outside project
```

### Sensitive File Filtering
Default exclusions include:
- `.env`, `.env.*` (if added to patterns)
- `.git/` (version control metadata)
- IDE configs (`.vscode/`, `.idea/`)

**Recommendation**: Add to `.gitignore` to exclude from tree.

## Testing

### Unit Tests (Python)

**Test tree generation**:
```bash
python3 hooks/get_context_tree.py /path/to/test/project
```

**Test empty detection**:
```bash
mkdir /tmp/empty-test && python3 hooks/get_context_tree.py /tmp/empty-test
# Should output: <<PROJECT_EMPTY_NO_STRUCTURE>>
```

**Test filtering**:
```bash
python3 hooks/get_context_tree.py /project/with/node_modules
# Should exclude node_modules from tree
```

### Integration Tests (Bash Hook)

**Test keyword trigger**:
```bash
printf '{"prompt":"implement auth","cwd":"/path/to/project"}' | bash hooks/context-aware-tree-injection.sh
# Should output: [CONTEXT-AWARE MODE ACTIVATED]...
```

**Test pass-through**:
```bash
printf '{"prompt":"hello","cwd":"/path/to/project"}' | bash hooks/context-aware-tree-injection.sh
# Should output nothing (pass-through)
```

### End-to-End Test

1. Register hook in hooks.json
2. Start Claude Code session
3. Submit prompt: "implement user authentication"
4. Verify:
   - Hook triggers (status message appears)
   - Tree is generated and injected
   - Claude's response references specific files from tree

## Debugging

### Enable Verbose Logging

**In get_context_tree.py** (add):
```python
import logging
logging.basicConfig(level=logging.DEBUG, filename='tree_generation.log')
logging.debug(f"Scanning: {dir_path}")
```

### Check Hook Execution

**Add to context-aware-tree-injection.sh**:
```bash
echo "Hook triggered: $PROMPT" >> /tmp/hook-debug.log
echo "Tree output length: ${#TREE_OUTPUT}" >> /tmp/hook-debug.log
```

### Validate JSON

**Test hooks.json**:
```bash
python3 -m json.tool < hooks/hooks.json
```

### Manual Testing

**Run Python script directly**:
```bash
python3 hooks/get_context_tree.py . --max-depth 3 --max-files 50
```

**Run hook directly**:
```bash
echo '{"prompt":"implement feature","cwd":"'$(pwd)'"}' | bash hooks/context-aware-tree-injection.sh
```

## Maintenance

### Version Compatibility
- Python: 3.6+ (uses f-strings, pathlib, type hints)
- Bash: 4.0+ (uses associative arrays, extended regex)
- Claude Code: 2.0+ (uses hook system v2)

### Dependencies
- **Python**: stdlib only (os, sys, argparse, pathlib, platform, signal, threading)
- **Bash**: coreutils (optional timeout command)

### Future Enhancements
1. **Caching**: Cache tree results per directory (5-minute TTL)
2. **Incremental Updates**: Detect changes since last scan
3. **Parallel Scanning**: Use multiprocessing for large projects
4. **Smart Filtering**: ML-based relevance filtering
5. **Syntax Highlighting**: Color-coded tree output

## Related Documentation

- [Context-Aware Mode User Guide](CONTEXT-AWARE-MODE.md)
- [Plugin Architecture](ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
