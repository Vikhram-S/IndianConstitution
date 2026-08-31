"""Cross-reference graph for the Constitution of India.

Builds a directed graph of inter-article references using NetworkX. Provides
centrality analysis, reference lookup, and graph export functionality.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..exceptions import DependencyMissingError
from .models import Article

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False


class ConstitutionGraph:
    """Analyzes and manages directed relationships between Articles.

    Attributes:
        articles: List of Article objects.
    """

    def __init__(self, articles: List[Article]) -> None:
        """Initialize ConstitutionGraph and build networkx graph if available."""
        self.articles = articles
        self._graph: Optional[Any] = None
        if NETWORKX_AVAILABLE:
            self._graph = nx.DiGraph()
            self._build_graph()

    def _extract_references(self, text: str) -> Set[str]:
        """Extract article numbers mentioned in text."""
        lowered = text.lower()
        pattern = r"article\s+(\d+[a-z]?)"
        matches = re.findall(pattern, lowered)
        return {m.upper() for m in matches}

    def _build_graph(self) -> None:
        """Build directed graph of article references."""
        article_numbers = {str(a.number) for a in self.articles}

        for article in self.articles:
            u = str(article.number)
            if self._graph is not None:
                self._graph.add_node(u, title=article.title)

            references = self._extract_references(article.content)
            for v in references:
                if v in article_numbers and v != u and self._graph is not None:
                    self._graph.add_edge(u, v)

    @property
    def graph(self) -> Any:  # noqa: ANN401
        """Return the underlying networkx.DiGraph instance."""
        return self._graph

    def get_references(self, number: str) -> List[str]:
        """Get list of article numbers that the given article references."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        if number not in self._graph:
            return []
        return sorted(list(self._graph.successors(number)))

    def get_referenced_by(self, number: str) -> List[str]:
        """Get list of article numbers that reference the given article."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        if number not in self._graph:
            return []
        return sorted(list(self._graph.predecessors(number)))

    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Identify central articles using PageRank scores."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        pagerank: Dict[str, float] = nx.pagerank(self._graph)
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:limit]

    def get_degree_centrality(self) -> Dict[str, float]:
        """Return degree centrality for every node in the graph."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return {}
        result: Dict[str, float] = nx.degree_centrality(self._graph)
        return result

    def get_communities(self) -> List[Set[str]]:
        """Detect communities using greedy modularity on undirected projection."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            return []
        from networkx.algorithms.community import greedy_modularity_communities

        undirected = self._graph.to_undirected()
        communities = greedy_modularity_communities(undirected)
        return [set(c) for c in communities]

    def export_gexf(self, path: Union[str, Path]) -> None:
        """Export cross-reference graph to GEXF format."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            raise DependencyMissingError("GEXF export", "data")
        nx.write_gexf(self._graph, str(path))

    def export_graphml(self, path: Union[str, Path]) -> None:
        """Export cross-reference graph to GraphML format."""
        if not NETWORKX_AVAILABLE or self._graph is None:
            raise DependencyMissingError("GraphML export", "data")
        nx.write_graphml(self._graph, str(path))
