#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

echo "======================================"
echo " 启动 LJC Capital AI Pro V8.0"
echo "======================================"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python -m pip install -r requirements.txt >/dev/null 2>&1 || true
streamlit run app.py
