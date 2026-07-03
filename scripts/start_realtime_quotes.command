#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo "启动实时行情更新，每10秒刷新一次 quotes.csv。按 Ctrl+C 停止。"

while true; do
  python - <<'PY'
from core.realtime import RealtimeQuoteService
print(RealtimeQuoteService().update_quotes())
PY
  sleep 10
done
