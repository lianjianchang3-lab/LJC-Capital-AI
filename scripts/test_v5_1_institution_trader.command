#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.institution import InstitutionEngine
from core.trader import AITrader
inst = InstitutionEngine().run()
print("institution:", inst.shape)
print(inst[["code","name","机构共振指数","机构评级","机构动作","机构证据"]].head())
sig = AITrader().signals()
print("signals:", sig.shape)
print(sig[["code","name","执行建议","AI交易强度","建议仓位V5","第一买点","止损价","第一止盈"]].head())
print(AITrader().today_plan_text())
print("PASS: V5.1 Institution Engine + AI Trader 可用")
PY
read -p "按回车退出"
