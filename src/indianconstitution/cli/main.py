import time
from pathlib import Path

import typer
from rich import print as rprint
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from .. import get_constitution
from . import rich_utils

# Initialize global console
console = Console()

# Sleek ASCII Logo
LOGO = """
  ___           _ _               ___                _   _ _         _   _             
 |_ _|_ __   __| (_) __ _ _ __   / __\\___  _ __  ___| |_(_) |_ _   _| |_(_) ___  _ __  
  | || '_ \\ / _` | |/ _` | '_ \\ / /  / _ \\| '_ \\/ __| __| | __| | | | __| |/ _ \\| '_ \\ 
  | || | | | (_| | | (_| | | | / /__| (_) | | | \\__ \\ |_| | |_| |_| | |_| | (_) | | | |
 |___|_| |_|\\__,_|_|\\__,_|_| |_\\____/\\___/|_| |_|___/\\__|_|\\__|\\__,_|\\__|_|\\___/|_| |_|
"""

def display_header():
    """Displays a beautiful, top-tier logo and creator details."""
    logo_text = Text(LOGO, style="bold gold1")
    
    creator_text = Text()
    creator_text.append("\nAn Elite CLI Tool for the Sovereign Democratic Republic", style="italic cyan")
    creator_text.append("\n\nCreated by: ", style="bold white")
    creator_text.append("Vikhram S", style="bold green")
    creator_text.append(" | Version: 1.1.0\n", style="bold magenta")

    panel = Panel(
        Align.center(logo_text + creator_text),
        border_style="gold1",
        padding=(1, 2),
        title="[bold white]Satyameva Jayate[/bold white]",
        title_align="center"
    )
    console.print(panel)
    console.print()

def get_const_instance():
    """Fetches the constitution instance with a sleek loading animation."""
    with Progress(
        SpinnerColumn(spinner_name="dots", style="gold1"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        progress.add_task(description="[cyan]Initializing Constitution Engine...", total=None)
        time.sleep(0.3)
        return get_constitution()

app = typer.Typer(
    name="indianconstitution",
    help="[bold gold1]Explore the Constitution of India[/bold gold1] with unparalleled elegance.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    epilog="[dim]Designed for legal professionals, scholars, and citizens.[/dim]"
)

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """[bold gold1]IndianConstitution CLI[/bold gold1] - A premium terminal experience.
    """
    if ctx.invoked_subcommand is None:
        display_header()
        rprint(ctx.get_help())

@app.command()
def get(
    number: str = typer.Argument(..., help="Article number (e.g., [cyan]14[/cyan], [cyan]21A[/cyan])"),
):
    """[bold blue]Retrieve[/bold blue] and display a specific article with rich formatting."""
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Fetching Article {number}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.2)
        article = const.get_article(number)
    
    if article:
        rich_utils.print_article(article)
    else:
        console.print(f"[bold red]✖ Error:[/bold red] Article {number} not found.")

@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show")
):
    """[bold green]Search[/bold green] the Constitution for specific keywords or phrases."""
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Searching for '{query}'..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.3)
        results = const.search(query, limit=limit)
    
    if results:
        rich_utils.print_articles_table(results, title=f"✨ Results for '{query}'")
    else:
        console.print(f"[bold yellow]⚠ No articles found matching '{query}'.[/bold yellow]")

@app.command()
def preamble():
    """[bold gold1]Display[/bold gold1] the beautifully formatted Preamble."""
    display_header()
    const = get_const_instance()
    rich_utils.print_preamble(const.preamble)

@app.command()
def export(
    format: str = typer.Argument(..., help="Export format ([cyan]json[/cyan], [cyan]csv[/cyan], [cyan]md[/cyan])"),
    output: Path = typer.Argument(..., help="Output file path")
):
    """[bold red]Export[/bold red] the complete Constitution dataset."""
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Exporting to {format.upper()}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        try:
            const.export(format, output)
            console.print(f"✨ [bold green]Successfully exported to [underline]{output}[/underline][/bold green]")
        except Exception as e:
            console.print(f"[bold red]✖ Failed to export:[/bold red] {e}")

@app.command()
def related(
    number: str = typer.Argument(..., help="Article number")
):
    """[bold magenta]View[/bold magenta] articles referenced by or referencing this article."""
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Finding relationships for Article {number}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.3)
        related = const.get_related_articles(number)
    
    if related["references"]:
        console.print(f"\n[bold cyan]Articles referenced by {number}:[/bold cyan]")
        for ref in related["references"]:
            console.print(f"  [gold1]•[/gold1] Article {ref}")
            
    if related["referenced_by"]:
        console.print(f"\n[bold cyan]Articles referencing {number}:[/bold cyan]")
        for ref in related["referenced_by"]:
            console.print(f"  [gold1]•[/gold1] Article {ref}")
            
    if not related["references"] and not related["referenced_by"]:
        console.print(f"[bold yellow]⚠ No direct relationships found for Article {number}.[/bold yellow]")

@app.command()
def stats():
    """[bold cyan]Discover[/bold cyan] detailed statistics about the Constitution."""
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn("[cyan]Calculating Statistics..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.4)
        articles = const.data.articles
        total_words = sum(len(a.content.split()) for a in articles)
    
    rich_utils.console.print(f"[bold blue]Total Articles:[/bold blue] {len(articles)}")
    rich_utils.console.print(f"[bold blue]Estimated Word Count:[/bold blue] {total_words:,}")

if __name__ == "__main__":
    app()
