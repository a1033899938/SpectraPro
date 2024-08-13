"""过滤Esc事件"""
import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 150)
        self.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.key_Escape:
            return True
        else:
            return QDialog.eventFilter(self, watched, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec()

    sys.exit(app.exec())
