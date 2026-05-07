import wave
import numpy as np
from IPython.display import Audio
import pyaudio as pya
import matplotlib.pyplot as plt


# paramètres du filtre
f_c = 2000
omega_c = 2*np.pi*f_c
ksi = .5
Te = 1/Fs
Q = 1/(2*ksi)  # Facteur de qualité (plus il est élevé, plus le filtre est étroit)

spf = wave.open("sounds/guitar_perturbe.wav")

ampwidth = spf.getsampwidth()
F_e = spf.getframerate()*ampwidth
n_frames = spf.getnframes()*ampwidth # nb_echantillons
signal = spf.readframes(int(n_frames/2))
signal = np.frombuffer(signal, dtype=np.int16)
print(signal)
#Audio(signal, rate=F_e)

length = signal.shape[0] / F_e

time = np.linspace(0., length, signal.shape[0])
plt.plot(time, signal)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.title("Signal")
plt.show()

signal_fft = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(signal), 1/F_e)
module = np.abs(signal_fft)
n = len(signal) // 2

#plt.stem(freqs[:n], module[:n])
#plt.title('Spectre d\'amplitude (module de la FFT)')
#plt.xlabel('Fréquence (Hz)')
#plt.ylabel('Amplitude')
#plt.grid(True)
#plt.show()
