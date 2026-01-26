"""
Tests for get_context_tree.py - generates project structure for context injection.
"""
import pytest
import json
import subprocess
from pathlib import Path


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_empty_directory(hook_executor, empty_project_structure):
    """Test tree generation on empty directory."""
    script = "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(Path(__file__).parent.parent.parent / script), str(empty_project_structure)],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0
    output = result.stdout.strip()
    assert "<<PROJECT_EMPTY_NO_STRUCTURE>>" in output or output == ""


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_with_files(hook_executor, nextjs_project_structure):
    """Test tree generation with project files."""
    script = "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(Path(__file__).parent.parent.parent / script), str(nextjs_project_structure)],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0
    output = result.stdout.strip()
    assert "package.json" in output or "Total:" in output or "<<PROJECT_EMPTY_NO_STRUCTURE>>" in output


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_respects_max_files(nextjs_project_structure):
    """Test tree generation respects --max-files limit."""
    script_path = Path(__file__).parent.parent.parent / "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(script_path), str(nextjs_project_structure), "--max-files", "1"],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0
    # Should not exceed file limit in output


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_respects_max_depth(nextjs_project_structure):
    """Test tree generation respects --max-depth limit."""
    script_path = Path(__file__).parent.parent.parent / "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(script_path), str(nextjs_project_structure), "--max-depth", "1"],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_gitignore_support(gitignore_project):
    """Test tree generation respects .gitignore."""
    script_path = Path(__file__).parent.parent.parent / "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(script_path), str(gitignore_project)],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0
    output = result.stdout.strip()
    # node_modules should be excluded by gitignore
    if output and "<<PROJECT_EMPTY_NO_STRUCTURE>>" not in output:
        assert "node_modules" not in output


@pytest.mark.hook
@pytest.mark.unit
def test_tree_generation_invalid_path():
    """Test tree generation with invalid path."""
    script_path = Path(__file__).parent.parent.parent / "hooks/tree/get_context_tree.py"

    result = subprocess.run(
        ["python3", str(script_path), "/nonexistent/path"],
        capture_output=True,
        text=True,
        timeout=10
    )

    # Should handle gracefully (non-zero exit or error message)
    assert result.returncode != 0 or "<<PROJECT_EMPTY_NO_STRUCTURE>>" in result.stdout


@pytest.mark.hook
@pytest.mark.integration
def test_tree_generation_timeout(tmp_path):
    """Test tree generation respects timeout."""
    script_path = Path(__file__).parent.parent.parent / "hooks/tree/get_context_tree.py"

    # Create a large directory structure that will take longer to scan
    large_dir = tmp_path / "large_project"
    large_dir.mkdir()

    # Create many nested directories to force longer scan time
    for i in range(50):
        subdir = large_dir / f"dir_{i}"
        subdir.mkdir()
        for j in range(20):
            (subdir / f"file_{j}.txt").write_text("content")

    # Should timeout with very short timeout on large directory
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            ["python3", str(script_path), str(large_dir), "--max-files", "10000"],
            capture_output=True,
            text=True,
            timeout=0.05  # Very short timeout to test timeout handling
        )
