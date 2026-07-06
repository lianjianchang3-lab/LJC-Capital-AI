#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"
python - <<'PY'
from core.watchlist_center import WatchlistCenter
wc = WatchlistCenter()
wc.add("300059", "东方财富", "测试")
df = wc.list()
print(df)
assert "300059" in set(df["code"])
wc.remove("300059")
df2 = wc.list()
print(df2)
assert "300059" not in set(df2["code"])
print("PASS: 自选股新增/删除/保存正常")
PY
read -p "按回车退出"
