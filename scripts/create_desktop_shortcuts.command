#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
DESKTOP="$HOME/Desktop"

cp "$PROJECT/scripts/start_ljc.command" "$DESKTOP/LJC Capital AI.command"
cp "$PROJECT/scripts/update_ljc.command" "$DESKTOP/LJC Update.command"

chmod +x "$DESKTOP/LJC Capital AI.command"
chmod +x "$DESKTOP/LJC Update.command"

echo "已创建桌面快捷方式："
echo "$DESKTOP/LJC Capital AI.command"
echo "$DESKTOP/LJC Update.command"

read -p "按回车退出"
