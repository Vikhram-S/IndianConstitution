import csv
import json
from pathlib import Path
from typing import List, Union

from ..core.models import Article


class Exporter:
    """Handles exporting constitution data to various formats."""

    def __init__(self, articles: List[Article]):
        self.articles = articles

    def to_json(self, path: Union[str, Path]):
        """Export articles to a JSON file."""
        data = [a.dict() for a in self.articles]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_csv(self, path: Union[str, Path]):
        """Export articles to a CSV file."""
        if not self.articles:
            return

        fieldnames = ["number", "title", "content"]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in self.articles:
                writer.writerow({"number": a.number, "title": a.title, "content": a.content})

    def to_markdown(self, path: Union[str, Path]):
        """Export articles to a Markdown file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Constitution of India\n\n")
            for a in self.articles:
                f.write(f"## Article {a.number}: {a.title}\n\n")
                f.write(f"{a.content}\n\n")
                f.write("---\n\n")
