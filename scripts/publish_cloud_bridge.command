#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python - <<'PY'
from core.cloud_bridge import CloudBridge
print(CloudBridge().publish())
PY

echo "Cloud Bridge 已发布到 cloud/live_state.json"
read -p "按回车退出"
