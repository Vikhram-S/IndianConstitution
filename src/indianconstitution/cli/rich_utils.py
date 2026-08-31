"""Rich formatting helper functions for CLI interface."""

from typing import List

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from ..core.models import Article

console = Console()


def print_article(article: Article) -> None:
    """Print an article in a formatted panel.

    Args:
        article: Article object to format and display.
    """
    content = f"# Article {article.number}: {article.title}\n\n{article.content}"
    md = Markdown(content)
    console.print(Panel(md, expand=False, border_style="blue"))


def print_articles_table(articles: List[Article], title: str = "Search Results") -> None:
    """Print a list of articles in a rich table format.

    Args:
        articles: List of Article instances.
        title: Header title for table.
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("No.", style="dim", width=6)
    table.add_column("Title")

    for article in articles:
        table.add_row(str(article.number), article.title)

    console.print(table)


def print_preamble(text: str) -> None:
    """Print the preamble in a formatted panel.

    Args:
        text: Preamble text string.
    """
    console.print(
        Panel(
            Markdown(f"# PREAMBLE\n\n{text}"),
            title="Constitution of India",
            subtitle="Adopted 26 Nov 1949",
            border_style="gold1",
            padding=(1, 2),
        )
    )
