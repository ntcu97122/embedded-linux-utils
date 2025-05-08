#!/bin/bash
#所有 Bash 腳本的開頭標準。

# 確保 udevadm 可用
command -v udevadm >/dev/null 2>&1 || { echo >&2 "udevadm 未安裝，請先安裝。"; exit 1; }
# command -v udevadm：檢查系統中是否有安裝 udevadm 指令。
# >/dev/null 把「標準輸出 stdout」丟進黑洞 /dev/null（= 不顯示在畫面上）
# 2>&1 把「標準錯誤 stderr」也導向到跟標準輸出一樣的地方（即 /dev/null）
# 2 是錯誤輸出的檔案編號，>&1 表示跟「標準輸出（1）」同一個地方
# || { ... }：如果上面那行失敗（也就是沒找到 udevadm），就執行 {} 裡的內容：
# echo >&2：印出錯誤訊息到「錯誤輸出」。
# exit 1：以錯誤碼 1 結束腳本。

echo "開始監控 USB 插入/拔除事件... (Ctrl+C 結束)"
udevadm monitor --udev --subsystem-match=usb | while read line; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $line"
done

# udevadm monitor：啟動即時監控 udev 事件（裝置插拔等）。
# --udev：只監控使用者空間的事件（不包含 kernel 層）。
# --subsystem-match=usb：只針對 USB 裝置的事件。
# | while read line; do：把每一行事件資訊傳入迴圈中逐行處理。
# echo "... | $line"：把時間與事件資訊印在同一行。
# udevadm 是 Linux 系統中 udev 的管理工具，專門用來管理與監控「裝置事件」的指令工具，常見於嵌入式與桌面系統中。
# udevadm = udev admin，用途包括：

# 功能		指令範例					說明
# 即時監控裝置事件	udevadm monitor				監看哪些裝置被插入、移除
# 查看裝置詳細資訊	udevadm info --query=all --name=/dev/sda	顯示裝置的屬性（如廠牌、序號）
# 測試規則是否會觸發	udevadm test /sys/class/usb_device/usb1		模擬事件，測試 udev rule
# 重新載入 udev 設定	udevadm control --reload-rules			編輯完 /etc/udev/rules.d/ 後要 reload

# command -v 是一個 用來確認指令是否存在 的常見 shell 工具指令，在 Bash（和其他 POSIX shell）中非常實用。