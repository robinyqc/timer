import time
import tkinter as tk

class Stopwatch:
    def __init__(self, display_label):
        self.display = display_label
        self.running = False
        self.start_time = 0
        self.elapsed = 0

    def start(self):
        self.running = True
        self.start_time = time.time() - self.elapsed
        self._update()

    def stop(self):
        self.running = False

    def _update(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            h, rem = divmod(self.elapsed, 3600)
            m, s = divmod(rem, 60)
            self.display.config(text=f"{int(h):02d}:{int(m):02d}:{int(s):02d}")
            self.display.after(200, self._update)
