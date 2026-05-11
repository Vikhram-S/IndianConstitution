# 🇮🇳 IndianConstitution <small>(v1.1.0)</small>

[![PyPI - Version](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/indianconstitution/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/indianconstitution?logo=python&logoColor=white)](https://pypi.org/project/indianconstitution/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/indianconstitution?logo=pypi&logoColor=white&color=black)](https://pepy.tech/project/indianconstitution)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue?logo=github&logoColor=white)](https://vikhram-s.github.io/IndianConstitution/)
[![License](https://img.shields.io/pypi/l/indianconstitution?color=red)](https://opensource.org/licenses/Apache-2.0)

> **The definitive Python library for the Sovereign Democratic Republic.**

`indianconstitution` is a professional, high-performance Python library designed for legal researchers, data scientists, and developers. It provides structured, programmatic access to the Articles, Parts, and Schedules of the Constitution of India.

---

## Features

- **Pythonic API**: Intuitive, type-hinted, and chainable access to all articles.
- **High Performance**: Inverted index for lightning-fast keyword search and lazy loading.
- **World-Class CLI**: Beautiful terminal interface powered by `Typer` and `Rich`.
- **Advanced Search**: Keyword, fuzzy, and (optional) semantic search capabilities.
- **Data Science Ready**: Export to JSON, CSV, and Pandas DataFrames.
- **Smart Caching**: Local disk caching for heavy operations.

---

## Quickstart in 30 Seconds

### Installation

```bash
pip install indianconstitution
```

### Basic Usage

```python
import indianconstitution as ic

# Get a specific article
article = ic.get_article(14)
print(f"{article.title}: {article.content}")

# Search across the entire constitution
results = ic.search("freedom of speech")
for a in results:
    print(f"Article {a.number}: {a.title}")
```

---

## CLI Interface

The library comes with a powerful command-line interface.

```bash
# Get an article
indianconstitution get 21A

# Search for keywords
indianconstitution search "equality"

# View the Preamble
indianconstitution preamble

# Show statistics
indianconstitution stats
```

---

## Advanced Features

### Semantic Search (AI-Powered)
Find articles by meaning, not just keywords.
```bash
pip install "indianconstitution[ai]"
```
```python
from indianconstitution import Constitution
ic = Constitution()
results = ic.semantic_search("rights of minority educational institutions")
```

### Pandas Integration
```python
import pandas as pd
df = pd.DataFrame([a.dict() for a in ic.data.articles])
```

---

## Why this library exists?

The Constitution of India is one of the longest written constitutions in the world. Accessing it programmatically should be as elegant as the document itself. This library aims to bridge the gap between legal text and modern development workflows, enabling better research, education, and civic-tech applications.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](contributing.md) for details.

## Acknowledgments

- This library uses publicly available data from official sources of the Government of India.
- Special thanks to the open-source community for the tools that made this library possible.

## Contact

- **Author**: Vikhram S
- **Email**: [vikhrams@saveetha.ac.in](mailto:vikhrams@saveetha.ac.in)
- **GitHub**: [https://github.com/Vikhram-S/IndianConstitution](https://github.com/Vikhram-S/IndianConstitution)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](license.md) file for details.

## Copyright

Copyright (c) 2026 Vikhram S. All rights reserved.
