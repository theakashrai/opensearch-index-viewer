#!/usr/bin/env python3
"""
Standalone entry point script for OpenSearch Index Viewer.
This can be used to run the tool without installing the package.
"""

import sys
from pathlib import Path

# Add the package directory to Python path
package_dir = Path(__file__).parent / "opensearch_index_viewer"
sys.path.insert(0, str(package_dir.parent))

from opensearch_index_viewer.cli import app

if __name__ == "__main__":
    app()