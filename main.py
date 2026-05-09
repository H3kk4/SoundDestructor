import ihm
import sys
from PyQt5 import QtWidgets


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ihm.MainWindow()
    win.show()
    sys.exit(app.exec_())