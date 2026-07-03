#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python - <<'PY'
from core.health import HealthCheck

h = HealthCheck().run()
print("======================================")
print(" LJC V8.0 Health Check")
print("======================================")
print("Score:", h["score"])
print("OK:", h["ok"])
print("--------------------------------------")
for r in h["results"]:
    status = "✓" if r["ok"] else "✗"
    print(f"{status} [{r['type']}] {r['item']} - {r['message']}")
print("======================================")
PY

read -p "按回车退出"
