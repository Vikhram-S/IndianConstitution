"""Inverted-index keyword search engine and string similarity search for Constitution articles.

Provides deterministic O(1) keyword lookups via inverted indexing and
fuzzy sequence matching using Python standard library difflib.
"""

import difflib
import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from ..core.models import Article, SearchResult


class SearchEngine:
    """Inverted index search engine with keyword and fuzzy matching capabilities.

    Attributes:
        articles: List of Article objects indexed by the engine.
    """

    def __init__(self, articles: List[Article]) -> None:
        """Initialize SearchEngine and build inverted index.

        Args:
            articles: List of Article objects to index.
        """
        self.articles: List[Article] = articles
        self._index: Dict[str, Set[int]] = defaultdict(set)
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """Convert text into lowercase alphanumeric tokens.

        Args:
            text: Input text string.

        Returns:
            List of normalized token strings.
        """
        return re.findall(r"\w+", text.lower())

    def _build_index(self) -> None:
        """Build the internal inverted index mapping tokens to article list indices."""
        for i, article in enumerate(self.articles):
            text = f"{article.title} {article.content}"
            tokens = self._tokenize(text)
            for token in tokens:
                self._index[token].add(i)

    def keyword_search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles containing ALL tokens in the query (AND search).

        Args:
            query: The search term or phrase.
            limit: Maximum number of articles to return.

        Returns:
            List of matching Article objects up to the specified limit.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        token_sets = [self._index.get(token, set()) for token in query_tokens]
        if not token_sets:
            return []

        matching_indices = token_sets[0].copy()
        for s in token_sets[1:]:
            matching_indices.intersection_update(s)

        results = [self.articles[i] for i in sorted(matching_indices)]
        return results[:limit]

    def fuzzy_search(self, query: str, limit: int = 10, min_score: float = 0.3) -> List[SearchResult]:
        """Perform fuzzy similarity search across article titles and contents.

        Uses standard library difflib.SequenceMatcher to compute similarity scores.

        Args:
            query: The search query string.
            limit: Maximum number of results to return.
            min_score: Minimum similarity score threshold (0.0 to 1.0).

        Returns:
            List of SearchResult objects containing matching articles and similarity scores.
        """
        query_trimmed = query.strip().lower()
        if not query_trimmed:
            return []

        scored_articles: List[Tuple[Article, float]] = []

        for article in self.articles:
            title_score = difflib.SequenceMatcher(None, query_trimmed, article.title.lower()).ratio()
            content_snippet = article.content[:300].lower()
            content_score = difflib.SequenceMatcher(None, query_trimmed, content_snippet).ratio()
            combined_score = max(title_score * 1.2, content_score)
            if combined_score >= min_score:
                scored_articles.append((article, float(min(1.0, combined_score))))

        scored_articles.sort(key=lambda x: x[1], reverse=True)
        return [SearchResult.from_article(art, score=score) for art, score in scored_articles[:limit]]
