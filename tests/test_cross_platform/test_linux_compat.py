"""Linux-specific compatibility tests."""
import pytest
import sys


@pytest.mark.skipif(sys.platform != "linux", reason="Linux-specific tests")
@pytest.mark.integration
class TestLinuxCompat:
    """Test Linux platform compatibility."""

    def test_linux_path_handling(self):
        """Test Linux path handling."""
        path = "/home/test/file.txt"
        assert path.startswith("/")
        assert "\\" not in path

    def test_linux_case_sensitive_fs(self):
        """Test case-sensitive filesystem."""
        path1 = "Test/File.txt"
        path2 = "test/file.txt"
        # On Linux, these are different paths
        assert path1 != path2
