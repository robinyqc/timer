import pygame
import threading

pygame.mixer.init()

def play_sound(path):
    def _play():
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    threading.Thread(target=_play, daemon=True).start()

def stop_sound():
    pygame.mixer.music.stop()