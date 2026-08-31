"""IndianConstitution: Programmatic access to the Constitution of India.

Provides structured access to articles, preamble, schedules, case law,
amendment history, fundamental duties, cross-reference graphs, and search engines.
"""

from typing import Dict, List, Optional, Union

from .core.engine import Constitution
from .core.models import (
    AmendmentEvent,
    Article,
    CaseLaw,
    ConstitutionData,
    DutyCrossReference,
    Part,
    Schedule,
    SearchResult,
)
from .exceptions import (
    ArticleNotFoundError,
    CorpusIntegrityError,
    DependencyMissingError,
    IndianConstitutionError,
    InvalidAmendmentRangeError,
    UnsupportedFormatError,
)

__version__ = "1.5.2"
__author__ = "Vikhram S"
__email__ = "vikhrams@saveetha.ac.in"

_default_instance: Optional[Constitution] = None


def get_constitution() -> Constitution:
    """Get singleton instance of Constitution engine.

    Returns:
        Constitution instance.

    Examples:
        >>> const = get_constitution()
        >>> len(const) > 0
        True
    """
    global _default_instance
    if _default_instance is None:
        _default_instance = Constitution()
    return _default_instance


def get_article(number: Union[int, str]) -> Optional[Article]:
    """Retrieve an article by number (e.g. 14, '21A').

    Args:
        number: Article identifier.

    Returns:
        Article instance if found, None otherwise.
    """
    return get_constitution().get_article(number)


def search(query: str, limit: int = 10) -> List[Article]:
    """Search articles matching keyword query.

    Args:
        query: Search term or phrase.
        limit: Maximum number of articles to return.

    Returns:
        List of matching Article instances.
    """
    return get_constitution().search(query, limit=limit)


def fuzzy_search(query: str, limit: int = 10, min_score: float = 0.3) -> List[SearchResult]:
    """Fuzzy search articles matching query.

    Args:
        query: Search query string.
        limit: Maximum number of results.
        min_score: Similarity score threshold.

    Returns:
        List of SearchResult objects with scores.
    """
    return get_constitution().fuzzy_search(query, limit=limit, min_score=min_score)


def get_related_cases(number: Union[int, str]) -> List[CaseLaw]:
    """Retrieve landmark Supreme Court judgments linked to an article."""
    return get_constitution().get_related_cases(number)


def get_amendment_history(number: Union[int, str]) -> List[AmendmentEvent]:
    """Retrieve historical amendment events for an article."""
    return get_constitution().get_amendment_history(number)


def diff_amendment(number: Union[int, str], from_year: int = 1950, to_year: int = 2026) -> str:
    """Compute textual diff between specified amendment years."""
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


__all__ = [
    "Constitution",
    "Article",
    "Part",
    "Schedule",
    "ConstitutionData",
    "SearchResult",
    "CaseLaw",
    "AmendmentEvent",
    "DutyCrossReference",
    "IndianConstitutionError",
    "ArticleNotFoundError",
    "CorpusIntegrityError",
    "InvalidAmendmentRangeError",
    "DependencyMissingError",
    "UnsupportedFormatError",
    "get_constitution",
    "get_article",
    "search",
    "fuzzy_search",
    "get_related_cases",
    "get_amendment_history",
    "diff_amendment",
    "get_related_duties",
    "get_translation",
    "get_translated_preamble",
    "__version__",
    "__author__",
    "__email__",
]
