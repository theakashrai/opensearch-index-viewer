"""Tests for the CLI interface."""

import json
import pytest
from typer.testing import CliRunner
from pathlib import Path
from opensearch_index_viewer.cli import app


@pytest.fixture
def sample_json_file(tmp_path):
    """Create a temporary JSON file with sample data."""
    sample_data = {
        "test-index": {
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "age": {"type": "integer"}
                }
            },
            "settings": {
                "index": {
                    "number_of_shards": "1",
                    "number_of_replicas": "0"
                }
            }
        },
        "another-index": {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "price": {"type": "double"}
                }
            },
            "settings": {
                "index": {
                    "number_of_shards": "2",
                    "number_of_replicas": "1"
                }
            }
        }
    }
    
    json_file = tmp_path / "test_indexes.json"
    with open(json_file, 'w') as f:
        json.dump(sample_data, f)
    
    return json_file


def test_list_indexes_command(sample_json_file):
    """Test the list-indexes command."""
    runner = CliRunner()
    result = runner.invoke(app, ["list-indexes", str(sample_json_file)])
    
    assert result.exit_code == 0
    assert "test-index" in result.stdout
    assert "another-index" in result.stdout


def test_view_command_all_indexes(sample_json_file):
    """Test the view command without specifying an index."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", str(sample_json_file)])
    
    assert result.exit_code == 0
    assert "test-index" in result.stdout
    assert "another-index" in result.stdout


def test_view_command_specific_index(sample_json_file):
    """Test the view command with a specific index."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", str(sample_json_file), "--index", "test-index"])
    
    assert result.exit_code == 0
    assert "test-index" in result.stdout
    assert "another-index" not in result.stdout


def test_view_command_with_search(sample_json_file):
    """Test the view command with search pattern."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", str(sample_json_file), "--search", "name"])
    
    assert result.exit_code == 0
    assert "name" in result.stdout


def test_view_command_with_no_tree(sample_json_file):
    """Test the view command with --no-tree option."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", str(sample_json_file), "--no-tree"])
    
    assert result.exit_code == 0
    # Should still show overview and summary, but not tree


def test_view_command_with_export(sample_json_file, tmp_path):
    """Test the view command with export option."""
    export_file = tmp_path / "export.json"
    runner = CliRunner()
    result = runner.invoke(app, [
        "view", str(sample_json_file), 
        "--index", "test-index",
        "--export", str(export_file)
    ])
    
    assert result.exit_code == 0
    assert export_file.exists()
    
    # Check exported content
    with open(export_file, 'r') as f:
        exported_data = json.load(f)
    
    assert exported_data["index_name"] == "test-index"


def test_compare_command(sample_json_file):
    """Test the compare command."""
    runner = CliRunner()
    result = runner.invoke(app, [
        "compare", str(sample_json_file), 
        "test-index", "another-index"
    ])
    
    assert result.exit_code == 0
    assert "test-index" in result.stdout
    assert "another-index" in result.stdout


def test_view_command_missing_index(sample_json_file):
    """Test the view command with non-existent index."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", str(sample_json_file), "--index", "missing"])
    
    assert result.exit_code == 0
    assert "not found" in result.stdout


def test_view_command_missing_file():
    """Test the view command with non-existent file."""
    runner = CliRunner()
    result = runner.invoke(app, ["view", "missing_file.json"])
    
    assert result.exit_code == 1
    assert "File not found" in result.stdout


def test_compare_command_missing_index(sample_json_file):
    """Test the compare command with non-existent index."""
    runner = CliRunner()
    result = runner.invoke(app, [
        "compare", str(sample_json_file), 
        "test-index", "missing-index"
    ])
    
    assert result.exit_code == 1
    assert "not found" in result.stdout