import numpy
from IPython.lib.display import Audio
from scipy.io import wavfile


class Utils :
    def load_sound(self, location :str) :
        # ouverture du fichier en wav
        Fs, data = wavfile.read('str')  # fréquence d'échantillonnage et données

    def play_sound(self, data, Fs):
        # jouer le son
        Audio(data, rate=Fs) 