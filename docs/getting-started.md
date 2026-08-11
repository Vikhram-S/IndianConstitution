# Getting Started

This guide covers setup and fundamental concepts of the `indianconstitution` library.

## Requirements

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- **Dependencies**: `pydantic >= 2.0`, `typer >= 0.9`, `rich >= 13.0`

## Installation Options

### 1. Core Package
Minimal installation with zero external data-science heavy dependencies:
```bash
pip install indianconstitution
```

### 2. Data Science Extra
Includes `pandas`, `networkx`, and `scipy` for graph analysis and tabular workflows:
```bash
pip install "indianconstitution[data]"
```

### 3. AI / Semantic Search Extra
Includes `sentence-transformers` and `torch` for vector embeddings:
```bash
pip install "indianconstitution[ai]"
```

## Basic Operations

### Accessing Articles

```python
from indianconstitution import get_article, get_constitution

# Fetch single article
art = get_article("14")
print(art.title)    # Equality before law
print(art.content)  # Full article text
print(art.part)     # 3 (Part III - Fundamental Rights)

# Access full Constitution instance
ic = get_constitution()
print(f"Total articles loaded: {len(ic)}")
print(f"Preamble: {ic.preamble[:150]}...")
```

### Keyword Search

```python
from indianconstitution import search

# Sub-millisecond inverted-index search
matches = search("freedom of speech", limit=5)
for m in matches:
    print(f"Art. {m.number}: {m.title}")
```

### Multi-Format Data Export

```python
from indianconstitution import get_constitution

ic = get_constitution()
ic.export("json", "constitution.json")
ic.export("csv", "constitution.csv")
ic.export("markdown", "constitution.md")
```
