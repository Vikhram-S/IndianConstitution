#!/usr/bin/env python3
"""
Elite Command-line interface for IndianConstitution library.
Provides a breathtaking, top 0.1% terminal experience akin to the Google Gemini CLI.
"""

import sys
import time
from pathlib import Path

# Ensure the src directory is in the path to utilize the new refactored architecture
sys.path.insert(0, str(Path(__file__).parent / "src"))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

try:
    from indianconstitution import get_constitution
    from indianconstitution.cli import rich_utils
except ImportError:
    print("Error: indianconstitution package not found in src/. Please check your installation.")
    sys.exit(1)

# Initialize global console
console = Console()

# Define the Typer app with premium rich styling
app = typer.Typer(
    name="indianconstitution",
    help="[bold gold1]Explore the Constitution of India[/bold gold1] with unparalleled elegance.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    epilog="[dim]Designed for legal professionals, scholars, and citizens.[/dim]"
)

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
    creator_text.append(" | ", style="dim")
    creator_text.append("vikhrams@saveetha.ac.in", style="underline blue")
    creator_text.append(" | ", style="dim")
    creator_text.append("Version: 1.0.0\n", style="bold magenta")

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
        time.sleep(0.4) # Brief pause for premium CLI feel
        return get_constitution()

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """
    [bold gold1]IndianConstitution CLI[/bold gold1] - A premium terminal experience.
    """
    if ctx.invoked_subcommand is None:
        display_header()
        rprint(ctx.get_help())

@app.command(name="get")
def get_article(
    number: str = typer.Argument(..., help="Article number (e.g., [cyan]14[/cyan], [cyan]21A[/cyan])")
):
    """
    [bold blue]Retrieve[/bold blue] and display a specific article with rich formatting.
    """
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Fetching Article {number}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.3)
        article = const.get_article(number)
    
    if article:
        rich_utils.print_article(article)
    else:
        console.print(f"[bold red]✖ Error:[/bold red] Article {number} not found.")

@app.command(name="search")
def search_articles(
    query: str = typer.Argument(..., help="Keyword to search for"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show")
):
    """
    [bold green]Search[/bold green] the Constitution for specific keywords or phrases.
    """
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

@app.command(name="preamble")
def show_preamble():
    """
    [bold gold1]Display[/bold gold1] the beautifully formatted Preamble.
    """
    display_header()
    const = get_const_instance()
    rich_utils.print_preamble(const.preamble)

@app.command(name="related")
def show_related(
    number: str = typer.Argument(..., help="Article number")
):
    """
    [bold magenta]View[/bold magenta] articles referenced by or referencing this article.
    """
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

@app.command(name="stats")
def show_statistics():
    """
    [bold cyan]Discover[/bold cyan] detailed statistics about the Constitution.
    """
    display_header()
    const = get_const_instance()
    
    with Progress(SpinnerColumn(), TextColumn("[cyan]Calculating Statistics..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.5)
        articles = const.data.articles
        total_words = sum(len(a.content.split()) for a in articles)
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold white")
    
    table.add_row("Total Articles", str(len(articles)))
    table.add_row("Estimated Word Count", f"{total_words:,}")
    
    console.print(Panel(table, title="[bold magenta]Constitution Statistics[/bold magenta]", border_style="magenta", expand=False))

@app.command(name="export")
def export_data(
    format: str = typer.Argument(..., help="Format: [cyan]json[/cyan], [cyan]csv[/cyan], or [cyan]md[/cyan]"),
    output: Path = typer.Argument(..., help="Path to save the output file")
):
    """
    [bold red]Export[/bold red] the complete Constitution dataset.
    """
    display_header()
    const = get_const_instance()
    
    valid_formats = ['json', 'csv', 'md']
    if format.lower() not in valid_formats:
        console.print(f"[bold red]✖ Error:[/bold red] Unsupported format '{format}'. Valid formats are: {', '.join(valid_formats)}")
        raise typer.Exit(code=1)
        
    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Exporting to {format.upper()}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        try:
            const.export(format.lower(), output)
        except Exception as e:
            console.print(f"[bold red]✖ Failed to export:[/bold red] {e}")
            raise typer.Exit(code=1)
            
    console.print(f"✨ [bold green]Successfully exported Constitution data to [underline]{output}[/underline][/bold green]")

if __name__ == "__main__":
    app()
