import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

class Filtres :
    def __init__(self):
        self.a = []
        self.b = []

    def FT_passe_bas1(self, omega_c:int):
        b = [1] # polynome au numérateur
        a = [1/omega_c, 1] # polynome au dénominateur
        return sig.lti(b, a)

    def FT_passe_haut1(self, omega_c:int):
        b = [1/omega_c,0] # polynome au numérateur
        a = [1/omega_c, 1] # polynome au dénominateur
        return sig.lti(b, a)

    def FT_passe_bas2(self, omega_c:int, ksi:float):
        b = [omega_c**2] # polynome au numérateur
        a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur

    def FT_passe_haut2(self, omega_c:int, ksi:float):
        b = [1,0,0] # polynome au numérateur
        a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur

    def fourier_transform(self, data:list, Fs:int):
        n = len(data)
        fft_result = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data), 1 / Fs)
        # On ne garde que les fréquences positives
        fft_magnitude = np.abs(fft_result) / n
        fft_magnitude = fft_magnitude[range(int(n / 2))]
        return fft_magnitude, frequencies

# réjecteur
#b = [1,0,omega_c**2] # polynome au numérateur
#a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur
# sélecteur
#b = [2*ksi*omega_c, 0] # polynome au numérateur
#a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur



#ft = sig.lti(b, a) # fonction de transfert de la forme B(p) / A(p)



