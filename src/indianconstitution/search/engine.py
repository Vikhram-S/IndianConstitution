import re
from collections import defaultdict
from typing import Dict, List, Set

from ..core.models import Article


class SearchEngine:
    """Advanced search engine for the Constitution.
    Implements an inverted index for O(1) keyword lookups.
    """

    def __init__(self, articles: List[Article]):
        self.articles = articles
        self._index: Dict[str, Set[int]] = defaultdict(set)
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """Convert text to lowercase tokens, removing non-alphanumeric chars."""
        # Simple tokenization: lowercase and split by non-word characters
        tokens = re.findall(r"\w+", text.lower())
        # Filter out common stop words if needed, but for legal text we keep most
        return tokens

    def _build_index(self) -> None:
        """Build the inverted index from articles."""
        for i, article in enumerate(self.articles):
            # Index title and content
            text = f"{article.title} {article.content}"
            tokens = self._tokenize(text)
            for token in tokens:
                self._index[token].add(i)

    def keyword_search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles containing ALL tokens in the query."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Find sets of article indices for each token
        sets = [self._index.get(token, set()) for token in query_tokens]

        # Intersection of all sets (AND search)
        if not sets:
            return []

        matching_indices = sets[0]
        for s in sets[1:]:
            matching_indices = matching_indices.intersection(s)

        # Convert indices back to Article objects
        results = [self.articles[i] for i in matching_indices]

        # Sort by article number or some relevance (here just original order)
        return results[:limit]

    def fuzzy_search(self, query: str, limit: int = 10) -> List[Article]:
        """Fuzzy search using basic string matching.
        Note: Could be enhanced with fuzzywuzzy or similar if available.
        """
        # Placeholder for fuzzy logic, currently falls back to keyword if simple
        return self.keyword_search(query, limit)
