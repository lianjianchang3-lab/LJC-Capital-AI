#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v30.commander import CommanderProV5
from core.pro_v30.signal import SignalCenterV5
from core.pro_v30.risk import PortfolioRiskV5
from core.pro_v30.calendar import TradeCalendarV5

s = SignalCenterV5().signals()
print("signals:", s.shape)
print(s[["code","name","信号","信号强度","一句话建议"]].head())

r = PortfolioRiskV5().analyze()
print("risk:", r["summary"])

print(TradeCalendarV5().text())

d = CommanderProV5().dashboard()
print("dashboard:", d["status"], d["mode"], d["risk_level"])
print("PASS: Pro V3.0 Sprint5 机构级决策引擎可用")
PY
read -p "按回车退出"
