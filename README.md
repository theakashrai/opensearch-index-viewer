# 🔍 OpenSearch Index Viewer

A clean, focused tool for visualizing OpenSearch index mappings with improved readability. No unnecessary charts - just clear, actionable information.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ What This Tool Does Right

- **Clean Terminal Output**: Beautiful, readable display using Rich library
- **Focused on Understanding**: Helps you understand index structure, not generate pretty pictures
- **Generic & Flexible**: Works with any OpenSearch index JSON export
- **Poetry Integration**: Proper dependency management with Poetry
- **Multiple Views**: Overview, field tree, search, comparison

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/opensearch-index-viewer.git
cd opensearch-index-viewer

# Install with Poetry
poetry install

# Or install with pip
pip install opensearch-index-viewer
```

### Basic Usage

```bash
# List all indexes in a file
opensearch-index-viewer list-indexes your_index_data.json

# View a specific index
opensearch-index-viewer view your_index_data.json --index your-index-name

# Search for specific fields
opensearch-index-viewer view your_index_data.json --search "symbol|date"

# Compare two indexes
opensearch-index-viewer compare your_index_data.json index1 index2

# Export clean summary
opensearch-index-viewer view your_index_data.json --export summary.json
```

### Using with Poetry (Development)

```bash
# Install dependencies
poetry install

# Run the tool
poetry run opensearch-index-viewer view your_index_data.json

# Or use the short alias
poetry run osiv view your_index_data.json
```

## 📋 Features

### 1. **Index Overview**
- Field count, shards, replicas
- Creation date and UUID
- Clean, at-a-glance summary

### 2. **Field Tree View**
- Hierarchical display of all fields
- Type indicators with emojis (📝 text, 🔤 keyword, 📅 date, etc.)
- Analyzer information
- Sub-field relationships
- Special properties (not indexed, no doc values)

### 3. **Field Types Summary**
- Count and percentage of each field type
- Examples of fields for each type
- Quick understanding of index composition

### 4. **Analyzer Analysis**
- Custom analyzer configurations
- Tokenizer and filter information
- Clear table format

### 5. **Search & Filter**
- Regex pattern search across field names
- Find specific fields quickly
- Filter results by properties

### 6. **Index Comparison**
- Side-by-side comparison of two indexes
- Spot differences in configuration
- Understand structural differences

### 7. **Clean JSON Export**
- Machine-readable summary export
- Structured data for further analysis
- Clean format without unnecessary nesting

## 🎯 Usage Examples

### Basic Index Analysis

```bash
# See everything about an index
opensearch-index-viewer view my_indexes.json --index products

# Just the field summary and analyzers
opensearch-index-viewer view my_indexes.json --index products --no-tree
```

### Search and Filter

```bash
# Find all date fields
opensearch-index-viewer view my_indexes.json --search "date|time|created"

# Find symbol-related fields
opensearch-index-viewer view my_indexes.json --search "symbol"
```

### Comparison and Analysis

```bash
# Compare two indexes
opensearch-index-viewer compare my_indexes.json prod-index dev-index

# Export for documentation
opensearch-index-viewer view my_indexes.json --export index_docs.json
```

## 📊 Sample Output

The tool produces clean, readable output like this:

```
────────────────────────── 📋 symbols-active ──────────────────────────

╭─────────────────────── 🗂️  Index Overview ───────────────────────╮
│ 📊 Index Name: symbols-active                                    │
│ 📈 Total Fields: 11                                              │
│ 🔧 Shards: 2                                                     │
│ 🔄 Replicas: 0                                                   │
│ 📅 Created: 2025-07-04 19:53:38                                  │
│ 🆔 UUID: XuXS1ZcBgTrB...                                         │
╰───────────────────────────────────────────────────────────────────╯

📋 symbols-active Fields
├── 📝 alternateExchange (text)
│   ├── 🔍 Analyzer: alt_exchange_analyzer
│   └── 🔎 Search Analyzer: description_analyzer
├── 📝 alternateSymbol (text)
│   └── 📎 Sub-fields
│       └── 🔤 keyword (keyword)
├── 🔤 currency (keyword)
├── 🔤 fidGroup (keyword)
│   ├── 🚫 Not Indexed
│   └── 📊 No Doc Values
└── 🔢 strike (float)
```

## 🛠️ Input Format

The tool expects a JSON file containing OpenSearch index data, typically obtained from:

```bash
# Get index mapping from OpenSearch
curl -X GET "localhost:9200/your-index/_mapping?pretty" > index_mapping.json

# Or get complete index info
curl -X GET "localhost:9200/your-index/?pretty" > index_complete.json
```

Example input format:

```json
{
  "your-index-name": {
    "mappings": {
      "properties": {
        "field1": {
          "type": "text",
          "analyzer": "standard"
        },
        "field2": {
          "type": "keyword"
        }
      }
    },
    "settings": {
      "index": {
        "number_of_shards": "1",
        "number_of_replicas": "0"
      }
    }
  }
}
```

## 📝 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `list-indexes` | Show all indexes in file | `opensearch-index-viewer list-indexes data.json` |
| `view` | Analyze a specific index | `opensearch-index-viewer view data.json --index my-index` |
| `compare` | Compare two indexes | `opensearch-index-viewer compare data.json idx1 idx2` |

### View Command Options

| Option | Description |
|--------|-------------|
| `--index` | Specific index to analyze |
| `--search` | Search pattern for fields |
| `--export` | Export summary to JSON |
| `--no-tree` | Hide field tree view |
| `--no-summary` | Hide field types summary |
| `--no-analyzers` | Hide analyzers table |

## 🔧 Development

### Setting up for Development

```bash
# Clone the repository
git clone https://github.com/yourusername/opensearch-index-viewer.git
cd opensearch-index-viewer

# Install development dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black opensearch_index_viewer/
poetry run isort opensearch_index_viewer/

# Type checking
poetry run mypy opensearch_index_viewer/
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=opensearch_index_viewer --cov-report=html

# Run specific test file
poetry run pytest tests/test_viewer.py
```

## 🎯 Why This Tool?

### Problems with Chart-Based Visualizers

- ❌ Generate unnecessary image files
- ❌ Focus on pretty pictures over useful information
- ❌ Hard to read in terminal environments
- ❌ Don't help with actual analysis tasks

### This Tool's Approach

- ✅ Terminal-native, readable output
- ✅ Focus on understanding structure
- ✅ Quick search and comparison
- ✅ Works with any OpenSearch index
- ✅ Clean data export for documentation
- ✅ Fast and lightweight

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Dependencies

- **Rich**: Beautiful terminal output
- **Typer**: Clean CLI interface
- **Python 3.9+**: Modern Python features

No heavy visualization libraries, no unnecessary dependencies!

---

This tool is designed for developers and DevOps engineers who need to quickly understand OpenSearch index structures without generating unnecessary files or charts.