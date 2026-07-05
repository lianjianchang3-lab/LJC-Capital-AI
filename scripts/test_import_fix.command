#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v20 import ProDecisionCenter, ProPortfolioCenter, ProWatchlistCenter
from core.pro_v20.decision import ProDecisionCenter as D2
print("ProDecisionCenter:", ProDecisionCenter)
print("Decision submodule:", D2)
print("brief:", ProDecisionCenter().morning_brief())
print("watch:", ProWatchlistCenter().analyze().shape)
print("portfolio:", ProPortfolioCenter().analyze()["summary"])
try:
    from core.pro_v20.report import ProMorningReport
    print("report:", ProMorningReport().build() if ProMorningReport else "None")
except Exception as e:
    print("report skipped:", e)
print("PASS: Pro V2.0 import fix OK")
PY
read -p "按回车退出"
