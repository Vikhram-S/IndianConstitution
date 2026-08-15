"""Comprehensive unit and Hypothesis property-based tests for v1.5.0 features.

- Landmark Judgments Linker
- Amendment Timeline & Diff View
- Fundamental Rights ↔ Fundamental Duties Cross-Reference
- Multilingual Preamble & Key Articles (i18n)
- Graph Export to GEXF/GraphML
- REST API Extra
- Quiz & New CLI Commands
"""

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

from indianconstitution import (
    diff_amendment,
    get_amendment_history,
    get_constitution,
    get_related_cases,
    get_related_duties,
    get_translated_preamble,
    get_translation,
)
from indianconstitution.cli.main import app
from indianconstitution.core.models import AmendmentEvent, CaseLaw, DutyCrossReference

runner = CliRunner()


# ── 1. Landmark Judgments Linker ──────────────────────────────────────────────

def test_get_related_cases():
    """get_related_cases returns landmark cases for key articles."""
    cases_21 = get_related_cases("21")
    assert len(cases_21) >= 2
    case_names = [c.case_name for c in cases_21]
    assert "Maneka Gandhi v. Union of India" in case_names
    assert "K.S. Puttaswamy v. Union of India" in case_names

    # Check CaseLaw model attributes
    case = cases_21[0]
    assert isinstance(case, CaseLaw)
    assert case.year > 1940
    assert len(case.holding) > 0
    assert case.article_number == "21"


def test_get_related_cases_nonexistent():
    """Non-existent or unlinked articles return an empty list."""
    cases = get_related_cases("9999Z")
    assert cases == []


@given(st.text())
def test_hypothesis_get_related_cases(article_num: str):
    """Property test: get_related_cases never crashes for arbitrary string inputs."""
    res = get_related_cases(article_num)
    assert isinstance(res, list)


# ── 2. Amendment Timeline & Diff View ─────────────────────────────────────────

def test_get_amendment_history():
    """get_amendment_history returns ordered amendment events for an article."""
    events = get_amendment_history("21A")
    assert len(events) >= 1
    event = events[0]
    assert isinstance(event, AmendmentEvent)
    assert event.amendment_number == "86th Amendment Act"
    assert event.year == 2002
    assert event.article_number == "21A"


def test_diff_amendment():
    """diff_amendment generates a unified diff string between amendment points."""
    diff = diff_amendment("21A", from_year=1950, to_year=2026)
    assert isinstance(diff, str)
    assert len(diff) > 0


def test_diff_amendment_unamended():
    """diff_amendment handles unamended articles gracefully."""
    diff = diff_amendment("9999Z")
    assert "No amendment history found" in diff


@given(st.text(), st.integers(min_value=1900, max_value=2100), st.integers(min_value=1900, max_value=2100))
def test_hypothesis_diff_amendment(article_num: str, from_year: int, to_year: int):
    """Property test: diff_amendment handles arbitrary inputs safely."""
    res = diff_amendment(article_num, from_year, to_year)
    assert isinstance(res, str)


# ── 3. Fundamental Rights ↔ Fundamental Duties Cross-Reference ────────────────

def test_get_related_duties():
    """get_related_duties links Part III rights to Part IVA duties."""
    duties_21a = get_related_duties("21A")
    assert len(duties_21a) >= 1
    d = duties_21a[0]
    assert isinstance(d, DutyCrossReference)
    assert d.duty_clause == "51A(k)"
    assert "education" in d.duty_text.lower()
    assert len(d.rationale) > 0


def test_get_related_duties_by_duty_clause():
    """get_related_duties works when querying by duty clause e.g. '51A(k)'."""
    duties = get_related_duties("51A(k)")
    assert len(duties) >= 1
    assert duties[0].right_article == "21A"


@given(st.text())
def test_hypothesis_get_related_duties(article_num: str):
    """Property test: get_related_duties handles arbitrary inputs safely."""
    res = get_related_duties(article_num)
    assert isinstance(res, list)


# ── 4. Multilingual i18n ──────────────────────────────────────────────────────

def test_get_translation_hindi():
    """get_translation returns Hindi title and content for key articles."""
    trans = get_translation("21A", lang="hi")
    assert trans is not None
    assert "शिक्षा का अधिकार" in trans["title"]
    assert "चौदह वर्ष" in trans["content"]


def test_get_translated_preamble_hindi():
    """get_translated_preamble returns Hindi Preamble text."""
    preamble_hi = get_translated_preamble("hi")
    assert "हम, भारत के लोग" in preamble_hi


def test_get_translation_nonexistent():
    """Non-existent translations return None / empty string."""
    assert get_translation("9999Z", lang="hi") is None
    assert get_translation("21A", lang="nonexistent_lang") is None
    assert get_translated_preamble("nonexistent_lang") == ""


# ── 5. Graph Export to GEXF / GraphML ──────────────────────────────────────────

def test_gexf_graphml_export(tmp_path: Path):
    """Export handles gexf and graphml formats."""
    try:
        import networkx  # noqa: F401
    except ImportError:
        pytest.skip("NetworkX not installed")

    ic = get_constitution()
    gexf_path = tmp_path / "graph.gexf"
    graphml_path = tmp_path / "graph.graphml"

    ic.export("gexf", gexf_path)
    ic.export("graphml", graphml_path)

    assert gexf_path.exists()
    assert gexf_path.stat().st_size > 0
    assert graphml_path.exists()
    assert graphml_path.stat().st_size > 0


# ── 6. Lightweight REST API ──────────────────────────────────────────────────

def test_fastapi_rest_api():
    """Test FastAPI application endpoints if fastapi is installed."""
    try:
        from fastapi.testclient import TestClient  # type: ignore[import-untyped]

        from indianconstitution.api.app import app as api_app
    except ImportError:
        pytest.skip("FastAPI not installed")

    if api_app is None:
        pytest.skip("FastAPI not available")

    client = TestClient(api_app)

    r_root = client.get("/")
    assert r_root.status_code == 200
    assert r_root.json()["status"] == "healthy"

    r_art = client.get("/api/v1/articles/14")
    assert r_art.status_code == 200
    assert r_art.json()["number"] == "14"

    r_search = client.get("/api/v1/search?q=equality")
    assert r_search.status_code == 200
    assert isinstance(r_search.json(), list)

    r_cases = client.get("/api/v1/cases/21")
    assert r_cases.status_code == 200
    assert len(r_cases.json()) >= 2

    r_amend = client.get("/api/v1/amendments/21A")
    assert r_amend.status_code == 200

    r_duties = client.get("/api/v1/duties/21A")
    assert r_duties.status_code == 200


# ── 7. New CLI Commands (Quiz, Cases, Amendments, Duties) ────────────────────

def test_cli_quiz():
    """CLI quiz command runs interactive trivia quiz."""
    result = runner.invoke(app, ["quiz", "--questions", "1"], input="B\n")
    assert result.exit_code == 0
    assert "Quiz Complete!" in result.output or "Correct!" in result.output


def test_cli_cases():
    """CLI cases command displays Supreme Court judgments."""
    result = runner.invoke(app, ["cases", "21"])
    assert result.exit_code == 0
    assert "Maneka Gandhi" in result.output or "Landmark" in result.output


def test_cli_amendments():
    """CLI amendments command displays amendment events."""
    result = runner.invoke(app, ["amendments", "21A"])
    assert result.exit_code == 0
    assert "86th Amendment" in result.output


def test_cli_duties():
    """CLI duties command displays duty cross-references."""
    result = runner.invoke(app, ["duties", "21A"])
    assert result.exit_code == 0
    assert "51A(k)" in result.output
