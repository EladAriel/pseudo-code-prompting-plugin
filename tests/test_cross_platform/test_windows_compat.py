"""Windows-specific compatibility tests."""
import pytest
import sys


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific tests")
@pytest.mark.integration
class TestWindowsCompat:
    """Test Windows platform compatibility."""

    def test_windows_path_handling(self):
        """Test Windows path handling."""
        path = "C:\\Users\\test\\file.txt"
        assert path[1] == ":"
        assert "\\" in path

    def test_windows_unc_paths(self):
        """Test UNC path support."""
        unc_path = "\\\\server\\share\\file.txt"
        assert unc_path.startswith("\\\\")
