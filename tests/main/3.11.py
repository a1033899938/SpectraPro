"""使用自定义的信号连接到自定义槽函数"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 100)
        button = QPushButton("close", self)
        button.clicked.connect(self.onClicked)
        self.closeSignal.connect(self.onClose)

    def onClicked(self):
        self.closeSignal.emit()

    def onClose(self):
        QMessageBox.information(self, "Notice", "Bye!", QMessageBox.Yes)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
