#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.monday_realtime import MondayRealtimeSystem
import pandas as pd
rt = MondayRealtimeSystem()
result = rt.smoke_test()
print("=== LJC Monday Realtime Smoke Test ===")
print(result["health"])
for c in result["checks"]:
    print(c)
if result["health"]["rows"] <= 0:
    raise SystemExit("没有可用行情数据，请检查网络或CSV备用文件")
print("PASS: Monday realtime system is usable")
PY
read -p "按回车退出"
