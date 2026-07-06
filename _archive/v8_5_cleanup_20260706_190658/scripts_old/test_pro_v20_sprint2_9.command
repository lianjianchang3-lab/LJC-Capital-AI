#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20.trading import TradePlanEngine
from core.pro_v20.scanner import MarketScanner
from core.pro_v20.alerts import AlertCenter
from core.pro_v20.review import ReviewCenter
from core.pro_v20.report import MorningReport

plans = TradePlanEngine().plans()
print("plans", plans.shape)
print(plans.head())
scan = MarketScanner().scan()
print("scan", scan.shape)
alerts = AlertCenter().generate()
print("alerts", alerts[:5])
text = MorningReport().generate_text()
print(text[:500])
print(ReviewCenter().summary())
assert hasattr(plans, "shape")
print("PASS: Pro V2.0 Sprint2-9 可用")
PY
read -p "按回车退出"
