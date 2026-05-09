from PyQt5 import QtCore
import numpy as np
import filtres
import microphone

class Controller(QtCore.QObject):
    data_ready = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, buffer_size):
        super().__init__()

        self.micro = microphone.Microphone()
        self.micro.new_data.connect(self.nouveau_signal)

        self.filtres = filtres.Filtres
        self.omega_c = 400
        self.ksi = 0.5
        self.fonction = None

    def start(self):
        self.micro.start()

    def stop(self):
        self.micro.stop()

    def nouveau_signal(self, samples):
        signal = samples

        if self.fonction:
            #TODO signal = self.filtres
            pass

        self.data_ready.emit(signal)