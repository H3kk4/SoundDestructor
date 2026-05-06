import numpy as np
#from IPython.lib.display import Audio
from scipy.io import wavfile
from playsound import playsound

def load_sound(location :str) :
    # ouverture du fichier en wav
    Fs, data = wavfile.read(location)  # fréquence d'échantillonnage et données
    return Fs, data

def play_sound(location:str):
    # jouer le son
    playsound(location)

def signal_sin(f:int):
    t = np.arange(0,1,1/1000)
    signal = np.sin(2*np.pi*f*t)
    return signal, t


