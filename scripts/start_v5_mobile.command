#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python -m streamlit run apps/v5_mobile.py --server.address 0.0.0.0 --server.port 8501
