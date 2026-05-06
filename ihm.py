import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

buffer_size = 1024

class SignalGenerator(QtCore.QObject):
    data_ready = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.fs = 44100
        self.frequency = 440  # Hz (note La)
        self.t = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.generate)

    def start(self):
        self.timer.start(20)  # toutes les 20 ms

    def stop(self):
        self.timer.stop()

    def generate(self):
        t_values = (np.arange(buffer_size) + self.t) / self.fs
        signal = np.sin(2 * np.pi * self.frequency * t_values)

        self.t += buffer_size
        self.data_ready.emit(signal)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oscilloscope (signal généré)")

        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Layout vertical
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # Graphique
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(-1, 1)
        self.curve = self.plot_widget.plot(pen='y')

        # Slider (pour fréquence)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(100)
        self.slider.setMaximum(2000)
        self.slider.setValue(440)

        # Bouton
        self.button = QtWidgets.QPushButton("Pause")

        # Ajout dans le layout
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.slider)
        layout.addWidget(self.button)

        # Connexions
        self.slider.valueChanged.connect(self.change_frequency)
        self.button.clicked.connect(self.toggle)

        # Signal
        self.data = np.zeros(buffer_size)
        self.generator = SignalGenerator()
        self.generator.data_ready.connect(self.update_plot)
        self.generator.start()

        self.running = True

        # Radio button
        self.rb_sans = QtWidgets.QRadioButton("Sans filtre")
        self.rb_sans.setChecked(True)
        self.rb_avec = QtWidgets.QRadioButton("Avec filtre") #TODO

        # Sélection filtre
        self.groupe_rb = QtWidgets.QButtonGroup()
        self.groupe_rb.addButton(self.rb_sans)
        self.groupe_rb.addButton(self.rb_avec)

    def update_plot(self, new_data):
        self.data = new_data
        self.curve.setData(self.data)

    def close_event(self, event):
        self.generator.stop()
        event.accept()

    def change_frequency(self, value):
        self.generator.frequency = value

    def toggle(self):
        if self.running:
            self.generator.stop()
            self.button.setText("Reprendre")
        else:
            self.generator.start()
            self.button.setText("Pause")
        self.running = not self.running


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())