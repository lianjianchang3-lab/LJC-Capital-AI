#!/bin/bash
set -e
PROJECT="$HOME/LJC-Capital-AI"
mkdir -p "$PROJECT/data/inbox"
open "$PROJECT/data/inbox"
echo "已打开 data/inbox。请把最新行情/资金/持仓 CSV 放入此文件夹，然后在页面点击导入。"
read -p "按回车退出"
