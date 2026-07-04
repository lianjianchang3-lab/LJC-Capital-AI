#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python -m streamlit run apps/v83_build500_ai_decision.py --server.address 0.0.0.0
