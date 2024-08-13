from PyQt5 import uic
from PyQt5.QtWidgets import *
"""通过Qt Designer设计一个.ui文件，再通过pyuic5 -o xx.py xx.ui来转换为.py文件，之后再调用"""
import sys
import os
# 确保项目根目录在 sys.path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 获取 mydlg2.ui 文件的绝对路径
ui_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../ui/uiFile/mydlg2.ui")
print(ui_file_path)


def btn_click():
    # 在.ui外部添加槽函数
    print("You click the button.")
    QMessageBox.information(dlg, 'Notice', "It is cold!", QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication([])
    CMyDlg, CDlg = uic.loadUiType(ui_file_path)
    dlg = CDlg()
    myDlg = CMyDlg()
    print(type(myDlg))
    print(type(dlg))
    myDlg.setupUi(dlg)
    myDlg.pushButton.clicked.connect(btn_click)  # 在.ui外部添加connect
    dlg.show()
    app.exec()
