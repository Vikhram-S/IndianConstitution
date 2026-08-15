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

from typing import Dict, List, Optional, Union

from .core.engine import Constitution
from .core.models import AmendmentEvent, Article, CaseLaw, DutyCrossReference, Part, Schedule, SearchResult

__version__ = "1.5.0"
__all__ = [
    "Constitution",
    "Article",
    "Part",
    "Schedule",
    "SearchResult",
    "CaseLaw",
    "AmendmentEvent",
    "DutyCrossReference",
    "get_constitution",
    "get_article",
    "search",
    "get_related_cases",
    "get_amendment_history",
    "diff_amendment",
    "get_related_duties",
    "get_translation",
    "get_translated_preamble",
]

# ── Singleton convenience layer ──────────────────────────────────────────

_instance: Optional[Constitution] = None


def get_constitution() -> Constitution:
    """Get or create a singleton instance of the Constitution."""
    global _instance
    if _instance is None:
        _instance = Constitution()
    return _instance


def get_article(number: Union[int, str]) -> Optional[Article]:
    """Retrieve an article by number (e.g. ``'14'``, ``'21A'``)."""
    return get_constitution().get_article(number)


def search(query: str, limit: int = 10) -> List[Article]:
    """Search for articles by keyword query."""
    return get_constitution().search(query, limit)


def get_related_cases(number: Union[int, str]) -> List[CaseLaw]:
    """Retrieve landmark Supreme Court judgments for an article."""
    return get_constitution().get_related_cases(number)


def get_amendment_history(number: Union[int, str]) -> List[AmendmentEvent]:
    """Retrieve historical amendment events for an article."""
    return get_constitution().get_amendment_history(number)


def diff_amendment(number: Union[int, str], from_year: int = 1950, to_year: int = 2026) -> str:
    """Compute textual diff between amendment states of an article."""
    return get_constitution().diff_amendment(number, from_year, to_year)


def get_related_duties(number: Union[int, str]) -> List[DutyCrossReference]:
    """Cross-reference Part III Fundamental Rights to Part IVA Fundamental Duties."""
    return get_constitution().get_related_duties(number)


def get_translation(number: Union[int, str], lang: str = "hi") -> Optional[Dict[str, str]]:
    """Get translated article title and content."""
    return get_constitution().get_translation(number, lang)


def get_translated_preamble(lang: str = "hi") -> str:
    """Get translated Preamble text."""
    return get_constitution().get_translated_preamble(lang)
