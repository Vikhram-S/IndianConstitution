# IndianConstitution <small> (v.1.0.1) </small>
Advanced Python library for accessing and analyzing the Constitution of India with DataFrame support, fuzzy search, export capabilities, and more.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/indianconstitution?label=Python) ![PyPI - License](https://img.shields.io/pypi/l/indianconstitution?label=License&color=red) ![Maintenance](https://img.shields.io/maintenance/yes/2026?label=Maintained) ![PyPI](https://img.shields.io/pypi/v/indianconstitution?label=PyPi) ![PyPI - Status](https://img.shields.io/pypi/status/indianconstitution?label=Status)
![PyPI - Downloads](https://img.shields.io/pypi/dm/indianconstitution?label=Monthly%20Downloads) 
![Total Downloads](https://static.pepy.tech/badge/indianconstitution?label=Total%20Downloads)
![SemVer](https://img.shields.io/badge/versioning-SemVer-blue)
![Wheel](https://img.shields.io/pypi/wheel/indianconstitution)
![Docs](https://img.shields.io/badge/docs-available-brightgreen)
---

## 🚀 Installation

### Basic Installation

#### Using pip (PyPI)
```bash
pip install indianconstitution
```

### With Advanced Features
```bash
# For DataFrame and visualization support
pip install indianconstitution[advanced]

# For fuzzy search capabilities
pip install indianconstitution[fuzzy]

# For all advanced features
pip install indianconstitution[all]
```

**Note:** Optional dependencies can also be installed separately:
```bash
# After conda install, add optional features
conda install pandas matplotlib
pip install fuzzywuzzy python-Levenshtein
```

---

## ✨ Features

### Core Features
- ✅ Full access to the Constitution of India data
- ✅ Retrieval of individual articles and summaries
- ✅ Keyword-based search for articles
- ✅ Count of total articles and search by title functionality

### Advanced Features
- 🐼 **DataFrame Support**: Convert to pandas DataFrame for advanced data manipulation
- 🔍 **Advanced Search**: Regex and fuzzy search capabilities
- 📊 **Statistical Analysis**: Get insights about the Constitution
- 📤 **Export Functionality**: Export to JSON, CSV, Markdown formats
- 🔗 **Relationship Mapping**: Find articles that reference each other
- 📈 **Visualization**: Word frequency charts and data visualization
- 🔄 **Method Chaining**: Fluent API design for complex operations
- 💻 **CLI Tool**: Command-line interface for quick access
- ⚡ **Performance**: Caching and optimized data structures
- 🎯 **Dictionary-like Access**: Access articles like `constitution[14]`

---

## 📖 Usage

### Basic Usage

```python
from indianconstitution import IndianConstitution

# Initialize
india = IndianConstitution()

# Access the Preamble
print(india.preamble())

# Get a specific article
print(india.get_article(14))

# Search for articles
print(india.search_keyword('equality'))

# Count articles
print(f"Total articles: {india.count_articles()}")
```

### Advanced Usage

#### DataFrame Support (pandas-like interface)

```python
import pandas as pd
from indianconstitution import IndianConstitution

india = IndianConstitution()

# Convert to DataFrame
df = india.to_dataframe()

# Use pandas operations
print(df.head())
print(df.describe())

# Filter articles
fundamental_rights = df[df['title'].str.contains('Fundamental', case=False)]
print(fundamental_rights[['article', 'title', 'word_count']])

# Sort by word count
longest_articles = df.nlargest(10, 'word_count')
print(longest_articles[['article', 'title', 'word_count']])
```

#### Advanced Search

```python
# Regex search
results = india.search_regex(r'\b(equality|liberty|fraternity)\b', case_sensitive=False)
for article in results:
    print(f"Article {article['article']}: {article['title']}")

# Fuzzy search (handles typos and partial matches)
results = india.fuzzy_search('fundamental rights', threshold=70, limit=10)
for article in results:
    print(f"Article {article['article']}: {article['title']}")
```

#### Export Functionality

```python
# Export to JSON
india.export_json('constitution.json')

# Export to CSV (requires pandas)
india.export_csv('constitution.csv')

# Export to Markdown
india.export_markdown('constitution.md')
```

#### Statistical Analysis

```python
# Get comprehensive statistics
stats = india.get_statistics()
print(f"Total Articles: {stats['total_articles']}")
print(f"Total Words: {stats['total_words']:,}")
print(f"Average Words per Article: {stats['average_words_per_article']}")
print(f"Longest Article: {stats['longest_article']['title']}")
```

---

## 💻 Command-Line Interface (CLI)

The library includes a CLI tool for quick access:

```bash
# Get a specific article
indianconstitution get 14

# Search for articles
indianconstitution search equality

# Fuzzy search
indianconstitution search --fuzzy "fundamental rights"

# Export to JSON
indianconstitution export json constitution.json

# Show statistics
indianconstitution stats

# Display the Preamble
indianconstitution preamble
```

---

## 🔧 Requirements

### Core Requirements
- Python 3.7+

### Optional Dependencies
- `pandas>=1.3.0` - For DataFrame support and CSV export
- `matplotlib>=3.3.0` - For visualization features
- `fuzzywuzzy>=0.18.0` - For fuzzy search
- `python-Levenshtein>=0.12.0` - For faster fuzzy search

Install all optional dependencies:
```bash
pip install indianconstitution[all]
```

---

## 📄 License

This project is licensed under the Apache License 2.0.
See the LICENSE file for more details.

---

## 📧 Contact

**Author**: Vikhram S  
**Email**: [vikhrams@saveetha.ac.in](mailto:vikhrams@saveetha.ac.in)  
**GitHub**: [https://github.com/Vikhram-S/IndianConstitution](https://github.com/Vikhram-S/IndianConstitution)

---

## 🙏 Acknowledgments

The Constitution data is compiled from publicly available resources, ensuring authenticity and accuracy.

---

## Copyright
&copy; 2026 Vikhram S. All rights reserved.
