#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python - <<'PY'
from core.realtime import RealtimeQuoteService
print(RealtimeQuoteService().update_quotes())
PY

read -p "按回车退出"
