"""使用内置的槽函数"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 100)
        button = QPushButton("close", self)
        button.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
