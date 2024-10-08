"""重新分发事件"""
import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        QMessageBox.information(self, "Notice", 'in keyPressEvent', QMessageBox.Yes)
        QDialog.keyPressEvent(self, event)

    def event(self, event):
        if event.type() == QKeyEvent.KeyPress:
            QMessageBox.information(self, "Notice", 'in event', QMessageBox.Yes)
            QDialog.event(self, event)
            return True
        return QDialog.event(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec()

    sys.exit(app.exec())
