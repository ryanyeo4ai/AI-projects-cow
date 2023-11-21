# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddUserUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (QLabel, QErrorMessage, QPushButton, QGridLayout, QStatusBar, QWidget, QTextEdit)
from PyQt5.QtGui import QFont
import pandas as pd
import os
from pandas import ExcelWriter
from pandas import ExcelFile


class Ui_AddUser(object):
    def setupUi(self, AddUserWindow):
        AddUserWindow.resize(320, 185)
        self.centralwidget = QWidget(AddUserWindow)
        self.centralwidget.setGeometry(QRect(10, 40, 300, 90))

        self.esmg = QErrorMessage(AddUserWindow)
        self.esmg.setWindowTitle("Error")
        self.statusbar = QStatusBar(AddUserWindow)
        self.statusbar.setGeometry(QRect(170, 0, 100, 15))

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textEdit = QTextEdit(self.centralwidget)
        self.gridLayout.addWidget(self.textEdit, 0, 1, 1, 1)
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.gridLayout.addWidget(self.textEdit_2, 1, 1, 1, 1)
        self.textEdit_3 = QTextEdit(self.centralwidget)
        self.gridLayout.addWidget(self.textEdit_3, 2, 1, 1, 1)
        self.label_4 = QLabel(AddUserWindow)
        self.label_4.setGeometry(QRect(10, 10, 80, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)

        self.SaveBox = QPushButton('Save', AddUserWindow)
        self.SaveBox.setGeometry(QRect(160, 140, 70, 20))
        self.CancelBox = QPushButton('Cancel', AddUserWindow)
        self.CancelBox.setGeometry(QRect(240, 140, 70, 20))

        self.retranslateUi(AddUserWindow)
        self.SaveBox.clicked.connect(self.saveButtonClicked)
        self.CancelBox.clicked.connect(self.cancleButtonClicked)
        QMetaObject.connectSlotsByName(AddUserWindow)

    def retranslateUi(self, AddUserWindow):
        _translate = QCoreApplication.translate
        AddUserWindow.setWindowTitle(_translate("AddUserWindow", "AddUserWindow"))
        self.label.setText(_translate("AddUserWindow", "Name"))
        self.label_2.setText(_translate("AddUserWindow", "Phone"))
        self.label_3.setText(_translate("AddUserWindow", "IP"))
        self.label_4.setText(_translate("AddUserWindow", "Add User"))

    def checkAllFilled(self):
        count = 0
        if self.textEdit.toPlainText() != '':
            count += 1
        if self.textEdit_2.toPlainText() != '':
            count += 1
        if self.textEdit_3.toPlainText() != '':
            count += 1
        return count

    def saveButtonClicked(self):
        if self.checkAllFilled() == 3:
            directory = os.path.abspath('Manager/users.xlsx')
            # print(os.path.isfile(directory))
            # directory = directory.replace('\\', '/')
            # directory = 'Manager/Users.xlsx'
            UserExcel = pd.read_excel(directory, sheet_name='Sheet1')
            try:
                os.remove(directory)

                names = UserExcel['Name'].tolist()
                Phones = UserExcel['Phone'].tolist()
                IPs = UserExcel['IP'].tolist()

                print(names, Phones, IPs)

                names.append(self.textEdit.toPlainText())
                Phones.append(self.textEdit_2.toPlainText())
                IPs.append(self.textEdit_3.toPlainText())

                dataFrame = pd.DataFrame({'Name': names,
                                          'Phone': Phones,
                                          'IP': IPs})
                writer = pd.ExcelWriter(directory, engine='xlsxwriter')
                dataFrame.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
                self.statusbar.showMessage('save success')
            except:
                self.esmg.showMessage('Please close users.xlsx excel file.')
        else:
            self.esmg.showMessage('You should input all labels correctly.')

    def cancleButtonClicked(self):
        self.textEdit.setText('')
        self.textEdit_2.setText('')
        self.textEdit_3.setText('')

    def close2(self):
        pass
