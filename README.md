# 🇮🇳 IndianConstitution <small>(v1.1.0)</small>

[![PyPI - Version](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/indianconstitution/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/indianconstitution?logo=python&logoColor=white)](https://pypi.org/project/indianconstitution/)
[![CI Status](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/ci.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions)
[![CodeQL](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codeql.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Vikhram-S/IndianConstitution/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Vikhram-S/IndianConstitution)
[![Snyk Security](https://snyk.io/test/github/Vikhram-S/IndianConstitution/badge.svg)](https://snyk.io/test/github/Vikhram-S/IndianConstitution)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Vikhram-S/IndianConstitution/)
[![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://github.com/Vikhram-S/IndianConstitution/network/updates)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/indianconstitution?logo=pypi&logoColor=white&color=black)](https://pepy.tech/project/indianconstitution)
[![License](https://img.shields.io/pypi/l/indianconstitution?color=red)](https://opensource.org/licenses/Apache-2.0)
[![Donate via UPI](https://img.shields.io/badge/Donate-UPI-orange?logo=google-pay&logoColor=white)](#-donations)

> **The definitive Python library for the Sovereign Democratic Republic.**

`indianconstitution` is a professional-grade, high-performance framework designed for legal professionals, researchers, and developers. It provides structured, programmatic access to the Articles, Parts, and Schedules of the Constitution of India with an elite CLI and AI-ready architecture.

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

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Acknowledgments

- This library uses publicly available data from official sources of the Government of India.
- Special thanks to the open-source community for the tools that made this library possible.

## Contact

- **Author**: Vikhram S
- **Email**: [vikhrams@saveetha.ac.in](mailto:vikhrams@saveetha.ac.in)
- **GitHub**: [https://github.com/Vikhram-S/IndianConstitution](https://github.com/Vikhram-S/IndianConstitution)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Copyright

Copyright (c) 2026 Vikhram S. All rights reserved.

---

## 💰 Donations

If you find this project useful and would like to support its maintenance and development, you can donate via UPI. Your contributions help keep the project alive and free for everyone!

**UPI ID**: `vikhrams15@okhdfcbank` (Google Pay)

<p align="left">
  <img src="https://img.shields.io/badge/UPI-Donate%20Now-orange?style=for-the-badge&logo=google-pay&logoColor=white" alt="UPI Donation">
</p>

*Thank you for your support!* 🇮🇳
