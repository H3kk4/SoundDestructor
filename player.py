import pyaudio
import wave
import numpy as np

class Player:
    def __init__(self, filename:str, CHUNK:int = 1024):
        self.CHUNK = CHUNK
        self.p = pyaudio.PyAudio()
        self.wf = wave.open(filename, 'rb')
        self.Fs = self.wf.getframerate()

    def open_stream(self):
        p = pyaudio.PyAudio()
        return p.open(format=p.get_format_from_width(self.wf.getsampwidth()),channels=self.wf.getnchannels(),rate=self.Fs,output=True)

    def get_data(self):
        return np.frombuffer(self.wf.readframes(self.CHUNK), dtype=np.int16)

    def get_Fs(self):
        return self.Fs

    def terminate(self):
        self.p.terminate()
