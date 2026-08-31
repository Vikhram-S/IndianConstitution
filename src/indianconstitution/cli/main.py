"""Command Line Interface for IndianConstitution package using Typer and Rich."""

import time
from pathlib import Path

import typer
from rich import print as rprint
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from .. import __version__, get_constitution
from ..core.engine import Constitution
from ..exceptions import IndianConstitutionError
from . import rich_utils

console = Console()

LOGO = """
  ___           _ _               ___                _   _ _         _   _             
 |_ _|_ __   __| (_) __ _ _ __   / __\\___  _ __  ___| |_(_) |_ _   _| |_(_) ___  _ __  
  | || '_ \\ / _` | |/ _` | '_ \\ / /  / _ \\| '_ \\/ __| __| | __| | | | __| |/ _ \\| '_ \\ 
  | || | | | (_| | | (_| | | | / /__| (_) | | | \\__ \\ |_| | |_| |_| | |_| | (_) | | | |
 |___|_| |_|\\__,_|_|\\__,_|_| |_\\____/\\___/|_| |_|___/\\__|_|\\__|\\__,_|\\__|_|\\___/|_| |_|
"""


def display_header() -> None:
    """Display CLI header with version metadata."""
    logo_text = Text(LOGO, style="bold gold1")
    creator_text = Text()
    creator_text.append("\nCommand Line Interface for the Constitution of India", style="italic cyan")
    creator_text.append("\n\nAuthor: ", style="bold white")
    creator_text.append("Vikhram S", style="bold green")
    creator_text.append(f" | Version: {__version__}\n", style="bold magenta")

    panel = Panel(
        Align.center(logo_text + creator_text),
        border_style="gold1",
        padding=(1, 2),
        title="[bold white]Constitution of India[/bold white]",
        title_align="center",
    )
    console.print(panel)
    console.print()


def get_const_instance() -> Constitution:
    """Fetch lazy-loaded Constitution instance with status spinner."""
    with Progress(
        SpinnerColumn(spinner_name="dots", style="gold1"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description="[cyan]Initializing Constitution Engine...", total=None)
        time.sleep(0.05)
        return get_constitution()


app = typer.Typer(
    name="indianconstitution",
    help="Programmatic CLI interface for querying and analyzing the Constitution of India.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    epilog="Designed for legal researchers, developers, and citizens.",
)


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context) -> None:
    """IndianConstitution CLI entry point."""
    if ctx.invoked_subcommand is None:
        display_header()
        rprint(ctx.get_help())


@app.command()
def get(
    number: str = typer.Argument(..., help="Article number (e.g., 14, 21A)"),
) -> None:
    """Retrieve and display a specific article."""
    display_header()
    const = get_const_instance()

    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Fetching Article {number}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.05)
        article = const.get_article(number)

    if article:
        rich_utils.print_article(article)
    else:
        console.print(f"[bold red]Error:[/bold red] Article '{number}' not found.")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to return"),
) -> None:
    """Search articles using inverted keyword index."""
    display_header()
    const = get_const_instance()

    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Searching for '{query}'..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.05)
        results = const.search(query, limit=limit)

    if results:
        rich_utils.print_articles_table(results, title=f"Results for '{query}'")
    else:
        console.print(f"[bold yellow]No articles found matching '{query}'.[/bold yellow]")


@app.command()
def preamble() -> None:
    """Display the Preamble text."""
    display_header()
    const = get_const_instance()
    rich_utils.print_preamble(const.preamble)


@app.command()
def export(
    format: str = typer.Argument(..., help="Export format (json, csv, md, gexf, graphml)"),
    output: Path = typer.Argument(..., help="Output file path"),
) -> None:
    """Export constitution dataset to specified file format."""
    display_header()
    const = get_const_instance()

    with Progress(SpinnerColumn(), TextColumn(f"[cyan]Exporting to {format.upper()}..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        try:
            const.export(format, output)
            console.print(f"[bold green]Successfully exported to [underline]{output}[/underline][/bold green]")
        except IndianConstitutionError as e:
            console.print(f"[bold red]Export failed:[/bold red] {e.message}")
        except Exception as e:
            console.print(f"[bold red]Unexpected error during export:[/bold red] {e}")


@app.command()
def related(number: str = typer.Argument(..., help="Article number")) -> None:
    """View cross-references and relationships for an article."""
    display_header()
    const = get_const_instance()

    with Progress(
        SpinnerColumn(), TextColumn(f"[cyan]Finding relationships for Article {number}..."), transient=True
    ) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.05)
        related_data = const.get_related_articles(number)

    if related_data["references"]:
        console.print(f"\n[bold cyan]Articles referenced by {number}:[/bold cyan]")
        for ref in related_data["references"]:
            console.print(f"  [gold1]*[/gold1] Article {ref}")

    if related_data["referenced_by"]:
        console.print(f"\n[bold cyan]Articles referencing {number}:[/bold cyan]")
        for ref in related_data["referenced_by"]:
            console.print(f"  [gold1]*[/gold1] Article {ref}")

    if not related_data["references"] and not related_data["referenced_by"]:
        console.print(f"[bold yellow]No direct relationships found for Article {number}.[/bold yellow]")


@app.command()
def stats() -> None:
    """Calculate and output statistics about the Constitution corpus."""
    display_header()
    const = get_const_instance()

    with Progress(SpinnerColumn(), TextColumn("[cyan]Calculating Statistics..."), transient=True) as progress:
        progress.add_task(description="", total=None)
        time.sleep(0.05)
        articles = const.data.articles
        total_words = sum(len(a.content.split()) for a in articles)

    rich_utils.console.print(f"[bold blue]Total Articles:[/bold blue] {len(articles)}")
    rich_utils.console.print(f"[bold blue]Estimated Word Count:[/bold blue] {total_words:,}")


QUIZ_QUESTIONS = [
    {
        "question": "Which landmark Supreme Court decision established the 'Basic Structure Doctrine'?",
        "options": [
            "A. AK Gopalan (1950)",
            "B. Kesavananda Bharati (1973)",
            "C. Maneka Gandhi (1978)",
            "D. Golaknath (1967)",
        ],
        "answer": "B",
        "explanation": "Kesavananda Bharati v. State of Kerala (1973) held that Parliament cannot alter the basic structure of the Constitution under Article 368.",
    },
    {
        "question": "Which Constitutional Amendment Act inserted Article 21A (Right to Education)?",
        "options": ["A. 42nd Amendment", "B. 44th Amendment", "C. 86th Amendment", "D. 103rd Amendment"],
        "answer": "C",
        "explanation": "The 86th Amendment Act, 2002 inserted Article 21A.",
    },
    {
        "question": "Which article of the Indian Constitution covers the Right to Constitutional Remedies?",
        "options": ["A. Article 14", "B. Article 19", "C. Article 21", "D. Article 32"],
        "answer": "D",
        "explanation": "Article 32 provides the right to move the Supreme Court for enforcement of Fundamental Rights.",
    },
    {
        "question": "In which case did a 9-judge bench affirm the Right to Privacy under Article 21?",
        "options": [
            "A. K.S. Puttaswamy (2017)",
            "B. Shreya Singhal (2015)",
            "C. Minerva Mills (1980)",
            "D. S.R. Bommai (1994)",
        ],
        "answer": "A",
        "explanation": "Justice K.S. Puttaswamy v. Union of India (2017) declared Privacy a fundamental right.",
    },
    {
        "question": "Article 51A (Fundamental Duties) was inserted by which Amendment?",
        "options": ["A. 1st Amendment", "B. 42nd Amendment", "C. 44th Amendment", "D. 73rd Amendment"],
        "answer": "B",
        "explanation": "The 42nd Amendment Act, 1976 added Part IVA and Article 51A.",
    },
]


@app.command()
def quiz(
    questions: int = typer.Option(5, "--questions", "-n", help="Number of questions (1-5)"),
) -> None:
    """Run interactive trivia quiz session."""
    display_header()
    console.print(
        Panel(
            "[bold green]Constitution Knowledge Quiz[/bold green]\n"
            "Test your knowledge of constitutional law, landmark cases, and fundamental rights.",
            title="Interactive Quiz",
        )
    )

    score = 0
    total = min(max(1, questions), len(QUIZ_QUESTIONS))

    for i, q in enumerate(QUIZ_QUESTIONS[:total], 1):
        console.print(f"\n[bold cyan]Question {i}/{total}:[/bold cyan] {q['question']}")
        for opt in q["options"]:
            console.print(f"  {opt}")

        explanation_str = str(q["explanation"])
        user_choice = typer.prompt("Your answer (A/B/C/D)").strip().upper()
        if user_choice == q["answer"]:
            console.print("[bold green]Correct![/bold green] " + explanation_str)
            score += 1
        else:
            console.print(
                f"[bold red]Incorrect.[/bold red] Correct answer is [bold green]{q['answer']}[/bold green]. "
                + explanation_str
            )

    console.print(f"\n[bold gold1]Quiz Complete![/bold gold1] Final Score: [bold green]{score}/{total}[/bold green]")


@app.command()
def cases(
    number: str = typer.Argument(..., help="Article number (e.g. 14, 21, 368)"),
) -> None:
    """View landmark Supreme Court judgments linked to an article."""
    display_header()
    const = get_const_instance()
    cases_list = const.get_related_cases(number)

    if not cases_list:
        console.print(f"[bold yellow]No landmark cases found for Article {number}.[/bold yellow]")
        return

    console.print(f"\n[bold cyan]Landmark Supreme Court Cases for Article {number}:[/bold cyan]\n")
    for c in cases_list:
        console.print(
            Panel(
                f"[bold gold1]{c.case_name}[/bold gold1] ({c.year})\n"
                f"[italic]{c.citation or 'Supreme Court of India'}[/italic] | [dim]{c.bench or ''}[/dim]\n\n"
                f"[bold white]Holding:[/bold white] {c.holding}",
                border_style="cyan",
            )
        )


@app.command()
def amendments(
    number: str = typer.Argument(..., help="Article number (e.g. 19, 21A, 31)"),
) -> None:
    """View amendment history and textual diff for an article."""
    display_header()
    const = get_const_instance()
    events = const.get_amendment_history(number)

    if not events:
        console.print(f"[bold yellow]No amendment history found for Article {number}.[/bold yellow]")
        return

    console.print(f"\n[bold cyan]Amendment History for Article {number}:[/bold cyan]\n")
    for e in events:
        console.print(f"[bold green]{e.amendment_number}[/bold green] ({e.year}): {e.title}")
        console.print(f"  [dim]{e.description}[/dim]\n")

    diff_text = const.diff_amendment(number)
    if diff_text:
        console.print(Panel(diff_text, title=f"Textual Delta (Article {number})", border_style="gold1"))


@app.command()
def duties(
    number: str = typer.Argument(..., help="Article number (e.g. 21A, 14, 32)"),
) -> None:
    """Cross-reference Fundamental Rights to Part IVA Fundamental Duties."""
    display_header()
    const = get_const_instance()
    d_list = const.get_related_duties(number)

    if not d_list:
        console.print(f"[bold yellow]No duty cross-references found for Article {number}.[/bold yellow]")
        return

    console.print(f"\n[bold cyan]Fundamental Duties Cross-References for Article {number}:[/bold cyan]\n")
    for d in d_list:
        console.print(
            Panel(
                f"[bold gold1]Right Article {d.right_article}[/bold gold1] <--> [bold green]{d.duty_clause}[/bold green]\n\n"
                f"[bold white]Duty:[/bold white] {d.duty_text}\n"
                f"[italic dim]Rationale: {d.rationale}[/italic dim]",
                border_style="magenta",
            )
        )


@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port number"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address"),
) -> None:
    """Launch REST API server."""
    display_header()
    try:
        import uvicorn
    except ImportError:
        console.print(
            "[bold red]FastAPI/Uvicorn not installed.[/bold red] Install with: [cyan]pip install 'indianconstitution[api]'[/cyan]"
        )
        return

    console.print(f"[bold green]Starting IndianConstitution REST API server on http://{host}:{port}[/bold green]")
    uvicorn.run("indianconstitution.api.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()
