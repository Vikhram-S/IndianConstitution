# Changelog

All notable changes to **IndianConstitution** are documented in this file.

The project follows **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`.

---

## [1.0.1] – 26 January 2026 🇮🇳
### Republic Day Stable Release

This release marks the **first stable (v1.0.0) version** of *IndianConstitution*, signifying API maturity, long-term support intent, and readiness for production, academic, and research use.

---

### ✨ Added

- **Command-Line Interface (CLI)** for direct terminal-based interaction
  - Retrieve articles
  - Search (keyword & fuzzy)
  - Export data
  - View statistics and Preamble

- **Native Pandas / DataFrame Integration**
  - Convert constitutional data to `pandas.DataFrame`
  - Enable NLP, ML, and statistical workflows

- **Advanced Search Capabilities**
  - Regex-based search
  - Fuzzy search with configurable thresholds

- **Export Utilities**
  - Export Constitution data to JSON
  - Export to CSV (via pandas)
  - Export to Markdown

- **Statistical Analysis Tools**
  - Total articles and word counts
  - Average article length
  - Longest and shortest articles

- **Dictionary-like Access**
  - Access articles using `constitution[14]`

---

### 🔧 Improved

- Refined and stabilized public API
- Improved internal data structures for faster access
- Caching mechanisms for performance optimization
- Cleaner separation between core logic and optional features
- Enhanced error handling and input validation

---

### 📚 Documentation

- Completely rewritten README for v1.0.0
- Added usage examples for CLI and DataFrame workflows
- Clear installation paths for PyPI and Conda

---

### 📦 Packaging & Distribution

- Stable **v1.0.0** PyPI release
- Conda package support via custom Anaconda Cloud channel
- Explicit optional dependency groups (`[advanced]`, `[fuzzy]`, `[all]`)

---

### 🧠 Design Notes

- API stability guaranteed within the 1.x series
- Offline-first design (no external API dependencies)
- Minimal core dependencies for reproducibility

---

### ⚠️ Breaking Changes

- None. This is the first stable release.

---

### 🙏 Acknowledgements

Thanks to the open-source community and users who adopted *IndianConstitution* during its pre-1.0 development phase and helped shape this stable release.

---

© 2026 Vikhram S. All rights reserved.

