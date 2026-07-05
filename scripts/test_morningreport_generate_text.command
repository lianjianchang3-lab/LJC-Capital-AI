#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20.report import MorningReport, ProMorningReport
r = MorningReport()
print(r.generate_text())
print("PASS: MorningReport generate_text OK")
PY
read -p "按回车退出"
