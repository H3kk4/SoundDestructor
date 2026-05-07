from IPython.lib.display import Audio
# import required module
from playsound import playsound
import player
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import wave
import pyaudio as pya

import filtres

filtres = Filtres.Filtres()

signal, t = Utils.signal_sin(10)

#plt.plot(t, signal)
#plt.xlim(0, 1)
#plt.show()

Fs, data = Utils.load_sound("sounds/guitar_perturbe.wav")

Te = np.arange(len(data)) / Fs

plt.plot(Te, data)
plt.show()

fft_magnitude, frequencies = filtres.fourier_transform(signal, len(t))

sound = wave.open("sounds/guitar_perturbe.wav", "rb")
Fs = sound.getframerate()





