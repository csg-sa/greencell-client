#!/usr/bin/env bash
set -Eeuo pipefail

# ---------------------------------------
# Sphinx docs preview helper
# - creates venv if missing
# - installs doc deps
# - (re)generates API stubs
# - builds HTML
# - serves locally
# ---------------------------------------

# Configuration
PORT="${1:-8000}"
PKG_PATH="${2:-src/greencell_client}"
VENV_DIR=".venv"
DOCS_DIR="docs"
BUILD_DIR="$DOCS_DIR/_build/html"

# Check tools
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python3 doesn't found in PATH." >&2
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo ">>> Create virtual env: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo ">>> Install Sphinx and dependencies"
python -m pip install --upgrade pip >/dev/null
if [[ -f "$DOCS_DIR/requirements.txt" ]]; then
  pip install -r "$DOCS_DIR/requirements.txt"
else
  pip install "sphinx>=7" furo myst-parser sphinx-autodoc-typehints
fi

# (Re)install project in editable mode
if [[ -f "pyproject.toml" || -f "setup.cfg" || -f "setup.py" ]]; then
  echo ">>> Install project in editable (pip install -e .)"
  pip install -e .
fi

mkdir -p "$DOCS_DIR/_static"

if [[ -d "$PKG_PATH" ]]; then
  echo ">>> Generate API files (sphinx-apidoc) from: $PKG_PATH"
  rm -rf "$DOCS_DIR/api"
  sphinx-apidoc -o "$DOCS_DIR/api" "$PKG_PATH" -f
else
  echo ">>> Skip sphinx-apidoc: packet '$PKG_PATH' doesn't exist."
fi

echo ">>> Build HTML documentation (sphinx-build)"
sphinx-build -b html "$DOCS_DIR" "$BUILD_DIR"

# Block Jekyll processing
touch "$BUILD_DIR/.nojekyll"

# Launch local server
echo ">>> Docs available on http://127.0.0.1:$PORT"
echo ">>> (Press Ctrl+C to stop)"
python -m http.server "$PORT" --directory "$BUILD_DIR"
