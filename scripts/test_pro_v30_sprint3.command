#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v30 import PortfolioCenterV3, MorningBriefPro, TradeLogbook
p = PortfolioCenterV3().analyze()
print("portfolio:", p["summary"])
print(p["table"].head())
m = MorningBriefPro()
print(m.text())
log = TradeLogbook()
print("log rows:", log.read().shape)
print("PASS: Pro V3.0 Sprint3 股票管理中心可用")
PY
read -p "按回车退出"
