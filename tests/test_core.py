from pathlib import Path

import pytest

from indianconstitution import get_article, get_constitution, search
from indianconstitution.core.models import SearchResult


def test_load_constitution():
    """Constitution loads successfully with articles and preamble."""
    ic = get_constitution()
    assert ic.data.preamble != ""
    assert len(ic.data.articles) > 0


def test_len():
    """len(ic) returns the number of articles."""
    ic = get_constitution()
    assert len(ic) == len(ic.data.articles)


def test_articles_property():
    """ic.articles returns the same list as ic.data.articles."""
    ic = get_constitution()
    assert ic.articles is ic.data.articles


def test_get_article():
    """get_article returns the correct article with proper fields."""
    article = get_article("14")
    assert article is not None
    assert article.number == "14"
    assert "equality" in article.title.lower()


def test_article_text_alias():
    """article.text is an alias for article.content."""
    article = get_article("14")
    assert article is not None
    assert article.text == article.content
    assert len(article.text) > 0


def test_search():
    """Keyword search returns matching results."""
    results = search("untouchability")
    assert len(results) > 0
    assert any("abolition" in a.title.lower() for a in results)


def test_invalid_article():
    """Requesting a non-existent article returns None."""
    article = get_article("999B")
    assert article is None


def test_get_related_articles():
    """get_related_articles returns references and referenced_by."""
    ic = get_constitution()
    related = ic.get_related_articles("32")
    assert "references" in related
    assert "referenced_by" in related
    assert isinstance(related["references"], list)
    assert isinstance(related["referenced_by"], list)


def test_get_graph():
    """get_graph returns a networkx DiGraph."""
    try:
        import networkx as nx
    except ImportError:
        return  # Skip if networkx not installed

    ic = get_constitution()
    graph_obj = ic.get_graph()
    assert isinstance(graph_obj, nx.DiGraph)
    assert graph_obj.number_of_nodes() > 0


def test_get_central_articles():
    """get_central_articles returns (article_num, score) tuples."""
    try:
        import networkx  # noqa: F401
    except ImportError:
        return

    ic = get_constitution()
    top = ic.get_central_articles(limit=5)
    assert len(top) == 5
    assert isinstance(top[0], tuple)
    assert isinstance(top[0][0], str)
    assert isinstance(top[0][1], float)


def test_search_result_from_article():
    """SearchResult.from_article correctly wraps an Article."""
    article = get_article("14")
    assert article is not None
    result = SearchResult.from_article(article, score=0.95)
    assert result.number == "14"
    assert result.score == 0.95
    assert result.text == article.content


def test_model_dump():
    """model_dump() works correctly (Pydantic v2 API)."""
    article = get_article("14")
    assert article is not None
    dump = article.model_dump()
    assert "number" in dump
    assert "title" in dump
    assert "content" in dump
    assert dump["number"] == "14"


def test_preamble():
    """Preamble is non-empty and contains expected text."""
    ic = get_constitution()
    assert "PEOPLE OF INDIA" in ic.preamble.upper()


def test_to_dataframe():
    """to_dataframe returns a pandas DataFrame."""
    try:
        import pandas as pd
    except ImportError:
        return

    ic = get_constitution()
    df = ic.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(ic)


def test_export_all_formats(tmp_path: Path):
    """Export handles json, csv, and markdown."""
    ic = get_constitution()
    ic.export("json", tmp_path / "out.json")
    ic.export("csv", tmp_path / "out.csv")
    ic.export("markdown", tmp_path / "out.md")

    assert (tmp_path / "out.json").exists()
    assert (tmp_path / "out.csv").exists()
    assert (tmp_path / "out.md").exists()


def test_export_invalid_format(tmp_path: Path):
    """Export raises ValueError on invalid format."""
    ic = get_constitution()
    with pytest.raises(ValueError, match="Unsupported export format"):
        ic.export("invalid_format", tmp_path / "out.xyz")


def test_repr():
    """__repr__ returns string representation."""
    ic = get_constitution()
    assert "<Constitution:" in repr(ic)

