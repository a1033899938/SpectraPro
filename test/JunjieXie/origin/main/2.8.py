"""通过Qt Designer设计一个.ui文件，再通过pyuic5 -o xx.py xx.ui来转换为.py文件，之后再调用"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将.ui目录放入系统路径中
from Testing.uiFile.mydlg1 import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    maindlg = Ui_Dialog()
    maindlg.setupUi(maindlg)
    maindlg.show()

    sys.exit(app.exec())