#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo "======================================"
echo " LJC V8.0 Release Check"
echo "======================================"

python -m compileall core services updater >/tmp/ljc_compile.log 2>&1 || {
  echo "Python 编译检查失败："
  cat /tmp/ljc_compile.log
  read -p "按回车退出"
  exit 1
}

python - <<'PY'
from core.health import HealthCheck
h = HealthCheck().run()
print("Health Score:", h["score"])
if h["score"] < 90:
    raise SystemExit("Health check failed")
print("Release Check OK")
PY

echo "======================================"
echo "V8.0 Release Check 通过"
echo "======================================"

read -p "按回车退出"
