#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"

echo "=================================================="
echo " Tag LJC V8.5 Final"
echo "=================================================="

git add .
git commit -m "V8.5 Final release readiness" || true
git tag -f v8.5.0
git push origin develop || true
git push origin v8.5.0 --force || true

echo "完成：已创建并推送 tag v8.5.0"
read -p "按回车退出"
