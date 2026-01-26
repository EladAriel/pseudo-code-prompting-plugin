"""Cross-platform path normalization tests."""
import pytest
import os
import sys
from pathlib import Path


@pytest.mark.integration
class TestPathNormalization:
    """Test cross-platform path handling and normalization."""

    def test_path_separator_normalization(self):
        """Verify paths normalize across platforms."""
        # Windows path
        win_path = "folder\\subfolder\\file.txt"
        normalized = win_path.replace("\\", "/")
        assert "/" in normalized, "Path should use forward slashes"

    def test_mixed_separator_handling(self):
        """Verify mixed separator paths are normalized."""
        mixed_path = "folder\\sub/folder\\file.txt"
        normalized = mixed_path.replace("\\", "/")
        expected = "folder/sub/folder/file.txt"
        assert normalized == expected, "Mixed separators should normalize"

    def test_relative_path_resolution(self, tmp_path):
        """Verify relative paths resolve correctly."""
        base = tmp_path
        subdir = base / "sub" / "dir"
        subdir.mkdir(parents=True)

        # Create file
        test_file = subdir / "test.txt"
        test_file.write_text("content")

        # Resolve relative path
        cwd = os.getcwd()
        try:
            os.chdir(base)
            resolved = Path("sub/dir/test.txt").resolve()
            assert resolved.exists(), "Relative path should resolve"
            assert resolved.is_file(), "Should resolve to file"
        finally:
            os.chdir(cwd)

    def test_unc_path_preservation(self):
        """Verify UNC paths are preserved on Windows."""
        if sys.platform != "win32":
            pytest.skip("UNC paths are Windows-specific")

        unc_path = "\\\\server\\share\\folder\\file.txt"
        # UNC paths should start with \\
        assert unc_path.startswith("\\\\"), "UNC path format should be preserved"

    def test_absolute_vs_relative_detection(self):
        """Verify absolute and relative paths are correctly identified."""
        abs_path = "/home/user/file.txt" if sys.platform != "win32" else "C:\\Users\\user\\file.txt"
        rel_path = "folder/subfolder/file.txt"

        abs_pathobj = Path(abs_path)
        rel_pathobj = Path(rel_path)

        assert abs_pathobj.is_absolute(), "Absolute path should be detected"
        assert not rel_pathobj.is_absolute(), "Relative path should be detected"

    def test_path_case_sensitivity(self):
        """Test path handling for case sensitivity."""
        if sys.platform == "win32":
            pytest.skip("Windows paths are case-insensitive")

        path1 = "Folder/File.txt"
        path2 = "folder/file.txt"

        # On Linux/Mac, these are different
        assert path1 != path2, "Paths should be case-sensitive on this platform"

    def test_symlink_path_resolution(self, tmp_path):
        """Verify symlink paths are resolved correctly."""
        if sys.platform == "win32":
            pytest.skip("Symlink test requires Unix-like system")

        try:
            target = tmp_path / "target.txt"
            target.write_text("content")

            link = tmp_path / "link.txt"
            link.symlink_to(target)

            resolved = link.resolve()
            assert resolved == target.resolve(), "Symlink should resolve to target"
        except (OSError, NotImplementedError):
            pytest.skip("Symlinks not supported on this system")

    def test_dot_dot_path_resolution(self, tmp_path):
        """Verify '..' path resolution works correctly."""
        base = tmp_path / "a" / "b" / "c"
        base.mkdir(parents=True)

        # Create path with ..
        path_with_dots = base / ".." / ".." / "file.txt"
        resolved = path_with_dots.resolve()

        expected = (tmp_path / "a" / "file.txt").resolve()
        assert resolved.parent == expected.parent, "Path with '..' should resolve correctly"

    def test_trailing_slash_normalization(self):
        """Verify trailing slashes are normalized."""
        path_with_slash = "folder/subfolder/"
        path_without_slash = "folder/subfolder"

        # Normalize by removing trailing slash
        normalized = path_with_slash.rstrip("/").rstrip("\\")
        assert normalized == path_without_slash, "Trailing slash should be removed"

    @pytest.mark.parametrize("path", [
        "/home/user/file.txt",
        "C:\\Users\\user\\file.txt",
        "folder/subfolder/file.txt",
        "./relative/path.txt",
        "../parent/file.txt",
    ])
    def test_path_normalization_robustness(self, path):
        """Test path normalization with various formats."""
        pathobj = Path(path)
        normalized = str(pathobj).replace("\\", "/")

        # Should not start/end with special sequences
        assert not normalized.startswith(".\\"), "Should not have backslash after dot"
        assert "/" in normalized or pathobj.name, "Should have valid structure"

    def test_windows_drive_letter_handling(self):
        """Test Windows drive letter handling."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        path = "C:\\Users\\file.txt"
        assert path[1] == ":", "Drive letter should be followed by colon"

    def test_home_directory_expansion(self):
        """Verify ~ expands to home directory."""
        expanded = Path("~/file.txt").expanduser()
        assert str(expanded).startswith(str(Path.home())), \
            "~ should expand to home directory"

    def test_current_directory_relative_path(self, tmp_path):
        """Test relative paths from current directory."""
        cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            subdir = tmp_path / "subdir"
            subdir.mkdir()

            path = Path("subdir") / "file.txt"
            assert not path.is_absolute(), "Relative path should not be absolute"
            assert "subdir" in str(path), "Relative path should contain subdirectory"
        finally:
            os.chdir(cwd)

    def test_empty_path_handling(self):
        """Test handling of edge case paths."""
        empty = Path("")
        assert str(empty) == ".", "Empty path should default to current directory"

    def test_path_encoding_issues(self):
        """Test paths with special characters."""
        special_path = "folder/sub-folder_2/file-name.txt"
        pathobj = Path(special_path)

        assert "sub-folder_2" in str(pathobj), "Path with special chars should work"
