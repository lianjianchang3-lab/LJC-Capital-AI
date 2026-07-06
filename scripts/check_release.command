#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.cockpit import TradingCockpit
from core.watchlist_center import WatchlistCenter
snap = TradingCockpit().snapshot()
print("version: 8.5.0-final")
print("market:", snap.get("market"))
print("buy:", snap.get("buy").shape)
print("watchlist:", WatchlistCenter().list().shape)
print("PASS: V8.5 Final release check")
PY
read -p "按回车退出"
