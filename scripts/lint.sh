#!/bin/bash
# Lint HarmonyØ4 codebase

set -e

echo "Running Black formatter..."
black harmony/ tests/ --check

echo "Running Ruff linter..."
ruff check harmony/ tests/

echo "✅ Lint checks passed"
