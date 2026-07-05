#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.enterprise import DecisionHub, EnterpriseCommander
from core.radar import MarketRadar

hub = DecisionHub()
print("market:", hub.market())

radar = MarketRadar()
print("health:", radar.health())
print("lcri_top:", radar.lcri_top(5).shape)
print("trader_top:", radar.trader_top(5).shape)
print("institution_top:", radar.institution_top(5).shape)

snap = EnterpriseCommander().snapshot()
print("services:", snap["services"])
print("configs:", snap["configs"])
print("summary:", snap["summary"])

print("PASS: V7 EnterpriseHub + MarketRadar 可用")
PY
read -p "按回车退出"
