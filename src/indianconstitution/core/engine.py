"""Constitution engine — main programmatic interface for accessing the Constitution of India.

Provides lazy-loaded access to:
- Article retrieval (:meth:`Constitution.get_article`)
- Full-text keyword search (:meth:`Constitution.search`)
- Fuzzy text search (:meth:`Constitution.fuzzy_search`)
- Cross-reference graph analysis (:meth:`Constitution.get_graph`)
- Semantic search on CPU (:meth:`Constitution.semantic_search`)
- Multi-format data export (:meth:`Constitution.export`)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..exceptions import (
    ArticleNotFoundError,
    CorpusIntegrityError,
    DependencyMissingError,
    InvalidAmendmentRangeError,
    UnsupportedFormatError,
)
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
    """Main entry point for accessing the Constitution of India dataset and tools.

    Uses lazy loading and singleton caching for performance optimization.

    Examples:
        >>> const = Constitution()
        >>> article = const.get_article("14")
        >>> article.number
        '14'
        >>> article.title
        'Equality before law'
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        """Initialize Constitution instance.

        Args:
            data_path: Path to custom constitution.json dataset file.
        """
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

    @property
    def data(self) -> ConstitutionData:
        """Lazy load the constitution data.

        Returns:
            ConstitutionData model instance.

        Raises:
            CorpusIntegrityError: If constitution data file is missing or invalid.
        """
        if self._data is None:
            self._load_data()
        assert self._data is not None
        return self._data

    def _load_data(self) -> None:
        """Load and parse JSON constitution data."""
        if not self._data_path.exists():
            raise CorpusIntegrityError("Data file does not exist", str(self._data_path))

        try:
            with open(self._data_path, encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            raise CorpusIntegrityError(f"Failed to parse JSON: {e}", str(self._data_path)) from e

        if isinstance(raw_data, list):
            preamble = ""
            articles: List[Article] = []
            for item in raw_data:
                if item.get("article") == 0 or item.get("title") == "Preamble":
                    preamble = item.get("description", "")
                else:
                    articles.append(Article(**item))
            self._data = ConstitutionData(preamble=preamble, articles=articles)
        elif isinstance(raw_data, dict):
            self._data = ConstitutionData(**raw_data)
        else:
            raise CorpusIntegrityError("Unexpected JSON root structure (expected dict or list)", str(self._data_path))

        self._article_map = {str(a.number): a for a in self._data.articles}
        self._search_engine = SearchEngine(self._data.articles)
        self._exporter = Exporter(self._data.articles)
        self._graph_obj = ConstitutionGraph(self._data.articles)

    def _ensure_loaded(self) -> None:
        """Ensure core dataset is loaded."""
        if self._data is None:
            self._load_data()

    def get_article(self, number: Union[int, str]) -> Optional[Article]:
        """Retrieve an article by number (e.g. 14, '21A').

        Args:
            number: Article identifier (int or str).

        Returns:
            Article instance if found, None otherwise.
        """
        self._ensure_loaded()
        return self._article_map.get(str(number).strip())

    def require_article(self, number: Union[int, str]) -> Article:
        """Retrieve an article by number, raising ArticleNotFoundError if missing.

        Args:
            number: Article identifier.

        Returns:
            Article instance.

        Raises:
            ArticleNotFoundError: If article does not exist.
        """
        art = self.get_article(number)
        if art is None:
            raise ArticleNotFoundError(str(number))
        return art

    @property
    def preamble(self) -> str:
        """Get Preamble text of the Constitution."""
        return self.data.preamble

    @property
    def articles(self) -> List[Article]:
        """Get list of all Article instances in the Constitution."""
        return self.data.articles

    def _ensure_case_law(self) -> List[CaseLaw]:
        """Load landmark Supreme Court case judgments."""
        if self._case_law_list is None:
            if not CASE_LAW_PATH.exists():
                self._case_law_list = []
            else:
                try:
                    with open(CASE_LAW_PATH, encoding="utf-8") as f:
                        raw = json.load(f)
                    self._case_law_list = [CaseLaw(**item) for item in raw]
                except Exception as e:
                    raise CorpusIntegrityError(f"Failed to load case law: {e}", str(CASE_LAW_PATH)) from e
        return self._case_law_list

    def _ensure_amendments(self) -> List[AmendmentEvent]:
        """Load amendment event history."""
        if self._amendments_list is None:
            if not AMENDMENTS_PATH.exists():
                self._amendments_list = []
            else:
                try:
                    with open(AMENDMENTS_PATH, encoding="utf-8") as f:
                        raw = json.load(f)
                    self._amendments_list = [AmendmentEvent(**item) for item in raw]
                except Exception as e:
                    raise CorpusIntegrityError(f"Failed to load amendments: {e}", str(AMENDMENTS_PATH)) from e
        return self._amendments_list

    def _ensure_duties(self) -> List[DutyCrossReference]:
        """Load Fundamental Duty cross references."""
        if self._duties_list is None:
            if not DUTIES_PATH.exists():
                self._duties_list = []
            else:
                try:
                    with open(DUTIES_PATH, encoding="utf-8") as f:
                        raw = json.load(f)
                    self._duties_list = [DutyCrossReference(**item) for item in raw]
                except Exception as e:
                    raise CorpusIntegrityError(f"Failed to load duties: {e}", str(DUTIES_PATH)) from e
        return self._duties_list

    def _ensure_i18n(self) -> Dict[str, Any]:
        """Load multilingual translation data."""
        if self._i18n_data is None:
            if not I18N_PATH.exists():
                self._i18n_data = {}
            else:
                try:
                    with open(I18N_PATH, encoding="utf-8") as f:
                        self._i18n_data = json.load(f)
                except Exception as e:
                    raise CorpusIntegrityError(f"Failed to load i18n data: {e}", str(I18N_PATH)) from e
        return self._i18n_data

    def get_related_cases(self, number: Union[int, str]) -> List[CaseLaw]:
        """Retrieve landmark Supreme Court judgments for an article."""
        cases = self._ensure_case_law()
        num_str = str(number).strip()
        return [c for c in cases if c.article_number == num_str]

    def get_amendment_history(self, number: Union[int, str]) -> List[AmendmentEvent]:
        """Retrieve historical amendment events for an article."""
        events = self._ensure_amendments()
        num_str = str(number).strip()
        filtered = [e for e in events if e.article_number == num_str]
        return sorted(filtered, key=lambda x: x.year)

    def diff_amendment(self, number: Union[int, str], from_year: int = 1950, to_year: int = 2026) -> str:
        """Compute unified diff showing textual changes between specified amendment years.

        Args:
            number: Article identifier.
            from_year: Starting year bound.
            to_year: Ending year bound.

        Returns:
            Unified diff formatted string.

        Raises:
            InvalidAmendmentRangeError: If from_year > to_year.
        """
        if from_year > to_year:
            raise InvalidAmendmentRangeError(from_year, to_year)

        import difflib

        history = self.get_amendment_history(number)
        if not history:
            return ""

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
        """Cross-reference Part III Fundamental Rights to Part IVA Fundamental Duties."""
        duties = self._ensure_duties()
        num_str = str(number).strip()
        return [d for d in duties if d.right_article == num_str or d.duty_clause == num_str]

    def get_translation(self, number: Union[int, str], lang: str = "hi") -> Optional[Dict[str, str]]:
        """Get translated article title and content."""
        data = self._ensure_i18n()
        articles_data = data.get("articles", {})
        art_lang = articles_data.get(str(number), {}).get(lang)
        if art_lang and isinstance(art_lang, dict):
            return {"title": str(art_lang.get("title", "")), "content": str(art_lang.get("content", ""))}
        return None

    def get_translated_preamble(self, lang: str = "hi") -> str:
        """Get translated Preamble text."""
        data = self._ensure_i18n()
        preambles = data.get("preamble", {})
        return str(preambles.get(lang, ""))

    def search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles matching query using inverted-index keyword matching."""
        self._ensure_loaded()
        assert self._search_engine is not None
        return self._search_engine.keyword_search(query, limit)

    def fuzzy_search(self, query: str, limit: int = 10, min_score: float = 0.3) -> List[SearchResult]:
        """Perform fuzzy similarity search across articles."""
        self._ensure_loaded()
        assert self._search_engine is not None
        return self._search_engine.fuzzy_search(query, limit=limit, min_score=min_score)

    def get_graph(self) -> Any:  # noqa: ANN401
        """Return the networkx.DiGraph instance for inter-article cross references.

        Raises:
            DependencyMissingError: If NetworkX is not installed.
        """
        self._ensure_loaded()
        assert self._graph_obj is not None
        if self._graph_obj.graph is None:
            raise DependencyMissingError("Graph analysis", "data")
        return self._graph_obj.graph

    def get_related_articles(self, number: str) -> Dict[str, List[str]]:
        """Get article numbers referenced by or referencing the specified article."""
        self._ensure_loaded()
        assert self._graph_obj is not None
        return {
            "references": self._graph_obj.get_references(number),
            "referenced_by": self._graph_obj.get_referenced_by(number),
        }

    def get_central_articles(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Return most central articles by PageRank score."""
        self._ensure_loaded()
        assert self._graph_obj is not None
        return self._graph_obj.get_central_articles(limit)

    def _load_semantic_model(self) -> None:
        """Lazy-load sentence-transformers model and encode articles on CPU."""
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        try:
            import torch

            torch.set_num_threads(max(1, os.cpu_count() or 1))
        except ImportError:
            pass

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise DependencyMissingError("Semantic search", "ai") from None

        self._ensure_loaded()
        self._semantic_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        texts = [f"{a.title}. {a.content}" for a in self.data.articles]
        self._semantic_embeddings = self._semantic_model.encode(texts, show_progress_bar=False, convert_to_tensor=False)

    def semantic_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Perform CPU-only semantic search using sentence-transformers.

        Args:
            query: Query string.
            top_k: Number of results.

        Returns:
            List of SearchResult objects sorted by similarity score.

        Raises:
            DependencyMissingError: If sentence-transformers is missing.
        """
        if self._semantic_model is None:
            self._load_semantic_model()

        assert self._semantic_model is not None
        assert self._semantic_embeddings is not None

        query_embedding = self._semantic_model.encode(query, convert_to_tensor=False)
        try:
            from sentence_transformers import util as st_util

            scores_tensor = st_util.cos_sim(query_embedding, self._semantic_embeddings)[0]
            scores = [float(s) for s in scores_tensor]
        except (ImportError, Exception):  # pragma: no cover
            import math

            q_vec = list(query_embedding) if not isinstance(query_embedding, list) else query_embedding
            q_norm = math.sqrt(sum(float(x) * float(x) for x in q_vec)) or 1.0
            scores = []
            for doc_vec in self._semantic_embeddings:
                d_vec = list(doc_vec) if not isinstance(doc_vec, list) else doc_vec
                d_norm = math.sqrt(sum(float(y) * float(y) for y in d_vec)) or 1.0
                dot = sum(float(x) * float(y) for x, y in zip(q_vec, d_vec))
                scores.append(dot / (q_norm * d_norm))

        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda item: item[1], reverse=True)
        top_indices = indexed_scores[:top_k]

        results: List[SearchResult] = []
        for idx_int, score in top_indices:
            article = self.data.articles[idx_int]
            results.append(SearchResult.from_article(article, score=float(score)))

        return results

    def export(self, format: str, path: Union[str, Path]) -> None:
        """Export constitution dataset to specified file format.

        Args:
            format: Output format ('json', 'csv', 'markdown', 'md', 'gexf', 'graphml').
            path: Destination file path.

        Raises:
            UnsupportedFormatError: If requested format is not supported.
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
            raise UnsupportedFormatError(format)

    def to_dataframe(self) -> Any:  # noqa: ANN401
        """Return all articles as a pandas.DataFrame.

        Raises:
            DependencyMissingError: If pandas is not installed.
        """
        try:
            import pandas as pd
        except ImportError:
            raise DependencyMissingError("Pandas export", "data") from None

        self._ensure_loaded()
        return pd.DataFrame([a.model_dump() for a in self.data.articles])

    def __repr__(self) -> str:
        """Return string representation of Constitution engine."""
        return f"<Constitution: {len(self.data.articles)} Articles>"

    def __len__(self) -> int:
        """Return total number of articles in Constitution corpus."""
        return len(self.data.articles)
