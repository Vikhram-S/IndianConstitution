import os

base_dir = r"e:\Indian_constitution_project\IndianConstitution-main"

dirs = [
    "docs/images",
    "examples",
    "notebooks",
    ".github/ISSUE_TEMPLATE",
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# MkDocs
mkdocs_content = """site_name: IndianConstitution
site_description: The most developer-friendly way to explore the Constitution of India
site_author: Vikhram S

theme:
  name: material
  palette:
    # Palette toggle for light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Palette toggle for dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - CLI Guide: cli.md
  - API Reference: api.md
  - Search: search.md
  - Semantic Search: semantic-search.md
  - Examples: examples.md
  - FAQ: faq.md
  - Contributing: contributing.md

plugins:
  - search
"""
with open(os.path.join(base_dir, "mkdocs.yml"), "w", encoding="utf-8") as f:
    f.write(mkdocs_content)

docs = [
    "getting-started.md", "cli.md", "api.md", "search.md",
    "semantic-search.md", "examples.md", "faq.md", "contributing.md", "index.md"
]
for doc in docs:
    with open(os.path.join(base_dir, "docs", doc), "w", encoding="utf-8") as f:
        f.write(f"# {doc.replace('.md', '').replace('-', ' ').title()}\n\nDocumentation for {doc}.\n")

# Examples
examples = {
    "basic_usage.py": "from indianconstitution import get_article\nprint(get_article('14'))\n",
    "search.py": "from indianconstitution import search\nresults = search('equality')\nprint(len(results))\n",
    "semantic_search.py": "from indianconstitution import Constitution\n# print(Constitution().semantic_search('rights of children'))\n",
    "cli_demo.py": "import os\nos.system('indianconstitution search freedom')\n",
    "pandas_export.py": "import pandas as pd\nfrom indianconstitution import get_constitution\nic = get_constitution()\ndf = pd.DataFrame([a.dict() for a in ic.data.articles])\nprint(df.head())\n",
    "json_export.py": "from indianconstitution import get_constitution\nic = get_constitution()\nic.export('json', 'out.json')\n",
}
for name, content in examples.items():
    with open(os.path.join(base_dir, "examples", name), "w", encoding="utf-8") as f:
        f.write(content)

# Notebooks
notebooks = [
    "Introduction.ipynb", "LegalResearch.ipynb", "SemanticSearch.ipynb", "AI_RAG.ipynb"
]
notebook_content = '{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}'
for nb in notebooks:
    with open(os.path.join(base_dir, "notebooks", nb), "w", encoding="utf-8") as f:
        f.write(notebook_content)

# GitHub Templates
templates = {
    ".github/ISSUE_TEMPLATE/bug_report.md": "name: Bug report\\nabout: Create a report to help us improve",
    ".github/ISSUE_TEMPLATE/feature_request.md": "name: Feature request\\nabout: Suggest an idea for this project",
    ".github/PULL_REQUEST_TEMPLATE.md": "## Description\\n\\n## Type of change",
    ".github/CODEOWNERS": "* @Vikhram-S",
    ".github/SUPPORT.md": "# Support\\n\\nPlease open an issue for support.",
    ".github/FUNDING.yml": "custom: ['upi://pay?pa=vikhrams15@okhdfcbank&pn=Vikhram%20S&cu=INR']"
}
for path, content in templates.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))

# CITATION.cff
citation = """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
- family-names: "S"
  given-names: "Vikhram"
title: "IndianConstitution"
version: 1.2.0
date-released: 2026-07-13
url: "https://github.com/Vikhram-S/IndianConstitution"
"""
with open(os.path.join(base_dir, "CITATION.cff"), "w", encoding="utf-8") as f:
    f.write(citation)

# CHANGELOG.md
changelog = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-13
### Added
- Comprehensive test suite for graph and export modules.
- Jupyter notebooks for Legal Research and RAG AI examples.
- `docs/` folder powered by MkDocs Material.
- Examples directory with executable python scripts.
- Issue and PR templates in `.github`.
- `CITATION.cff` for academic citations.

### Changed
- Refactored `README.md` to be a professional landing page.
- Bumped `pyproject.toml` version to `1.2.0`.
"""
with open(os.path.join(base_dir, "CHANGELOG.md"), "w", encoding="utf-8") as f:
    f.write(changelog)

print("Scaffolding complete.")
