"""IndianConstitution — A research-grade Python framework for the Constitution of India.

Quick start::

    from indianconstitution import get_article, search, get_constitution

    article = get_article("21A")
    print(article.title)  # → Right to Education

    results = search("right to equality", limit=5)
    for r in results:
        print(f"[{r.number}] {r.title}")

    ic = get_constitution()
    print(ic.preamble[:200])
"""

from typing import List, Optional

from .core.engine import Constitution
from .core.models import Article, Part, Schedule, SearchResult

__version__ = "1.4.0"
__all__ = [
    "Constitution",
    "Article",
    "Part",
    "Schedule",
    "SearchResult",
    "get_constitution",
    "get_article",
    "search",
]

# ── Singleton convenience layer ──────────────────────────────────────────

_instance: Optional[Constitution] = None


def get_constitution() -> Constitution:
    """Get or create a singleton instance of the Constitution."""
    global _instance
    if _instance is None:
        _instance = Constitution()
    return _instance


def get_article(number: str) -> Optional[Article]:
    """Retrieve an article by number (e.g. ``'14'``, ``'21A'``)."""
    return get_constitution().get_article(number)


def search(query: str, limit: int = 10) -> List[Article]:
    """Search for articles by keyword query."""
    return get_constitution().search(query, limit)
