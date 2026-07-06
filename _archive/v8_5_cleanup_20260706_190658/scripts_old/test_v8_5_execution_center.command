#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.execution import ExecutionCenter
from core.professional import LCRIExplain
exe = ExecutionCenter().dataframe()
print("execution:", exe.shape)
print(exe[["code","name","买入优先级","首次建仓","最大允许仓位","风险预算","执行结论"]].head())
exp = LCRIExplain().dataframe()
print("explain:", exp.shape)
print(exp[["code","name","推荐原因","风险原因","解释文本"]].head())
print(ExecutionCenter().text(5))
print("PASS: V8.5 Execution Center 可用")
PY
read -p "按回车退出"
