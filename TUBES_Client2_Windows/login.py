# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login_form(object):
    def setupUi(self, login_form):
        login_form.setObjectName("login_form")
        login_form.resize(975, 823)
        login_form.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.label = QtWidgets.QLabel(login_form)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(10, 90, 961, 141))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size:28pt;\n"
"text-allign: center;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(login_form)
        self.label_2.setGeometry(QtCore.QRect(150, 340, 151, 71))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size : 15pt;\n"
"")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(login_form)
        self.label_3.setGeometry(QtCore.QRect(150, 420, 151, 71))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size : 15pt;\n"
"")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.username = QtWidgets.QLineEdit(login_form)
        self.username.setGeometry(QtCore.QRect(350, 350, 311, 51))
        self.username.setStyleSheet("font-size:14pt;\n"
"color: rgb(255, 255, 255);\n"
"padd")
        self.username.setText("")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(login_form)
        self.password.setGeometry(QtCore.QRect(350, 430, 311, 51))
        self.password.setStyleSheet("font-size:14pt;\n"
"color: rgb(255, 255, 255);\n"
"padd")
        self.password.setText("")
        self.password.setObjectName("password")
        self.loginbutton = QtWidgets.QPushButton(login_form)
        self.loginbutton.setGeometry(QtCore.QRect(450, 580, 101, 41))
        self.loginbutton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size : 14pt;")
        self.loginbutton.setObjectName("loginbutton")
        self.buatakunbutton = QtWidgets.QPushButton(login_form)
        self.buatakunbutton.setGeometry(QtCore.QRect(170, 610, 141, 41))
        self.buatakunbutton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size : 14pt;")
        self.buatakunbutton.setObjectName("buatakunbutton")
        self.responsetext = QtWidgets.QLabel(login_form)
        self.responsetext.setGeometry(QtCore.QRect(350, 500, 581, 61))
        self.responsetext.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 8pt \"Myanmar Text\";")
        self.responsetext.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.responsetext.setWordWrap(True)
        self.responsetext.setObjectName("responsetext")

        self.retranslateUi(login_form)
        QtCore.QMetaObject.connectSlotsByName(login_form)

    def retranslateUi(self, login_form):
        _translate = QtCore.QCoreApplication.translate
        login_form.setWindowTitle(_translate("login_form", "Form"))
        self.label.setText(_translate("login_form", "LOGIN"))
        self.label_2.setText(_translate("login_form", "Username"))
        self.label_3.setText(_translate("login_form", "Password"))
        self.username.setPlaceholderText(_translate("login_form", "Masukkan Username"))
        self.password.setPlaceholderText(_translate("login_form", "Masukkan Password"))
        self.loginbutton.setText(_translate("login_form", "Login"))
        self.buatakunbutton.setText(_translate("login_form", "Register"))
        self.responsetext.setText(_translate("login_form", "TextLabel"))
