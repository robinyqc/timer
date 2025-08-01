from tkinter import messagebox
from timer_app.utils import play_sound, stop_sound
from timer_app.config import load_config

class Countdown:
    def __init__(self, display_label, master):
        self.display = display_label
        self.master = master 
        self.remaining = 0
        self.running = False
        self.active = True


    def start(self, total_seconds, sound=load_config().get("sound_path", "")):
        self.remaining = total_seconds
        self.sound = sound
        self.running = True
        self.init = False
        self._update()

    def _update(self):
        if self.running and self.remaining >= 0:
            rem_s = self.remaining // 100
            h, rem = divmod(rem_s, 3600)
            m, s = divmod(rem, 60)
            self.display.config(text=f"{int(h):02d}:{int(m):02d}:{int(s):02d}")
            if self.remaining == 0:
                self.running = False
                if not self.running:
                    # print(self.sound, file=sys.stderr)
                    if self.sound != '':
                        play_sound(self.sound)
                    
                    def stop():
                        messagebox.showwarning(message="Time's up" ,title="Notice")
                        if self.sound != '':
                            stop_sound()
                        self.active = False
                    
                    self.master.after(100, stop)

            else:
                self.remaining -= 1
                self.display.after(10, self._update)
