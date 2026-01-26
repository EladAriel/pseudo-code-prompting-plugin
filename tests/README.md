# Testing Guide for Pseudo-Code-Prompting Plugin

This directory contains comprehensive tests for the pseudo-code-prompting Claude Code plugin. Tests are organized by component and test type.

## Quick Start

### Install test dependencies
```bash
pip install -r ../requirements-test.txt
```

### Run all tests
```bash
pytest tests/ -v
```

### Run tests by category
```bash
pytest tests/ -m "hook" -v              # Hook execution tests
pytest tests/ -m "memory" -v            # Memory persistence tests
pytest tests/ -m "golden" -v            # Golden file comparison tests
pytest tests/ -m "chaining" -v          # Agent chaining protocol tests
pytest tests/ -m "unit" -v              # Unit tests
pytest tests/ -m "integration" -v       # Integration tests
```

### Run with coverage
```bash
pytest tests/ --cov=hooks --cov-report=html
```

## Test Structure

```
tests/
├── conftest.py                         # Shared fixtures and configuration
├── test_agent_chaining/                # Agent chaining protocol tests
│   ├── test_workflow_continues.py      # WORKFLOW_CONTINUES protocol tests
│   └── test_next_agent.py              # NEXT_AGENT protocol tests
├── test_hooks/                         # Hook execution tests
│   ├── test_user_prompt_submit.py      # Command detection hook tests
│   ├── test_get_context_tree.py        # Tree generation hook tests
│   └── test_context_tree_injection.py  # Context injection hook tests
├── test_memory/                        # Memory persistence tests
│   └── test_memory_operations.py       # Read/Write/Edit file operations
├── test_transformations/               # Transformation validation tests
│   └── test_golden_files.py            # Golden file comparison tests
└── golden/                             # Expected output files
    └── transformations/                # Golden files for each pattern
```

## Test Categories

### Agent Chaining Tests (`@pytest.mark.chaining`)
Tests for multi-agent workflow protocols and coordination:
- **WORKFLOW_CONTINUES**: Agent state transitions and workflow continuation
- **NEXT_AGENT**: Agent delegation, routing, and context handoff

**Coverage**:
- Workflow signal parsing (WORKFLOW_CONTINUES: YES/NO)
- Agent routing and delegation (NEXT_AGENT signals)
- Context handoff between agents
- Chain progress tracking
- Error recovery and continuation
- Memory state persistence across steps
- Complete multi-step pipeline execution

**Test Files**:
- `test_workflow_continues.py`: 6 tests validating workflow state transitions
- `test_next_agent.py`: 7 tests validating agent routing and delegation

### Hook Tests (`@pytest.mark.hook`)
Tests for plugin hooks that execute in Claude Code lifecycle events:
- **user-prompt-submit**: Detects pseudo-code transformation commands
- **context-tree-injection**: Injects project structure for context-aware mode
- **get_context_tree**: Generates directory trees for scanned projects

**Coverage**:
- Command detection (`/smart`, `/complete-process`, `/transform-query`)
- Plugin reference detection ("Use pseudo-code prompting plugin")
- Implementation keyword detection (implement, create, add, refactor, build)
- Empty directory handling
- .gitignore support
- File size and depth limits

### Memory Tests (`@pytest.mark.memory`)
Tests for persistent memory file operations:
- **activeContext.md**: Short-term, high-churn transformations
- **patterns.md**: Long-term learned patterns
- **progress.md**: Session metrics and history

**Coverage**:
- File creation and initialization
- Read/Write/Edit operations
- Multiline content handling
- Multiple file coexistence

### Golden File Tests (`@pytest.mark.golden`)
Tests that compare expected outputs with golden files for transformation patterns:

**Patterns covered** (10 files):
1. `rest_api_basic.txt` - Basic REST API endpoint
2. `auth_jwt.txt` - JWT authentication flow
3. `crud_operations.txt` - CRUD operations
4. `database_query.txt` - Database query generation
5. `validation_endpoint.txt` - Input validation
6. `compression_basic.txt` - Context compression
7. `rate_limiting.txt` - Rate limiting configuration
8. `error_handling.txt` - Error response handling
9. `pagination.txt` - Pagination strategy
10. `security_headers.txt` - Security headers configuration

**Validation**:
- Golden file existence
- Content structure validation
- Whitespace normalization

### Unit Tests (`@pytest.mark.unit`)
Fast tests with no I/O or subprocess calls:
- Memory file operations with mocked filesystem
- Golden file normalization
- Hook input parsing

### Integration Tests (`@pytest.mark.integration`)
Tests that execute actual code (hooks, subprocess calls):
- Hook subprocess execution
- Tree generation on real directory structures
- JSON input parsing
- Hook timeout validation

## Fixtures

### Filesystem Fixtures

- `temp_dir`: Temporary directory for test files
- `mock_memory_dir`: Mock `.claude/pseudo-code-prompting/` directory
- `empty_active_context`: Initialized activeContext.md file
- `empty_patterns`: Initialized patterns.md file
- `empty_progress`: Initialized progress.md file
- `memory_file_factory`: Factory for creating memory files with custom content

### Hook Input Fixtures

- `hook_input_factory`: Factory for creating hook JSON inputs
- `implement_auth_input`: Pre-configured input for auth implementation
- `create_api_input`: Pre-configured input for API creation
- `non_implementation_input`: Non-implementation query for negative tests
- `empty_prompt_input`: Empty prompt for edge case testing

### Project Structure Fixtures

- `empty_project_structure`: Empty directory
- `nextjs_project_structure`: Mock Next.js project
- `python_project_structure`: Mock Python project
- `gitignore_project`: Project with .gitignore file

### Execution Fixtures

- `hook_executor`: Subprocess executor for hook scripts
- `mock_claude_env`: Mock Claude Code environment variables

### Validation Fixtures

- `golden_dir`: Path to golden files directory
- `transformation_golden`: Load golden file by name
- `golden_comparator`: Compare outputs with whitespace normalization

### Agent Chaining Fixtures

- `mock_agent_response_factory`: Factory for creating mock agent responses with workflow signals
- `mock_transform_agent`: Mock prompt-transformer agent that outputs WORKFLOW_CONTINUES: YES
- `mock_validator_agent`: Mock requirement-validator agent that outputs NEXT_AGENT signal
- `mock_optimizer_agent`: Mock prompt-optimizer agent that terminates the workflow
- `orchestrator_mock`: Mock orchestrator that reads signals and routes to next agent
- `workflow_memory_state`: Tracker for memory file snapshots and comparisons

## Running Tests Locally

### Test all components
```bash
pytest tests/ -v
```

### Test specific module
```bash
pytest tests/test_hooks/test_user_prompt_submit.py -v
```

### Test with specific marker
```bash
pytest tests/ -m "hook and integration" -v
```

### Run specific test
```bash
pytest tests/test_hooks/test_user_prompt_submit.py::test_hook_detects_smart_command -v
```

### Run with output capture disabled (see print statements)
```bash
pytest tests/ -s -v
```

### Run with timeout (pytest-timeout required)
```bash
pytest tests/ --timeout=30 -v
```

## CI/CD Integration

Tests run automatically on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to those branches
- Manual workflow dispatch

**CI Jobs**:
1. `validate-json`: JSON schema validation
2. `validate-bash`: Shell script linting
3. `validate-python`: Python syntax validation
4. `test-suite`: pytest test suite (unit, integration, golden, memory, hook)
5. `integration-test`: Manual integration tests
6. `summary`: CI results summary

**Coverage Report**: Generated in CI and available after test run

## Adding New Tests

### New Agent Chaining Test
```python
@pytest.mark.chaining
@pytest.mark.unit
def test_agent_chaining_new_scenario(mock_transform_agent, orchestrator_mock):
    """Test description."""
    transform_output = mock_transform_agent("query")

    should_continue = orchestrator_mock.should_continue(transform_output)
    next_agent = orchestrator_mock.get_next_agent(transform_output)

    assert should_continue is True
    assert next_agent == "requirement-validator"
```

### New Hook Test
```python
@pytest.mark.hook
@pytest.mark.integration
def test_hook_new_feature(hook_executor, temp_dir):
    """Test description."""
    hook_input = json.dumps({
        "prompt": "test prompt",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/path/to/hook.py", hook_input)

    assert result.returncode == 0
```

### New Memory Test
```python
@pytest.mark.memory
@pytest.mark.unit
def test_memory_new_feature(mock_memory_dir):
    """Test description."""
    test_file = mock_memory_dir / "test.md"
    test_file.write_text("content")

    assert test_file.read_text() == "content"
```

### New Golden File
1. Create file: `tests/golden/transformations/pattern_name.txt`
2. Add golden file test in `test_golden_files.py`:
```python
@pytest.mark.golden
def test_golden_pattern_name_exists(transformation_golden):
    """Test golden file for pattern exists."""
    content = transformation_golden("pattern_name")
    assert content
```

## Best Practices

1. **Use appropriate markers**: Mark tests with `@pytest.mark.unit`, `@pytest.mark.integration`, etc.
2. **Use fixtures**: Leverage conftest fixtures for consistency
3. **Test edge cases**: Empty inputs, invalid paths, missing files
4. **Keep tests focused**: One concept per test
5. **Use descriptive names**: Test names should explain what they test
6. **Normalize output**: Use golden_comparator for whitespace-insensitive comparison
7. **Mock external calls**: Use mock_claude_env for environment variables

## Troubleshooting

### Tests fail with "python3 not found"
The hook_executor falls back to `python`. Ensure Python 3 is installed.

### Golden file tests fail with "Golden file not found"
Check that golden files exist in `tests/golden/transformations/`.

### Integration tests timeout
Check that hooks don't have infinite loops. Timeout is 10s by default, 15s for tree injection.

### Memory tests fail
Ensure pytest has permission to create files in temp directory.

## Coverage Goals

- **Hooks**: 70% (all execution paths, basic error handling)
- **Memory**: 80% (all operations, file I/O)
- **Transformations**: 60% (basic patterns, golden file validation)
- **Overall Target**: 65%+ code coverage

## Future Enhancements

Potential additions to test suite:
- ✅ Agent chaining protocol tests (WORKFLOW_CONTINUES, NEXT_AGENT) - **COMPLETED**
- Smart router context caching validation
- Performance benchmarks (tree generation on large projects)
- Cross-platform testing (Windows, macOS)
- Hook sequence and timing validation
- Transformation quality metrics (semantic preservation)
- Parallel agent execution testing
- Agent error recovery and timeout scenarios
