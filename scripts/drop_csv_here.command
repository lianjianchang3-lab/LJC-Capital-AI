#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
INBOX="$PROJECT/data/inbox"

mkdir -p "$INBOX"
open "$INBOX"

echo "已打开 data/inbox 文件夹。"
echo "把同花顺 / Moomoo / 东方财富 / 持仓 CSV 拖进去即可。"
echo "App 会自动导入。"

read -p "按回车退出"
