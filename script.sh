#!/bin/bash
rm -rf build dist
python -m PyInstaller pythonserialconsole.spec
cp *.kv dist