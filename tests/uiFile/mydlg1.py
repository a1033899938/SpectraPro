# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mydlg.ui'
#
# Created by: PyQt5 ui code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)  # Dialog为按钮的父控件。当父对象被销毁时，按钮也会被销毁。
        self.pushButton.setGeometry(QtCore.QRect(130, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.myclick)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        # 主要目的是为了支持国际化（i18n）。
        # 当你想要翻译应用程序的用户界面时，可以使用 Qt 提供的翻译机制，retranslateUi 方法就是在这个过程中动态更新界面文本的一部分。
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "myButton1"))

    def myclick(self):
        reply = QMessageBox.information(self, 'Notice', 'It is cold!', QMessageBox.Yes)
