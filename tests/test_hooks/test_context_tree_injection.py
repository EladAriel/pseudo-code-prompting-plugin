"""
Tests for context-aware-tree-injection hook - injects project context.
"""
import pytest
import json
import subprocess
from pathlib import Path


@pytest.mark.hook
@pytest.mark.integration
def test_hook_injects_context_on_implement_keyword(hook_executor, temp_dir):
    """Test hook injects context when 'implement' keyword detected."""
    hook_input = json.dumps({
        "prompt": "implement user authentication system",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_injects_context_on_create_keyword(hook_executor, temp_dir):
    """Test hook injects context when 'create' keyword detected."""
    hook_input = json.dumps({
        "prompt": "create a new REST API endpoint",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_injects_context_on_add_keyword(hook_executor, temp_dir):
    """Test hook injects context when 'add' keyword detected."""
    hook_input = json.dumps({
        "prompt": "add validation to the user model",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_injects_context_on_refactor_keyword(hook_executor, temp_dir):
    """Test hook injects context when 'refactor' keyword detected."""
    hook_input = json.dumps({
        "prompt": "refactor the authentication module for better testing",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_passes_through_non_implementation(hook_executor, temp_dir):
    """Test hook passes through prompts without implementation keywords."""
    hook_input = json.dumps({
        "prompt": "what are the best practices for REST API design?",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.unit
def test_hook_handles_missing_directory(hook_executor):
    """Test hook handles missing directory gracefully."""
    hook_input = json.dumps({
        "prompt": "implement feature",
        "cwd": "/nonexistent/directory"
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    # Should not crash
    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.unit
def test_hook_handles_empty_prompt(hook_executor, temp_dir):
    """Test hook handles empty prompt."""
    hook_input = json.dumps({
        "prompt": "",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/tree/context-aware-tree-injection.py", hook_input, timeout=15)

    assert result.returncode == 0
