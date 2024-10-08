"""未使用布局、有控件的Qt程序"""
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        self.setWindowTitle('hello')
        self.lb1 = QPushButton('Button 1', self)
        self.lb1.setGeometry(10, 20, 80, 50)
        self.lb2 = QPushButton('Button 2', self)
        self.lb2.setGeometry(110, 20, 80, 50)  # 左上角横坐标、左上角纵坐标、长度、高度
        self.lb1.clicked.connect(self.myclick)
        self.lb2.clicked.connect(self.myclick)

    def myclick(self):
        button = self.sender()
        QMessageBox.information(self, 'Notice', button.text()+' is cool!', QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Example()
    main.show()
    sys.exit(app.exec())