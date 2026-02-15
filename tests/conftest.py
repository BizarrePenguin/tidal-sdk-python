"""Pytest configuration for loading a local `.env` during development.

This module will load `tests/.env` if present and inject variables into
`os.environ` but will NOT override any environment variables that are
already set (so CI-provided secrets take precedence).
"""
from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        # Do not override already-set environment variables
        if key and key not in os.environ:
            os.environ[key] = val


def pytest_configure(config):
    tests_dir = Path(__file__).parent
    dotenv = tests_dir / ".env"
    _load_dotenv(dotenv)
