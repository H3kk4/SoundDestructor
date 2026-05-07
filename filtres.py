import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

class Filtres :
    def __init__(self):
        self.a = []
        self.b = []

    def normalisation_coefficients(self, B_z, A_z):
        B_z = [x / A_z[0] for x in B_z]
        A_z = [x / A_z[0] for x in A_z]
        return B_z, A_z

    def go_filtre(self,code_filtre:str, f_c:int, Fs, ksi=None):
        if code_filtre == "R":
            return self.FT_rejecteur(f_c, Fs, ksi)
        elif code_filtre == "P1":
            return self.FT_passe_bas1(f_c, Fs, ksi)
        elif code_filtre == "H1":
            return self.FT_passe_haut1(f_c, Fs, ksi)
        elif code_filtre == "P2":
            return self.FT_passe_bas2(f_c, Fs, ksi)
        elif code_filtre == "H2":
            return self.FT_passe_haut2(f_c, Fs, ksi)
        else:
            raise Exception("Filtre inconnu. (Usage : R, P1, H1, P2, H2)")

    def FT_passe_bas1(self, f_c:int, Fs, ksi=None):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        B_z = [Te*omega_c]
        A_z = [1+Te*omega_c, -1]
        return self.normalisation_coefficients(B_z, A_z)

    def FT_passe_bas2(self, f_c:int, Fs, ksi=None):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        B_z = [(omega_c*Te)**2]
        A_z = [(1 + 2*ksi*omega_c*Te + (omega_c*Te)**2), (-2 - 2*ksi*omega_c*Te), 1]
        return self.normalisation_coefficients(B_z, A_z)

    def FT_passe_haut1(self, f_c:int, Fs, ksi=None):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        B_z = [1, -1]
        A_z = [1+Te*omega_c, -1]
        return self.normalisation_coefficients(B_z, A_z)

    def FT_passe_haut2(self, f_c:int, Fs, ksi=None):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        B_z = [1,-2,1]
        A_z = [(1 + 2 * ksi * omega_c * Te + (omega_c * Te) ** 2), (-2 - 2 * ksi * omega_c * Te), 1]
        return self.normalisation_coefficients(B_z, A_z)

    def FT_rejecteur(self, f_c:int, Fs, ksi):
        omega_c = 2 * np.pi * f_c
        Te = 1 / Fs
        Q = 1 / (2 * ksi)
        # par Euler
        B_z = [1 + (omega_c * Te) ** 2, -2, 1]
        A_z = [1 + 2 * ksi * omega_c * Te + (omega_c * Te) ** 2, -2 - 2 * ksi * omega_c * Te,1]
        return self.normalisation_coefficients(B_z, A_z)


    def init_traitement_chunk(self, data, A_z, B_z):
        s_e = np.zeros(len(B_z))
        s_e[0] = data[0]
        s_s = np.zeros(len(A_z) - 1)  # a0 = 1 et est directement enlevé
        return s_e, s_s

    def load_chunk(self):
        pass

    def traitement_chunk(self, data, A_z, B_z, s_e=None, s_s=None):
        return_data = False
        if s_e is None and s_s is None :
            s_e, s_s = self.init_traitement_chunk(data, A_z, B_z)
            return_data = True
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

        return (data_bytes_filt, s_e, s_s) if return_data else data_bytes_filt

