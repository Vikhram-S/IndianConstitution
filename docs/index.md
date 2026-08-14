# IndianConstitution

<div align="center">

## *A Developer-First, Research-Grade Python Framework for the Constitution of India*

</div>

`indianconstitution` is a production-grade Python library providing programmatic, structured, and type-safe access to the complete text of the Constitution of India — including all 448 articles, 12 schedules, the Preamble, and amendments through the **Constitution (106th Amendment) Act, 2023**.

## Key Capabilities

- **Typed Article API**: Fully annotated Pydantic v2 data models (`Article`, `Part`, `Schedule`, `SearchResult`).
- **Inverted-Index Search**: Sub-millisecond lexical search via built-in inverted index ($O(1)$ token lookup).
- **Graph Analysis**: NetworkX-backed relational graph mapping inter-article cross-references.
- **Semantic / AI Search**: Sentence-Transformers embeddings for contextual retrieval and RAG pipelines.
- **Multi-Format Export**: Single-call export to JSON, CSV, and Markdown.
- **pandas Integration**: Direct `DataFrame` generation for data science workflows.
- **Rich CLI**: Terminal interface with syntax highlighting and interactive exploration.

## Quick Installation

```bash
# Core framework
pip install indianconstitution

# With data science integrations (pandas, NetworkX)
pip install "indianconstitution[data]"

# With AI & semantic search (sentence-transformers)
pip install "indianconstitution[ai]"

# Full installation
pip install "indianconstitution[data,ai]"
```

## Quick Example

```python
from indianconstitution import get_article, search, get_constitution

# Retrieve by article number
article = get_article("21A")
print(f"Article {article.number}: {article.title}")
# -> Article 21A: Right to Education

# Inverted-index search
results = search("equality before law", limit=5)
for r in results:
    print(f"[{r.number}] {r.title}")

# Graph analysis
ic = get_constitution()
related = ic.get_related_articles("32")
print("Articles referencing Article 32:", related["referenced_by"])
```
