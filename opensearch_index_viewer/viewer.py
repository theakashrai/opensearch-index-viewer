#!/usr/bin/env python3
"""
OpenSearch Index Viewer - Core visualization functionality
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich import box


class OpenSearchIndexViewer:
    """Clean, readable viewer for OpenSearch index configurations."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.console = Console()
    
    def get_index_overview(self, index_name: str) -> Panel:
        """Get a clean overview panel for an index."""
        if index_name not in self.data:
            return Panel(f"❌ Index '{index_name}' not found", style="red")
        
        index_data = self.data[index_name]
        settings = index_data.get("settings", {}).get("index", {})
        mappings = index_data.get("mappings", {})
        
        # Count properties
        properties = mappings.get("properties", {})
        field_count = len(properties)
        
        # Get creation date
        creation_date = settings.get("creation_date", "Unknown")
        if creation_date != "Unknown" and creation_date.isdigit():
            from datetime import datetime
            creation_date = datetime.fromtimestamp(int(creation_date) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        
        # Build overview text
        overview_text = f"""
📊 [bold]Index Name:[/bold] {index_name}
📈 [bold]Total Fields:[/bold] {field_count}
🔧 [bold]Shards:[/bold] {settings.get('number_of_shards', 'Unknown')}
🔄 [bold]Replicas:[/bold] {settings.get('number_of_replicas', 'Unknown')}
📅 [bold]Created:[/bold] {creation_date}
🆔 [bold]UUID:[/bold] {settings.get('uuid', 'Unknown')[:12]}...
        """.strip()
        
        return Panel(overview_text, title="🗂️  Index Overview", border_style="blue")
    
    def get_field_tree(self, index_name: str, max_depth: int = 3) -> Tree:
        """Create a clean tree view of fields."""
        if index_name not in self.data:
            tree = Tree("❌ Index not found")
            return tree
        
        mappings = self.data[index_name].get("mappings", {})
        properties = mappings.get("properties", {})
        
        tree = Tree(f"📋 [bold]{index_name}[/bold] Fields")
        
        for field_name, field_config in properties.items():
            field_type = field_config.get("type", "object")
            
            # Create field node with type and key info
            field_label = self._format_field_label(field_name, field_config)
            field_node = tree.add(field_label)
            
            # Add analyzer info if present
            if field_config.get("analyzer"):
                field_node.add(f"🔍 Analyzer: {field_config['analyzer']}")
            
            if field_config.get("search_analyzer"):
                field_node.add(f"🔎 Search Analyzer: {field_config['search_analyzer']}")
            
            # Add sub-fields
            if "fields" in field_config:
                sub_fields_node = field_node.add("📎 Sub-fields")
                for sub_name, sub_config in field_config["fields"].items():
                    sub_label = self._format_field_label(sub_name, sub_config)
                    sub_fields_node.add(sub_label)
            
            # Special indicators
            indicators = []
            if field_config.get("index") is False:
                indicators.append("🚫 Not Indexed")
            if field_config.get("doc_values") is False:
                indicators.append("📊 No Doc Values")
            
            for indicator in indicators:
                field_node.add(f"[yellow]{indicator}[/yellow]")
        
        return tree
    
    def _format_field_label(self, field_name: str, field_config: Dict[str, Any]) -> str:
        """Format a field label with type and key properties."""
        field_type = field_config.get("type", "object")
        
        # Type emoji mapping
        type_emojis = {
            "text": "📝",
            "keyword": "🔤",
            "date": "📅",
            "long": "🔢",
            "integer": "🔢",
            "float": "🔢",
            "double": "🔢",
            "boolean": "✅",
            "object": "📦",
            "nested": "🔗"
        }
        
        emoji = type_emojis.get(field_type, "❓")
        
        # Style based on type
        if field_type in ["text"]:
            style = "cyan"
        elif field_type in ["keyword"]:
            style = "green"
        elif field_type in ["date"]:
            style = "magenta"
        elif field_type in ["long", "integer", "float", "double"]:
            style = "yellow"
        else:
            style = "white"
        
        return f"{emoji} [{style}]{field_name}[/{style}] ([dim]{field_type}[/dim])"
    
    def get_analyzers_table(self, index_name: str) -> Table:
        """Create a clean table of analyzers."""
        table = Table(title=f"🔍 Analyzers - {index_name}", box=box.ROUNDED)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Type", style="green")
        table.add_column("Tokenizer", style="yellow")
        table.add_column("Filters", style="magenta")
        
        if index_name not in self.data:
            table.add_row("❌", "Index not found", "", "")
            return table
        
        settings = self.data[index_name].get("settings", {}).get("index", {})
        analysis = settings.get("analysis", {})
        analyzers = analysis.get("analyzer", {})
        
        if not analyzers:
            table.add_row("ℹ️", "No custom analyzers", "", "")
            return table
        
        for name, config in analyzers.items():
            filters = ", ".join(config.get("filter", []))
            table.add_row(
                name,
                config.get("type", "custom"),
                config.get("tokenizer", ""),
                filters or "None"
            )
        
        return table
    
    def get_field_types_summary(self, index_name: str) -> Table:
        """Create a summary table of field types."""
        table = Table(title=f"📊 Field Types Summary - {index_name}", box=box.ROUNDED)
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        table.add_column("Examples", style="dim")
        
        if index_name not in self.data:
            table.add_row("❌", "0", "0%", "Index not found")
            return table
        
        mappings = self.data[index_name].get("mappings", {})
        properties = mappings.get("properties", {})
        
        # Count field types and collect examples
        type_counts = {}
        type_examples = {}
        
        for field_name, field_config in properties.items():
            field_type = field_config.get("type", "object")
            type_counts[field_type] = type_counts.get(field_type, 0) + 1
            
            if field_type not in type_examples:
                type_examples[field_type] = []
            if len(type_examples[field_type]) < 3:
                type_examples[field_type].append(field_name)
        
        total_fields = len(properties)
        
        # Sort by count (descending)
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        
        for field_type, count in sorted_types:
            percentage = f"{(count / total_fields * 100):.1f}%" if total_fields > 0 else "0%"
            examples = ", ".join(type_examples[field_type][:2])
            if len(type_examples[field_type]) > 2:
                examples += f" (+{len(type_examples[field_type]) - 2} more)"
            
            table.add_row(field_type, str(count), percentage, examples)
        
        return table
    
    def search_fields(self, index_name: str, pattern: str) -> Table:
        """Search for fields matching a pattern."""
        table = Table(title=f"🔍 Search Results for '{pattern}' in {index_name}", box=box.ROUNDED)
        table.add_column("Field", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Analyzer", style="yellow")
        table.add_column("Properties", style="magenta")
        
        if index_name not in self.data:
            table.add_row("❌", "Index not found", "", "")
            return table
        
        mappings = self.data[index_name].get("mappings", {})
        properties = mappings.get("properties", {})
        
        import re
        matches = []
        
        for field_name, field_config in properties.items():
            if re.search(pattern, field_name, re.IGNORECASE):
                field_type = field_config.get("type", "object")
                analyzer = field_config.get("analyzer", "")
                
                # Collect properties
                props = []
                if field_config.get("index") is False:
                    props.append("Not Indexed")
                if field_config.get("doc_values") is False:
                    props.append("No Doc Values")
                if "fields" in field_config:
                    props.append(f"{len(field_config['fields'])} sub-fields")
                
                matches.append((field_name, field_type, analyzer, ", ".join(props)))
        
        if not matches:
            table.add_row("ℹ️", "No matches found", "", "")
        else:
            for field_name, field_type, analyzer, props in matches:
                table.add_row(field_name, field_type, analyzer or "None", props or "Standard")
        
        return table
    
    def export_readable_json(self, index_name: str, output_file: Path):
        """Export a clean, readable JSON summary."""
        if index_name not in self.data:
            self.console.print(f"❌ Index '{index_name}' not found", style="red")
            return
        
        index_data = self.data[index_name]
        settings = index_data.get("settings", {}).get("index", {})
        mappings = index_data.get("mappings", {})
        properties = mappings.get("properties", {})
        
        # Create clean summary
        summary = {
            "index_name": index_name,
            "overview": {
                "total_fields": len(properties),
                "shards": settings.get("number_of_shards"),
                "replicas": settings.get("number_of_replicas"),
                "creation_date": settings.get("creation_date"),
                "uuid": settings.get("uuid")
            },
            "field_types": {},
            "fields": {},
            "analyzers": settings.get("analysis", {}).get("analyzer", {}),
            "tokenizers": settings.get("analysis", {}).get("tokenizer", {})
        }
        
        # Count field types
        for field_name, field_config in properties.items():
            field_type = field_config.get("type", "object")
            if field_type not in summary["field_types"]:
                summary["field_types"][field_type] = {"count": 0, "examples": []}
            
            summary["field_types"][field_type]["count"] += 1
            if len(summary["field_types"][field_type]["examples"]) < 5:
                summary["field_types"][field_type]["examples"].append(field_name)
        
        # Clean field information
        for field_name, field_config in properties.items():
            clean_config = {
                "type": field_config.get("type", "object"),
                "analyzer": field_config.get("analyzer"),
                "search_analyzer": field_config.get("search_analyzer"),
                "normalizer": field_config.get("normalizer"),
                "indexed": field_config.get("index", True),
                "doc_values": field_config.get("doc_values", True),
                "sub_fields": list(field_config.get("fields", {}).keys()) if "fields" in field_config else []
            }
            # Remove None values
            summary["fields"][field_name] = {k: v for k, v in clean_config.items() if v is not None}
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, sort_keys=True)
        
        self.console.print(f"✅ Exported readable summary to: {output_file}", style="green")