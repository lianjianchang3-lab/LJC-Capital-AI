#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
cd "$PROJECT"

echo "======================================"
echo " 更新 LJC Capital AI Pro V8.0"
echo "======================================"

git checkout develop || true
git pull origin develop || {
  echo "GitHub 网络连接失败，请稍后重试。"
  read -p "按回车退出"
  exit 1
}

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python -m pip install -r requirements.txt >/dev/null 2>&1 || true

echo "更新完成。"
read -p "按回车退出"
