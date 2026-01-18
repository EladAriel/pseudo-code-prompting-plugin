#!/usr/bin/env python3
"""
Context-Aware Tree Generator for Claude Code Plugin
Generates ASCII tree structures for project directories with intelligent filtering.

Features:
- Python 3.6+ compatible, stdlib only
- Cross-platform support (Windows/Unix)
- Intelligent filtering (.gitignore support, default exclusions)
- Performance bounded (timeout, file limits, output size)
- Graceful error handling
"""

import os
import sys
import argparse
import platform
import signal
import threading
from pathlib import Path
from typing import List, Tuple, Set, Optional

# Constants
DEFAULT_MAX_DEPTH = 10
DEFAULT_MAX_FILES = 1000
DEFAULT_TIMEOUT = 10
MAX_OUTPUT_BYTES = 50 * 1024  # 50KB
EMPTY_FLAG = "<<PROJECT_EMPTY_NO_STRUCTURE>>"

# Default exclusions
DEFAULT_EXCLUDE_DIRS = {
    '.git', 'node_modules', 'dist', 'build', '__pycache__',
    'venv', '.next', '.venv', 'target', 'out', '.idea',
    '.vscode', 'coverage', '.pytest_cache', '.mypy_cache',
    'vendor', 'bower_components', '.nuxt', '.gradle'
}

DEFAULT_EXCLUDE_PATTERNS = {
    '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.bin',
    '*.o', '*.class', '*.log', '.DS_Store', 'Thumbs.db'
}


class TimeoutError(Exception):
    """Custom timeout exception."""
    pass


class TreeGenerator:
    """Generates ASCII tree structures from directory hierarchies."""

    def __init__(self, root_path: str, max_depth: int = DEFAULT_MAX_DEPTH,
                 max_files: int = DEFAULT_MAX_FILES, include_hidden: bool = False,
                 timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize tree generator.

        Args:
            root_path: Root directory to scan
            max_depth: Maximum recursion depth
            max_files: Maximum number of files to process
            include_hidden: Whether to include hidden files/dirs
            timeout: Maximum execution time in seconds
        """
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.max_files = max_files
        self.include_hidden = include_hidden
        self.timeout = timeout
        self.file_count = 0
        self.dir_count = 0
        self.skipped_count = 0
        self.errors = []
        self.gitignore_patterns = set()
        self.timed_out = False

    def load_gitignore_patterns(self) -> Set[str]:
        """
        Load and parse .gitignore patterns if available.

        Returns:
            Set of gitignore patterns (simplified glob patterns)
        """
        gitignore_path = self.root_path / '.gitignore'
        patterns = set()

        if not gitignore_path.exists():
            return patterns

        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        # Remove leading slash
                        if line.startswith('/'):
                            line = line[1:]
                        patterns.add(line)
        except Exception as e:
            self.errors.append(f"Failed to parse .gitignore: {e}")

        return patterns

    def should_exclude(self, path: Path, name: str, is_dir: bool) -> bool:
        """
        Check if a path should be excluded from the tree.

        Args:
            path: Full path to the file/directory
            name: Name of the file/directory
            is_dir: Whether this is a directory

        Returns:
            True if should be excluded, False otherwise
        """
        # Exclude hidden files/directories unless explicitly included
        if not self.include_hidden and name.startswith('.') and name != '.':
            return True

        # Exclude default directories
        if is_dir and name in DEFAULT_EXCLUDE_DIRS:
            return True

        # Check default file patterns
        if not is_dir:
            for pattern in DEFAULT_EXCLUDE_PATTERNS:
                if pattern.startswith('*') and name.endswith(pattern[1:]):
                    return True
                elif name == pattern:
                    return True

        # Check gitignore patterns (simplified matching)
        for pattern in self.gitignore_patterns:
            # Simple glob matching
            if pattern.endswith('/') and is_dir and name == pattern[:-1]:
                return True
            elif pattern.startswith('*') and name.endswith(pattern[1:]):
                return True
            elif pattern == name:
                return True
            elif '/' not in pattern and name == pattern:
                return True

        return False

    def scan_directory(self, dir_path: Path, current_depth: int = 0) -> List[Tuple[int, str, bool, Path]]:
        """
        Recursively scan directory and build tree structure.

        Args:
            dir_path: Directory to scan
            current_depth: Current recursion depth

        Returns:
            List of tuples: (depth, name, is_dir, full_path)
        """
        if self.timed_out:
            return []

        if current_depth >= self.max_depth:
            return []

        if self.file_count >= self.max_files:
            return []

        tree = []

        try:
            # Get directory contents
            entries = []
            try:
                entries = list(dir_path.iterdir())
            except PermissionError:
                self.errors.append(f"Permission denied: {dir_path}")
                self.skipped_count += 1
                return tree
            except Exception as e:
                self.errors.append(f"Error reading {dir_path}: {e}")
                return tree

            # Separate dirs and files, filter, and sort
            dirs = []
            files = []

            for entry in entries:
                try:
                    name = entry.name
                    is_dir = entry.is_dir()
                    is_symlink = entry.is_symlink()

                    # Skip symlinks to avoid cycles
                    if is_symlink:
                        continue

                    # Check exclusions
                    if self.should_exclude(entry, name, is_dir):
                        continue

                    if is_dir:
                        dirs.append((name, entry))
                    else:
                        files.append((name, entry))

                except (PermissionError, OSError) as e:
                    self.skipped_count += 1
                    continue

            # Sort alphabetically
            dirs.sort(key=lambda x: x[0].lower())
            files.sort(key=lambda x: x[0].lower())

            # Process directories first
            for name, entry in dirs:
                if self.file_count >= self.max_files or self.timed_out:
                    break

                self.dir_count += 1
                tree.append((current_depth, name, True, entry))

                # Recurse into subdirectory
                subtree = self.scan_directory(entry, current_depth + 1)
                tree.extend(subtree)

            # Then process files
            for name, entry in files:
                if self.file_count >= self.max_files or self.timed_out:
                    break

                self.file_count += 1
                tree.append((current_depth, name, False, entry))

        except Exception as e:
            self.errors.append(f"Unexpected error scanning {dir_path}: {e}")

        return tree

    def format_tree_ascii(self, tree: List[Tuple[int, str, bool, Path]]) -> str:
        """
        Format tree structure as ASCII art.

        Args:
            tree: List of tuples (depth, name, is_dir, path)

        Returns:
            ASCII tree string
        """
        if not tree:
            return EMPTY_FLAG

        lines = []
        lines.append(self.root_path.name + "/")

        # Track which depths need continuation lines
        depth_continues = {}

        for i, (depth, name, is_dir, _) in enumerate(tree):
            # Check if there are more items at this depth level
            is_last = True
            for j in range(i + 1, len(tree)):
                if tree[j][0] < depth:
                    break
                if tree[j][0] == depth:
                    is_last = False
                    break

            # Build prefix
            prefix = ""
            for d in range(depth):
                if depth_continues.get(d, False):
                    prefix += "|   "
                else:
                    prefix += "    "

            # Add branch
            if is_last:
                prefix += "+-- "
                depth_continues[depth] = False
            else:
                prefix += "|-- "
                depth_continues[depth] = True

            # Add name (with trailing slash for directories)
            if is_dir:
                lines.append(prefix + name + "/")
            else:
                lines.append(prefix + name)

        return "\n".join(lines)

    def truncate_output(self, tree_string: str) -> str:
        """
        Truncate output if it exceeds maximum size.

        Args:
            tree_string: Original tree string

        Returns:
            Truncated tree string with stats
        """
        tree_bytes = tree_string.encode('utf-8')

        if len(tree_bytes) <= MAX_OUTPUT_BYTES:
            return tree_string

        # Truncate to max size
        truncated_bytes = tree_bytes[:MAX_OUTPUT_BYTES - 500]  # Leave room for footer

        try:
            truncated_string = truncated_bytes.decode('utf-8', errors='ignore')
        except:
            truncated_string = tree_string[:int(MAX_OUTPUT_BYTES / 4)]  # Assume ~4 bytes per char

        # Add truncation notice
        footer = f"\n\n[TRUNCATED: Output exceeded {MAX_OUTPUT_BYTES} bytes]"
        footer += f"\nShowing partial tree (scanned {self.file_count} files, {self.dir_count} directories)"

        return truncated_string + footer

    def generate(self) -> str:
        """
        Generate the complete tree structure.

        Returns:
            ASCII tree string or empty flag
        """
        # Load gitignore patterns
        self.gitignore_patterns = self.load_gitignore_patterns()

        # Check if directory exists
        if not self.root_path.exists():
            return f"[ERROR: Directory does not exist: {self.root_path}]"

        if not self.root_path.is_dir():
            return f"[ERROR: Not a directory: {self.root_path}]"

        # Scan directory
        tree = self.scan_directory(self.root_path)

        # Check if empty
        if not tree:
            return EMPTY_FLAG

        # Format as ASCII
        tree_string = self.format_tree_ascii(tree)

        # Add stats footer
        footer = f"\n\nTotal: {self.file_count} files, {self.dir_count} directories"
        if self.file_count >= self.max_files:
            footer += f" (limited to {self.max_files} files)"
        footer += f" (scanned to depth {self.max_depth})"

        if self.skipped_count > 0:
            footer += f"\nSkipped: {self.skipped_count} items (permission denied or errors)"

        if self.errors and len(self.errors) <= 3:
            footer += "\n\nWarnings:"
            for error in self.errors[:3]:
                footer += f"\n- {error}"

        tree_string += footer

        # Truncate if needed
        return self.truncate_output(tree_string)


def handle_timeout(generator: TreeGenerator):
    """Timeout handler that sets flag on generator."""
    generator.timed_out = True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate ASCII tree structure for directories'
    )
    parser.add_argument('path', nargs='?', default='.',
                       help='Directory to scan (default: current directory)')
    parser.add_argument('--max-depth', type=int, default=DEFAULT_MAX_DEPTH,
                       help=f'Maximum recursion depth (default: {DEFAULT_MAX_DEPTH})')
    parser.add_argument('--max-files', type=int, default=DEFAULT_MAX_FILES,
                       help=f'Maximum number of files (default: {DEFAULT_MAX_FILES})')
    parser.add_argument('--include-hidden', action='store_true',
                       help='Include hidden files and directories')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                       help=f'Execution timeout in seconds (default: {DEFAULT_TIMEOUT})')

    args = parser.parse_args()

    # Create generator
    generator = TreeGenerator(
        args.path,
        max_depth=args.max_depth,
        max_files=args.max_files,
        include_hidden=args.include_hidden,
        timeout=args.timeout
    )

    # Set up timeout
    timer = None
    if platform.system() == 'Windows':
        # Use threading.Timer on Windows (no signal.alarm)
        timer = threading.Timer(args.timeout, handle_timeout, args=[generator])
        timer.daemon = True
        timer.start()
    else:
        # Use signal.alarm on Unix
        def timeout_handler(signum, frame):
            generator.timed_out = True
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(args.timeout)

    try:
        # Generate tree
        result = generator.generate()

        # Cancel timer if using threading
        if timer:
            timer.cancel()
        elif platform.system() != 'Windows':
            signal.alarm(0)

        # Output result
        print(result)

        # Exit with appropriate code
        if result == EMPTY_FLAG:
            sys.exit(0)
        elif result.startswith('[ERROR'):
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n[INTERRUPTED: Tree generation cancelled]", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR: {e}]", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
