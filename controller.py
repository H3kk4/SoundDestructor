from PyQt5 import QtCore
import numpy as np
import filtres

class Controller(QtCore.QObject):
    data_ready = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, buffer_size):
        super().__init__()
        self.fs = 44100
        self.frequency = 440  # Hz (note La)
        self.t = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.generate)
        self.buffer_size = buffer_size

        self.filtres = filtres.Filtres
        self.omega_c = 400
        self.ksi = 0.5
        self.fonction = None

    def start(self):
        self.timer.start(20)  # toutes les 20 ms

    def stop(self):
        self.timer.stop()

    def generate(self):
        t_values = (np.arange(self.buffer_size) + self.t) / self.fs
        signal = np.sin(2 * np.pi * self.frequency * t_values)

        if self.fonction:
            #TODO signal = self.filtres
            pass

        self.t += self.buffer_size
        self.data_ready.emit(signal)