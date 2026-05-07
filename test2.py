"""PyAudio Example: Play a WAVE file."""
import Filtres
import pyaudio
import wave
import numpy as np
import scipy.signal as sig

CHUNK = 1024

wf = wave.open("sounds/guitar_perturbe.wav", 'rb')
Fs = wf.getframerate()

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=Fs,
                output=True)

data_bytes = wf.readframes(CHUNK) # Lecture de 1024 bits d'audio
data = np.frombuffer(data_bytes, dtype=np.int16)
print(data)

# Application d'un filtre sur ces données
# paramètres du filtre
f_c = 2000
omega_c = 2*np.pi*f_c
ksi = 1
Te = 1/Fs
Q = 1/(2*ksi)  # Facteur de qualité (plus il est élevé, plus le filtre est étroit)

filtres = Filtres.Filtres()
f_transfert = filtres.FT_passe_bas1(omega_c)

#B_z, A_z = sig.iirnotch(f_c, Q, Fs)
# par Euler
B_z = [1 + (omega_c * Te) ** 2, -2, 1]  # polynome B(z) (dénominateur de la fonction de transfert)
A_z = [1 + 2 * ksi * omega_c * Te + (omega_c * Te) ** 2, -2 - 2 * ksi * omega_c * Te,1]  # polynome A(z) (numérateur de la fonction de transfert)
# normalisation des coefficients
B_z = [x / A_z[0] for x in B_z]
A_z = [x / A_z[0] for x in A_z]

#Passe bas O1
#B_z = []
#A_z = []


s_e = np.zeros(len(B_z))
s_e[0] = data[0]
s_s = np.zeros(len(A_z)-1) # a0 = 1 et est directement enlevé

# calcul de l'audio filtré
data_filt = np.zeros(len(data)) # initialisation à 0

for ii in range(len(data)):
    s_e[0] = data[ii]
    # initialisation de l'entrée
    for jj in range(len(s_e)):
        data_filt[ii] += s_e[jj] * B_z[jj]
    for jj in range(len(s_s)):
        data_filt[ii] -= s_s[jj] * A_z[jj+1] # +1 car a0 est déjà inclu
    # récursion
    s_e[1:len(s_e)] = s_e[0:len(s_e)-1]
    s_s[1:len(s_s)] = s_s[0:len(s_s)-1]
    s_s[0] = data_filt[ii]

data_filt = np.clip(data_filt, -32768, 32767)
data_filt = data_filt.astype(np.int16)
data_bytes_filt = data_filt.tobytes()

while len(data_bytes) != 0:
    stream.write(data_bytes_filt) # écriture des 1024 bits filtrés

    data_bytes = wf.readframes(CHUNK) # chargement des 1024 bits d'après
    data = np.frombuffer(data_bytes, dtype=np.int16) # conversion en array de float

    #B_z, A_z = sig.iirnotch(f_c, Q, Fs)

    # par Euler
    B_z = [1 + (omega_c * Te) ** 2, -2, 1]  # polynome B(z) (dénominateur de la fonction de transfert)
    A_z = [1 + 2 * ksi * omega_c * Te + (omega_c * Te) ** 2, -2 - 2 * ksi * omega_c * Te,1]  # polynome A(z) (numérateur de la fonction de transfert)
    # normalisation des coefficients
    B_z = [x / A_z[0] for x in B_z]
    A_z = [x / A_z[0] for x in A_z]

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


stream.stop_stream()
stream.close()

p.terminate()