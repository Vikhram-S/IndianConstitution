# Keyword Search Engine

`indianconstitution` includes a custom **inverted-index search engine** built directly into the core library without external dependencies.

## Key Features

- **Sub-millisecond Latency**: $O(1)$ token lookup speed.
- **AND Logic**: Multi-token queries return articles containing all query terms.
- **Zero Dependencies**: Pure Python dictionary and set operations.

## Usage

```python
from indianconstitution import search

# Single keyword
results = search("untouchability")

# Phrase / multi-token search
results = search("fundamental rights equality", limit=5)
for art in results:
    print(f"[{art.number}] {art.title}")
```
