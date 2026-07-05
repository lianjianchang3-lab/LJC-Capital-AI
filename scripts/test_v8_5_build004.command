#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.enterprise import EnterpriseCommander
from core.execution import ExecutionCenter
from core.portfolio_center import PortfolioCenter
from core.watchlist_center import WatchlistCenter

snap = EnterpriseCommander().snapshot()
exe = ExecutionCenter().dataframe()
pf = PortfolioCenter().analyze()
wl = WatchlistCenter().analyze()

print("market:", snap.get("market"))
print("execution:", exe.shape)
print("portfolio:", pf.shape)
print("watchlist:", wl.shape)
print("PASS: V8.5 Build004 Stable Terminal 可用")
PY
read -p "按回车退出"
