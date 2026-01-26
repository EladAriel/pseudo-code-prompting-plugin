"""
Pytest configuration and shared fixtures for pseudo-code-prompting plugin tests.
"""
import pytest
import json
import tempfile
import subprocess
import time
import tracemalloc
import sys
from pathlib import Path
from typing import Dict, Any, Callable, List
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict


# ============================================================================
# FILESYSTEM FIXTURES
# ============================================================================

@pytest.fixture
def plugin_root():
    """Absolute path to plugin root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files."""
    return tmp_path


@pytest.fixture
def mock_memory_dir(tmp_path, monkeypatch):
    """Mock .claude/pseudo-code-prompting directory."""
    memory_dir = tmp_path / ".claude" / "pseudo-code-prompting"
    memory_dir.mkdir(parents=True)
    return memory_dir


@pytest.fixture
def empty_active_context(mock_memory_dir):
    """Create empty activeContext.md file."""
    context_file = mock_memory_dir / "activeContext.md"
    context_file.write_text("# Active Context\n\nNo transformations yet.")
    return context_file


@pytest.fixture
def empty_patterns(mock_memory_dir):
    """Create empty patterns.md file."""
    patterns_file = mock_memory_dir / "patterns.md"
    patterns_file.write_text("# Learned Patterns\n\nNo patterns learned yet.")
    return patterns_file


@pytest.fixture
def empty_progress(mock_memory_dir):
    """Create empty progress.md file."""
    progress_file = mock_memory_dir / "progress.md"
    progress_file.write_text("# Progress\n\nSession started.")
    return progress_file


@pytest.fixture
def memory_file_factory(mock_memory_dir):
    """Factory for creating memory files with predefined content."""
    def _create(filename: str, content: str) -> Path:
        file_path = mock_memory_dir / filename
        file_path.write_text(content)
        return file_path
    return _create


# ============================================================================
# HOOK INPUT FIXTURES
# ============================================================================

@pytest.fixture
def hook_input_factory():
    """Factory for creating hook JSON inputs."""
    def _create(prompt: str, cwd: str = None, **kwargs) -> str:
        data = {"prompt": prompt}
        if cwd:
            data["cwd"] = cwd
        data.update(kwargs)
        return json.dumps(data)
    return _create


@pytest.fixture
def implement_auth_input(hook_input_factory, temp_dir):
    """Hook input for 'implement authentication'."""
    return hook_input_factory("implement user authentication", str(temp_dir))


@pytest.fixture
def create_api_input(hook_input_factory, temp_dir):
    """Hook input for 'create REST API'."""
    return hook_input_factory("create REST API for user management", str(temp_dir))


@pytest.fixture
def non_implementation_input(hook_input_factory, temp_dir):
    """Hook input for non-implementation query."""
    return hook_input_factory("what are the best practices?", str(temp_dir))


@pytest.fixture
def empty_prompt_input(hook_input_factory, temp_dir):
    """Hook input with empty prompt."""
    return hook_input_factory("", str(temp_dir))


# ============================================================================
# SUBPROCESS EXECUTION FIXTURES
# ============================================================================

@pytest.fixture
def hook_executor(plugin_root):
    """Execute hook scripts as subprocess."""
    def _execute(
        hook_path: str,
        stdin_data: str,
        timeout: int = 10
    ) -> subprocess.CompletedProcess:
        script_path = plugin_root / hook_path
        try:
            result = subprocess.run(
                ["python3", str(script_path)],
                input=stdin_data,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=timeout
            )
            return result
        except FileNotFoundError:
            # Fallback to 'python' if python3 not found
            result = subprocess.run(
                ["python", str(script_path)],
                input=stdin_data,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=timeout
            )
            return result
    return _execute


# ============================================================================
# GOLDEN FILE FIXTURES
# ============================================================================

@pytest.fixture
def golden_dir():
    """Directory containing golden files."""
    return Path(__file__).parent / "golden"


@pytest.fixture
def transformation_golden(golden_dir):
    """Load transformation golden file."""
    def _load(name: str) -> str:
        path = golden_dir / "transformations" / f"{name}.txt"
        if not path.exists():
            pytest.fail(f"Golden file not found: {path}")
        return path.read_text().strip()
    return _load


@pytest.fixture
def golden_comparator():
    """Compare actual output with golden file (with normalization)."""
    def _compare(actual: str, expected: str) -> bool:
        import re
        # Normalize: remove ALL whitespace (newlines, spaces, tabs, etc.)
        def normalize(text: str) -> str:
            # Remove all whitespace characters
            return re.sub(r'\s', '', text.strip())

        return normalize(actual) == normalize(expected)
    return _compare


# ============================================================================
# PROJECT STRUCTURE FIXTURES
# ============================================================================

@pytest.fixture
def empty_project_structure(temp_dir):
    """Empty project directory."""
    return temp_dir


@pytest.fixture
def nextjs_project_structure(temp_dir):
    """Mock Next.js project structure."""
    (temp_dir / "package.json").write_text(
        json.dumps({"name": "test", "dependencies": {"next": "13.0.0"}})
    )
    (temp_dir / "src" / "app").mkdir(parents=True)
    (temp_dir / "src" / "lib").mkdir(parents=True)
    return temp_dir


@pytest.fixture
def python_project_structure(temp_dir):
    """Mock Python project structure."""
    (temp_dir / "requirements.txt").write_text("fastapi==0.95.0\nsqlalchemy==2.0.0")
    (temp_dir / "src").mkdir(parents=True)
    (temp_dir / "tests").mkdir(parents=True)
    return temp_dir


@pytest.fixture
def gitignore_project(temp_dir):
    """Project with .gitignore file."""
    (temp_dir / ".gitignore").write_text(
        "node_modules/\n.env\n__pycache__/\n*.pyc\n.git/"
    )
    (temp_dir / "node_modules").mkdir(parents=True)
    (temp_dir / ".env").touch()
    (temp_dir / "src").mkdir(parents=True)
    (temp_dir / "src" / "app.py").touch()
    return temp_dir


# ============================================================================
# AGENT CHAINING FIXTURES
# ============================================================================

@pytest.fixture
def mock_agent_response_factory():
    """Factory for creating mock agent responses with workflow signals."""
    def _create(
        agent_name: str,
        output_content: str,
        workflow_continues: bool,
        next_agent: str = None,
        chain_progress: str = None,
        todo_list: list = None
    ) -> Dict[str, Any]:
        response = {
            "agent_name": agent_name,
            "output": output_content,
            "WORKFLOW_CONTINUES": "YES" if workflow_continues else "NO",
        }
        if next_agent:
            response["NEXT_AGENT"] = next_agent
        if chain_progress:
            response["CHAIN_PROGRESS"] = chain_progress
        if todo_list:
            response["TODO_LIST"] = todo_list
            response["CHAIN_COMPLETE"] = "All steps finished"
        return response
    return _create


@pytest.fixture
def mock_transform_agent(mock_agent_response_factory):
    """Mock prompt-transformer agent output."""
    def _invoke(query: str) -> Dict[str, Any]:
        return mock_agent_response_factory(
            agent_name="prompt-transformer",
            output_content=f"implement_{query.replace(' ', '_')}(param=\"value\")",
            workflow_continues=True,
            next_agent="requirement-validator",
            chain_progress="prompt-transformer [1/3] → requirement-validator → prompt-optimizer"
        )
    return _invoke


@pytest.fixture
def mock_validator_agent(mock_agent_response_factory):
    """Mock requirement-validator agent output."""
    def _invoke(pseudo_code: str) -> Dict[str, Any]:
        return mock_agent_response_factory(
            agent_name="requirement-validator",
            output_content="Validation Report: ✓ PASSED\n- Security checks passed\n- Parameters complete",
            workflow_continues=True,
            next_agent="prompt-optimizer",
            chain_progress="prompt-transformer ✓ → requirement-validator [2/3] → prompt-optimizer"
        )
    return _invoke


@pytest.fixture
def mock_optimizer_agent(mock_agent_response_factory):
    """Mock prompt-optimizer agent output."""
    def _invoke(pseudo_code: str, validation_report: str = None) -> Dict[str, Any]:
        return mock_agent_response_factory(
            agent_name="prompt-optimizer",
            output_content="implement_auth(type=\"oauth\", security={\"mfa\": true})",
            workflow_continues=False,
            chain_progress="prompt-transformer ✓ → requirement-validator ✓ → prompt-optimizer [3/3] ✓",
            todo_list=["Implement OAuth flow", "Add error handling", "Configure security headers"]
        )
    return _invoke


@pytest.fixture
def orchestrator_mock():
    """Mock orchestrator that reads workflow signals and routes to next agent."""
    class OrchestratorMock:
        def __init__(self):
            self.execution_log = []
            self.memory_updates = []

        def get_next_agent(self, agent_output: Dict[str, Any]) -> str:
            """Extract NEXT_AGENT from agent output."""
            self.execution_log.append(agent_output["agent_name"])
            return agent_output.get("NEXT_AGENT")

        def should_continue(self, agent_output: Dict[str, Any]) -> bool:
            """Check if workflow should continue."""
            return agent_output["WORKFLOW_CONTINUES"] == "YES"

        def update_memory(self, key: str, value: str):
            """Track memory updates during workflow."""
            self.memory_updates.append({"key": key, "value": value})

        def get_execution_order(self) -> list:
            """Return order of agent invocations."""
            return self.execution_log

        def reset(self):
            """Reset mock state for new test."""
            self.execution_log = []
            self.memory_updates = []

    return OrchestratorMock()


@pytest.fixture
def workflow_memory_state(mock_memory_dir):
    """Track memory state during workflow execution."""
    class MemoryState:
        def __init__(self, memory_dir):
            self.memory_dir = memory_dir
            self.snapshots = {}

        def snapshot(self, label: str):
            """Take snapshot of memory files."""
            context_file = self.memory_dir / "activeContext.md"
            patterns_file = self.memory_dir / "patterns.md"
            progress_file = self.memory_dir / "progress.md"

            self.snapshots[label] = {
                "activeContext": context_file.read_text() if context_file.exists() else "",
                "patterns": patterns_file.read_text() if patterns_file.exists() else "",
                "progress": progress_file.read_text() if progress_file.exists() else ""
            }

        def get_snapshot(self, label: str) -> Dict[str, str]:
            """Retrieve memory snapshot."""
            return self.snapshots.get(label, {})

        def compare_snapshots(self, label1: str, label2: str) -> Dict[str, bool]:
            """Compare two memory snapshots."""
            snap1 = self.get_snapshot(label1)
            snap2 = self.get_snapshot(label2)

            return {
                "activeContext_changed": snap1.get("activeContext") != snap2.get("activeContext"),
                "patterns_changed": snap1.get("patterns") != snap2.get("patterns"),
                "progress_changed": snap1.get("progress") != snap2.get("progress")
            }

    return MemoryState(mock_memory_dir)


# ============================================================================
# MOCK CLAUDE CODE ENVIRONMENT
# ============================================================================

@pytest.fixture
def mock_claude_env(monkeypatch, plugin_root):
    """Mock Claude Code environment variables."""
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(plugin_root))
    return {"CLAUDE_PLUGIN_ROOT": str(plugin_root)}


# ============================================================================
# TEST MARKERS
# ============================================================================

def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "golden: mark test as a golden file comparison"
    )
    config.addinivalue_line(
        "markers", "memory: mark test as a memory persistence test"
    )
    config.addinivalue_line(
        "markers", "hook: mark test as a hook execution test"
    )
    config.addinivalue_line(
        "markers", "chaining: mark test as an agent chaining protocol test"
    )
    config.addinivalue_line(
        "markers", "cache: mark test as a cache validation test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance benchmark test"
    )
    config.addinivalue_line(
        "markers", "parallel: mark test as a parallel execution test"
    )


# ============================================================================
# NEW FIXTURES FOR TEST SUITE ENHANCEMENTS
# ============================================================================

@pytest.fixture
def large_project_structure(tmp_path):
    """Generate synthetic project structures with configurable file counts."""
    def _generate(scale: str = "1k") -> Path:
        scale_map = {
            "1k": 1000,
            "10k": 10000,
            "50k": 50000,
            "100k": 100000
        }
        file_count = scale_map.get(scale, 1000)

        # Create directory structure
        base = tmp_path / f"project_{scale}"
        base.mkdir(exist_ok=True)

        # Create nested directories with files
        files_per_dir = 50
        dir_levels = 5

        for i in range(file_count):
            dir_path = base
            for level in range(dir_levels):
                dir_path = dir_path / f"dir_{level}_{i % (file_count // (10 ** level) if level < 3 else 100)}"

            dir_path.mkdir(parents=True, exist_ok=True)
            file_path = dir_path / f"file_{i}.py"
            file_path.write_text(f"# File {i}\nindex = {i}\n")

        return base

    return _generate


@pytest.fixture
def performance_monitor():
    """Track execution time and memory usage."""
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.memory_before = 0
            self.memory_after = 0
            self.metrics = {}

        def __enter__(self):
            self.start_time = time.perf_counter()
            self.memory_before = self._get_memory_mb()
            tracemalloc.start()
            return self

        def __exit__(self, *args):
            self.end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.memory_after = peak / 1024 / 1024

            self.metrics = {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration_ms": (self.end_time - self.start_time) * 1000,
                "memory_before": self.memory_before,
                "memory_after": self.memory_after,
                "memory_delta_mb": self.memory_after - self.memory_before
            }

        def _get_memory_mb(self) -> float:
            try:
                import psutil
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            except ImportError:
                return 0.0

    return PerformanceMonitor()


@pytest.fixture
def cache_state_tracker():
    """Track cache hit/miss metrics."""
    class CacheStateTracker:
        def __init__(self):
            self.hits = 0
            self.misses = 0
            self.evictions = 0
            self.operations = []
            self.lock = threading.Lock()

        def record_hit(self):
            with self.lock:
                self.hits += 1
                self.operations.append(("hit", time.perf_counter()))

        def record_miss(self):
            with self.lock:
                self.misses += 1
                self.operations.append(("miss", time.perf_counter()))

        def record_eviction(self):
            with self.lock:
                self.evictions += 1
                self.operations.append(("eviction", time.perf_counter()))

        def get_metrics(self) -> Dict[str, Any]:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0

            lookup_times = []
            for i in range(1, len(self.operations)):
                lookup_times.append(
                    (self.operations[i][1] - self.operations[i-1][1]) * 1000
                )

            avg_lookup = sum(lookup_times) / len(lookup_times) if lookup_times else 0

            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "evictions": self.evictions,
                "total_operations": total,
                "average_lookup_time_ms": avg_lookup
            }

        def reset(self):
            with self.lock:
                self.hits = 0
                self.misses = 0
                self.evictions = 0
                self.operations = []

    return CacheStateTracker()


@pytest.fixture
def concurrent_executor():
    """Execute functions concurrently."""
    class ConcurrentExecutor:
        def __init__(self):
            self.results = []
            self.timings = {}

        def run_agents(self, functions: List[Callable], max_workers: int = 4) -> List[Any]:
            self.results = []
            self.timings = {}

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {}
                for func in functions:
                    start = time.perf_counter()
                    future = executor.submit(func)
                    futures[future] = (func.__name__, start)

                for future in futures:
                    func_name, start = futures[future]
                    try:
                        result = future.result(timeout=30)
                        self.results.append(result)
                        self.timings[func_name] = (time.perf_counter() - start) * 1000
                    except Exception as e:
                        self.results.append({"error": str(e)})
                        self.timings[func_name] = None

            return self.results

        def get_timings(self) -> Dict[str, float]:
            return self.timings

    return ConcurrentExecutor()


@pytest.fixture
def platform_detector():
    """Detect platform and return configuration."""
    class PlatformDetector:
        def __init__(self):
            self.platform = sys.platform
            self.is_ci = "CI" in sys.modules or "CI_ENVIRONMENT" in sys.modules or \
                        any(x in os.environ for x in ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "CIRCLECI"])

        def get_info(self) -> Dict[str, Any]:
            multipliers = {
                "win32": 1.5,
                "darwin": 1.0,
                "linux": 1.0,
                "ci": 2.0 if self.is_ci else 1.0
            }

            return {
                "platform": self.platform,
                "is_ci": self.is_ci,
                "timeout_multiplier": multipliers["ci"] if self.is_ci else multipliers.get(self.platform, 1.0),
                "is_windows": self.platform == "win32",
                "is_macos": self.platform == "darwin",
                "is_linux": self.platform == "linux"
            }

        def skip_if_not_platform(self, required_platform: str):
            if required_platform == "windows" and not self.is_windows:
                pytest.skip(f"Test requires Windows, current: {self.platform}")
            elif required_platform == "macos" and not self.is_macos:
                pytest.skip(f"Test requires macOS, current: {self.platform}")
            elif required_platform == "linux" and not self.is_linux:
                pytest.skip(f"Test requires Linux, current: {self.platform}")

    return PlatformDetector()


@pytest.fixture
def memory_profiler():
    """Profile memory usage with tracemalloc."""
    class MemoryProfiler:
        def __init__(self):
            self.snapshots = []
            self.current_snapshot = None

        def start(self):
            tracemalloc.start()
            self.current_snapshot = tracemalloc.take_snapshot()

        def stop(self) -> Dict[str, Any]:
            if not tracemalloc.is_tracing():
                return {}

            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.compare_to(self.current_snapshot, 'lineno')

            self.snapshots.append(snapshot)
            tracemalloc.stop()

            return {
                "total_allocated_mb": sum(stat.size for stat in top_stats) / 1024 / 1024,
                "peak_allocated_mb": tracemalloc.get_traced_memory()[1] / 1024 / 1024,
                "top_allocations": [(stat.traceback, stat.size) for stat in top_stats[:5]]
            }

        def get_leak_analysis(self) -> Dict[str, Any]:
            if len(self.snapshots) < 2:
                return {}

            first = self.snapshots[0]
            last = self.snapshots[-1]
            stats = last.compare_to(first, 'lineno')

            leaked = sum(stat.size for stat in stats if stat.size_diff > 0)
            return {
                "leaked_mb": leaked / 1024 / 1024,
                "top_leaked": [(stat.traceback, stat.size_diff) for stat in stats[:5] if stat.size_diff > 0]
            }

    return MemoryProfiler()


@pytest.fixture
def latency_tracker():
    """Track hook callback latencies."""
    class LatencyTracker:
        def __init__(self):
            self.latencies = defaultdict(list)
            self.lock = threading.Lock()

        def record(self, hook_name: str, latency_ms: float):
            with self.lock:
                self.latencies[hook_name].append(latency_ms)

        def get_metrics(self, hook_name: str = None) -> Dict[str, Any]:
            with self.lock:
                if hook_name:
                    latencies = self.latencies[hook_name]
                else:
                    latencies = [l for ls in self.latencies.values() for l in ls]

                if not latencies:
                    return {}

                latencies = sorted(latencies)
                return {
                    "min_ms": min(latencies),
                    "max_ms": max(latencies),
                    "avg_ms": sum(latencies) / len(latencies),
                    "p95_ms": latencies[int(len(latencies) * 0.95)],
                    "p99_ms": latencies[int(len(latencies) * 0.99)],
                    "count": len(latencies)
                }

        def get_cumulative_overhead(self, total_duration_ms: float) -> float:
            with self.lock:
                total_latency = sum(l for ls in self.latencies.values() for l in ls)
            return (total_latency / total_duration_ms * 100) if total_duration_ms > 0 else 0

        def reset(self):
            with self.lock:
                self.latencies.clear()

    return LatencyTracker()


@pytest.fixture
def golden_performance_baseline(platform_detector):
    """Load performance thresholds from configuration."""
    info = platform_detector.get_info()
    multiplier = info["timeout_multiplier"]

    return {
        "tree_generation": {
            "1k": 1000 * multiplier,
            "10k": 15000 * multiplier,
            "50k": 60000 * multiplier,
            "100k": 180000 * multiplier
        },
        "hook_latency": {
            "single_max_ms": 100 * multiplier,
            "cumulative_overhead_max_percent": 10
        },
        "cache_operations": {
            "get_max_ms": 5 * multiplier,
            "set_max_ms": 10 * multiplier,
            "throughput_min_ops_per_sec": 1000
        },
        "platform_multiplier": multiplier
    }


import os
import json
from datetime import datetime


# ============================================================================
# TEST METRICS COLLECTION
# ============================================================================

class TestMetricsCollector:
    """Collect and report test execution metrics."""

    def __init__(self):
        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "test_results": [],
            "performance_metrics": {},
            "platform_info": platform_detector().get_info() if 'platform_detector' in dir() else {}
        }

    def record_test(self, test_name, duration_ms, status):
        """Record individual test result."""
        self.metrics["test_results"].append({
            "name": test_name,
            "duration_ms": duration_ms,
            "status": status
        })

    def record_performance(self, metric_name, value, unit):
        """Record performance metric."""
        if metric_name not in self.metrics["performance_metrics"]:
            self.metrics["performance_metrics"][metric_name] = []
        self.metrics["performance_metrics"][metric_name].append({
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        })

    def get_summary(self):
        """Get test execution summary."""
        results = self.metrics["test_results"]
        if not results:
            return {}

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = sum(1 for r in results if r["status"] == "failed")
        total_duration = sum(r["duration_ms"] for r in results)

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "total_duration_ms": total_duration,
            "average_test_duration_ms": total_duration / total if total > 0 else 0
        }

    def save_metrics(self, filepath):
        """Save metrics to JSON file."""
        summary = self.get_summary()
        output = {
            **self.metrics,
            "summary": summary
        }

        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)


@pytest.fixture(scope="session")
def metrics_collector():
    """Session-wide metrics collector."""
    return TestMetricsCollector()


def pytest_runtest_logreport(report):
    """Hook to collect metrics after each test."""
    if report.when == "call":
        # Could be extended to record metrics
        pass


def pytest_sessionfinish(session, exitstatus):
    """Save metrics at end of test session."""
    if hasattr(session, 'config') and hasattr(session.config, '_metrics'):
        metrics_file = session.config.option.metrics_file
        session.config._metrics.save_metrics(metrics_file)


class PlatformDetector:
    """Detect platform and return configuration."""
    def __init__(self):
        self.platform = sys.platform
        self.is_ci = "CI" in os.environ

    def get_info(self):
        multipliers = {
            "win32": 1.5,
            "darwin": 1.0,
            "linux": 1.0,
            "ci": 2.0 if self.is_ci else 1.0
        }
        return {
            "platform": self.platform,
            "is_ci": self.is_ci,
            "timeout_multiplier": multipliers["ci"] if self.is_ci else multipliers.get(self.platform, 1.0),
            "is_windows": self.platform == "win32",
            "is_macos": self.platform == "darwin",
            "is_linux": self.platform == "linux"
        }
