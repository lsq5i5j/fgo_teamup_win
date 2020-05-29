# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectTargetUi_Inverse.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 188)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_3 = QtWidgets.QPushButton(Dialog)
        self.btn_3.setMinimumSize(QtCore.QSize(110, 120))
        self.btn_3.setMaximumSize(QtCore.QSize(110, 120))
        self.btn_3.setText("")
        self.btn_3.setIconSize(QtCore.QSize(120, 120))
        self.btn_3.setObjectName("btn_3")
        self.horizontalLayout_2.addWidget(self.btn_3)
        self.btn_2 = QtWidgets.QPushButton(Dialog)
        self.btn_2.setMinimumSize(QtCore.QSize(110, 120))
        self.btn_2.setMaximumSize(QtCore.QSize(110, 120))
        self.btn_2.setText("")
        self.btn_2.setIconSize(QtCore.QSize(120, 120))
        self.btn_2.setObjectName("btn_2")
        self.horizontalLayout_2.addWidget(self.btn_2)
        self.btn_1 = QtWidgets.QPushButton(Dialog)
        self.btn_1.setMinimumSize(QtCore.QSize(110, 120))
        self.btn_1.setMaximumSize(QtCore.QSize(110, 120))
        self.btn_1.setText("")
        self.btn_1.setIconSize(QtCore.QSize(120, 120))
        self.btn_1.setObjectName("btn_1")
        self.horizontalLayout_2.addWidget(self.btn_1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "选择对象"))
