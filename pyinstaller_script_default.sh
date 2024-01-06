#!/usr/bin/env bash

# Install pyinstaller
pyinstaller_version=$(pyinstaller --version 2>/dev/null)
if [ "$pyinstaller_version" != "5.9" ]; then
    pip install pyinstaller==5.9
fi

rm -rf build
rm -rf dist
pyinstaller cli.py --name SimpleAdb --add-data "./assets/*.png:assets" -F