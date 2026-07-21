#!/usr/bin/env bash
set -euo pipefail

WEEK5_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_SCOPE="${1:-backend/tests}"
PYTHON_BIN="${CS146S_PYTHON:-/root/miniconda3/envs/cs146s/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python)"
fi

cd "$WEEK5_DIR"

printf 'Week 5 quality gate\n'
printf 'Directory: %s\n' "$WEEK5_DIR"
printf 'Python: %s\n' "$PYTHON_BIN"
printf 'Test scope: %s\n\n' "$TEST_SCOPE"

PYTHONPATH=. "$PYTHON_BIN" -m pytest -q "$TEST_SCOPE"
"$PYTHON_BIN" -m ruff check .
"$PYTHON_BIN" -m black --check .
git diff --check

printf '\nQuality gate passed.\n'
