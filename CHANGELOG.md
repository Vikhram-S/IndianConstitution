# Changelog

All notable changes to `indianconstitution` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Transformer-based semantic search via `sentence-transformers` (optional `[ai]` extra).
- Amendment timeline API: retrieve constitutional history per article.
- Hindi language support for the preamble and article summaries.
- Async I/O adapter (`asyncio`-compatible data loading for FastAPI/Starlette apps).
- Zenodo DOI registration for persistent academic citation.

---

## [1.3.0] - 2026-07-16

### Added
- **Elite README**: Research-grade landing page with Abstract section, RAG pipeline examples,
  reproducibility checklist for NeurIPS/ACL/EMNLP authors, Acknowledgements, and social badges.
- **ACL-format citation**: Added ACL Anthology citation format alongside BibTeX, APA, and IEEE.
- **Enhanced CITATION.cff**: Upgraded to full CFF 1.2.0 schema with `identifiers`, `references`
  (5 entries including Smith et al. 2016 software citation principles), and `preferred-citation`.
- **Extended PyPI keywords**: Added `constitutional-informatics`, `legal-ai`, `civic-ai`,
  `semantic-search`, `inverted-index`, `research-software`, `reproducibility`, `legal-tech`.
- **Enhanced classifiers**: Added `Information Technology` audience, `Text Processing :: Indexing`,
  `Internet :: WWW/HTTP :: Indexing/Search`, `Natural Language :: English`,
  and `Programming Language :: Python :: 3 :: Only`.
- **Improved SECURITY.md**: Updated supported versions table to cover v1.2.x and v1.3.x.
- **Improved CONTRIBUTING.md**: Full NeurIPS-style development guide with pre-commit hooks,
  Hypothesis property-based testing, coverage requirements, and PR checklist.

### Changed
- Description in `pyproject.toml` expanded to highlight NLP, RAG, civic AI, and informatics.
- README benchmarks table now includes semantic search latency (`[ai]` extra).
- README architecture diagram expanded with `Amendment` model node.
- CITATION.cff abstract expanded to match publication-quality abstract standards.

---

## [1.2.2] - 2026-07-14

### Fixed
- Pinned all GitHub Actions to SHA hashes for OSSF Scorecard compliance (supply-chain security).
- Resolved `scipy`/`networkx` version conflicts in CI matrix on Python 3.13.
- Stabilised `mypy` strict-mode type checking pass across all public APIs.

### Changed
- `CITATION.cff` upgraded to full CFF 1.2.0 schema with abstract, keywords, and references.
- CI matrix now includes Python 3.13.

---

## [1.2.1] - 2026-07-13

### Fixed
- Corrected `ConstitutionData` field aliasing in legacy flat-list JSON loader.
- Removed erroneous duplicate article entries caused by preamble mis-classification.

### Changed
- Documentation workflow now caches MkDocs Material assets per ISO week number.

---

## [1.2.0] - 2026-07-13

### Added
- Comprehensive test suite: `test_core.py`, `test_export.py`, `test_graph.py`.
- Jupyter notebooks: `legal_research.ipynb`, `rag_ai_integration.ipynb`.
- `docs/` directory powered by MkDocs Material.
- `examples/` directory with executable Python scripts.
- GitHub Issue/PR templates and `CODEOWNERS`.
- `CITATION.cff` for academic citation.
- `SECURITY.md` and `CODE_OF_CONDUCT.md`.

### Changed
- Refactored `README.md` to a professional research landing page.
- Bumped package version to `1.2.0`.

---

## [1.1.0] - 2026-06-01

### Added
- `Constitution.export()`: multi-format export to JSON, CSV, and Markdown.
- `ConstitutionGraph`: NetworkX-backed relational graph for cross-article reference analysis.
- `[data]` optional extra: `pandas`, `networkx`, `scipy`.
- CLI sub-commands: `get`, `search`, `stats`.

### Changed
- Migrated build system from `setuptools` to `hatchling`.
- Replaced flat `setup.py` with `pyproject.toml` (PEP 517/518 compliant).

---

## [1.0.0] - 2026-04-15

### Added
- Initial public release on PyPI.
- `Constitution` class with lazy-loading and inverted-index keyword search.
- Pydantic v2 data models: `Article`, `Part`, `Schedule`, `ConstitutionData`.
- Package-level convenience functions: `get_article()`, `search()`, `get_constitution()`.
- CLI entry point (`indianconstitution`) powered by Typer + Rich.
- Apache-2.0 license.

[Unreleased]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Vikhram-S/IndianConstitution/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Vikhram-S/IndianConstitution/releases/tag/v1.0.0
