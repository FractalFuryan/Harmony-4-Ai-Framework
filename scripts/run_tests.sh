#!/bin/bash
# Run HarmonyØ4 test suite

set -e

echo "Running pytest with coverage..."
pytest --cov=harmony --cov-report=term-missing --cov-report=html -v

echo "✅ All tests passed"
