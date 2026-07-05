#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.professional import LCRIPro, InstitutionCenter
lcri = LCRIPro().dataframe()
inst = InstitutionCenter().dataframe()
print("lcri_pro:", lcri.shape)
print(lcri[["code","name","V8动作","V8综合分","胜率估算","V8仓位","第一买点","止损价"]].head())
print("institution:", inst.shape)
if not inst.empty:
    print(inst[["code","name","V8机构热度","资金状态","机构共振指数"]].head())
print(LCRIPro().execution_text(5))
print("PASS: V8 Enterprise Professional 可用")
PY
read -p "按回车退出"
