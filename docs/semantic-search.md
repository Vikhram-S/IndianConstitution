# Semantic & AI Search

Semantic search empowers contextual retrieval beyond exact keyword matching, making it ideal for legal AI and RAG applications.

## Requirements

```bash
pip install "indianconstitution[ai]"
```

## Usage

```python
from indianconstitution import get_constitution

ic = get_constitution()

# Natural-language query
results = ic.semantic_search(
    "protection against arbitrary state action",
    top_k=5
)

for r in results:
    print(f"Article {r.number}: {r.title} (score: {r.score:.4f})")
```

## RAG Integration Example

```python
def build_rag_context(query: str) -> str:
    results = ic.semantic_search(query, top_k=3)
    return "\n---\n".join([f"**Article {r.number}**: {r.text}" for r in results])
```
