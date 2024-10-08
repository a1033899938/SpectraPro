# coding:utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys

app = QApplication(sys.argv)
widget = QWidget()
btn = QPushButton(widget)
btn.setText('PushButton')
btn.move(0, 0) # 移动按钮，以QWidget窗口客户区左上角为(0, 0)点
# 不同操作系统可能对窗口的最小宽度有限定，若设置宽度小于规定值，则会以规定值进行显示
widget.resize(300, 200)
widget.move(250, 20) # 以屏幕左上角为(0, 0)点
widget.setWindowTitle('PyQt坐标系统例子')
widget.show()
print('QWidget:')
print('w.x()={}'.format(widget.x()))  #输出窗口在屏幕中的x坐标
print('w.y()={}'.format(widget.y()))  #输出窗口在屏幕中的y坐标
print('w.width()={}'.format(widget.width())) #输出窗口的客户区宽度
print('w.height()={}'.format(widget.height()))  #//输出窗口的客户区高度

print('QWidget frameGeometry:')
print('QWidget.frameGeometry().x()={}'.format(widget.frameGeometry().x())) #输出窗口在屏幕中的x坐标
print('QWidget.frameGeometry().y()={}'.format(widget.frameGeometry().y()))  #输出窗口在屏幕中的y坐标
print('QWidget.frameGeometry().width()={}'.format(widget.frameGeometry().width())) #输出窗口的宽度
print('QWidget.frameGeometry().height()={}'.format(widget.frameGeometry().height()))#输出窗口的高度，包括标题栏

print('QWidget.geometry(Client Area):')
print('widget.geometry().x()={}'.format(widget.geometry().x())) #输出客户区原点的在屏幕中的横坐标
print('widget.geometry().y()={}'.format(widget.geometry().y())) #输出客户区原点的在屏幕中的纵坐标
print('widget.geometry().width()={}'.format(widget.geometry().width())) #输出客户区的宽度
print('widget.geometry().height()={}'.format(widget.geometry().height())) #输出客户区的高度

print('-------------PushButton:----------------')
print('PushButton.x()={}'.format(btn.x())) #输出按钮在窗口（Widget）中的x坐标
print('PushButton.y()={}'.format(btn.y())) #输出按钮在窗口（Widget）中的y坐标
print('PushButton.width()={}'.format(btn.width())) #输出按钮在窗口（Widget）中的宽度
print('PushButton.height()={}'.format(btn.height())) #输出按钮在窗口（Widget）中的高度

print('PushButton.geometry().x()={}'.format(btn.geometry().x()))
print('PushButton.geometry().y()={}'.format(btn.geometry().y()))
print('PushButton.geometry().width()={}'.format(btn.geometry().width()))
print('PushButton.geometry().height()={}'.format(btn.geometry().height()))

print('PushButton.frameGeometry().x()={}'.format(btn.frameGeometry().x()))
print('PushButton.frameGeometry().y()={}'.format(btn.frameGeometry().y()))
print('PushButton.frameGeometry().width()={}'.format(btn.frameGeometry().width()))
print('PushButton.frameGeometry().height()={}'.format(btn.frameGeometry().height()))

sys.exit(app.exec_())