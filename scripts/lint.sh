#!/bin/bash
# Lint HarmonyØ4 codebase

set -e

echo "Running Black formatter..."
black harmony/ tests/ --check

echo "Running Ruff linter..."
ruff check harmony/ tests/

echo "Running mypy type check..."
scripts/type_check.sh

echo "✅ Lint checks passed"
