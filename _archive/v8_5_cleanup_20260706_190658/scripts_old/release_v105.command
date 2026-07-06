#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python -m pytest tests/test_v105_oneclick.py || true
git add .
git commit -m "V10.1-10.5 continuous one-click deploy" || true
git push -u origin develop || true
python -m streamlit run apps/v105_oneclick.py
