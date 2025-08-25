"""
OpenSearch Index Viewer

A clean, readable tool for visualizing OpenSearch index mappings.
Focus on clarity and understanding rather than flashy charts.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .viewer import OpenSearchIndexViewer
from .cli import app

__all__ = ["OpenSearchIndexViewer", "app"]