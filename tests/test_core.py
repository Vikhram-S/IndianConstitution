import pytest
from indianconstitution import get_constitution, get_article, search
from indianconstitution.core.models import Article

def test_load_constitution():
    ic = get_constitution()
    assert ic.data.preamble != ""
    assert len(ic.data.articles) > 0

def test_get_article():
    article = get_article("14")
    assert article.number == "14"
    assert "equality" in article.title.lower()

def test_search():
    results = search("untouchability")
    assert len(results) > 0
    assert any("abolition" in a.title.lower() for a in results)

def test_invalid_article():
    article = get_article("999B")
    assert article is None
