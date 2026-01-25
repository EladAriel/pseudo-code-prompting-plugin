"""
Pytest configuration and shared fixtures for pseudo-code-prompting plugin tests.
"""
import pytest
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Callable


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
        # Normalize whitespace and line endings
        actual_lines = [line.strip() for line in actual.strip().split("\n") if line.strip()]
        expected_lines = [line.strip() for line in expected.strip().split("\n") if line.strip()]
        return actual_lines == expected_lines
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
