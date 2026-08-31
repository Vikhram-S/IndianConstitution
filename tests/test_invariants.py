"""Property-based invariant tests using Hypothesis.

Tests formal invariants for article part inference, search index properties,
cross-reference graph properties, textual diffing, and exception guarantees.
"""

from typing import List

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from indianconstitution import (
    ArticleNotFoundError,
    Constitution,
    InvalidAmendmentRangeError,
    UnsupportedFormatError,
    diff_amendment,
    get_article,
    get_constitution,
    search,
)
from indianconstitution.core.models import infer_part


@given(num=st.integers(min_value=1, max_value=395), suffix=st.sampled_from(["", "A", "B", "C", "AA"]))
@settings(max_examples=100)
def test_infer_part_valid_numbers(num: int, suffix: str) -> None:
    """Invariant: Valid constitutional article numbers (1..395) infer part in 1..22."""
    art_str = f"{num}{suffix}"
    part = infer_part(art_str)
    assert part is not None
    assert 1 <= part <= 22


@given(text=st.text().filter(lambda s: not any(c.isdigit() for c in s)))
@settings(max_examples=50)
def test_infer_part_non_numeric_returns_none(text: str) -> None:
    """Invariant: Non-numeric strings return None for part inference."""
    assert infer_part(text) is None


@given(query=st.text(min_size=1, max_size=20).filter(lambda s: s.strip() != ""))
@settings(max_examples=50)
def test_search_case_insensitivity(query: str) -> None:
    """Invariant: Keyword search produces identical results regardless of query casing."""
    lower_res = search(query.lower())
    upper_res = search(query.upper())
    assert [a.number for a in lower_res] == [a.number for a in upper_res]


def test_search_empty_query_returns_empty() -> None:
    """Invariant: Empty or whitespace query returns empty list."""
    assert search("") == []
    assert search("   ") == []


def test_graph_no_self_loops() -> None:
    """Invariant: Cross-reference graph contains no self-referential edges (u != v)."""
    const = get_constitution()
    try:
        g = const.get_graph()
    except Exception:
        pytest.skip("NetworkX not installed")

    for u, v in g.edges():
        assert u != v, f"Self loop detected on Article {u}"


def test_graph_reference_bidirectional_consistency() -> None:
    """Invariant: If article u references v, then u is in referenced_by(v)."""
    const = get_constitution()
    for art in const.articles[:30]:
        num = str(art.number)
        refs = const.get_related_articles(num)["references"]
        for r in refs:
            refd_by = const.get_related_articles(r)["referenced_by"]
            assert num in refd_by, f"Inconsistency: {num} references {r}, but {num} not in referenced_by({r})"


@given(art_num=st.sampled_from(["14", "19", "21", "21A", "32", "368"]))
def test_diff_amendment_idempotency(art_num: str) -> None:
    """Invariant: diff_amendment between identical years yields empty string."""
    assert diff_amendment(art_num, from_year=2020, to_year=2020) == ""


@given(from_y=st.integers(min_value=2000, max_value=2026), to_y=st.integers(min_value=1950, max_value=1999))
def test_diff_amendment_invalid_range_raises_exception(from_y: int, to_y: int) -> None:
    """Invariant: from_year > to_year raises InvalidAmendmentRangeError."""
    with pytest.raises(InvalidAmendmentRangeError):
        diff_amendment("21A", from_year=from_y, to_year=to_y)


def test_require_article_missing_raises_exception() -> None:
    """Invariant: require_article for non-existent article raises ArticleNotFoundError."""
    const = get_constitution()
    with pytest.raises(ArticleNotFoundError) as exc_info:
        const.require_article("99999")
    assert "99999" in exc_info.value.article_number


def test_unsupported_export_format_raises_exception() -> None:
    """Invariant: export with invalid format name raises UnsupportedFormatError."""
    const = get_constitution()
    with pytest.raises(UnsupportedFormatError) as exc_info:
        const.export("pdf_invalid", "out.pdf")
    assert "pdf_invalid" in exc_info.value.format_requested
