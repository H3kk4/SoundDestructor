from IPython.lib.display import Audio
# import required module
from playsound import playsound
import Utils
import matplotlib.pyplot as plt

import Filtres

filtres = Filtres.Filtres()

signal, t = Utils.signal_sin(10)

plt.plot(t, signal)
plt.xlim(0, 1)
plt.show()

a,b = filtres.fourier_transform(signal, len(t))

plt.plot(b, a)
plt.show()




