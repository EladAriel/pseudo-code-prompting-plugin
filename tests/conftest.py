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
