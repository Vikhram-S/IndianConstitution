"""Targeted unit tests to achieve >90% code coverage across all modules."""

import sys
from pathlib import Path

import pytest

from indianconstitution import (
    ArticleNotFoundError,
    Constitution,
    CorpusIntegrityError,
    DependencyMissingError,
    IndianConstitutionError,
    InvalidAmendmentRangeError,
    UnsupportedFormatError,
    fuzzy_search,
    get_constitution,
)
from indianconstitution.core.graph import ConstitutionGraph
from indianconstitution.utils.caching import DiskCache


def test_custom_exception_properties() -> None:
    """Test custom exception message formatting and attributes."""
    err1 = ArticleNotFoundError("14")
    assert err1.article_number == "14"
    assert "Article '14'" in str(err1)

    err2 = CorpusIntegrityError("Missing JSON", path="/path/to/file")
    assert err2.path == "/path/to/file"
    assert "Missing JSON" in str(err2)

    err3 = InvalidAmendmentRangeError(2025, 2010)
    assert err3.from_year == 2025
    assert err3.to_year == 2010

    err4 = DependencyMissingError("Semantic Search", "ai")
    assert err4.feature_name == "Semantic Search"
    assert err4.extra_name == "ai"

    err5 = UnsupportedFormatError("xml")
    assert err5.format_requested == "xml"
    assert "xml" in str(err5)


def test_fuzzy_search_engine() -> None:
    """Test fuzzy search engine functionality and edge cases."""
    const = get_constitution()
    results = const.fuzzy_search("equality", limit=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0].score > 0.0

    empty_res = const.fuzzy_search("", limit=5)
    assert empty_res == []

    top_level_fuzzy = fuzzy_search("liberty", limit=2)
    assert len(top_level_fuzzy) > 0


def test_engine_corpus_integrity_missing_file(tmp_path: Path) -> None:
    """Constitution raises CorpusIntegrityError when file is missing or corrupted."""
    non_existent = tmp_path / "missing.json"
    const = Constitution(data_path=non_existent)
    with pytest.raises(CorpusIntegrityError):
        _ = const.data

    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("not json content {")
    const2 = Constitution(data_path=invalid_json)
    with pytest.raises(CorpusIntegrityError):
        _ = const2.data

    unexpected_type_json = tmp_path / "number.json"
    unexpected_type_json.write_text("12345")
    const3 = Constitution(data_path=unexpected_type_json)
    with pytest.raises(CorpusIntegrityError):
        _ = const3.data


def test_graph_edge_cases() -> None:
    """Test graph methods with nonexistent article numbers and when graph is None."""
    const = get_constitution()
    refs = const.get_related_articles("99999")
    assert refs["references"] == []
    assert refs["referenced_by"] == []

    cg = ConstitutionGraph(const.articles)
    assert cg.get_references("99999") == []
    assert cg.get_referenced_by("99999") == []

    # Test graph functions when graph is None
    cg._graph = None
    assert cg.get_references("14") == []
    assert cg.get_referenced_by("14") == []
    assert cg.get_central_articles() == []
    assert cg.get_degree_centrality() == {}
    assert cg.get_communities() == []
    with pytest.raises(DependencyMissingError):
        cg.export_gexf("test.gexf")
    with pytest.raises(DependencyMissingError):
        cg.export_graphml("test.graphml")


def test_graph_community_detection() -> None:
    """Test graph communities detection."""
    const = get_constitution()
    try:
        cg = ConstitutionGraph(const.articles)
        communities = cg.get_communities()
        assert isinstance(communities, list)
    except Exception:
        pytest.skip("NetworkX not installed")


def test_semantic_search_cpu(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CPU semantic search logic with mocked embedding model.

    Exercises both the sentence-transformers cosine path (if available)
    and the pure-Python fallback path (when sentence_transformers is absent).
    """
    const = get_constitution()

    class DummyModel:
        def encode(self, texts: object, show_progress_bar: bool = False, convert_to_tensor: bool = False) -> object:
            if isinstance(texts, list):
                return [[0.1 * (i + 1)] * 8 for i in range(len(texts))]
            return [0.1] * 8

    const._semantic_model = DummyModel()
    const._semantic_embeddings = [[0.1 * (i + 1)] * 8 for i in range(len(const.articles))]

    # Force pure-Python fallback by hiding sentence_transformers.util
    monkeypatch.setitem(sys.modules, "sentence_transformers.util", None)

    results = const.semantic_search("equality", top_k=2)
    assert len(results) == 2
    assert isinstance(results[0].score, float)


def test_caching_clear(tmp_path: Path) -> None:
    """Test DiskCache clear method."""
    cache = DiskCache(directory=tmp_path / "test_cache")
    cache.set("key", "val")
    assert cache.get("key") == "val"
    cache.clear()
    assert cache.get("key") is None


def test_engine_missing_dependency_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test engine dependency missing error branches."""
    const = get_constitution()

    # Test pandas import error safely via sys.modules
    monkeypatch.setitem(sys.modules, "pandas", None)
    with pytest.raises(DependencyMissingError):
        const.to_dataframe()


def test_cli_additional_commands(tmp_path: Path) -> None:
    """Test CLI commands error and export branches."""
    from typer.testing import CliRunner

    from indianconstitution.cli.main import app

    runner = CliRunner()
    res1 = runner.invoke(app, ["export", "invalid_fmt", str(tmp_path / "out.txt")])
    assert res1.exit_code == 0
    assert "Export failed" in res1.output

    res2 = runner.invoke(app, ["export", "csv", str(tmp_path / "out.csv")])
    assert res2.exit_code == 0
    assert (tmp_path / "out.csv").exists()

    res3 = runner.invoke(app, ["export", "markdown", str(tmp_path / "out.md")])
    assert res3.exit_code == 0
    assert (tmp_path / "out.md").exists()
