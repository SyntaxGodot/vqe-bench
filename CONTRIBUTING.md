# Contributing to vqe-bench

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs
Open an issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (`python --version`, `pip list | grep qiskit`)

### 💡 Suggesting Enhancements
Open an issue with:
- The motivation behind the enhancement
- A clear description of the desired behavior
- Any alternative solutions you've considered

### 🔧 Pull Requests
1. Fork the repo and create your branch from `main`.
2. Install dependencies: `make install`
3. Set up pre-commit hooks: `pre-commit install`
4. Make your changes and add tests.
5. Ensure the test suite passes: `make test`
6. Ensure linting passes: `make lint && make type-check`
7. Open the PR!

## Style Guidelines
- Follow PEP 8 (enforced by `ruff`)
- Use type hints (enforced by `mypy`)
- Write docstrings in Google format
- Keep PRs focused on a single feature

## Code of Conduct
Be respectful. We're all here to learn and build great software.