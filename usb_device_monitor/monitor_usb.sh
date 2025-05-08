#!/bin/bash

# 確保 udevadm 可用
command -v udevadm >/dev/null 2>&1 || { echo >&2 "udevadm 未安裝，請先安裝。"; exit 1; }

echo "開始監控 USB 插入/拔除事件... (Ctrl+C 結束)"

udevadm monitor --udev --subsystem-match=usb | while read line; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $line"
done
