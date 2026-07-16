import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from ..export.engine import Exporter
from ..search.engine import SearchEngine
from .graph import ConstitutionGraph
from .models import Article, ConstitutionData

DATA_PATH = Path(__file__).parent.parent / "data" / "constitution.json"


class Constitution:
    """Main entry point for accessing the Constitution of India.
    Uses lazy loading and caching for optimal performance.
    """
    
    def __init__(self, data_path: Optional[Path] = None):
        self._data_path = data_path or DATA_PATH
        self._data: Optional[ConstitutionData] = None
        self._article_map: Dict[str, Article] = {}
        self._search_engine: Optional[SearchEngine] = None
        self._exporter: Optional[Exporter] = None
        self._graph: Optional[ConstitutionGraph] = None

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
            articles = []
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
        self._graph = ConstitutionGraph(self._data.articles)

    def get_article(self, number: Union[int, str]) -> Optional[Article]:
        """Retrieve an article by its number (e.g., 14, '21A')."""
        if self._data is None:
            self._load_data()
        return self._article_map.get(str(number))

    def search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles using the specialized search engine."""
        if self._data is None:
            self._load_data()
        assert self._search_engine is not None
        return self._search_engine.keyword_search(query, limit)

    def export(self, format: str, path: Union[str, Path]):
        """Export the constitution to JSON, CSV, or Markdown."""
        if self._data is None:
            self._load_data()
        
        assert self._exporter is not None
            
        if format == "json":
            self._exporter.to_json(path)
        elif format == "csv":
            self._exporter.to_csv(path)
        elif format == "markdown" or format == "md":
            self._exporter.to_markdown(path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_related_articles(self, number: str) -> Dict[str, List[str]]:
        """Get articles related to the given article via references."""
        if self._data is None:
            self._load_data()
        assert self._graph is not None
        return {
            "references": self._graph.get_references(number),
            "referenced_by": self._graph.get_referenced_by(number)
        }

    @property
    def preamble(self) -> str:
        """Get the Preamble of the Constitution."""
        return self.data.preamble

    def __repr__(self) -> str:
        return f"<Constitution: {len(self.data.articles)} Articles>"
