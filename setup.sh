#!/usr/bin/env bash
# Host preparation only. On Windows PowerShell setup.ps1 is recommended.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
command -v uv >/dev/null || { printf '%s\n' 'Install uv first; see SETUP.md' >&2; exit 1; }
command -v git >/dev/null || { printf '%s\n' 'Install Git first; see SETUP.md' >&2; exit 1; }
uv sync --frozen
uv run --frozen python scripts/setup/bootstrap.py "$@"
uv run --frozen python scripts/setup/doctor.py
