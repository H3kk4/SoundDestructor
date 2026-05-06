import numpy
from IPython.lib.display import Audio
from scipy.io import wavfile


def load_sound(location :str) :
    # ouverture du fichier en wav
    Fs, data = wavfile.read(location)  # fréquence d'échantillonnage et données
    return Fs, data

def play_sound(data, Fs):
    # jouer le son
    Audio(data, rate=Fs)

