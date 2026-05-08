import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from controller import Controller

buffer_size = 1024

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sound Destroyer")

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



        # Radio button
        self.rb_sans = QtWidgets.QRadioButton("Sans filtre")
        self.rb_sans.setChecked(True)
        self.rb_pb1 = QtWidgets.QRadioButton("Passe bas 1")
        self.rb_ph1 = QtWidgets.QRadioButton("Passe haut 1")
        self.rb_pb2 = QtWidgets.QRadioButton("Passe bas 2")
        self.rb_ph2 = QtWidgets.QRadioButton("Passe haut 2")

        # Sélection filtre
        self.selection = QtWidgets.QHBoxLayout()
        self.groupe_rb = QtWidgets.QButtonGroup()
        self.groupe_rb.addButton(self.rb_sans)
        self.groupe_rb.addButton(self.rb_pb1)
        self.groupe_rb.addButton(self.rb_ph1)
        self.groupe_rb.addButton(self.rb_pb2)
        self.groupe_rb.addButton(self.rb_ph2)
        self.groupe_rb.buttonClicked.connect(self.radio_clicked)

        for bouton in self.groupe_rb.buttons():
            self.selection.addWidget(bouton)

        # Slider Omega C
        self.omega_c = QtWidgets.QLabel()
        self.omega_c.setText("Omega C: 100")
        self.omega_c.hide()

        self.slider_omega_c = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_omega_c.setTickInterval(40)
        self.slider_omega_c.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_omega_c.setMinimum(20)
        self.slider_omega_c.setMaximum(2000)
        self.slider_omega_c.setValue(100)
        self.slider_omega_c.hide()

        # Slider KSI
        self.ksi = QtWidgets.QLabel()
        self.ksi.setText("KSI: 0.5")
        self.ksi.hide()

        self.slider_ksi = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_ksi.setTickInterval(50)
        self.slider_ksi.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_ksi.setMinimum(1)
        self.slider_ksi.setMaximum(1000)
        self.slider_ksi.setValue(500)
        self.slider_ksi.hide()

        # Bouton
        self.button = QtWidgets.QPushButton("Pause")

        # Ajout dans le layout
        layout.addWidget(self.plot_widget)
        layout.addLayout(self.selection)
        layout.addWidget(self.omega_c)
        layout.addWidget(self.slider_omega_c)
        layout.addWidget(self.ksi)
        layout.addWidget(self.slider_ksi)
        layout.addWidget(self.button)

        # Connexions
        self.slider_omega_c.valueChanged.connect(self.change_omega_c)
        self.slider_ksi.valueChanged.connect(self.change_ksi)
        self.button.clicked.connect(self.toggle)

        # Signal
        self.data = np.zeros(buffer_size)
        self.controller = Controller(buffer_size)
        self.controller.data_ready.connect(self.update_plot)
        self.controller.start()

        self.running = True

    def update_plot(self, new_data):
        self.data = new_data
        self.curve.setData(self.data)

    def close_event(self, event):
        self.controller.stop()
        event.accept()

    def change_omega_c(self, value):
        self.controller.omega_c = value
        self.omega_c.setText(f"Omega C: {value}")

    def change_ksi(self, value):
        self.ksi.setText(f"KSI: {value * 0.001}")
        self.controller.ksi = value

    def toggle(self):
        if self.running:
            self.controller.stop()
            self.button.setText("Reprendre")
        else:
            self.controller.start()
            self.button.setText("Pause")
        self.running = not self.running

    def radio_clicked(self, button):

        match button.text():
            case "Sans filtre":
                self.omega_c.hide()
                self.ksi.hide()
                self.slider_omega_c.hide()
                self.slider_ksi.hide()
                self.controller.fonction = None

            case "Passe bas 1":
                self.omega_c.show()
                self.ksi.hide()
                self.slider_omega_c.show()
                self.slider_ksi.hide()
                self.controller.fonction = "P1"


            case "Passe bas 2":
                self.omega_c.show()
                self.ksi.show()
                self.slider_omega_c.show()
                self.slider_ksi.show()
                self.controller.fonction = "P2"

            case "Passe haut 1":
                self.omega_c.show()
                self.ksi.hide()
                self.slider_omega_c.show()
                self.slider_ksi.hide()
                self.controller.fonction = "H1"

            case "Passe haut 2":
                self.omega_c.show()
                self.ksi.show()
                self.slider_omega_c.show()
                self.slider_ksi.show()
                self.controller.fonction = "H2"

            case _:
                raise ValueError("Unknown filter: {}".format(button))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())