# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UpdateUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(444, 232)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_data_new = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_data_new.sizePolicy().hasHeightForWidth())
        self.label_data_new.setSizePolicy(sizePolicy)
        self.label_data_new.setText("")
        self.label_data_new.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data_new.setObjectName("label_data_new")
        self.gridLayout.addWidget(self.label_data_new, 1, 1, 1, 1)
        self.label_data_old = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_data_old.sizePolicy().hasHeightForWidth())
        self.label_data_old.setSizePolicy(sizePolicy)
        self.label_data_old.setText("")
        self.label_data_old.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data_old.setObjectName("label_data_old")
        self.gridLayout.addWidget(self.label_data_old, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_data_state = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_data_state.sizePolicy().hasHeightForWidth())
        self.label_data_state.setSizePolicy(sizePolicy)
        self.label_data_state.setMinimumSize(QtCore.QSize(0, 40))
        self.label_data_state.setText("")
        self.label_data_state.setObjectName("label_data_state")
        self.verticalLayout.addWidget(self.label_data_state)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_data_update = QtWidgets.QPushButton(self.groupBox)
        self.btn_data_update.setObjectName("btn_data_update")
        self.horizontalLayout.addWidget(self.btn_data_update)
        self.btn_remove_backup = QtWidgets.QPushButton(self.groupBox)
        self.btn_remove_backup.setObjectName("btn_remove_backup")
        self.horizontalLayout.addWidget(self.btn_remove_backup)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn_data_confirm = QtWidgets.QPushButton(self.groupBox)
        self.btn_data_confirm.setEnabled(False)
        self.btn_data_confirm.setObjectName("btn_data_confirm")
        self.verticalLayout.addWidget(self.btn_data_confirm)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "数据更新"))
        self.label_2.setText(_translate("Dialog", "当前数据库: "))
        self.label_4.setText(_translate("Dialog", "最新数据库:"))
        self.btn_data_update.setText(_translate("Dialog", "检查更新"))
        self.btn_remove_backup.setText(_translate("Dialog", "删除备份"))
        self.btn_data_confirm.setText(_translate("Dialog", "确  定"))
