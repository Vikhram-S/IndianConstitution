"""Tests for the ConstitutionGraph cross-reference engine."""

import pytest

from indianconstitution.core.graph import NETWORKX_AVAILABLE, ConstitutionGraph
from indianconstitution.core.models import Article


@pytest.mark.skipif(not NETWORKX_AVAILABLE, reason="NetworkX is required")
def test_graph_building():
    """Graph correctly captures cross-article references."""
    articles = [
        Article(number="13", title="Laws", content="Derogation of fundamental rights"),
        Article(number="32", title="Remedies", content="See article 13 for details."),
    ]
    graph = ConstitutionGraph(articles)

    refs = graph.get_references("32")
    assert "13" in refs

    ref_by = graph.get_referenced_by("13")
    assert "32" in ref_by

    central = graph.get_central_articles(limit=1)
    assert len(central) > 0
    assert central[0][0] == "13"


@pytest.mark.skipif(not NETWORKX_AVAILABLE, reason="NetworkX is required")
def test_graph_suffix_capture():
    """Regex correctly captures article suffixes like 21A."""
    articles = [
        Article(number="21A", title="Education", content="Right to education."),
        Article(number="45", title="Education", content="See article 21a for details."),
    ]
    graph = ConstitutionGraph(articles)

    refs = graph.get_references("45")
    assert "21A" in refs


@pytest.mark.skipif(not NETWORKX_AVAILABLE, reason="NetworkX is required")
def test_graph_property():
    """Graph property returns a networkx DiGraph."""
    import networkx as nx

    articles = [
        Article(number="1", title="Name", content="India"),
        Article(number="2", title="Test", content="See article 1."),
    ]
    graph = ConstitutionGraph(articles)
    assert isinstance(graph.graph, nx.DiGraph)


@pytest.mark.skipif(not NETWORKX_AVAILABLE, reason="NetworkX is required")
def test_degree_centrality():
    """get_degree_centrality returns a dict of article -> score."""
    articles = [
        Article(number="1", title="A", content="See article 2"),
        Article(number="2", title="B", content="Some text"),
    ]
    graph = ConstitutionGraph(articles)
    centrality = graph.get_degree_centrality()
    assert isinstance(centrality, dict)
    assert "1" in centrality
    assert "2" in centrality


def test_graph_no_references():
    """Graph handles articles with no cross-references."""
    articles = [Article(number="1", title="Name", content="No refs")]
    graph = ConstitutionGraph(articles)
    assert graph.get_references("1") == []
    assert graph.get_referenced_by("1") == []
