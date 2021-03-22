#!/usr/bin/env bash

rm -rf build
rm -rf dist
pyinstaller cli.py --name SimpleAdb --add-data "assets/*.png:assets" --hidden-import='sqlalchemy.sql.default_comparator' -F