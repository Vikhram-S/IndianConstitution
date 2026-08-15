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
from .models import AmendmentEvent, Article, CaseLaw, ConstitutionData, DutyCrossReference, SearchResult

DATA_PATH = Path(__file__).parent.parent / "data" / "constitution.json"
CASE_LAW_PATH = Path(__file__).parent.parent / "data" / "case_law.json"
AMENDMENTS_PATH = Path(__file__).parent.parent / "data" / "amendments.json"
DUTIES_PATH = Path(__file__).parent.parent / "data" / "duties.json"
I18N_PATH = Path(__file__).parent.parent / "data" / "i18n.json"


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
        self._case_law_list: Optional[List[CaseLaw]] = None
        self._amendments_list: Optional[List[AmendmentEvent]] = None
        self._duties_list: Optional[List[DutyCrossReference]] = None
        self._i18n_data: Optional[Dict[str, Any]] = None

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

    # ── Feature Loaders & Landmark Cases / Amendments / Duties / i18n ────────

    def _ensure_case_law(self) -> List[CaseLaw]:
        if self._case_law_list is None:
            if not CASE_LAW_PATH.exists():
                self._case_law_list = []
            else:
                with open(CASE_LAW_PATH, encoding="utf-8") as f:
                    raw = json.load(f)
                self._case_law_list = [CaseLaw(**item) for item in raw]
        return self._case_law_list

    def _ensure_amendments(self) -> List[AmendmentEvent]:
        if self._amendments_list is None:
            if not AMENDMENTS_PATH.exists():
                self._amendments_list = []
            else:
                with open(AMENDMENTS_PATH, encoding="utf-8") as f:
                    raw = json.load(f)
                self._amendments_list = [AmendmentEvent(**item) for item in raw]
        return self._amendments_list

    def _ensure_duties(self) -> List[DutyCrossReference]:
        if self._duties_list is None:
            if not DUTIES_PATH.exists():
                self._duties_list = []
            else:
                with open(DUTIES_PATH, encoding="utf-8") as f:
                    raw = json.load(f)
                self._duties_list = [DutyCrossReference(**item) for item in raw]
        return self._duties_list

    def _ensure_i18n(self) -> Dict[str, Any]:
        if self._i18n_data is None:
            if not I18N_PATH.exists():
                self._i18n_data = {}
            else:
                with open(I18N_PATH, encoding="utf-8") as f:
                    self._i18n_data = json.load(f)
        return self._i18n_data

    def get_related_cases(self, number: Union[int, str]) -> List[CaseLaw]:
        """Retrieve landmark Supreme Court judgments for an article.

        Args:
            number: Article number (e.g. 14, '21', '368').

        Returns:
            A list of :class:`CaseLaw` objects.
        """
        cases = self._ensure_case_law()
        num_str = str(number).strip()
        return [c for c in cases if c.article_number == num_str]

    def get_amendment_history(self, number: Union[int, str]) -> List[AmendmentEvent]:
        """Retrieve historical amendment events for an article.

        Args:
            number: Article number (e.g. '19', '21A', '31').

        Returns:
            A list of :class:`AmendmentEvent` objects ordered by year.
        """
        events = self._ensure_amendments()
        num_str = str(number).strip()
        filtered = [e for e in events if e.article_number == num_str]
        return sorted(filtered, key=lambda x: x.year)

    def diff_amendment(self, number: Union[int, str], from_year: int = 1950, to_year: int = 2026) -> str:
        """Compute textual delta between amendment states of an article using stdlib difflib.

        Args:
            number: Article number (e.g. '19', '21A').
            from_year: Starting year cutoff.
            to_year: Ending year cutoff.

        Returns:
            A unified diff string showing changes.
        """
        import difflib

        history = self.get_amendment_history(number)
        if not history:
            return f"No amendment history found for Article {number}."

        from_events = [e for e in history if e.year <= from_year]
        to_events = [e for e in history if e.year <= to_year]

        text_before = (
            from_events[-1].text_after
            if from_events and from_events[-1].text_after
            else (
                from_events[0].text_before
                if from_events and from_events[0].text_before
                else f"Article {number} prior to {from_year}"
            )
        )
        text_after = (
            to_events[-1].text_after
            if to_events and to_events[-1].text_after
            else (
                to_events[0].text_after
                if to_events and to_events[0].text_after
                else f"Article {number} as of {to_year}"
            )
        )

        diff = difflib.unified_diff(
            text_before.splitlines(keepends=True),
            text_after.splitlines(keepends=True),
            fromfile=f"Article_{number}_{from_year}",
            tofile=f"Article_{number}_{to_year}",
        )
        return "".join(diff)

    def get_related_duties(self, number: Union[int, str]) -> List[DutyCrossReference]:
        """Cross-reference Part III Fundamental Rights to Part IVA Fundamental Duties.

        Args:
            number: Right article number (e.g. '21A', '21', '14') or duty clause.

        Returns:
            A list of :class:`DutyCrossReference` objects.
        """
        duties = self._ensure_duties()
        num_str = str(number).strip()
        return [d for d in duties if d.right_article == num_str or d.duty_clause == num_str]

    def get_translation(self, number: Union[int, str], lang: str = "hi") -> Optional[Dict[str, str]]:
        """Get translated article title and content.

        Args:
            number: Article number.
            lang: Language code (e.g. 'hi').

        Returns:
            Dict containing 'title' and 'content' or None if not available.
        """
        data = self._ensure_i18n()
        articles_data = data.get("articles", {})
        art_lang = articles_data.get(str(number), {}).get(lang)
        if art_lang and isinstance(art_lang, dict):
            return {"title": str(art_lang.get("title", "")), "content": str(art_lang.get("content", ""))}
        return None

    def get_translated_preamble(self, lang: str = "hi") -> str:
        """Get translated Preamble text.

        Args:
            lang: Language code (e.g. 'hi').

        Returns:
            Translated Preamble string or empty string.
        """
        data = self._ensure_i18n()
        preambles = data.get("preamble", {})
        return str(preambles.get(lang, ""))

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
        """Export the constitution to JSON, CSV, Markdown, GEXF, or GraphML.

        Args:
            format: One of ``'json'``, ``'csv'``, ``'markdown'`` (or ``'md'``), ``'gexf'``, ``'graphml'``.
            path: Output file path.

        Raises:
            ValueError: If an unsupported format is specified.
        """
        self._ensure_loaded()
        assert self._exporter is not None

        fmt_lower = format.lower()
        if fmt_lower == "json":
            self._exporter.to_json(path)
        elif fmt_lower == "csv":
            self._exporter.to_csv(path)
        elif fmt_lower in ("markdown", "md"):
            self._exporter.to_markdown(path)
        elif fmt_lower == "gexf":
            assert self._graph_obj is not None
            self._graph_obj.export_gexf(path)
        elif fmt_lower == "graphml":
            assert self._graph_obj is not None
            self._graph_obj.export_graphml(path)
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
