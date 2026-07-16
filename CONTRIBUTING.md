# Contributing to IndianConstitution

Thank you for considering contributing to `indianconstitution`! This guide describes how to contribute effectively, whether you are a researcher, legal technologist, or software developer.

We hold contributions to a high standard — clear, reproducible, well-tested, and thoroughly documented.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Quality Standards](#code-quality-standards)
- [Running the Test Suite](#running-the-test-suite)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Pull Request Checklist](#pull-request-checklist)
- [Reporting Bugs](#reporting-bugs)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to a welcoming, inclusive, and harassment-free environment.

---

## How to Contribute

### 🐛 Reporting Bugs

1. Search [existing issues](https://github.com/Vikhram-S/IndianConstitution/issues) first
2. Use the **Bug Report** issue template
3. Include: Python version, OS, `indianconstitution.__version__`, and a minimal reproducible example

### 💡 Suggesting Enhancements

1. Open a [Feature Request](https://github.com/Vikhram-S/IndianConstitution/issues/new?template=feature_request.md)
2. Explain the use case, expected behaviour, and any related research context

### 📚 Data Corrections

If you find an inaccuracy in the constitutional corpus (`constitution.json`), please:
1. Reference the official [Ministry of Law and Justice](https://legislative.gov.in/) source
2. Open an issue with the article number, field, current value, and correct value

---

## Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/IndianConstitution.git
cd IndianConstitution

# 2. Create a virtual environment (Python 3.9+ recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install with all development dependencies
pip install -e ".[dev,data,ai]"

# 4. Install pre-commit hooks
pre-commit install
```

---

## Code Quality Standards

This project enforces **research-grade code quality**:

| Tool | Standard | Config |
|:---|:---|:---|
| **Ruff** | Linting + formatting | `[tool.ruff]` in `pyproject.toml` |
| **Mypy** | Strict type checking | `[tool.mypy]` — `strict = true` |
| **Pytest** | Unit + property-based tests | `[tool.pytest.ini_options]` |
| **Hypothesis** | Property-based testing | Used in `tests/` |
| **Coverage** | ≥ 80% line + branch | `[tool.coverage]` |

**All public API functions must have:**
- Full type annotations (enforced by mypy strict mode)
- Google-style docstrings (enforced by ruff `D` rules)
- At least one unit test and one Hypothesis property test where applicable

---

## Running the Test Suite

```bash
# Run all tests with coverage
pytest

# Run a specific test file
pytest tests/test_core.py -v

# Run only fast tests (exclude slow property-based tests)
pytest -m "not slow"

# Run with parallel workers (faster on multi-core)
pytest -n auto

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Auto-fix lint issues
ruff check --fix src/
```

### Coverage Requirements

- **Minimum**: 80% line coverage (enforced by CI — PRs will fail below this threshold)
- **Target**: 90%+ for all new code contributions

---

## Pre-commit Hooks

The repository uses `pre-commit` to enforce quality gates before every commit:

```bash
# Install hooks (one-time setup)
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

Hooks include: `ruff` (lint + format), `mypy` (type check), `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`.

---

## Pull Request Checklist

Before opening a PR, verify:

- [ ] Tests pass locally: `pytest`
- [ ] Type checking passes: `mypy src/`
- [ ] Linting passes: `ruff check src/`
- [ ] New functionality has corresponding tests (unit + Hypothesis where applicable)
- [ ] Public API changes have Google-style docstrings
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]` describing the change
- [ ] The PR title follows [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

### PR Size Guidelines

| Type | Recommended Size |
|:---|:---|
| Bug fix | < 100 lines changed |
| New feature | < 300 lines changed; split if larger |
| Refactor | Discuss in an issue first |
| Docs only | Any size |

---

## Branch Strategy

- `main` — protected; only merges via PR with CI passing
- `feat/<name>` — feature branches
- `fix/<name>` — bug fix branches
- `docs/<name>` — documentation-only branches

---

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat(search): add wildcard support to inverted index
fix(export): handle empty schedules in CSV export
docs(readme): add RAG pipeline example
test(graph): add Hypothesis property test for centrality
```

---

*Questions? Open a [Discussion](https://github.com/Vikhram-S/IndianConstitution/discussions) or email [vikhrams@saveetha.ac.in](mailto:vikhrams@saveetha.ac.in).*
