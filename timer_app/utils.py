import sys
import subprocess

def play_sound(path):
    if sys.platform.startswith('win'):
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME)
    else:
        subprocess.call(['afplay', path])
