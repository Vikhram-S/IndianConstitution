<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Vikhram-S/IndianConstitution/main/docs/assets/logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Vikhram-S/IndianConstitution/main/docs/assets/logo_light.png">
  <img alt="IndianConstitution Logo" src="https://raw.githubusercontent.com/Vikhram-S/IndianConstitution/main/docs/assets/logo_light.png" width="180">
</picture>

# IndianConstitution

### *A Developer-First, Research-Grade Python Framework for the Constitution of India*

<br>

[![PyPI Version](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=006DAE&style=for-the-badge)](https://pypi.org/project/indianconstitution/)
[![Monthly Downloads](https://img.shields.io/pypi/dm/indianconstitution?logo=pypi&logoColor=white&color=FF6B35&style=for-the-badge)](https://pypi.org/project/indianconstitution/)
[![Total Downloads](https://static.pepy.tech/badge/indianconstitution?style=for-the-badge)](https://pepy.tech/project/indianconstitution)
[![CI Status](https://img.shields.io/github/actions/workflow/status/Vikhram-S/IndianConstitution/ci.yml?branch=main&style=for-the-badge&logo=github&label=CI)](https://github.com/Vikhram-S/IndianConstitution/actions)
[![Coverage](https://img.shields.io/codecov/c/github/Vikhram-S/IndianConstitution?style=for-the-badge&logo=codecov)](https://codecov.io/gh/Vikhram-S/IndianConstitution)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/Vikhram-S/IndianConstitution?label=OpenSSF%20Scorecard&style=for-the-badge)](https://securityscorecards.dev/viewer/?uri=github.com/Vikhram-S/IndianConstitution)

[![License](https://img.shields.io/pypi/l/indianconstitution?color=brightgreen&style=for-the-badge)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/indianconstitution?style=for-the-badge&logo=python)](https://pypi.org/project/indianconstitution/)
[![Mypy](https://img.shields.io/badge/type%20checked-mypy-blue?style=for-the-badge)](http://mypy-lang.org/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Cite](https://img.shields.io/badge/cite-BibTeX-blue?style=for-the-badge)](#-citation)

<br>

> **Sub-millisecond search · Strictly-typed API · Graph analysis · AI/RAG-ready · Zero external dependencies in core**

[📖 **Documentation**](https://vikhram-s.github.io/IndianConstitution/) &nbsp;·&nbsp;
[🚀 **Quick Start**](#-quick-start) &nbsp;·&nbsp;
[🔬 **Research Use**](#-research--academic-use) &nbsp;·&nbsp;
[📊 **Benchmarks**](#-performance-benchmarks) &nbsp;·&nbsp;
[📜 **Cite**](#-citation)

</div>

---

## Abstract

`indianconstitution` is a **production-grade, research-ready Python library** providing programmatic, structured, and type-safe access to the complete text of the Constitution of India — including all 448 articles, 12 schedules, the Preamble, and 106 amendments through the **Constitution (One Hundred and Sixth Amendment) Act, 2023**.

The library implements a **zero-dependency inverted-index search engine** (O(1) token lookup), a **Pydantic v2 data model layer** for type-safe constitutional data access, a **NetworkX-backed relational graph** for cross-article analysis, and a **multi-format export engine** — all designed for deployment in legal AI, retrieval-augmented generation (RAG), civic NLP, and constitutional informatics research.

This package is designed to meet the infrastructure standards expected by NeurIPS, ACL, and EMNLP research workflows — offering reproducibility, strict typing, and offline-first guarantees.

---

## 📑 Table of Contents

- [Key Capabilities](#-key-capabilities)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Data Science Integration](#-data-science-integration)
- [AI / Semantic Search](#-ai--semantic-search)
- [CLI Reference](#️-command-line-interface)
- [Performance Benchmarks](#-performance-benchmarks)
- [Research & Academic Use](#-research--academic-use)
- [Citation](#-citation)
- [Contributing](#-contributing)
- [Security](#️-security)
- [License](#-license)

---

## ✨ Key Capabilities

| Capability | Description | Install Extra |
|:---|:---|:---:|
| **Typed Article API** | Fully annotated `Article`, `Part`, `Schedule`, `Preamble` Pydantic v2 models | *core* |
| **Inverted-Index Search** | Sub-millisecond lexical search via built-in inverted index — O(1) per token | *core* |
| **Graph Analysis** | NetworkX-backed relational graph of constitutional cross-references | `[data]` |
| **Semantic / AI Search** | Sentence-Transformers embeddings for contextual RAG retrieval | `[ai]` |
| **Multi-Format Export** | Export to JSON, CSV, and Markdown with a single call | *core* |
| **pandas Integration** | Direct `DataFrame` output of articles for data science workflows | `[data]` |
| **Rich CLI** | Terminal-native interface powered by Typer + Rich with syntax highlighting | *core* |
| **Fully Offline** | No API keys, no rate limits, no network calls required in core mode | *core* |
| **Type Safety** | 100% mypy strict-mode compliance across all public APIs | *core* |
| **Reproducible** | Deterministic outputs; hermetic data layer pinned to 106th Amendment | *core* |

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Public API Layer                         │
│          get_article()  ·  search()  ·  get_constitution()      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
               ┌────────────────▼────────────────┐
               │    Constitution  (engine.py)     │
               │  Lazy-loading · Singleton cache  │
               └──┬──────────────┬───────────────┘
                  │              │
     ┌────────────▼───┐  ┌───────▼───────────┐  ┌──────────────────┐
     │  SearchEngine  │  │  ConstitutionGraph │  │    Exporter      │
     │ (inverted idx) │  │  (NetworkX graph)  │  │  JSON · CSV · MD │
     └────────────────┘  └────────────────────┘  └──────────────────┘
                  │
     ┌────────────▼──────────────────────────────────┐
     │             Pydantic v2 Data Layer             │
     │   Article · Part · Schedule · Preamble ·       │
     │   ConstitutionData · Amendment                 │
     └───────────────────────────────────────────────┘
                  │
     ┌────────────▼──────────────────────────────────┐
     │      constitution.json  (data/)                │
     │   Authoritative corpus — 106th Amendment 2023  │
     └────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Installation

```bash
# ─── Core installation (zero external dependencies) ───────────────
pip install indianconstitution

# ─── Data science integrations (pandas, NetworkX, SciPy) ──────────
pip install "indianconstitution[data]"

# ─── AI/semantic search (sentence-transformers) ───────────────────
pip install "indianconstitution[ai]"

# ─── Full installation ────────────────────────────────────────────
pip install "indianconstitution[data,ai]"
```

### Programmatic Access

```python
from indianconstitution import get_article, search, get_constitution

# ─── Type-safe Article Retrieval ──────────────────────────────────
article = get_article("21A")
print(f"Article {article.number}: {article.title}")
# → Article 21A: Right to Education
print(f"  Part: {article.part}  |  Amendment: {article.inserted_by}")

# ─── Sub-millisecond Keyword Search ───────────────────────────────
results = search("right to equality", limit=5)
for r in results:
    print(f"  [{r.number}] {r.title} — Part {r.part}")

# ─── Full Constitution Object ──────────────────────────────────────
ic = get_constitution()
print(ic.preamble[:200])
print(f"Total Articles : {len(ic.data.articles)}")
print(f"Total Schedules: {len(ic.data.schedules)}")
```

### Graph Analysis

```python
from indianconstitution import get_constitution

ic = get_constitution()

# ─── Discover cross-article relational structure ──────────────────
related = ic.get_related_articles("32")
print("Article 32 references   :", related["references"])
print("Articles referencing 32 :", related["referenced_by"])

# ─── Compute centrality (which articles are most referenced?) ─────
import networkx as nx
G = ic.get_graph()
centrality = nx.degree_centrality(G)
top_5 = sorted(centrality, key=centrality.get, reverse=True)[:5]
print("Most referenced articles:", top_5)
```

### Data Science Integration

```python
from indianconstitution import get_constitution
import pandas as pd

ic = get_constitution()

# ─── Direct pandas DataFrame ──────────────────────────────────────
df = pd.DataFrame([a.model_dump() for a in ic.data.articles])
print(df[["number", "title", "part"]].head(10))

# ─── Multi-format export ──────────────────────────────────────────
ic.export("json",     "constitution_export.json")
ic.export("csv",      "constitution_export.csv")
ic.export("markdown", "constitution_export.md")
```

### AI / Semantic Search

```python
from indianconstitution import get_constitution

ic = get_constitution()

# ─── Contextual retrieval beyond keyword matching ─────────────────
# Requires: pip install "indianconstitution[ai]"
results = ic.semantic_search(
    "protection against arbitrary state action",
    top_k=5
)
for r in results:
    print(f"[{r.number}] {r.title}  (score: {r.score:.4f})")
```

### RAG Pipeline Integration

```python
from indianconstitution import get_constitution

ic = get_constitution()

def build_rag_context(query: str, top_k: int = 3) -> str:
    """Build a constitutional context block for LLM prompting."""
    results = ic.search(query, limit=top_k)
    context_blocks = []
    for article in results:
        context_blocks.append(
            f"**Article {article.number} — {article.title}**\n"
            f"{article.text}\n"
        )
    return "\n---\n".join(context_blocks)

# Usage with any LLM
context = build_rag_context("right to life and personal liberty")
print(context)
```

---

## 🖥️ Command-Line Interface

```bash
# ─── Retrieve and display an article with syntax highlighting ─────
indianconstitution get 21

# ─── Full-text search across all articles ────────────────────────
indianconstitution search "equality before law"

# ─── Display constitution statistics and metadata ─────────────────
indianconstitution stats

# ─── Export to JSON / CSV / Markdown ────────────────────────────
indianconstitution export --format json     --output constitution.json
indianconstitution export --format csv      --output constitution.csv
indianconstitution export --format markdown --output constitution.md

# ─── Show version ────────────────────────────────────────────────
indianconstitution --version
```

---

## 📊 Performance Benchmarks

Benchmarks measured on a commodity laptop (Intel Core i7-11th Gen, 16 GB RAM, Python 3.11, single thread, averaged over 1,000 iterations).

| Operation | Latency | Notes |
|:---|---:|:---|
| Initial data load | ~45 ms | First call only; lazy-loaded from bundled JSON |
| Subsequent calls | ~0 ms | In-process singleton cache — zero I/O |
| Keyword search (single token) | **< 0.1 ms** | Inverted-index O(1) lookup |
| Keyword search (multi-token, 3) | **< 0.5 ms** | Set intersection over index |
| Full CSV export (all articles) | ~12 ms | Streaming writer |
| Full JSON export | ~8 ms | `orjson`-compatible output |
| Graph construction (NetworkX) | ~30 ms | One-time, lazy; cached thereafter |
| Semantic search (sentence-transformers) | ~80 ms | GPU-accelerated with `[ai]` extra |

> **Reproducibility note:** All benchmarks are fully deterministic. The bundled `constitution.json` corpus is static and version-pinned. No external I/O is required in core mode.

---

## 🔬 Research & Academic Use

`indianconstitution` is engineered for research-grade deployment. It is suitable as a corpus infrastructure layer for:

- **Constitutional NLP** — structured retrieval for legal reasoning models, clause boundary detection
- **RAG pipelines** — grounding LLM outputs with authoritative, citation-traceable constitutional text
- **Civic data science** — network analysis of rights inter-dependencies and amendment history
- **Legal education technology** — interactive constitutional exploration platforms and quiz engines
- **Multilingual legal AI** — Hindi/English constitutional analysis (see `[Unreleased]` roadmap)
- **Comparative constitutional law** — structured data enabling cross-jurisdictional ML studies

### Data Provenance & Corpus Integrity

The constitutional corpus (`constitution.json`) is derived from the **official text of the Constitution of India** as published by the **Ministry of Law and Justice, Government of India**. The data is:

- Curated and validated to the **Constitution (One Hundred and Sixth Amendment) Act, 2023**
- Structured against the Pydantic v2 schema — every field is validated on load
- Versioned alongside the library — data updates are tracked via the `CHANGELOG.md`
- Reproducible — the corpus is deterministic and hermetically bundled in the wheel

### Reproducibility Checklist

For NeurIPS / ACL / EMNLP paper authors using this library:

- [x] Pin to a specific release: `pip install indianconstitution==1.3.0`
- [x] Record the `__version__` in your experiment scripts
- [x] Cite via the BibTeX entry below
- [x] Archive the data corpus via [Zenodo](https://zenodo.org) DOI (see Citation section)

---

## 📜 Citation

If you use `indianconstitution` in academic research, a thesis, or any published work, please cite it as follows:

### BibTeX (Preferred)

```bibtex
@software{vikhram2026indianconstitution,
  author       = {S, Vikhram},
  title        = {{IndianConstitution: A Developer-First, Research-Grade
                   Python Framework for the Constitution of India}},
  year         = {2026},
  version      = {1.3.0},
  publisher    = {PyPI},
  url          = {https://github.com/Vikhram-S/IndianConstitution},
  doi          = {10.5281/zenodo.XXXXXXX},
  note         = {Available on PyPI: \url{https://pypi.org/project/indianconstitution/}
                  Corpus pinned to the Constitution (106th Amendment) Act, 2023.},
  license      = {Apache-2.0},
}
```

### APA 7th Edition

> S, Vikhram. (2026). *IndianConstitution: A Developer-First, Research-Grade Python Framework for the Constitution of India* (Version 1.3.0) [Software]. PyPI. https://doi.org/10.5281/zenodo.XXXXXXX

### IEEE

> V. S, "IndianConstitution: A Developer-First, Research-Grade Python Framework for the Constitution of India," version 1.3.0, 2026. [Online]. Available: https://github.com/Vikhram-S/IndianConstitution. DOI: 10.5281/zenodo.XXXXXXX.

### ACL Anthology Format

```
Vikhram S. 2026. IndianConstitution: A Developer-First, Research-Grade Python Framework 
for the Constitution of India. Software release v1.3.0. 
Available: https://github.com/Vikhram-S/IndianConstitution
```

A machine-readable `CITATION.cff` is provided at the repository root for use with GitHub's **"Cite this repository"** feature and Zenodo DOI minting.

---

## 🛡️ Security

Security vulnerabilities should be reported **privately** via the [GitHub Security Advisory](https://github.com/Vikhram-S/IndianConstitution/security/advisories/new) mechanism. Do **not** open public issues for security reports.

- Supply-chain security: All GitHub Actions are pinned to immutable SHA hashes (OSSF Scorecard compliant)
- Dependency hygiene: Automated Dependabot PRs for all dependency updates
- Static analysis: CodeQL scanning on every push to `main`
- Vulnerability disclosure: See [`SECURITY.md`](SECURITY.md) for the full policy

---

## 🤝 Contributing

We welcome contributions from researchers, legal professionals, and developers. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on:

- Setting up the development environment
- Running the test suite (pytest + Hypothesis property-based testing)
- Code quality standards (Ruff + Mypy strict mode)
- Documentation contributions (MkDocs Material)
- Submitting pull requests and the review process

---

## 🙏 Acknowledgements

This library is developed and maintained by **Vikhram S** at [Saveetha Engineering College](https://www.saveetha.ac.in/), Chennai, India. We gratefully acknowledge:

- The **Ministry of Law and Justice, Government of India** for maintaining the authoritative constitutional text
- The developers of [Pydantic](https://docs.pydantic.dev/), [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [NetworkX](https://networkx.org/), and [sentence-transformers](https://www.sbert.net/) — the foundational libraries that power this framework
- The open-source community for their invaluable feedback and contributions

---

## 📄 License

Copyright © 2026 Vikhram S. Released under the **Apache License 2.0**.

You may use this software freely for academic, commercial, and government purposes with proper attribution. See [`LICENSE`](LICENSE) for the full text.

---

<div align="center">

*Built with ❤️ for the Indian legal tech ecosystem · Engineered to research-grade standards*

[![GitHub Stars](https://img.shields.io/github/stars/Vikhram-S/IndianConstitution?style=social)](https://github.com/Vikhram-S/IndianConstitution)
[![GitHub Forks](https://img.shields.io/github/forks/Vikhram-S/IndianConstitution?style=social)](https://github.com/Vikhram-S/IndianConstitution/fork)
[![Follow](https://img.shields.io/github/followers/Vikhram-S?style=social)](https://github.com/Vikhram-S)

</div>
