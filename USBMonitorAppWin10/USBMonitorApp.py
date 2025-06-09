import tkinter as tk
from tkinter import scrolledtext
import win32con
import win32gui
import win32api
import win32gui_struct
import threading


class USBMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USB 監控程式")
        self.root.geometry("500x300")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        # scrolledtext.ScrolledText：是 tkinter 提供的 文字框加上垂直捲軸。
        # self.root：代表這個文字框屬於主視窗。
        # wrap=tk.WORD：文字到達右邊邊界時會「以單字為單位自動換行」，不會把中文字或英文單字截斷。
        self.text_area.pack(expand=True, fill='both')
        # pack()：是 tkinter 的 版面配置函式，把元件加進介面。
        # expand=True：允許這個元件在視窗大小改變時也隨之「擴展」。
        # fill='both'：讓元件在 水平與垂直方向都填滿空間。
        self.text_area.insert(tk.END, "正在監控 USB 裝置...\n")
        # tk.END：代表「插入到最後一行的末端」。
        # \n：換行符號，確保輸出的文字換行顯示。

        # 啟動背景訊息監聽執行緒
        self.message_thread = threading.Thread(target=self.listen_windows_messages, daemon=True)
        # threading.Thread(...)：Python 的 threading 模組用來執行多執行緒。
        # target=self.listen_windows_messages：指定這個執行緒啟動時要執行的函式，就是你寫的 listen_windows_messages 方法，用來處理 USB 訊息。
        # daemon=True：表示這是一個「守護執行緒」，意思是：
        # 主程式（GUI）關閉時，這個執行緒會自動結束，不會讓程式卡住。
        self.message_thread.start()

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        # insert()	插入訊息到文字區塊末端
        # see()	自動捲到最新那一行
        # 換行 \n	保持訊息清晰分隔

    def listen_windows_messages(self):

        wc = win32gui.WNDCLASS()
        #建立一個視窗類別結構（WNDCLASS），這是 Windows 用來識別「視窗行為和樣式」的資料結構。

        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        #取得目前這個程式的模組實例（instance handle），Windows 用它來識別視窗的擁有者。

        wc.lpszClassName = "USBMonitorHiddenWindow"
        wc.lpfnWndProc = self.win_proc
        # 指定這個視窗要使用的事件處理函式（window procedure），就是你自己定義的 self.win_proc()，用來接收 WM_DEVICECHANGE 訊息。

        class_atom = win32gui.RegisterClass(wc)
        #把這個視窗類別註冊給 Windows 系統使用。

        hwnd = win32gui.CreateWindow(
            wc.lpszClassName,
            "USBMonitorHiddenWindow",
            0,
            0, 0, 0, 0,
            0, 0, hinst, None
        )

        # 註冊裝置通知
        self.register_device_notification(hwnd)

        # 開始訊息處理循環
        win32gui.PumpMessages()
        # 啟動一個無限迴圈，持續等待並處理 Windows 發送來的訊息（例如 USB 插拔事件）。
        # 如果不呼叫這行，這個視窗就無法處理事件，也就完全不會收到插拔通知。

    def win_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DEVICECHANGE:
            if wparam == win32con.DBT_DEVICEARRIVAL:
                self.root.after(0, self.log, "📥 USB 裝置已插入")
            elif wparam == win32con.DBT_DEVICEREMOVECOMPLETE:
                self.root.after(0, self.log, "📤 USB 裝置已移除")
        return True
    # 0：延遲 0 毫秒 → 意思是「儘快排入 UI 事件佇列」。
    # self.log：要呼叫的函式。
    # "📥 USB 裝置已插入"：要傳給 self.log() 的參數。

    #這是定義一個函式，用來註冊「裝置通知」。hwnd 是前面建立的隱藏視窗的 handle，Windows 會透過這個視窗發送通知訊息。
    def register_device_notification(self, hwnd):
        GUID_DEVINTERFACE_USB_DEVICE = "{A5DCBF10-6530-11D2-901F-00C04FB951ED}"
        filter = win32gui_struct.PackDEV_BROADCAST_DEVICEINTERFACE(GUID_DEVINTERFACE_USB_DEVICE)
        win32gui.RegisterDeviceNotification(hwnd, filter, win32con.DEVICE_NOTIFY_WINDOW_HANDLE)


if __name__ == "__main__":
    root = tk.Tk()
    app = USBMonitorApp(root)
    root.mainloop()
