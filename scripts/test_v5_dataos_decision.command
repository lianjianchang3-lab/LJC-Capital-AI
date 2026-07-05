#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.data import MarketDataService
from core.decision import DecisionCore

svc = MarketDataService()
print("health:", svc.health())
df = svc.dataframe()
print("dataframe:", df.shape)
dc = DecisionCore()
print("market:", dc.market())
stocks = dc.stocks()
print("stocks:", stocks.shape)
print(stocks[["code","name","LCRI Score","LCRI Grade","LCRI Evidence"]].head())
plan = dc.trade_plan()
print("plan:", plan.shape)
print(plan[["code","name","Action","Position","Buy Zone","Stop Loss","Target 1"]].head())
print(dc.morning_report())
print("PASS: V5 DataOS + DecisionCore 可用")
PY
read -p "按回车退出"
