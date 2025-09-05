# 在虚拟环境下的Lib\site-packages\PySide6底下，打开这个文件夹，可以看到Qt Designer
# D:\BaiduSyncdisk\Junjie Xie Backup\Script\Python\ui\.venv\Lib\site-packages\PySide6
# ui2py：方法1
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

# 在QApplication之前先实例化
uiLoader = QUiLoader()

class Stats:

    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load('main.ui')

    # 其它代码 ...

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec() # PySide6 是 exec 而不是 exec_

# ui2py：方法2
# 1、执行如下的命令 把UI文件直接转化为包含界面定义的Python代码文件
# pyside2-uic main.ui > ui_main.py
# 2、然后在你的代码文件中这样使用定义界面的类
# from PySide2.QtWidgets import QApplication,QMainWindow
# from ui_main import Ui_MainWindow
#
# # 注意 这里选择的父类 要和你UI文件窗体一样的类型
# # 主窗口是 QMainWindow， 表单是 QWidget， 对话框是 QDialog
# class MainWindow(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         # 使用ui文件导入定义界面类
#         self.ui = Ui_MainWindow()
#         # 初始化界面
#         self.ui.setupUi(self)
#
#         # 使用界面定义的控件，也是从ui里面访问
#         self.ui.webview.load('http://www.baidu.com')
#
# ESP32-Backup = QApplication([])
# mainw = MainWindow()
# mainw.show()
# ESP32-Backup.exec_()