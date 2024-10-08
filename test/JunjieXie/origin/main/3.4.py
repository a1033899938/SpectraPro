"""拦截Esc键，不退出对话框"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class myDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() != Qt.Key_Escape:
            QDialog.keyPressEvent(self, event)
        else:
            QMessageBox.information(self, "Notice", "No close!", QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = myDialog()
    dialog.exec()

    sys.exit(app.exec())
