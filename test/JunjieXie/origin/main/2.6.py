"""有布局、有控件的Qt程序"""
from PyQt5.QtWidgets import *
import sys


class CMYDlg(QDialog):
    def __init__(self):
        super(CMYDlg, self).__init__()
        self.resize(330, 100)
        self.setWindowTitle('Hello Dialog')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')

        self.textEdit1 = QTextEdit("hello")
        button1.clicked.connect(self.myclick)
        button2.clicked.connect(self.myclick)
        button3.clicked.connect(self.close)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(self.textEdit1)
        self.setLayout(layout)

    def myclick(self):
        button = self.sender()
        print(button.text())
        self.textEdit1.setText("You click the "+button.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CMYDlg()
    main.show()
    sys.exit(app.exec())