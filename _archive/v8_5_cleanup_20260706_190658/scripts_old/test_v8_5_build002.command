#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.portfolio_center import PortfolioCenter
from core.watchlist_center import WatchlistCenter
from core.daily_plan import DailyPlan

pf = PortfolioCenter().analyze()
wl = WatchlistCenter().analyze()
plan = DailyPlan().generate()

print("portfolio:", pf.shape)
print(pf.head())
print("watchlist:", wl.shape)
print(wl.head())
print("daily plan:")
print(plan["text"])
print("PASS: V8.5 Build002 Portfolio + Watchlist + DailyPlan 可用")
PY
read -p "按回车退出"
