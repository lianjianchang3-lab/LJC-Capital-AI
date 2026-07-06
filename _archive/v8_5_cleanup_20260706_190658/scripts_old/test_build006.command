#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.build006 import Build006Commander
cmd = Build006Commander()
d = cmd.dashboard()
print("Dashboard:", d)
p = cmd.trading_plan()
print("Plans:", len(p.get("plans", [])))
assert d["status"] in ["OK","NO DATA"]
print("PASS: Build006 AI Commander 可用")
PY
read -p "按回车退出"
