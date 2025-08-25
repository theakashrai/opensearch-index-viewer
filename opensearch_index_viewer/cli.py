#!/usr/bin/env python3
"""
OpenSearch Index Viewer - CLI interface
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import typer
from rich.console import Console
from rich.layout import Layout

from .viewer import OpenSearchIndexViewer

app = typer.Typer(help="OpenSearch Index Viewer - Clear visualization of index mappings")
console = Console()


def load_index_data(file_path: Path) -> Dict[str, Any]:
    """Load OpenSearch index data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"❌ File not found: {file_path}", style="red")
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        console.print(f"❌ Invalid JSON: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def view(
    file_path: Path = typer.Argument(..., help="Path to JSON file containing index data"),
    index: Optional[str] = typer.Option(None, "--index", "-i", help="Specific index to analyze"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search pattern for fields"),
    export: Optional[Path] = typer.Option(None, "--export", "-e", help="Export clean summary to JSON"),
    show_tree: bool = typer.Option(True, "--tree/--no-tree", help="Show field tree view"),
    show_summary: bool = typer.Option(True, "--summary/--no-summary", help="Show field types summary"),
    show_analyzers: bool = typer.Option(True, "--analyzers/--no-analyzers", help="Show analyzers table"),
):
    """View OpenSearch index mappings in a clean, readable format."""
    
    # Load data
    data = load_index_data(file_path)
    viewer = OpenSearchIndexViewer(data)
    
    # Determine which indexes to show
    indexes = [index] if index else list(data.keys())
    
    if not indexes:
        console.print("❌ No indexes found in the data", style="red")
        raise typer.Exit(1)
    
    for idx_name in indexes:
        if idx_name not in data:
            console.print(f"❌ Index '{idx_name}' not found", style="red")
            continue
        
        console.print()
        console.rule(f"[bold blue]📋 {idx_name}[/bold blue]")
        console.print()
        
        # Show overview
        console.print(viewer.get_index_overview(idx_name))
        console.print()
        
        # Search if pattern provided
        if search:
            console.print(viewer.search_fields(idx_name, search))
            console.print()
        
        # Show components based on options
        if show_summary:
            console.print(viewer.get_field_types_summary(idx_name))
            console.print()
        
        if show_analyzers:
            console.print(viewer.get_analyzers_table(idx_name))
            console.print()
        
        if show_tree:
            console.print(viewer.get_field_tree(idx_name))
            console.print()
        
        # Export if requested
        if export:
            viewer.export_readable_json(idx_name, export)


@app.command()
def list_indexes(
    file_path: Path = typer.Argument(..., help="Path to JSON file containing index data")
):
    """List all indexes in the JSON file."""
    data = load_index_data(file_path)
    
    if not data:
        console.print("❌ No indexes found", style="red")
        return
    
    console.print("[bold blue]📋 Available Indexes:[/bold blue]")
    for i, index_name in enumerate(data.keys(), 1):
        console.print(f"  {i}. [cyan]{index_name}[/cyan]")


@app.command()
def compare(
    file_path: Path = typer.Argument(..., help="Path to JSON file containing index data"),
    index1: str = typer.Argument(..., help="First index to compare"),
    index2: str = typer.Argument(..., help="Second index to compare"),
):
    """Compare two indexes side by side."""
    data = load_index_data(file_path)
    viewer = OpenSearchIndexViewer(data)
    
    if index1 not in data or index2 not in data:
        console.print("❌ One or both indexes not found", style="red")
        raise typer.Exit(1)
    
    # Create layout for comparison
    layout = Layout()
    layout.split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    
    # Left side
    left_content = [
        viewer.get_index_overview(index1),
        viewer.get_field_types_summary(index1)
    ]
    
    # Right side  
    right_content = [
        viewer.get_index_overview(index2),
        viewer.get_field_types_summary(index2)
    ]
    
    layout["left"].split_column(*[Layout(c) for c in left_content])
    layout["right"].split_column(*[Layout(c) for c in right_content])
    
    console.print(layout)


if __name__ == "__main__":
    app()