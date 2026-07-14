# IndianConstitution

[![PyPI - Version](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/indianconstitution/) [![PyPI Downloads](https://static.pepy.tech/badge/indianconstitution)](https://pepy.tech/project/indianconstitution) [![Monthly Downloads](https://static.pepy.tech/badge/indianconstitution/month)](https://pepy.tech/project/indianconstitution) [![CI](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/ci.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions) [![License](https://img.shields.io/pypi/l/indianconstitution?color=red)](https://opensource.org/licenses/Apache-2.0)

A high-performance, developer-first Python framework for programmatically analyzing, searching, and integrating the Constitution of India into production systems.

`indianconstitution` serves as the foundational legal data infrastructure for AI applications, civic technology, and legal research. Engineered for reliability and scale, it provides a strictly-typed Pythonic API, an advanced local search engine, and seamless data interoperability.

## Core Capabilities

- **Strictly Typed API:** Fully annotated programmatic access to Articles, Parts, Schedules, and the Preamble, designed for integration into robust, type-checked Python applications.
- **High-Performance Search:** Implements a localized inverted index for sub-millisecond lexical search without external dependencies.
- **Semantic & AI-Ready:** Native embeddings integration for semantic search, enabling retrieval-augmented generation (RAG) and legal AI workflows.
- **Data Engineering Integrations:** Native export capabilities to standard analytical formats (CSV, JSON) and direct compatibility with pandas and NetworkX.
- **Zero-Dependency Core:** The base installation is 100% offline, operates with zero rate limits, and requires no external API keys.

## Quick Start

Install the package via standard python tooling:

```bash
# Standard installation
pip install indianconstitution

# Include data science (pandas, networkx) integrations
pip install "indianconstitution[data]"

# Include AI capabilities (sentence-transformers)
pip install "indianconstitution[ai]"
```

### Programmatic Access

```python
from indianconstitution import get_article, search

# Type-hinted article retrieval
article = get_article("21A")
print(f"Article {article.number}: {article.title}")
print(article.content)

# Sub-millisecond localized search
results = search("right to privacy")
for match in results:
    print(f"Article {match.number}: {match.title}")
```

### Semantic Search (AI Integration)

```python
from indianconstitution import Constitution

ic = Constitution()
# Contextual retrieval without strict keyword matching
results = ic.semantic_search("protection against self incrimination")
```

## Command Line Interface (CLI)

The package includes a comprehensive, terminal-native CLI powered by Typer and Rich.

```bash
# Display an article
indianconstitution get 14

# Full-text search
indianconstitution search "equality"

# View repository metrics
indianconstitution stats
```

## Documentation

Comprehensive documentation, API reference, and advanced usage examples can be found at [vikhram-s.github.io/IndianConstitution](https://vikhram-s.github.io/IndianConstitution/).

## Citation & Licensing

If you integrate this library into academic or research workflows, please cite it using the provided `CITATION.cff`.

Licensed under the Apache License 2.0. Copyright (c) 2026 Vikhram S.
