# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/nikita/Documents/network/project_aiosmtpd/project_aiosmtpd/login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(348, 152)
        Dialog.setStyleSheet("QDialog{\n"
"    backgroung: rgb(238, 238, 236)\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.email_le = QtWidgets.QLineEdit(Dialog)
        self.email_le.setObjectName("email_le")
        self.gridLayout.addWidget(self.email_le, 1, 1, 1, 1)
        self.pass_le = QtWidgets.QLineEdit(Dialog)
        self.pass_le.setObjectName("pass_le")
        self.gridLayout.addWidget(self.pass_le, 3, 1, 1, 1)
        self.welcome_label = QtWidgets.QLabel(Dialog)
        self.welcome_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setObjectName("welcome_label")
        self.gridLayout.addWidget(self.welcome_label, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Mail Client"))
        self.label.setText(_translate("Dialog", "Email:"))
        self.label_2.setText(_translate("Dialog", "Password:"))
        self.welcome_label.setText(_translate("Dialog", "Welcome to the Mail Client App!"))

