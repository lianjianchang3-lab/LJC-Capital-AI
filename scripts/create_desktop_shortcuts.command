#!/bin/bash
set -e

PROJECT="$HOME/LJC-Capital-AI"
DESKTOP="$HOME/Desktop"

cp "$PROJECT/scripts/start_ljc.command" "$DESKTOP/LJC Capital AI.command"
cp "$PROJECT/scripts/update_ljc.command" "$DESKTOP/LJC Update.command"
cp "$PROJECT/scripts/health_check.command" "$DESKTOP/LJC Health Check.command"
cp "$PROJECT/scripts/release_check.command" "$DESKTOP/LJC Release Check.command"
cp "$PROJECT/scripts/drop_csv_here.command" "$DESKTOP/LJC Drop CSV Here.command"
cp "$PROJECT/scripts/publish_cloud_bridge.command" "$DESKTOP/LJC Publish Cloud.command"
cp "$PROJECT/scripts/start_cloud_publisher.command" "$DESKTOP/LJC Cloud Publisher.command"

chmod +x "$DESKTOP/LJC Capital AI.command"
chmod +x "$DESKTOP/LJC Update.command"
chmod +x "$DESKTOP/LJC Health Check.command"
chmod +x "$DESKTOP/LJC Release Check.command"
chmod +x "$DESKTOP/LJC Drop CSV Here.command"
chmod +x "$DESKTOP/LJC Publish Cloud.command"
chmod +x "$DESKTOP/LJC Cloud Publisher.command"

echo "已创建桌面快捷方式。"
read -p "按回车退出"
