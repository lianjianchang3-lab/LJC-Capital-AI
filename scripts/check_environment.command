#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
echo "=== LJC V8.5 Environment Check ==="
python --version
test -d core && echo "OK core"
test -d apps && echo "OK apps"
test -d scripts && echo "OK scripts"
mkdir -p data/cache data/watchlist data/portfolio logs
test -f app.py && echo "OK app.py"
test -f scripts/start_desktop.command && echo "OK desktop"
test -f scripts/start_mobile.command && echo "OK mobile"
echo "PASS: environment ready"
read -p "按回车退出"
