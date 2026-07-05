#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v30.watchlist.watchlist_manager import WatchlistManager
from core.pro_v30.portfolio.holding_manager import HoldingManager
from core.pro_v30.dashboard.dashboard_v3 import DashboardV3

w = WatchlistManager()
h = HoldingManager()
d = DashboardV3()

print("watchlist:", w.load().shape)
print(w.load().head())
print("holdings:", h.load().shape)
print(h.load().head())
print("summary:", d.summary())
print("watch_decision:", d.watchlist_decision().shape)
print("portfolio_decision:", d.portfolio_decision().shape)
print("PASS: Pro V3.0 Sprint3 股票管理中心可用")
PY
read -p "按回车退出"
