# IndianConstitution

A concise, high-performance Python toolkit for the Constitution of India.

`indianconstitution` is the definitive open-source Python library for accessing, searching, analyzing, and integrating the Constitution of India into software, legal research, AI systems, educational tools, and civic technology. Built with a focus on developer experience, it provides a pythonic API, an elegant CLI, advanced search capabilities (including semantic search), and robust data export features.

**Why use `indianconstitution`?**
*   **Intuitive API**: Chainable, type-hinted access to Articles, Parts, Schedules, and the Preamble.
*   **High Performance**: Uses an inverted index for sub-millisecond keyword searches.
*   **AI & Data Science Ready**: Native semantic search integration and seamless pandas DataFrame export.
*   **Professional CLI**: A beautiful, terminal-native experience powered by Typer and Rich.
*   **Fully Offline**: No API keys, no rate limits, and 100% local operation.

---

## Project Status

| Metric | Status |
| :--- | :--- |
| **PyPI** | [![PyPI - Version](https://img.shields.io/pypi/v/indianconstitution?logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/indianconstitution/) [![PyPI Downloads](https://static.pepy.tech/badge/indianconstitution)](https://pepy.tech/project/indianconstitution) [![Monthly Downloads](https://static.pepy.tech/badge/indianconstitution/month)](https://pepy.tech/project/indianconstitution) |
| **Environment** | [![Python Versions](https://img.shields.io/pypi/pyversions/indianconstitution?logo=python&logoColor=white)](https://pypi.org/project/indianconstitution/) [![License](https://img.shields.io/pypi/l/indianconstitution?color=red)](https://opensource.org/licenses/Apache-2.0) |
| **Quality** | [![CI](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/ci.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions) [![Codacy](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codacy.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codacy.yml) [![Typing](https://img.shields.io/badge/typing-PEP%20561-blue?logo=python)](https://peps.python.org/pep-0561/) [![Ruff](https://img.shields.io/badge/lint-ruff-black?logo=ruff)](https://github.com/astral-sh/ruff) |
| **Security** | [![CodeQL](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codeql.yml/badge.svg)](https://github.com/Vikhram-S/IndianConstitution/actions/workflows/codeql.yml) [![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Vikhram-S/IndianConstitution/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Vikhram-S/IndianConstitution) |
| **Support** | [![Donate via UPI](https://img.shields.io/badge/Donate-UPI-orange?logo=google-pay&logoColor=white)](#support-the-project) |

---

## Features Matrix

| Capability | Supported |
| :--- | :---: |
| Articles, Parts & Schedules | ✅ |
| Preamble Access | ✅ |
| CLI Interface | ✅ |
| Fast Keyword Search | ✅ |
| Semantic Search (AI) | ✅ |
| CSV & JSON Export | ✅ |
| Pandas Integration | ✅ |
| Full Type Hints | ✅ |
| Local Disk Caching | ✅ |

---

## Visual Previews

### CLI Preview
![CLI Preview](docs/images/cli_preview.png)
*A look at the interactive terminal interface.*

### Python Example
![Python Example](docs/images/python_example.png)
*Pythonic API usage with type hints.*

### Keyword Search
![Search Example](docs/images/search_example.png)
*Blazing-fast inverted index search.*

### Semantic Search
![Semantic Search](docs/images/semantic_search.png)
*Context-aware search for legal concepts without exact keyword matches.*

---

## Quick Start

### Installation

```bash
# Standard installation
pip install indianconstitution

# With Data Science capabilities (pandas)
pip install "indianconstitution[data]"

# With AI/Semantic Search capabilities
pip install "indianconstitution[ai]"
```

### Basic Usage

```python
from indianconstitution import get_constitution, get_article

# Load the entire constitution
ic = get_constitution()
print(f"Preamble: {ic.preamble}")

# Get a specific article
article_21a = get_article("21A")
print(f"Article {article_21a.number}: {article_21a.title}")
print(article_21a.content)
```

### Searching

```python
from indianconstitution import search

# Fast keyword search
results = search("freedom of speech")
for article in results:
    print(f"Article {article.number}: {article.title}")
```

### Semantic Search (AI)

```python
from indianconstitution import Constitution

ic = Constitution()
# Find articles conceptually related to "protection of children"
results = ic.semantic_search("safeguarding minors and young people")
for article in results:
    print(f"Article {article.number}: {article.title}")
```

### Exporting Data

```python
from indianconstitution import get_constitution

ic = get_constitution()
ic.export(format="json", path="constitution.json")
ic.export(format="csv", path="constitution.csv")
```

### Command Line Interface

```bash
# View an article
indianconstitution get 14

# Search the text
indianconstitution search "equality"

# View the preamble
indianconstitution preamble

# Show dataset statistics
indianconstitution stats
```

---

## Real-world Use Cases

*   **Legal Research**: Quickly retrieve interrelated articles and build graphs of references.
*   **Constitutional Law**: Compare semantic nuances and analyze terminology distribution.
*   **Universities & Education**: Integrate interactive CLI tools into political science curriculums.
*   **AI Agents & LLMs**: Provide a clean, structured corpus for grounding agentic applications.
*   **RAG (Retrieval-Augmented Generation)**: High-quality indexed embeddings for custom legal chatbots.
*   **Civic Tech**: Build open-source dashboards and apps for citizen awareness.
*   **Data Analysis**: Export directly to Pandas and NetworkX to study structural complexity.

---

## Documentation

Full documentation is available at [https://vikhram-s.github.io/IndianConstitution/](https://vikhram-s.github.io/IndianConstitution/).

*   [Getting Started](docs/getting-started.md)
*   [CLI Guide](docs/cli.md)
*   [API Reference](docs/api.md)
*   [Search](docs/search.md)
*   [Semantic Search](docs/semantic-search.md)
*   [Examples](docs/examples.md)
*   [FAQ](docs/faq.md)
*   [Contributing](docs/contributing.md)

---

## Citation

If you use this software in your research or project, please cite it using the accompanying `CITATION.cff` file.

**APA Format:**
> S, V. (2026). IndianConstitution (Version 1.2.0) [Computer software]. https://github.com/Vikhram-S/IndianConstitution

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on setting up your environment, running tests, and submitting PRs.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Copyright

Copyright (c) 2026 Vikhram S. All rights reserved.

---

## Support the Project

If this project provides value to you or your organization, consider supporting its continued development and maintenance.

Support helps fund:
*   ongoing package maintenance and improvements
*   new features, datasets, and documentation
*   infrastructure, testing, and release automation
*   long-term open-source sustainability

### Support via UPI (Unified Payments Interface)

**UPI ID:** `vikhrams15@okhdfcbank`

<p align="left">
  <a href="upi://pay?pa=vikhrams15@okhdfcbank&pn=Vikhram%20S&cu=INR">
    <img src="https://img.shields.io/badge/Support%20Development-UPI-orange?style=for-the-badge&logo=google-pay&logoColor=white" alt="Support via UPI">
  </a>
</p>

Contributions, feature requests, issue reports, documentation improvements, and GitHub stars are also appreciated.
