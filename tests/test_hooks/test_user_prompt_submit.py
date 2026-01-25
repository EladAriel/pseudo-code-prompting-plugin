"""
Tests for user-prompt-submit hook - detects pseudo-code transformation commands.
"""
import pytest
import json


@pytest.mark.hook
@pytest.mark.integration
def test_hook_detects_smart_command(hook_executor, temp_dir):
    """Test hook detects /smart command invocation."""
    hook_input = json.dumps({
        "prompt": "/smart transform-query implement authentication",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    assert result.returncode == 0
    assert "PROMPTCONVERTER" in result.stdout or len(result.stdout) == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_detects_complete_process_command(hook_executor, temp_dir):
    """Test hook detects /complete-process command."""
    hook_input = json.dumps({
        "prompt": "/complete-process implement JWT authentication",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_detects_plugin_reference(hook_executor, temp_dir):
    """Test hook detects pseudo-code prompting plugin reference."""
    hook_input = json.dumps({
        "prompt": "Use pseudo-code prompting plugin to implement REST API",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_ignores_non_matching_input(hook_executor, temp_dir):
    """Test hook passes through non-matching input."""
    hook_input = json.dumps({
        "prompt": "What are the best practices for Python?",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.unit
def test_hook_handles_empty_prompt(hook_executor, temp_dir):
    """Test hook handles empty prompt gracefully."""
    hook_input = json.dumps({
        "prompt": "",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_hook_json_input_parsing(hook_executor, temp_dir):
    """Test hook correctly parses JSON input."""
    hook_input = json.dumps({
        "prompt": "/transform-query implement database schema",
        "cwd": str(temp_dir)
    })

    result = hook_executor("hooks/core/user-prompt-submit.py", hook_input)

    # Should not crash on valid JSON
    assert result.returncode == 0
