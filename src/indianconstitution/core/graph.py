"""Cross-reference graph for the Constitution of India.

Builds a directed graph of inter-article references using NetworkX (optional
dependency). Provides centrality analysis, reference lookup, and direct
access to the underlying ``networkx.DiGraph``.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import Article

try:
    import networkx as nx  # type: ignore[import-untyped]

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False


class ConstitutionGraph:
    """Analyzes and manages relationships between Articles.

    Maps how articles reference each other (e.g., Article 32 references Article 13).
    """

    def __init__(self, articles: List[Article]) -> None:
        self.articles = articles
        self._graph: Any = None
        if NETWORKX_AVAILABLE:
            self._graph = nx.DiGraph()
            self._build_graph()

    def _extract_references(self, text: str) -> Set[str]:
        """Extract article numbers mentioned in the text.

        Handles patterns like "article 14", "Article 21A",
        "articles 14 and 15", "Article 368", etc.
        """
        lowered = text.lower()
        # Match "article <number>" with optional letter suffix (e.g. 21a)
        pattern = r"article\s+(\d+[a-z]?)"
        matches = re.findall(pattern, lowered)
        # Normalise to uppercase suffix: "21a" → "21A", "14" → "14"
        return {m.upper() for m in matches}

    def _build_graph(self) -> None:
        """Build a directed graph of article references."""
        article_numbers = {str(a.number) for a in self.articles}

        for article in self.articles:
            u = str(article.number)
            if self._graph is not None:
                self._graph.add_node(u, title=article.title)

            references = self._extract_references(article.content)
            for v in references:
                if v in article_numbers and v != u:
                    if self._graph is not None:
                        self._graph.add_edge(u, v)

    # ── Public API ───────────────────────────────────────────────────────

    @property
    def graph(self) -> Any:
        """Return the underlying ``networkx.DiGraph`` (or ``None``)."""
        return self._graph

    def get_references(self, number: str) -> List[str]:
        """Get list of articles that the given article references."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        if number not in self._graph:
            return []
        return sorted(self._graph.successors(number))

    def get_referenced_by(self, number: str) -> List[str]:
        """Get list of articles that reference the given article."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        if number not in self._graph:
            return []
        return sorted(self._graph.predecessors(number))

    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Identify 'central' articles using PageRank (most referenced)."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        pagerank: Dict[str, float] = nx.pagerank(self._graph)
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:limit]

    def get_degree_centrality(self) -> Dict[str, float]:
        """Return degree centrality for every node in the graph."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return {}
        return nx.degree_centrality(self._graph)  # type: ignore[no-any-return]

    def get_communities(self) -> List[Set[str]]:
        """Detect communities using greedy modularity (undirected projection)."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        from networkx.algorithms.community import greedy_modularity_communities

        undirected = self._graph.to_undirected()
        return [set(c) for c in greedy_modularity_communities(undirected)]
