"""
Pytest configuration for orchestration hooks tests.
Enables proper module imports for unit testing.
"""

import sys
from pathlib import Path

# Add orchestration directory to path for direct imports
orchestration_dir = Path(__file__).parent
sys.path.insert(0, str(orchestration_dir))
