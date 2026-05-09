from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from ..core.models import Article

console = Console()

def print_article(article: Article):
    """Print an article in a beautiful panel."""
    content = f"# Article {article.number}: {article.title}\n\n{article.content}"
    md = Markdown(content)
    console.print(Panel(md, expand=False, border_style="blue"))

def print_articles_table(articles: List[Article], title: str = "Search Results"):
    """Print a list of articles in a table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("No.", style="dim", width=6)
    table.add_column("Title")
    
    for article in articles:
        table.add_row(str(article.number), article.title)
        
    console.print(table)

def print_preamble(text: str):
    """Print the preamble in a premium panel."""
    console.print(Panel(
        Markdown(f"# PREAMBLE\n\n{text}"),
        title="Constitution of India",
        subtitle="Adopted 26 Nov 1949",
        border_style="gold1",
        padding=(1, 2)
    ))
