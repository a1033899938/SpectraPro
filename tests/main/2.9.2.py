import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Testing.uiFile.myForm import Ui_Form


class mySubForm(QtWidgets.QWidget, Ui_Form):
    m_cn = 0

    def __init__(self):
        super(mySubForm, self).__init__()
        self.setupUi(self)

    def btn_click(self):
        self.m_cn = self.m_cn + 1
        self.textEdit.setText("You click the button."+str(self.m_cn))

        QMessageBox.information(self, "Notice", 'It is cold!', QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = mySubForm()
    my_pyqt_form.show()
    sys.exit(app.exec())