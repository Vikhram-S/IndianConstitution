import os
import json
import csv
from pathlib import Path
from indianconstitution.export.engine import Exporter
from indianconstitution.core.models import Article

def test_to_json(tmp_path):
    articles = [Article(number="1", title="Name", content="India, that is Bharat")]
    exporter = Exporter(articles)
    out_file = tmp_path / "out.json"
    exporter.to_json(out_file)
    
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["number"] == "1"

def test_to_csv(tmp_path):
    articles = [Article(number="1", title="Name", content="India, that is Bharat")]
    exporter = Exporter(articles)
    out_file = tmp_path / "out.csv"
    exporter.to_csv(out_file)
    
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["number"] == "1"

def test_to_markdown(tmp_path):
    articles = [Article(number="1", title="Name", content="India, that is Bharat")]
    exporter = Exporter(articles)
    out_file = tmp_path / "out.md"
    exporter.to_markdown(out_file)
    
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "## Article 1: Name" in content
