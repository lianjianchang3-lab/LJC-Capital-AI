#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python -m pytest tests/test_v11_rc.py || true
git add .
git commit -m "V11 RC centers one-click release" || true
git push -u origin develop || true
python -m streamlit run apps/v11_rc.py
