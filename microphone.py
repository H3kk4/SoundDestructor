import sounddevice as sd
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

class Microphone(QObject):

    new_data = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()

        self.stream = sd.InputStream(
            channels=1,
            samplerate=44100,
            blocksize=512,
            callback=self.audio_callback
        )

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)

        samples = indata[:, 0].copy()

        self.new_data.emit(samples)