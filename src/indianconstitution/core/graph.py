import re
from typing import List, Set, Tuple

from .models import Article

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False


class ConstitutionGraph:
    """Analyzes and manages relationships between Articles.
    Maps how articles reference each other (e.g., Article 32 references Article 13).
    """

    def __init__(self, articles: List[Article]):
        self.articles = articles
        self.graph = nx.DiGraph() if NETWORKX_AVAILABLE else None
        if NETWORKX_AVAILABLE:
            self._build_graph()

    def _extract_references(self, text: str) -> Set[str]:
        """Extract article numbers mentioned in the text."""
        # Look for patterns like "article 14", "articles 14 and 15", etc.
        pattern = r"article\s+([0-9]+[A-Z]?)"
        matches = re.findall(pattern, text.lower())
        return {m.upper() for m in matches}

    def _build_graph(self) -> None:
        """Build a directed graph of article references."""
        article_numbers = {str(a.number) for a in self.articles}

        for article in self.articles:
            u = str(article.number)
            if self.graph is not None:
                self.graph.add_node(u, title=article.title)

            references = self._extract_references(article.content)
            for v in references:
                if v in article_numbers and v != u:
                    if self.graph is not None:
                        self.graph.add_edge(u, v)

    def get_references(self, number: str) -> List[str]:
        """Get list of articles that the given article references."""
        if not NETWORKX_AVAILABLE or self.graph is None:
            return []
        if number not in self.graph:
            return []
        return list(self.graph.successors(number))

    def get_referenced_by(self, number: str) -> List[str]:
        """Get list of articles that reference the given article."""
        if not NETWORKX_AVAILABLE or self.graph is None:
            return []
        if number not in self.graph:
            return []
        return list(self.graph.predecessors(number))

    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Identify 'central' articles using PageRank (most referenced)."""
        if not NETWORKX_AVAILABLE or self.graph is None:
            return []
        pagerank = nx.pagerank(self.graph)
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:limit]
