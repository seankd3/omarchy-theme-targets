#!/usr/bin/env bash
set -euo pipefail

if python -m pytest --version >/dev/null 2>&1; then
  PYTHONPATH=src python -m pytest -q
elif command -v uv >/dev/null 2>&1; then
  PYTHONPATH=src uv run --no-project --with pytest python -m pytest -q
else
  printf 'pytest is required. Install test dependencies with: python -m pip install -e .[test]\n' >&2
  exit 1
fi
