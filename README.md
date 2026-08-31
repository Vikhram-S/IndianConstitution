<div align="center">

# IndianConstitution

### *High-Performance Algorithmic Infrastructure & Deterministic Corpus Engine for the Constitution of India*

[![PyPI](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=006DAE&style=for-the-badge)](https://pypi.org/project/indianconstitution/)
[![Total Downloads](https://img.shields.io/pepy/dt/indianconstitution?style=for-the-badge&color=blue)](https://pepy.tech/project/indianconstitution)
[![CI](https://img.shields.io/github/actions/workflow/status/Vikhram-S/IndianConstitution/ci.yml?branch=main&style=for-the-badge&logo=github&label=CI)](https://github.com/Vikhram-S/IndianConstitution/actions)
[![Codecov](https://img.shields.io/codecov/c/github/Vikhram-S/IndianConstitution?logo=codecov&style=for-the-badge)](https://codecov.io/gh/Vikhram-S/IndianConstitution)
[![License](https://img.shields.io/pypi/l/indianconstitution?color=brightgreen&style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/indianconstitution?style=for-the-badge&logo=python)](https://pypi.org/project/indianconstitution/)
[![Typed](https://img.shields.io/badge/type%20checked-mypy%20strict-blue?style=for-the-badge)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18200429-blue?style=for-the-badge)](https://doi.org/10.5281/zenodo.18200429)

> **CPU-Only Deterministic Execution · Strict Mypy Static Type Safety · Sub-Millisecond Inverted Index Search · Formal Exception Invariants · Zero Remote API Dependencies**

[📖 **Documentation**](https://vikhram-s.github.io/IndianConstitution/) &nbsp;·&nbsp;
[🚀 **Quickstart**](#-quickstart) &nbsp;·&nbsp;
[📐 **System Architecture**](#-system-architecture) &nbsp;·&nbsp;
[📊 **Empirical Performance**](#-empirical-performance) &nbsp;·&nbsp;
[📜 **Citation**](#-citation)

</div>

---

## Executive Summary

`indianconstitution` is a production-grade Python infrastructure package engineered for high-throughput, deterministic algorithmic analysis of the Constitution of India. It provides formalized programmatic representations of all 464 articles, 12 schedules, the Preamble, landmark Supreme Court precedent mappings, amendment timelines, fundamental rights/duties cross-references, and multilingual translations — up to and including the **Constitution (One Hundred and Sixth Amendment) Act, 2023**.

Designed to serve as a foundational corpus infrastructure for legal NLP, Retrieval-Augmented Generation (RAG) pipelines, and civic data science, the engine operates under strict **CPU-only execution guarantees** with zero required network calls or cloud API keys.

---

## ⚡ Algorithmic Complexity & Guarantees

| Operation Component | Algorithm / Invariant | Time Complexity | Space Complexity |
| :--- | :--- | :---: | :---: |
| **Article Lookup** | Hash map lookup by normalized string identifier | $\mathcal{O}(1)$ | $\mathcal{O}(N)$ memory |
| **Keyword Search** | Tokenized inverted posting-list intersection | $\mathcal{O}(K)$ for $K$ tokens | $\mathcal{O}(V + P)$ index size |
| **Fuzzy Matching** | Character ratio matrix calculation | $\mathcal{O}(N \times M)$ | $\mathcal{O}(1)$ dynamic RAM |
| **Relational Graph Construction** | Directed citation adjacency graph assembly | $\mathcal{O}(\vert V \vert + \vert E \vert)$ | $\mathcal{O}(\vert V \vert + \vert E \vert)$ graph space |
| **Amendment Text Delta** | Unified sequence difference computation | $\mathcal{O}(L_1 \times L_2)$ | $\mathcal{O}(L_1 + L_2)$ diff text |
| **Corpus Integrity Verification** | Streaming cryptographic SHA-256 validation | $\mathcal{O}(S)$ for $S$ bytes | $\mathcal{O}(1)$ buffer |

---

## 💻 Hardware Requirements & CPU Constraints

`indianconstitution` strictly enforces **hardware portability and zero-GPU execution dependencies**:

- **Runtime Target**: Runs on commodity x86_64 and ARM64 single-core or multi-core CPU dev machines.
- **Hardware Isolation**: AI and semantic retrieval pipelines (`indianconstitution[ai]`) disable GPU acceleration paths (`CUDA_VISIBLE_DEVICES=""`, `torch.set_num_threads(...)`) to guarantee deterministic offline CPU execution without GPU driver dependencies.
- **Memory Overhead**: Instance heap footprint remains under **15 MB RAM**, enabling microservice, serverless (AWS Lambda, Google Cloud Run), and embedded CLI execution.

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Public API Layer                         │
│   get_article() · search() · fuzzy_search() · get_constitution()│
└───────────────────────────────┬─────────────────────────────────┘
                                │
               ┌────────────────▼────────────────┐
               │    Constitution  (engine.py)     │
               │  Lazy-loading · Singleton cache  │
               └──┬──────────────┬───────────────┘
                  │              │
     ┌────────────▼───┐  ┌───────▼───────────┐  ┌──────────────────┐
     │  SearchEngine  │  │  ConstitutionGraph │  │    Exporter      │
     │ (inverted idx) │  │  (NetworkX graph)  │  │ JSON · CSV · MD  │
     └────────────────┘  └────────────────────┘  └──────────────────┘
                  │              │
     ┌────────────▼──────────────▼──────────────────┐
     │            Pydantic v2 Data Models           │
     │   Article · Part · Schedule · SearchResult   │
     │   CaseLaw · AmendmentEvent · DutyCrossRef    │
     └──────────────────────┬───────────────────────┘
                            │
     ┌──────────────────────▼───────────────────────┐
     │         Custom Typed Exception Hierarchy     │
     │  IndianConstitutionError (BaseException)     │
     │  ├── ArticleNotFoundError                    │
     │  ├── CorpusIntegrityError                    │
     │  ├── InvalidAmendmentRangeError              │
     │  ├── DependencyMissingError                  │
     │  └── UnsupportedFormatError                  │
     └──────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### Installation

```bash
# Core package (zero external runtime dependencies)
pip install indianconstitution

# With network analysis & data science utilities (NetworkX, pandas)
pip install "indianconstitution[data]"

# With offline CPU semantic embeddings (sentence-transformers)
pip install "indianconstitution[ai]"

# Full installation suite
pip install "indianconstitution[all]"
```

### Deterministic Python Usage

```python
>>> from indianconstitution import get_article, search, get_constitution

>>> # Type-safe article retrieval (O(1) lookup)
>>> article = get_article("21A")
>>> article.number
'21A'
>>> article.title
'Right to Education'

>>> # Sub-millisecond inverted posting-list search
>>> results = search("equality before law", limit=3)
>>> [r.number for r in results]
['14', '15']

>>> # Full Constitution engine instance
>>> const = get_constitution()
>>> len(const) > 0
True
```

---

## 🛡️ Formal Exception Invariants

The library enforces fail-fast error reporting through a strict exception hierarchy derived from `IndianConstitutionError`:

```python
from indianconstitution import (
    Constitution,
    ArticleNotFoundError,
    InvalidAmendmentRangeError,
    UnsupportedFormatError,
)

const = Constitution()

# 1. Missing Article Access Guard
try:
    article = const.require_article("99999")
except ArticleNotFoundError as err:
    print(f"Article identifier missing: {err.article_number}")

# 2. Year Bound Invariant Check
try:
    diff = const.diff_amendment("21A", from_year=2026, to_year=2010)
except InvalidAmendmentRangeError as err:
    print(f"Invalid temporal range: {err.from_year} > {err.to_year}")

# 3. Export Specification Enforcement
try:
    const.export("unsupported_fmt", "output.dat")
except UnsupportedFormatError as err:
    print(f"Format rejected: {err.format_requested}")
```

---

## 📊 Empirical Performance

Empirical execution benchmarks gathered via `python scripts/benchmark.py` over 1,000 iterations on a single CPU core:

| Benchmark Target | Samples | p50 Latency | p95 Latency | p99 Latency | Throughput (QPS) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Article Lookup (by num)** | 2,000 | `0.0002 ms` | `0.0003 ms` | `0.0004 ms` | **2,591,680 QPS** |
| **Inverted Index Keyword Search** | 1,000 | `0.0026 ms` | `0.0029 ms` | `0.0058 ms` | **255,180 QPS** |
| **Fuzzy Similarity Search** | 500 | `36.2227 ms` | `38.6790 ms` | `40.8080 ms` | **27.4 QPS** |
| **Graph Relational Traversal** | 1,000 | `0.0014 ms` | `0.0015 ms` | `0.0017 ms` | **653,295 QPS** |
| **Amendment Diff (Art 21A)** | 1,000 | `0.0147 ms` | `0.0158 ms` | `0.0210 ms` | **59,606 QPS** |
| **Graph Reconstruction** | 100 | `46.0691 ms` | `51.9408 ms` | `54.7579 ms` | **21.5 QPS** |

---

## 🛠️ Verification & Quality Assurance Matrix

Every code modification and mathematical claim is verifiable via standard verification targets:

```bash
# 1. Static code quality analysis (Ruff)
ruff check src/indianconstitution

# 2. Code formatting verification (Ruff)
ruff format --check src/indianconstitution

# 3. Strict static type safety analysis (Mypy --strict)
mypy src/indianconstitution

# 4. Property-based & unit test suite (>90% coverage enforcement)
pytest

# 5. SHA-256 data integrity & schema validation
python scripts/validate_corpus.py

# 6. Local CPU empirical benchmark suite
python scripts/benchmark.py
```

---

## 📜 Citation

If you incorporate `indianconstitution` into software systems, research papers, or legal informatics benchmarks, please cite:

```bibtex
@software{vikhram2026indianconstitution,
  author       = {S, Vikhram},
  title        = {{IndianConstitution: High-Performance Algorithmic Infrastructure
                   \& Deterministic Corpus Engine for the Constitution of India}},
  year         = {2026},
  version      = {1.5.1},
  publisher    = {PyPI},
  url          = {https://github.com/Vikhram-S/IndianConstitution},
  doi          = {10.5281/zenodo.18200429},
  license      = {Apache-2.0},
}
```

---

## 📄 License

Copyright © 2026 Vikhram S. Distributed under the terms of the **Apache License 2.0**. See [`LICENSE`](LICENSE).
