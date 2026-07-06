#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.cockpit import TradingCockpit
snap = TradingCockpit().snapshot()
print("market:", snap.get("market"))
print("execution:", snap["execution"].shape)
print("portfolio:", snap["portfolio"].shape)
print("watchlist:", snap["watchlist"].shape)
print("buy:", snap["buy"].shape)
print("reduce:", snap["reduce"].shape)
print("plan:")
print(snap["plan_text"])
print("PASS: V8.5 Build005 Trading Cockpit 可用")
PY
read -p "按回车退出"
