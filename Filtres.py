import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

class Filtres :
    def __init__(self):
        self.a = []
        self.b = []

    def FT_rejecteur(self, f_c:int, ksi, Fs):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        # par Euler
        B_z = [1 + (omega_c * Te) ** 2, -2, 1]  # polynome B(z) (dénominateur de la fonction de transfert)
        A_z = [1 + 2 * ksi * omega_c * Te + (omega_c * Te) ** 2, -2 - 2 * ksi * omega_c * Te,1]  # polynome A(z) (numérateur de la fonction de transfert)
        # normalisation des coefficients
        B_z = [x / A_z[0] for x in B_z]
        A_z = [x / A_z[0] for x in A_z]
        return B_z, A_z


    def FT_passe_bas1(self, omega_c):
        b = [1] # polynome au numérateur
        a = [1/omega_c, 1] # polynome au dénominateur
        return sig.lti(b, a)

    def FT_passe_haut1(self, omega_c):
        b = [1/omega_c,0] # polynome au numérateur
        a = [1/omega_c, 1] # polynome au dénominateur
        return sig.lti(b, a)

    def FT_passe_bas2(self, omega_c, ksi:float):
        b = [omega_c**2] # polynome au numérateur
        a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur

    def FT_passe_haut2(self, omega_c, ksi:float):
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

    def init_chunk(self):


    def load_chunk(self):

    def traitement_chunk(self, data, filtre:str):
        if filtre == "r":
            B_z, A_z = self.FT_rejecteur() # TODO


        # calcul de l'audio filtré
        data_filt = np.zeros(len(data))  # initialisation à 0

        for ii in range(len(data)):
            s_e[0] = data[ii]
            # initialisation de l'entrée
            for jj in range(len(s_e)):
                data_filt[ii] += s_e[jj] * B_z[jj]
            for jj in range(len(s_s)):
                data_filt[ii] -= s_s[jj] * A_z[jj + 1]  # +1 car a0 est déjà inclu
            # récursion
            s_e[1:len(s_e)] = s_e[0:len(s_e) - 1]
            s_s[1:len(s_s)] = s_s[0:len(s_s) - 1]
            s_s[0] = data_filt[ii]

        data_filt = np.clip(data_filt, -32768, 32767)
        data_filt = data_filt.astype(np.int16)
        data_bytes_filt = data_filt.tobytes()
# réjecteur
#b = [1,0,omega_c**2] # polynome au numérateur
#a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur
# sélecteur
#b = [2*ksi*omega_c, 0] # polynome au numérateur
#a = [1, 2*ksi*omega_c, omega_c**2] # polynome au dénominateur



#ft = sig.lti(b, a) # fonction de transfert de la forme B(p) / A(p)



