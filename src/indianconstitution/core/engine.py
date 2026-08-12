"""Constitution engine — the single entry-point for all library features.

Provides lazy-loaded, singleton-cached access to:
- Article retrieval (``get_article``)
- Full-text keyword search (``search``)
- Cross-reference graph analysis (``get_graph``, ``get_related_articles``, ``get_central_articles``)
- Semantic / AI search (``semantic_search``) — requires ``[ai]`` extra
- Multi-format export (``export``)
- Direct DataFrame creation (``to_dataframe``) — requires ``[data]`` extra
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..export.engine import Exporter
from ..search.engine import SearchEngine
from .graph import ConstitutionGraph
from .models import Article, ConstitutionData, SearchResult

DATA_PATH = Path(__file__).parent.parent / "data" / "constitution.json"


class Constitution:
    """Main entry point for accessing the Constitution of India.

    Uses lazy loading and caching for optimal performance.

    Example::

        from indianconstitution import get_constitution
        ic = get_constitution()
        article = ic.get_article("21A")
        print(article.title)
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        self._data_path = data_path or DATA_PATH
        self._data: Optional[ConstitutionData] = None
        self._article_map: Dict[str, Article] = {}
        self._search_engine: Optional[SearchEngine] = None
        self._exporter: Optional[Exporter] = None
        self._graph_obj: Optional[ConstitutionGraph] = None
        self._semantic_model: Any = None
        self._semantic_embeddings: Any = None

    # ── Data loading ─────────────────────────────────────────────────────

    @property
    def data(self) -> ConstitutionData:
        """Lazy load the constitution data."""
        if self._data is None:
            self._load_data()
        assert self._data is not None
        return self._data

    def _load_data(self) -> None:
        """Internal method to load and parse JSON data."""
        if not self._data_path.exists():
            raise FileNotFoundError(f"Constitution data not found at {self._data_path}")

        with open(self._data_path, encoding="utf-8") as f:
            raw_data = json.load(f)

        # Handle the legacy flat list format if necessary
        if isinstance(raw_data, list):
            preamble = ""
            articles: List[Article] = []
            for item in raw_data:
                if item.get("article") == 0 or item.get("title") == "Preamble":
                    preamble = item.get("description", "")
                else:
                    articles.append(Article(**item))
            self._data = ConstitutionData(preamble=preamble, articles=articles)
        else:
            self._data = ConstitutionData(**raw_data)

        # Build indexes
        self._article_map = {str(a.number): a for a in self._data.articles}
        self._search_engine = SearchEngine(self._data.articles)
        self._exporter = Exporter(self._data.articles)
        self._graph_obj = ConstitutionGraph(self._data.articles)

    def _ensure_loaded(self) -> None:
        """Ensure data has been loaded."""
        if self._data is None:
            self._load_data()

    # ── Article access ───────────────────────────────────────────────────

    def get_article(self, number: Union[int, str]) -> Optional[Article]:
        """Retrieve an article by its number (e.g., 14, '21A').

        Returns ``None`` if the article does not exist.
        """
        self._ensure_loaded()
        return self._article_map.get(str(number))

    @property
    def preamble(self) -> str:
        """Get the Preamble of the Constitution."""
        return self.data.preamble

    @property
    def articles(self) -> List[Article]:
        """Return all articles in the Constitution."""
        return self.data.articles

    # ── Keyword search ───────────────────────────────────────────────────

    def search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles using the inverted-index keyword engine.

        All tokens in the query must appear in an article for it to match.
        """
        self._ensure_loaded()
        assert self._search_engine is not None
        return self._search_engine.keyword_search(query, limit)

    # ── Graph analysis ───────────────────────────────────────────────────

    def get_graph(self) -> Any:
        """Return the underlying ``networkx.DiGraph`` of cross-references.

        Each node is an article number; each directed edge ``(u, v)`` means
        article *u* textually references article *v*.

        Requires ``pip install indianconstitution[data]``.

        Raises:
            RuntimeError: If NetworkX is not installed.
        """
        self._ensure_loaded()
        assert self._graph_obj is not None
        if self._graph_obj.graph is None:
            raise RuntimeError(
                "NetworkX is required for graph analysis. Install with: pip install 'indianconstitution[data]'"
            )
        return self._graph_obj.graph

    def get_related_articles(self, number: str) -> Dict[str, List[str]]:
        """Get articles related to the given article via references.

        Returns a dict with keys ``references`` (articles this one cites)
        and ``referenced_by`` (articles that cite this one).
        """
        self._ensure_loaded()
        assert self._graph_obj is not None
        return {
            "references": self._graph_obj.get_references(number),
            "referenced_by": self._graph_obj.get_referenced_by(number),
        }

    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Return the most central articles by PageRank.

        Each element is a ``(article_number, score)`` tuple, sorted
        descending by score.
        """
        self._ensure_loaded()
        assert self._graph_obj is not None
        return self._graph_obj.get_central_articles(limit)

    # ── Semantic / AI search ─────────────────────────────────────────────

    def _load_semantic_model(self) -> None:
        """Lazy-load the sentence-transformers model and pre-encode articles."""
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Semantic search requires sentence-transformers. Install with: pip install 'indianconstitution[ai]'"
            ) from None

        self._ensure_loaded()
        self._semantic_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Pre-encode all article texts
        texts = [f"{a.title}. {a.content}" for a in self.data.articles]
        self._semantic_embeddings = self._semantic_model.encode(texts, show_progress_bar=False, convert_to_tensor=False)

    def semantic_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Contextual retrieval beyond keyword matching.

        Uses sentence-transformers to encode the query and find the
        most semantically similar articles.

        Requires ``pip install "indianconstitution[ai]"``.

        Args:
            query: Natural-language query string.
            top_k: Number of results to return.

        Returns:
            A list of :class:`SearchResult` objects, each containing
            the matched article data plus a ``score`` attribute.
        """
        if self._semantic_model is None:
            self._load_semantic_model()

        assert self._semantic_model is not None
        assert self._semantic_embeddings is not None

        try:
            from sentence_transformers import util as st_util  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Semantic search requires sentence-transformers. Install with: pip install 'indianconstitution[ai]'"
            ) from None

        query_embedding = self._semantic_model.encode(query, convert_to_tensor=False)
        scores = st_util.cos_sim(query_embedding, self._semantic_embeddings)[0]

        # Get top_k indices
        top_indices = scores.argsort(descending=True)[:top_k]

        results: List[SearchResult] = []
        for idx in top_indices:
            idx_int = int(idx)
            article = self.data.articles[idx_int]
            score = float(scores[idx_int])
            results.append(SearchResult.from_article(article, score=score))

        return results

    # ── Export ────────────────────────────────────────────────────────────

    def export(self, format: str, path: Union[str, Path]) -> None:
        """Export the constitution to JSON, CSV, or Markdown.

        Args:
            format: One of ``'json'``, ``'csv'``, ``'markdown'`` (or ``'md'``).
            path: Output file path.

        Raises:
            ValueError: If an unsupported format is specified.
        """
        self._ensure_loaded()
        assert self._exporter is not None

        if format == "json":
            self._exporter.to_json(path)
        elif format == "csv":
            self._exporter.to_csv(path)
        elif format in ("markdown", "md"):
            self._exporter.to_markdown(path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    # ── DataFrame ────────────────────────────────────────────────────────

    def to_dataframe(self) -> Any:
        """Return all articles as a ``pandas.DataFrame``.

        Requires ``pip install "indianconstitution[data]"``.
        """
        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError("pandas is required. Install with: pip install 'indianconstitution[data]'") from None

        self._ensure_loaded()
        return pd.DataFrame([a.model_dump() for a in self.data.articles])

    # ── Dunder ────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<Constitution: {len(self.data.articles)} Articles>"

    def __len__(self) -> int:
        return len(self.data.articles)
