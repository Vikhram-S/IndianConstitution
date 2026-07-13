from typing import Optional

from .core.engine import Constitution
from .core.models import Article, Part, Schedule

__version__ = "1.2.0"
__all__ = ["Constitution", "Article", "Part", "Schedule", "get_constitution", "get_article", "search"]

# Singleton instance for convenience
_instance = None

def get_constitution() -> Constitution:
    """Get or create a singleton instance of the Constitution."""
    global _instance
    if _instance is None:
        _instance = Constitution()
    return _instance

# Expose common methods at package level for ease of use
def get_article(number: str) -> Optional[Article]:
    """Retrieve an article by number."""
    return get_constitution().get_article(number)

def search(query: str, limit: int = 10):
    """Search for articles by query."""
    return get_constitution().search(query, limit)
