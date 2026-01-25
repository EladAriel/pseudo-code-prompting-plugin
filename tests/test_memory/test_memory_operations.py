"""
Tests for memory persistence - Read/Write/Edit operations.
"""
import pytest


@pytest.mark.memory
@pytest.mark.unit
def test_empty_memory_initialization(mock_memory_dir):
    """Test memory directory can be created."""
    assert mock_memory_dir.exists()
    assert mock_memory_dir.is_dir()


@pytest.mark.memory
@pytest.mark.unit
def test_memory_file_creation(memory_file_factory):
    """Test memory files can be created."""
    file_path = memory_file_factory("test.md", "Test content")
    assert file_path.exists()
    assert file_path.read_text() == "Test content"


@pytest.mark.memory
@pytest.mark.unit
def test_active_context_creation(empty_active_context):
    """Test activeContext.md file creation."""
    assert empty_active_context.exists()
    content = empty_active_context.read_text()
    assert "Active Context" in content


@pytest.mark.memory
@pytest.mark.unit
def test_patterns_creation(empty_patterns):
    """Test patterns.md file creation."""
    assert empty_patterns.exists()
    content = empty_patterns.read_text()
    assert "Learned Patterns" in content or "patterns" in content.lower()


@pytest.mark.memory
@pytest.mark.unit
def test_progress_creation(empty_progress):
    """Test progress.md file creation."""
    assert empty_progress.exists()
    content = empty_progress.read_text()
    assert "Progress" in content or "Session" in content


@pytest.mark.memory
@pytest.mark.unit
def test_memory_file_read_write(mock_memory_dir):
    """Test reading and writing memory files."""
    test_file = mock_memory_dir / "test.md"
    test_file.write_text("Initial content")

    content = test_file.read_text()
    assert content == "Initial content"

    # Update content
    test_file.write_text("Updated content")
    updated_content = test_file.read_text()
    assert updated_content == "Updated content"


@pytest.mark.memory
@pytest.mark.unit
def test_memory_file_append(mock_memory_dir):
    """Test appending to memory files."""
    test_file = mock_memory_dir / "log.md"
    test_file.write_text("# Log\n\n")

    # Append entry
    existing = test_file.read_text()
    test_file.write_text(existing + "- Entry 1\n")

    content = test_file.read_text()
    assert "Entry 1" in content


@pytest.mark.memory
@pytest.mark.unit
def test_memory_multiple_files_coexist(mock_memory_dir):
    """Test multiple memory files can coexist."""
    context_file = mock_memory_dir / "activeContext.md"
    patterns_file = mock_memory_dir / "patterns.md"
    progress_file = mock_memory_dir / "progress.md"

    context_file.write_text("Context")
    patterns_file.write_text("Patterns")
    progress_file.write_text("Progress")

    assert context_file.read_text() == "Context"
    assert patterns_file.read_text() == "Patterns"
    assert progress_file.read_text() == "Progress"


@pytest.mark.memory
@pytest.mark.unit
def test_memory_multiline_content(mock_memory_dir):
    """Test memory files handle multiline content."""
    test_file = mock_memory_dir / "multiline.md"
    content = """# Header

Line 1
Line 2
Line 3

- Item 1
- Item 2
"""
    test_file.write_text(content)
    assert test_file.read_text() == content
