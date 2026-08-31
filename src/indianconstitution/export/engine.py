"""Multi-format export engine for constitution data.

Supports JSON, CSV, and Markdown output formats.
"""

import csv
import json
from pathlib import Path
from typing import List, Union

from ..core.models import Article


class Exporter:
    """Handles exporting constitution data to various file formats.

    Attributes:
        articles: List of Article instances to export.
    """

    def __init__(self, articles: List[Article]) -> None:
        """Initialize Exporter with article list.

        Args:
            articles: List of Article objects.
        """
        self.articles: List[Article] = articles

    def to_json(self, path: Union[str, Path]) -> None:
        """Export articles to a JSON file.

        Args:
            path: Destination file path.
        """
        data = [a.model_dump() for a in self.articles]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_csv(self, path: Union[str, Path]) -> None:
        """Export articles to a CSV file.

        Args:
            path: Destination file path.
        """
        fieldnames = ["number", "title", "content", "part", "chapter"]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in self.articles:
                writer.writerow(
                    {
                        "number": a.number,
                        "title": a.title,
                        "content": a.content,
                        "part": a.part,
                        "chapter": a.chapter,
                    }
                )

    def to_markdown(self, path: Union[str, Path]) -> None:
        """Export articles to a Markdown document.

        Args:
            path: Destination file path.
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Constitution of India\n\n")
            for a in self.articles:
                f.write(f"## Article {a.number}: {a.title}\n\n")
                f.write(f"{a.content}\n\n")
                f.write("---\n\n")
