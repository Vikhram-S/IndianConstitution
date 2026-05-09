import typer
from typing import Optional
from .. import get_constitution
from . import rich_utils

app = typer.Typer(
    help="Explore the Constitution of India with ease.",
    add_completion=True,
    rich_markup_mode="rich"
)

@app.command()
def get(
    number: str = typer.Argument(..., help="Article number (e.g., 14, 21A)"),
):
    """Retrieve and display a specific article."""
    constitution = get_constitution()
    article = constitution.get_article(number)
    if article:
        rich_utils.print_article(article)
    else:
        typer.secho(f"Error: Article {number} not found.", fg=typer.colors.RED)

@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show")
):
    """Search for articles by keyword."""
    constitution = get_constitution()
    results = constitution.search(query, limit=limit)
    if results:
        rich_utils.print_articles_table(results, title=f"Results for '{query}'")
    else:
        typer.secho(f"No results found for '{query}'.", fg=typer.colors.YELLOW)

@app.command()
def preamble():
    """Display the Preamble of the Constitution."""
    constitution = get_constitution()
    rich_utils.print_preamble(constitution.preamble)

@app.command()
def export(
    format: str = typer.Argument(..., help="Export format (json, csv, md)"),
    output: Path = typer.Argument(..., help="Output file path")
):
    """Export the constitution to a file."""
    constitution = get_constitution()
    try:
        constitution.export(format, output)
        typer.secho(f"✓ Successfully exported to {output}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

@app.command()
def related(
    number: str = typer.Argument(..., help="Article number")
):
    """View articles referenced by or referencing this article."""
    constitution = get_constitution()
    related = constitution.get_related_articles(number)
    
    if related["references"]:
        typer.echo(f"\nArticles referenced by {number}:")
        for ref in related["references"]:
            typer.echo(f"  - Article {ref}")
            
    if related["referenced_by"]:
        typer.echo(f"\nArticles referencing {number}:")
        for ref in related["referenced_by"]:
            typer.echo(f"  - Article {ref}")
            
    if not related["references"] and not related["referenced_by"]:
        typer.echo(f"No direct relationships found for Article {number}.")

@app.command()
def stats():
    """Show interesting statistics about the Constitution."""
    constitution = get_constitution()
    articles = constitution.data.articles
    total_words = sum(len(a.content.split()) for a in articles)
    
    rich_utils.console.print(f"[bold blue]Total Articles:[/bold blue] {len(articles)}")
    rich_utils.console.print(f"[bold blue]Estimated Word Count:[/bold blue] {total_words:,}")

if __name__ == "__main__":
    app()
