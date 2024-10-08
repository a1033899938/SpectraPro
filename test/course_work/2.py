import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    # 定义一个自定义信号，带一个字符串参数
    custom_signal = pyqtSignal(str)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.comm = Communicate()  # 创建信号对象
        self.initUI()

    def initUI(self):
        # 创建一个标签和按钮
        self.label = QLabel('未点击按钮', self)
        button = QPushButton('点击我', self)

        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(button)

        self.setLayout(vbox)

        # 连接自定义信号到槽函数
        self.comm.custom_signal.connect(self.update_label)

        # 当按钮被点击时，发出自定义信号
        button.clicked.connect(self.emit_custom_signal)

        # 设置窗口属性
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('自定义信号与槽示例')
        self.show()

    def emit_custom_signal(self):
        # 发送自定义信号，传递自定义的字符串
        self.comm.custom_signal.emit('按钮已被点击！')

    def update_label(self, text):
        # 更新标签文字
        self.label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
