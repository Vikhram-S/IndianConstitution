# Contributing Guidelines

We welcome contributions from developers, researchers, and legal professionals.

## Local Setup

```bash
git clone https://github.com/Vikhram-S/IndianConstitution.git
cd IndianConstitution
pip install -e ".[all]"
```

## Running Tests & Quality Checks

```bash
pytest
ruff check .
mypy src/indianconstitution
```
