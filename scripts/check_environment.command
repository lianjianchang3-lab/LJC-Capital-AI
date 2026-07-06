#!/bin/bash
set -e
cd "$HOME/LJC-Capital-AI"
echo "=== LJC V8.5 Final Environment Check ==="
python --version
mkdir -p data/cache data/watchlist data/portfolio logs
test -f app.py && echo "OK app.py"
test -f apps/cockpit.py && echo "OK cockpit"
test -f apps/mobile.py && echo "OK mobile"
test -f scripts/start_desktop.command && echo "OK desktop script"
test -f scripts/start_mobile.command && echo "OK mobile script"
test -d core && echo "OK core"
echo "PASS: environment ready"
read -p "按回车退出"
