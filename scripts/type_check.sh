#!/bin/bash
# Type-check HarmonyØ4 with the workspace venv to avoid missing stubs.

set -e

VENV_PY="$(pwd)/.venv/bin/python"
if [[ -x "$VENV_PY" ]]; then
  "$VENV_PY" -m mypy harmony
else
  python -m mypy harmony
fi
