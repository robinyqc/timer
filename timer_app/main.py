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
        self.root.geometry("300x200")
        self.sound_path = DEFAULT_SOUND

        self.mode = tk.StringVar(value="stopwatch")
        self.night_mode = tk.BooleanVar(value=False)

        self.widgets = []

        self.label = tk.Label(root, text="00:00:00", font=("Arial", 30))
        self.label.pack(pady=10)
        self.widgets.append(self.label)

        self.stopwatch = Stopwatch(self.label)
        self.countdown = Countdown(self.label)

        mode_frame = tk.Frame(root)
        mode_frame.pack()
        self.widgets.append(mode_frame)
        tk.Radiobutton(mode_frame, text="Stopwatch", variable=self.mode, value="stopwatch").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Countdown", variable=self.mode, value="countdown").pack(side=tk.LEFT)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.widgets.append(btn_frame)
        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.widgets.append(self.start_btn)
        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.widgets.append(self.stop_btn)
        self.set_btn = tk.Button(btn_frame, text="Set Time", command=self.set_time)
        self.set_btn.pack(side=tk.LEFT, padx=5)
        self.widgets.append(self.set_btn)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack()
        self.widgets.append(bottom_frame)
        self.sound_btn = tk.Button(bottom_frame, text="铃声", command=self.load_sound)
        self.sound_btn.pack(side=tk.LEFT, padx=5)
        self.widgets.append(self.sound_btn)
        self.night_check = tk.Checkbutton(bottom_frame, text="夜间模式", variable=self.night_mode, command=self.toggle_night)
        self.night_check.pack(side=tk.LEFT)
        self.widgets.append(self.night_check)

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
                messagebox.showwarning("未设置时间", "请先设置倒计时时间")

    def stop(self):
        if self.mode.get() == "stopwatch":
            self.stopwatch.stop()
        else:
            self.countdown.running = False
        self.is_running = False

    def set_time(self):
        t = tk.simpledialog.askstring("设置倒计时时间", "格式为 hh:mm:ss")
        try:
            h, m, s = map(int, t.strip().split(":"))
            self.countdown_seconds = h * 3600 + m * 60 + s
            self.label.config(text=f"{h:02}:{m:02}:{s:02}")
        except:
            messagebox.showerror("格式错误", "请输入正确的时间格式，例如 00:05:00")

    def load_sound(self):
        path = filedialog.askopenfilename(title="选择铃声", filetypes=[("音频文件", "*.wav *.mp3")])
        if path:
            self.sound_path = path

    def toggle_night(self):
        bg = "black" if self.night_mode.get() else "white"
        fg = "white" if self.night_mode.get() else "black"
        self.root.configure(bg=bg)
        for widget in self.widgets:
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass
            for child in widget.winfo_children():
                try:
                    child.configure(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)
                except:
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
