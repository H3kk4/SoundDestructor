import Utils
import time

Fs, data = Utils.load_sound("sounds/guitar_perturbe.wav")

Utils.play_sound(data, Fs)

time.sleep(5)