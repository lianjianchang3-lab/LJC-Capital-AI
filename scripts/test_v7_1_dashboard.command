#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.enterprise import EnterpriseCommander

snap = EnterpriseCommander().snapshot()
print("summary:", snap.get("summary"))
print("market:", snap.get("market"))
print("lcri_top:", len(snap.get("lcri_top", [])))
print("trader_top:", len(snap.get("trader_top", [])))
print("institution_top:", len(snap.get("institution_top", [])))
print("risk_top:", len(snap.get("risk_top", [])))
assert snap.get("market") is not None
print("PASS: V7.1 Professional Dashboard 可用")
PY
read -p "按回车退出"
