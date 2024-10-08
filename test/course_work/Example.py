import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QCheckBox, QSlider, QMainWindow, QStatusBar,
                             QMenuBar, QToolBar, QTextEdit, QFileDialog, QGraphicsView)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建中央Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建控件
        self.label = QLabel('选中的文件夹路径将显示在这里', self)
        button = QPushButton('选择文件夹', self)
        checkbox = QCheckBox('复选框', self)
        slider = QSlider(self)
        textedit = QTextEdit(self)
        graphics_view = QGraphicsView(self)

        # 布局管理
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)  # 显示文件夹路径的标签
        vbox.addWidget(button)      # 选择文件夹的按钮
        vbox.addWidget(checkbox)    # 复选框
        vbox.addWidget(slider)      # 滑动条
        vbox.addWidget(textedit)    # 文本编辑器
        vbox.addWidget(graphics_view)  # 图形视图

        central_widget.setLayout(vbox)

        # 连接按钮到文件夹选择对话框
        button.clicked.connect(self.showDialog)

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 设置工具栏
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # 设置状态栏
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # 设置窗口
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('PyQt5 控件示例')
        self.show()

    def showDialog(self):
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(self, '选择文件夹')

        # 如果选择了文件夹，将路径显示在Label上，并更新状态栏
        if folder:
            self.label.setText(f'选中的文件夹: {folder}')
            self.statusBar.showMessage(f'选中的文件夹路径: {folder}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
