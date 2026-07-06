#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.mobile_ready import MobileCommander
snap = MobileCommander().snapshot()
print("summary:", snap["summary"])
print("market:", snap["market"])
print("buy:", snap["buy"].shape)
print("risk:", snap["risk"].shape)
print("watchlist:", snap["watchlist"].shape)
print("status:", snap["status"])
print("PASS: V8.5 Build006 手机开盘前稳定版可用")
PY
read -p "按回车退出"
