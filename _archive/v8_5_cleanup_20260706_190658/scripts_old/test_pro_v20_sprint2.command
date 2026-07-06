#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20.commander import CommanderCenterV2
from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
from core.pro_v20.alerts.alert_engine_v2 import AlertEngineV2
d = CommanderCenterV2().dashboard()
print("dashboard:", d)
p = TradePlannerV2().plan()
print("plan:", p.shape)
print(p.head())
a = AlertEngineV2().scan()
print("alerts:", a.shape)
print(a.head())
assert d["status"] in ["OK","NO DATA"]
print("PASS: Pro V2.0 Sprint2 可用")
PY
read -p "按回车退出"
