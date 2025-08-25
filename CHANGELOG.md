# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-25

### Added

- Initial release of OpenSearch Index Viewer
- Clean terminal-based visualization of OpenSearch index mappings
- Field tree view with type indicators and emojis
- Index overview with metadata (shards, replicas, creation date)
- Field types summary with counts and examples
- Analyzer analysis with configuration details
- Search functionality with regex pattern matching
- Index comparison feature for side-by-side analysis
- JSON export for machine-readable summaries
- CLI interface with multiple commands and options
- Poetry packaging with proper dependency management
- Rich library integration for beautiful terminal output
- Typer integration for clean command-line interface

### Features

- **list-indexes**: List all available indexes in a JSON file
- **view**: Analyze a specific index with various display options
- **compare**: Compare two indexes side by side
- Support for OpenSearch/Elasticsearch index JSON exports
- Configurable display options (--no-tree, --no-summary, --no-analyzers)
- Search field names with regex patterns
- Export clean summaries to JSON format

### Documentation

- Comprehensive README with usage examples
- API documentation for core classes
- Sample data files for testing
- MIT license for open source distribution
