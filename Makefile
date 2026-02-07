.PHONY: help install install-dev test test-cov lint format type-check clean

help:
	@echo "Available commands:"
	@echo "  make install          Install the package"
	@echo "  make install-dev      Install the package with dev dependencies"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make lint             Run linting (ruff)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make format-check     Check code formatting without changes"
	@echo "  make type-check       Run type checking (mypy)"
	@echo "  make pre-commit       Run all checks (lint, format-check, type-check)"
	@echo "  make clean            Remove build artifacts and cache files"

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

test:
	uv run pytest

test-cov:
	uv run pytest --cov=tidal_sdk --cov-report=html --cov-report=term-missing

lint:
	uv run ruff check .

format:
	uv run black .
	uv run isort .

format-check:
	uv run black --check .
	uv run isort --check-only .

type-check:
	uv run mypy tidal_sdk

pre-commit: lint format-check type-check
	@echo "All checks passed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .coverage.*
