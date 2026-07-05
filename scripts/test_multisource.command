#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.multisource import MultiSourceRealtimeHub
hub = MultiSourceRealtimeHub()
h = hub.health()
print("=== MultiSource Health ===")
print(h)
df = hub.quotes()
print("quotes:", df.shape)
print(df.head())
s = hub.score()
print("score:", s.shape)
print(s.head())
if len(df) <= 0:
    raise SystemExit("FAIL: 没有任何可用数据")
print("PASS: 多源实时系统可用")
PY
read -p "按回车退出"
