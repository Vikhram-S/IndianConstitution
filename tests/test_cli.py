"""Tests for the IndianConstitution CLI interface."""

from pathlib import Path

from typer.testing import CliRunner

from indianconstitution.cli.main import app

runner = CliRunner()


def test_cli_help():
    """CLI prints help menu."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Explore the Constitution of India" in result.output


def test_cli_get():
    """CLI get command retrieves an article."""
    result = runner.invoke(app, ["get", "14"])
    assert result.exit_code == 0
    assert "Article 14" in result.output or "Equality" in result.output


def test_cli_get_invalid():
    """CLI get command handles non-existent article."""
    result = runner.invoke(app, ["get", "9999Z"])
    assert result.exit_code == 0
    assert "not found" in result.output


def test_cli_search():
    """CLI search command finds matching articles."""
    result = runner.invoke(app, ["search", "equality", "--limit", "3"])
    assert result.exit_code == 0
    assert "equality" in result.output.lower() or "Results" in result.output


def test_cli_search_no_results():
    """CLI search handles queries with zero matches."""
    result = runner.invoke(app, ["search", "xyznonexistent123"])
    assert result.exit_code == 0
    assert "No articles found" in result.output


def test_cli_preamble():
    """CLI preamble command displays preamble."""
    result = runner.invoke(app, ["preamble"])
    assert result.exit_code == 0
    assert "PREAMBLE" in result.output or "PEOPLE OF INDIA" in result.output


def test_cli_stats():
    """CLI stats command displays statistics."""
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "Total Articles" in result.output


def test_cli_related():
    """CLI related command displays cross-references."""
    result = runner.invoke(app, ["related", "32"])
    assert result.exit_code == 0


def test_cli_export(tmp_path: Path):
    """CLI export command exports dataset."""
    out_file = tmp_path / "out.json"
    result = runner.invoke(app, ["export", "json", str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()

