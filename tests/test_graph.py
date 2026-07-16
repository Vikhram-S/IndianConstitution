import pytest
from indianconstitution.core.models import Article
from indianconstitution.core.graph import ConstitutionGraph, NETWORKX_AVAILABLE


@pytest.mark.skipif(not NETWORKX_AVAILABLE, reason="NetworkX is required")
def test_graph_building():
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


def test_graph_no_references():
    articles = [Article(number="1", title="Name", content="No refs")]
    graph = ConstitutionGraph(articles)
    assert graph.get_references("1") == []
    assert graph.get_referenced_by("1") == []
