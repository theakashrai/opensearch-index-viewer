"""Tests for the OpenSearchIndexViewer class."""

import json
import pytest
from pathlib import Path
from opensearch_index_viewer.viewer import OpenSearchIndexViewer


@pytest.fixture
def sample_data():
    """Sample OpenSearch index data for testing."""
    return {
        "test-index": {
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "age": {
                        "type": "integer"
                    },
                    "created_at": {
                        "type": "date"
                    },
                    "tags": {
                        "type": "keyword"
                    }
                }
            },
            "settings": {
                "index": {
                    "number_of_shards": "1",
                    "number_of_replicas": "0",
                    "creation_date": "1640995200000",
                    "uuid": "test-uuid-123456"
                }
            }
        }
    }


@pytest.fixture
def viewer(sample_data):
    """OpenSearchIndexViewer instance with sample data."""
    return OpenSearchIndexViewer(sample_data)


def test_viewer_initialization(sample_data):
    """Test viewer initialization with data."""
    viewer = OpenSearchIndexViewer(sample_data)
    assert viewer.data == sample_data
    assert viewer.console is not None


def test_get_index_overview(viewer):
    """Test index overview generation."""
    overview = viewer.get_index_overview("test-index")
    assert "test-index" in overview.renderable
    assert "4" in overview.renderable  # field count
    assert "1" in overview.renderable  # shards
    assert "0" in overview.renderable  # replicas


def test_get_index_overview_missing_index(viewer):
    """Test overview for non-existent index."""
    overview = viewer.get_index_overview("missing-index")
    assert "not found" in overview.renderable


def test_get_field_tree(viewer):
    """Test field tree generation."""
    tree = viewer.get_field_tree("test-index")
    assert "test-index" in str(tree.label)
    assert len(tree.children) == 4  # 4 fields


def test_get_field_tree_missing_index(viewer):
    """Test field tree for non-existent index."""
    tree = viewer.get_field_tree("missing-index")
    assert "not found" in str(tree.label)


def test_format_field_label(viewer):
    """Test field label formatting."""
    field_config = {"type": "text", "analyzer": "standard"}
    label = viewer._format_field_label("test_field", field_config)
    
    assert "📝" in label  # text emoji
    assert "test_field" in label
    assert "text" in label


def test_get_analyzers_table_no_analyzers(viewer):
    """Test analyzers table when no custom analyzers exist."""
    table = viewer.get_analyzers_table("test-index")
    # Should contain "No custom analyzers" message
    assert len(table.rows) >= 1


def test_get_field_types_summary(viewer):
    """Test field types summary generation."""
    table = viewer.get_field_types_summary("test-index")
    
    # Should have rows for different field types (one per type)
    assert len(table.rows) >= 4  # text, integer, date, keyword
    
    # Check table has the right structure
    assert len(table.columns) == 4  # Type, Count, Percentage, Examples
    assert "Field Types Summary" in table.title


def test_search_fields(viewer):
    """Test field search functionality."""
    # Search for 'name' field
    table = viewer.search_fields("test-index", "name")
    assert len(table.rows) == 1
    assert "Search Results" in table.title
    
    # Search for non-existent field
    table = viewer.search_fields("test-index", "nonexistent")
    assert len(table.rows) == 1  # Should have "No matches found" row


def test_search_fields_pattern(viewer):
    """Test field search with regex pattern."""
    # Search for fields containing 'a' (should match 'name', 'age', 'created_at', 'tags')
    table = viewer.search_fields("test-index", "a")
    assert len(table.rows) == 4  # name, age, created_at, tags


def test_export_readable_json(viewer, tmp_path):
    """Test JSON export functionality."""
    output_file = tmp_path / "test_export.json"
    viewer.export_readable_json("test-index", output_file)
    
    # Check file was created
    assert output_file.exists()
    
    # Check content
    with open(output_file, 'r') as f:
        exported_data = json.load(f)
    
    assert exported_data["index_name"] == "test-index"
    assert exported_data["overview"]["total_fields"] == 4
    assert "field_types" in exported_data
    assert "fields" in exported_data


def test_export_readable_json_missing_index(viewer, tmp_path):
    """Test JSON export for non-existent index."""
    output_file = tmp_path / "test_export.json"
    viewer.export_readable_json("missing-index", output_file)
    
    # File should not be created
    assert not output_file.exists()