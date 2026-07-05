#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20.report import MorningReport, ProMorningReport
print("MorningReport:", MorningReport)
print("ProMorningReport:", ProMorningReport)
print(MorningReport().build())
print("PASS: MorningReport import fix OK")
PY
read -p "按回车退出"
