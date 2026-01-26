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
pytest tests/ -m "cache" -v             # Cache validation tests
pytest tests/ -m "performance" -v       # Performance benchmark tests
pytest tests/ -m "parallel" -v          # Parallel execution tests
```

### Run tests by scale
```bash
pytest tests/test_performance_benchmarks/ --scale=1k   # 1k file scale
pytest tests/test_performance_benchmarks/ --scale=10k  # 10k file scale
pytest tests/test_performance_benchmarks/ --scale=50k  # 50k file scale
```

### Run with coverage
```bash
pytest tests/ --cov=hooks --cov-report=html
```

## Test Structure

```
tests/
├── conftest.py                         # Shared fixtures and configuration (8 new fixtures added)
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
├── test_cache_validation/              # Cache validation tests (NEW)
│   ├── test_cache_hit_miss.py          # Cache hit/miss tracking
│   ├── test_cache_invalidation.py      # Cache invalidation mechanisms
│   └── test_cache_performance.py       # Cache operation performance
├── test_performance_benchmarks/        # Performance benchmarks (NEW)
│   ├── test_tree_generation_scaling.py # Tree generation at scales 1k-100k
│   ├── test_memory_profiling.py        # Memory usage tracking
│   └── test_bottleneck_analysis.py     # Performance bottleneck identification
├── test_cross_platform/                # Cross-platform tests (NEW)
│   ├── test_windows_compat.py          # Windows-specific tests
│   ├── test_macos_compat.py            # macOS-specific tests
│   ├── test_linux_compat.py            # Linux-specific tests
│   ├── test_path_normalization.py      # Path handling across platforms
│   └── test_platform_timeouts.py       # Platform-specific timeout adjustments
├── test_hook_timing/                   # Hook timing tests (NEW)
│   ├── test_hook_execution_order.py    # Hook execution sequence validation
│   ├── test_hook_latency.py            # Hook callback latency measurement
│   └── test_concurrent_hooks.py        # Concurrent hook execution
├── test_quality_metrics/               # Quality metrics tests (NEW)
│   ├── test_semantic_preservation.py   # Semantic preservation validation
│   ├── test_output_consistency.py      # Output consistency checking
│   └── test_regression_detection.py    # Regression detection
├── test_parallel_execution/            # Parallel execution tests (NEW)
│   ├── test_concurrent_agents.py       # Concurrent agent invocation
│   ├── test_resource_contention.py     # Resource contention detection
│   └── test_output_synchronization.py  # Output synchronization
├── test_error_recovery/                # Error recovery tests (NEW)
│   ├── test_timeout_handling.py        # Timeout handling and recovery
│   ├── test_partial_failure.py         # Partial failure recovery
│   ├── test_graceful_degradation.py    # Graceful degradation testing
│   └── test_retry_logic.py             # Retry and backoff strategies
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

## New Test Categories (Recently Added)

### Cache Validation Tests (`@pytest.mark.cache`)
Comprehensive cache validation and performance testing:
- **test_cache_hit_miss.py** (9 tests): Cache hit/miss tracking, hit rate validation (80%+ threshold), thread-safe operations
- **test_cache_invalidation.py** (8 tests): Manual/TTL/dependency invalidation, state consistency, concurrent invalidation
- **test_cache_performance.py** (10 tests): Get/set latency (<5ms/<10ms), throughput (>1000 ops/sec), memory efficiency

**Thresholds**:
- Cache get: <5ms per operation
- Cache set: <10ms per operation
- Cache throughput: >1000 operations/sec
- Hit rate requirement: >80% for repeated queries

### Performance Benchmarks (`@pytest.mark.performance`)
Comprehensive performance testing with scaling:
- **test_tree_generation_scaling.py** (6 tests): 1k/10k/50k/100k file scales, sub-linear scaling verification
- **test_memory_profiling.py** (8 tests): Peak memory tracking, leak detection, per-file ratio analysis
- **test_bottleneck_analysis.py** (9 tests): cProfile-based bottleneck identification, scaling analysis

**Performance Thresholds**:
- Tree generation (platform-adjusted):
  - 1k files: <1000ms
  - 10k files: <15s
  - 50k files: <60s
  - 100k files: <180s
- Platform multipliers: Windows 1.5x, macOS/Linux 1.0x, CI 2.0x

### Cross-Platform Tests (`@pytest.mark.integration`)
Platform-specific compatibility and path normalization:
- **test_windows_compat.py**: UNC paths, backslash handling, drive letters
- **test_macos_compat.py**: Case-insensitive filesystem, resource forks
- **test_linux_compat.py**: Standard Unix paths, case-sensitive filesystem
- **test_path_normalization.py** (12 tests): Forward slash normalization, relative/absolute paths, symlink resolution
- **test_platform_timeouts.py** (11 tests): Platform detection, timeout multiplier application, threshold ordering

### Hook Timing Tests (`@pytest.mark.hook`)
Hook execution timing and performance validation:
- **test_hook_execution_order.py** (4 tests): Execution sequence, dependency validation, chain continuity
- **test_hook_latency.py** (10 tests): Latency percentiles (p95, p99), consistency, jitter detection, load testing
- **test_concurrent_hooks.py** (7 tests): Deadlock prevention, result consistency, isolation, scalability

**Hook Thresholds**:
- Single hook latency: <100ms
- Cumulative overhead: <10% of total execution time
- p95 latency: tracked and reported
- p99 latency: tracked and reported

### Quality Metrics Tests (`@pytest.mark.golden`)
Transformation quality and regression detection:
- **test_semantic_preservation.py** (10 tests): Semantic equivalence, information preservation, multi-layer validation
- **test_output_consistency.py** (3 tests): Same input → same output, whitespace normalization
- **test_regression_detection.py** (4 tests): Golden file baseline comparison, regression detection, quality metrics

### Parallel Execution Tests (`@pytest.mark.parallel`)
Concurrent agent execution and resource management:
- **test_concurrent_agents.py** (8 tests): Concurrent invocation, completion verification, error isolation
- **test_resource_contention.py** (3 tests): Memory scaling, CPU efficiency, I/O contention
- **test_output_synchronization.py** (3 tests): Shared state protection, atomicity, output ordering

### Error Recovery Tests (`@pytest.mark.integration`)
Resilience and error recovery mechanisms:
- **test_timeout_handling.py** (8 tests): Graceful timeout, partial results, resource cleanup, platform-adjusted timeouts
- **test_partial_failure.py** (3 tests): Partial agent failure handling, result recovery, error isolation
- **test_graceful_degradation.py** (4 tests): Reduced features on error, no cascading failures, informative messages
- **test_retry_logic.py** (10 tests): Retry count limits, exponential backoff, transient failure recovery, jitter

## Fixtures Added

### Performance Monitoring Fixtures
1. **large_project_structure** - Generates projects with 1k/10k/50k/100k files
2. **performance_monitor** - Tracks execution time and memory usage (context manager)
3. **cache_state_tracker** - Records cache hits/misses with thread safety
4. **concurrent_executor** - Runs functions concurrently with ThreadPoolExecutor
5. **platform_detector** - Detects OS and applies timeout multipliers
6. **memory_profiler** - Tracemalloc wrapper for leak detection
7. **latency_tracker** - Measures hook latencies with percentile calculation
8. **golden_performance_baseline** - Returns platform-adjusted thresholds

## Test Statistics

- **Total Test Files**: 7 categories + 24 new files = 31 test modules
- **Total Test Cases**: ~200+ new test cases
- **Fixture Coverage**: 8 new fixtures for performance testing
- **Documentation**: Comprehensive test guide with examples

## Running Enhanced Tests

```bash
# Run all performance tests
pytest tests/test_performance_benchmarks/ -v

# Run cache validation only
pytest tests/test_cache_validation/ -m cache -v

# Run cross-platform tests (Windows only)
pytest tests/test_cross_platform/test_windows_compat.py -v

# Run with performance metrics
pytest tests/test_performance_benchmarks/ -v --tb=short

# Run error recovery tests
pytest tests/test_error_recovery/ -v

# Run parallel execution tests
pytest tests/test_parallel_execution/ -m parallel -v

# Run with detailed timing
pytest tests/test_hook_timing/ -v -s

# Run quality metrics
pytest tests/test_quality_metrics/ -m golden -v
```

## CI/CD Integration

Tests automatically include:
- Platform-specific timeout multipliers for Windows/macOS/Linux/CI
- Concurrent execution for parallel agent tests
- Memory profiling for leak detection
- Performance threshold validation
- Cross-platform compatibility checks

## Future Enhancements

- ✅ Smart router context caching validation - **COMPLETED**
- ✅ Performance benchmarks (tree generation on large projects) - **COMPLETED**
- ✅ Cross-platform testing (Windows, macOS, Linux) - **COMPLETED**
- ✅ Hook sequence and timing validation - **COMPLETED**
- ✅ Transformation quality metrics (semantic preservation) - **COMPLETED**
- ✅ Parallel agent execution testing - **COMPLETED**
- ✅ Agent error recovery and timeout scenarios - **COMPLETED**
