"""使用自定义的信号连接到内置槽函数"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtCore import pyqtSignal


class MainWindow(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 100)

        button = QPushButton("close", self)
        button.clicked.connect(self.close)

    def myClose(self):
        self.closeSignal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
