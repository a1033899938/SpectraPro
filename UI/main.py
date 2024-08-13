import sys
from PyQt5.QtWidgets import *
from UI.Tree import Ui_Form
from PyQt5.QtCore import pyqtSignal


class myDlg(QWidget, Ui_Form):
    openFolderSignal = pyqtSignal()
    filepathnow = ''

    def __init__(self):
        super(myDlg, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn)
        self.openFolderSignal.connect(self.showTree)
    def btn(self):
        self.filepathnow = QFileDialog.getExistingDirectory(self, "select folder", "C:/")
        self.textEdit.setText(self.filepathnow)

    def showTree(self):
        s =1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = myDlg()
    mydlg.show()

    sys.exit(app.exec())
