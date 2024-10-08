import sys
from PyQt5 import QtWidgets, QtCore

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(320, 240)
    widget.setWindowTitle("Hello PyQt5")
    widget.show()
    sys.exit(app.exec())