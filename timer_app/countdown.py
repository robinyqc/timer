import tkinter as tk
import threading
from timer_app.utils import play_sound
from timer_app.config import DEFAULT_SOUND

class Countdown:
    def __init__(self, display_label):
        self.display = display_label
        self.remaining = 0
        self.running = False

    def start(self, total_seconds, sound=DEFAULT_SOUND):
        self.remaining = total_seconds
        self.sound = sound
        self.running = True
        self._update()

    def _update(self):
        if self.running and self.remaining >= 0:
            h, rem = divmod(self.remaining, 3600)
            m, s = divmod(rem, 60)
            self.display.config(text=f"{int(h):02d}:{int(m):02d}:{int(s):02d}")
            if self.remaining == 0:
                self.running = False
                threading.Thread(target=lambda: play_sound(self.sound), daemon=True).start()
            else:
                self.remaining -= 1
                self.display.after(1000, self._update)
