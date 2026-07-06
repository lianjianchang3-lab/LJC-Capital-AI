#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.watchlist_center import WatchlistCenter

wc = WatchlistCenter()
wc.add("300059", "东方财富", "测试加入")
df = wc.list()
print("watchlist:", df.shape)
print(df.head())
ana = wc.analyze()
print("analyze:", ana.shape)
print(ana.head())
assert "300059" in set(df["code"])
print("PASS: V8.5 Watchlist Add/Delete 可用")
PY
read -p "按回车退出"
