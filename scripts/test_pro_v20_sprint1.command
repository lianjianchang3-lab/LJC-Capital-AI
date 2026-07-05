#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20 import ProDecisionCenter, ProWatchlistCenter, ProPortfolioCenter, ProConfigCenter
print("watchlist", ProConfigCenter().watchlist().shape)
print("holdings", ProConfigCenter().holdings().shape)
brief = ProDecisionCenter().morning_brief()
print("brief", brief)
watch = ProWatchlistCenter().analyze()
print("watch", watch.shape)
portfolio = ProPortfolioCenter().analyze()
print("portfolio", portfolio["status"], portfolio["summary"])
print("PASS: Pro V2.0 Sprint1 可用")
PY
read -p "按回车退出"
