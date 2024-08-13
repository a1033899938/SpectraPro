"""使用自定义的槽函数"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 100)
        button = QPushButton("do close", self)
        button.clicked.connect(self.myclose)

    def myclose(self):
        reply = QMessageBox.question(self, "Notice", "Are you sure to close?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
