#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo "启动 Cloud Bridge Publisher，每30秒同步一次。按 Ctrl+C 停止。"

while true; do
  python - <<'PY'
from core.cloud_bridge import CloudBridge
r = CloudBridge().publish()
print("published", r)
PY
  sleep 30
done
