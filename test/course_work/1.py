import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot

class Example(QWidget):
    def __init__(self):
        super().__init__()
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

        # 连接信号与槽：点击按钮时调用 on_click 方法
        button.clicked.connect(self.on_click)

        # 设置窗口属性
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('信号与槽示例')
        self.show()

    @pyqtSlot()
    def on_click(self):
        # 槽函数：更新标签文字
        self.label.setText('按钮已被点击！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
