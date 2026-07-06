#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.pro_v40 import V40Commander, UnifiedAIEngine, InstitutionSignalCenter, PositionController, LearningCenter

df = UnifiedAIEngine().run()
print("engine:", df.shape)
print(df[["code","name","Unified AI Score","统一建议","证据链"]].head())

sig = InstitutionSignalCenter().signals()
print("signals:", sig.shape)
print(sig[["code","name","机构信号","执行动作"]].head())

pos = PositionController().allocation()
print("position:", pos["summary"])

dash = V40Commander().dashboard()
print("dashboard:", dash["state"])

print("learning:", LearningCenter().stats())
print("PASS: Pro V4.0 Unified Commander 可用")
PY
read -p "按回车退出"
