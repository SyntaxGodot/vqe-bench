.PHONY: help install test lint format type-check clean docs build

help:
	@echo "vqe-bench — available commands:"
	@echo "  make install     Install dependencies (dev + chemistry)"
	@echo "  make test        Run full test suite with coverage"
	@echo "  make fast-test   Run tests, skipping slow benchmarks"
	@echo "  make lint        Run ruff linter"
	@echo "  make format      Auto-format code with ruff"
	@echo "  make type-check  Run mypy static analysis"
	@echo "  make clean       Remove caches and build artifacts"
	@echo "  make docs        Build Sphinx documentation"
	@echo "  make build       Build the distribution package"

install:
	pip install -e ".[dev,chemistry]"

test:
	pytest --cov=vqe_bench --cov-report=term-missing

fast-test:
	pytest -m "not slow" --cov=vqe_bench

lint:
	ruff check src tests

format:
	ruff format src tests
	ruff check --fix src tests

type-check:
	mypy src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

docs:
	cd docs && make html

build:
	python -m build