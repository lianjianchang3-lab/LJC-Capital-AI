#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
export PYTHONPATH="$PWD"

echo "=================================================="
echo " LJC V8.5 Final Release Check"
echo "=================================================="

echo ""
echo "1. Python 环境"
python --version

echo ""
echo "2. 核心目录"
for d in core apps scripts config data docs; do
  if [ -d "$d" ]; then echo "OK $d"; else echo "MISS $d"; exit 1; fi
done

echo ""
echo "3. 统一启动入口"
for f in app.py scripts/start_desktop.command scripts/start_mobile.command; do
  if [ -f "$f" ]; then echo "OK $f"; else echo "MISS $f"; exit 1; fi
done

echo ""
echo "4. 数据目录"
mkdir -p data/cache data/watchlist data/portfolio logs
echo "OK data/cache"
echo "OK data/watchlist"
echo "OK data/portfolio"
echo "OK logs"

echo ""
echo "5. Python 模块导入检查"
python - <<'PY'
checks = [
    ("TradingCockpit", "from core.cockpit import TradingCockpit"),
    ("WatchlistCenter", "from core.watchlist_center import WatchlistCenter"),
    ("ExecutionCenter", "from core.execution import ExecutionCenter"),
    ("PortfolioCenter", "from core.portfolio_center import PortfolioCenter"),
]
for name, stmt in checks:
    try:
        exec(stmt, {})
        print("OK", name)
    except Exception as e:
        print("FAIL", name, e)
        raise
PY

echo ""
echo "6. 自选股新增/删除/保存检查"
python - <<'PY'
from core.watchlist_center import WatchlistCenter
wc = WatchlistCenter()
wc.add("300059", "东方财富", "release check")
df = wc.list()
assert "300059" in set(df["code"]), "add failed"
wc.remove("300059")
df = wc.list()
assert "300059" not in set(df["code"]), "remove failed"
print("OK watchlist add/remove/save")
PY

echo ""
echo "7. 持仓文件检查"
python - <<'PY'
from pathlib import Path
import pandas as pd
p = Path("data/portfolio/holdings.csv")
p.parent.mkdir(parents=True, exist_ok=True)
if not p.exists():
    pd.DataFrame([{"code":"300059","name":"东方财富","shares":0,"cost":0}]).to_csv(p, index=False)
df = pd.read_csv(p, dtype={"code": str})
for c in ["code","name","shares","cost"]:
    assert c in df.columns, f"missing {c}"
print("OK holdings.csv", df.shape)
PY

echo ""
echo "8. 驾驶舱快照检查"
python - <<'PY'
from core.cockpit import TradingCockpit
snap = TradingCockpit().snapshot()
print("market:", snap.get("market"))
print("buy:", getattr(snap.get("buy"), "shape", None))
print("watchlist:", getattr(snap.get("watchlist"), "shape", None))
print("portfolio:", getattr(snap.get("portfolio"), "shape", None))
assert isinstance(snap, dict)
print("OK cockpit snapshot")
PY

echo ""
echo "9. 文档检查"
for f in README.md CHANGELOG.md docs/INSTALL.md docs/USER_GUIDE.md docs/ARCHITECTURE.md; do
  if [ -f "$f" ]; then echo "OK $f"; else echo "WARN missing $f"; fi
done

echo ""
echo "10. Git 状态"
git status --short || true

echo ""
echo "=================================================="
echo "PASS: LJC V8.5 Final 发布前检查通过"
echo "下一步可执行：git tag v8.5.0 && git push origin v8.5.0"
echo "=================================================="
read -p "按回车退出"
