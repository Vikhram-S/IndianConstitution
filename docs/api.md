# API Reference

Complete documentation of the `indianconstitution` public API.

## Module Exports (`indianconstitution`)

### `get_constitution() -> Constitution`
Returns the global singleton instance of the `Constitution` engine.

### `get_article(number: str) -> Optional[Article]`
Retrieves an `Article` object by number (e.g., `'14'`, `'21A'`). Returns `None` if not found.

### `search(query: str, limit: int = 10) -> List[Article]`
Performs inverted-index keyword search across all article titles and text.

---

## Core Classes

### `Constitution`

```python
class Constitution:
    def get_article(self, number: Union[int, str]) -> Optional[Article]: ...
    def search(self, query: str, limit: int = 10) -> List[Article]: ...
    def get_graph(self) -> networkx.DiGraph: ...
    def get_related_articles(self, number: str) -> Dict[str, List[str]]: ...
    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]: ...
    def semantic_search(self, query: str, top_k: int = 5) -> List[SearchResult]: ...
    def export(self, format: str, path: Union[str, Path]) -> None: ...
    def to_dataframe(self) -> pandas.DataFrame: ...
```

### `Article`

Pydantic v2 data model representing a single article.

- `number: str` - Article number string (e.g., `'21A'`)
- `title: str` - Title of the article
- `content: str` - Full text of the article
- `text: str` - Property alias for `content`
- `part: Optional[int]` - Inferred Part number (1–22)
- `chapter: Optional[int]` - Chapter number within Part

### `SearchResult`

Inherits fields from `Article` and adds relevance score:

- `score: float` - Similarity score (0.0 to 1.0)
