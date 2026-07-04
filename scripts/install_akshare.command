#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
source .venv/bin/activate 2>/dev/null || true
python -m pip install akshare
echo "AKShare 安装完成"
read -p "按回车退出"
