# Contributing to IndianConstitution

First off, thank you for considering contributing to `indianconstitution`! It's people like you that make this library better for everyone.

## How Can I Contribute?

### Reporting Bugs
- Use the GitHub Issue Tracker.
- Describe the bug and include steps to reproduce.

### Suggesting Enhancements
- Open a feature request on GitHub.
- Explain why the feature would be useful.

### Pull Requests
1. Fork the repo.
2. Create a branch: `git checkout -b feature/my-new-feature`.
3. Make your changes.
4. Run tests: `pytest`.
5. Run linting: `ruff check .`.
6. Commit your changes: `git commit -am 'Add some feature'`.
7. Push to the branch: `git push origin feature/my-new-feature`.
8. Submit a pull request.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/vikhram-s/indianconstitution
cd indianconstitution

# Install dependencies with dev extras
pip install -e ".[dev,data,ai]"
```

## Code Style
We use **Ruff** for linting and **Black** (via Ruff) for formatting. Please ensure your code follows the established style.
