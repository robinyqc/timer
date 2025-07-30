import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from timer_app.stopwatch import Stopwatch
from timer_app.countdown import Countdown
from timer_app.utils import play_sound
from timer_app.config import SHORTCUT_KEY, DEFAULT_SOUND
import threading

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.geometry("320x240")
        self.sound_path = DEFAULT_SOUND

        self.lang = tk.StringVar(value="中文")
        self.mode = tk.StringVar(value="stopwatch")

        self.widgets = []

        self.label = tk.Label(root, text="00:00:00", font=("Arial", 30))
        self.label.pack(pady=10)
        self.widgets.append(self.label)

        self.stopwatch = Stopwatch(self.label)
        self.countdown = Countdown(self.label)

        mode_frame = tk.Frame(root)
        mode_frame.pack()
        self.widgets.append(mode_frame)
        self.rbtn_sw = tk.Radiobutton(mode_frame, text="秒表", variable=self.mode, value="stopwatch")
        self.rbtn_cd = tk.Radiobutton(mode_frame, text="倒计时", variable=self.mode, value="countdown")
        self.rbtn_sw.pack(side=tk.LEFT)
        self.rbtn_cd.pack(side=tk.LEFT)
        self.widgets.extend([self.rbtn_sw, self.rbtn_cd])

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.widgets.append(btn_frame)
        self.start_stop_btn = tk.Button(btn_frame, text="开始/停止", command=self.toggle_start_stop)
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)
        self.set_btn = tk.Button(btn_frame, text="设定时间", command=self.set_time)
        if self.mode.get() == "countdown":
            self.set_btn.pack(side=tk.LEFT, padx=5)
        def on_mode_change(*args):
            if self.mode.get() == "countdown":
                self.set_btn.pack(side=tk.LEFT, padx=5)
            else:
                self.set_btn.pack_forget()
        self.mode.trace_add("write", on_mode_change)
        self.reset_btn = tk.Button(btn_frame, text="清零", command=self.reset_stopwatch)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        self.widgets.extend([self.start_stop_btn, self.reset_btn, self.set_btn])

        bottom_frame = tk.Frame(root)
        bottom_frame.pack()
        self.widgets.append(bottom_frame)
        self.sound_btn = tk.Button(bottom_frame, text="铃声", command=self.load_sound)
        self.sound_btn.pack(side=tk.LEFT, padx=5)
        self.lang_btn = tk.Button(bottom_frame, text="Switch to English", command=self.switch_language)
        self.lang_btn.pack(side=tk.LEFT, padx=5)

        self.root.bind(SHORTCUT_KEY, lambda event: self.toggle_start_stop())
        self.is_running = False
        self.countdown_seconds = 0

    def toggle_start_stop(self):
        if self.is_running:
            self.stop()
        else:
            self.start()

    def start(self):
        if self.mode.get() == "stopwatch":
            self.stopwatch.start()
            self.is_running = True
        else:
            if self.countdown_seconds > 0:
                self.countdown.start(self.countdown_seconds, self.sound_path)
                self.is_running = True
            else:
                messagebox.showwarning(self._("未设置时间"), self._("请先设置倒计时时间"))

    def stop(self):
        if self.mode.get() == "stopwatch":
            self.stopwatch.stop()
        else:
            self.countdown.running = False
        self.is_running = False
    
    def reset_stopwatch(self):
        if self.mode.get() == "stopwatch":
            self.stopwatch.reset()
            self.label.config(text="00:00:00")
            self.is_running = False

    def set_time(self):
        t = tk.simpledialog.askstring(self._("设置倒计时时间"), self._("格式为 hh:mm:ss"))
        try:
            h, m, s = map(int, t.strip().split(":"))
            self.countdown_seconds = h * 3600 + m * 60 + s
            self.label.config(text=f"{h:02}:{m:02}:{s:02}")
        except:
            messagebox.showerror(self._("格式错误"), self._("请输入正确的时间格式，例如 00:05:00"))

    def load_sound(self):
        path = filedialog.askopenfilename(title=self._("选择铃声"), filetypes=[("音频文件", "*.wav *.mp3")])
        if path:
            self.sound_path = path

    def switch_language(self):
        self.lang.set("English" if self.lang.get() == "中文" else "中文")
        self._refresh_labels()

    def _refresh_labels(self):
        self.rbtn_sw.config(text=self._("秒表"))
        self.rbtn_cd.config(text=self._("倒计时"))
        self.start_stop_btn.config(text=self._("开始/停止"))
        self.reset_btn.config(text=self._("清零"))
        self.set_btn.config(text=self._("设定时间"))
        self.sound_btn.config(text=self._("铃声"))
        self.lang_btn.config(text=self._("切换为中文") if self.lang.get() == "English" else "Switch to English")

    def _(self, text):
        translations = {
            "秒表": "Stopwatch", "倒计时": "Countdown", "开始/停止": "Start/Stop", 
            "设定时间": "Set Time", "铃声": "Sound",
            "切换为中文": "切换为中文", "格式为 hh:mm:ss": "Format: hh:mm:ss",
            "设置倒计时时间": "Set Countdown Time", "请输入正确的时间格式，例如 00:05:00":
                "Please enter time in correct format, e.g., 00:05:00",
            "格式错误": "Invalid Format", "未设置时间": "Time Not Set", "请先设置倒计时时间":
                "Please set countdown time first", "选择铃声": "Choose Sound", "清零": "reset"
        }
        if self.lang.get() == "中文":
            return text
        return translations.get(text, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
