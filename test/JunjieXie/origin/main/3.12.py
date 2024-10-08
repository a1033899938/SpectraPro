"""在控制台程序（没有任何窗口部件）中自定义发射信号"""
import sys
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication


class MyTask(QObject):
    mySig = pyqtSignal()

    def send_mySig(self):
        print("now, send signal")
        self.mySig.emit()

    def do_mySig(self):
        print("ok, task is over.")


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    item = MyTask()
    item.mySig.connect(item.do_mySig)
    item.send_mySig()

    sys.exit(app.exec())

    sys.exit(app.exec())
