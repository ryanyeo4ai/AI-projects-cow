# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QTableWidget, QPushButton, QLineEdit, QComboBox, QMenuBar, QStatusBar,
                             QTableWidgetItem, QMessageBox, QHeaderView, QMainWindow, QErrorMessage, QDialog)
from PyQt5.QtCore import QRect, QCoreApplication, Qt, QMetaObject
from PyQt5.Qt import qApp
# from FarmCCTV.FarmCCTV_ui import Ui_FarmCCTV
from FarmCCTV.FarmCCTVall_ui import Ui_FarmCCTVall
# from SecureCCTV.SecureCCTV_ui import Ui_Secure
from SecureCCTV.SecureCCTVall_ui import Ui_SecureAll
from Manager.AddUser_ui import Ui_AddUser
import cv2
import pandas as pd
import os
import psutil
from Manager.URLs import checkCCTVs, checkAllCCTVs
from Manager import readUser
# import pymongo

class Ui_COW(object):
    def setupUi(self, COW):
        COW.resize(1000, 590)
        COW.setWindowTitle("Farm Managing")
        self.centralwidget = QWidget(COW)
        self.esmg = QErrorMessage(self.centralwidget)
        self.esmg.setWindowTitle("Notification")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QRect(10, 50, 980, 480))
        self.tableWidget.setColumnCount(6)
        indexes = ['Check', 'Owner', 'Phone', 'IP', 'CCTVs', 'Test']
        self.tableWidget.setHorizontalHeaderLabels(indexes)
        self.isSetManagerUiFirst = True
        self.setManagerUi()

        self.runAllRideButton = QPushButton('Run All Mounting', self.centralwidget)
        self.runAllRideButton.setGeometry(QRect(10, 540, 140, 20))
        self.runAllRideButton.clicked.connect(lambda: self.checkAllCCTVs('cow'))
        self.runAllPeopleButton = QPushButton('Run All People', self.centralwidget)
        self.runAllPeopleButton.setGeometry(QRect(840, 540, 140, 20))
        self.runAllPeopleButton.clicked.connect(lambda: self.checkAllCCTVs('people'))
        self.SearchButton = QPushButton("Search", self.centralwidget)
        self.SearchButton.setGeometry(QRect(430, 10, 50, 20))
        self.SearcLineEdit = QLineEdit(self.centralwidget)
        self.SearcLineEdit.setGeometry(QRect(335, 10, 90, 20))
        self.SearchComboBox = QComboBox(self.centralwidget)
        self.SearchComboBox.setGeometry(QRect(250, 10, 80, 20))
        # self.searchComboBox.addItem("Owner")
        self.SearchComboBox.addItem("Phone")
        # self.searchComboBox.addItem("IP")
        self.AddButton = QPushButton("Add User", self.centralwidget)
        self.AddButton.setGeometry(QRect(10, 10, 100, 23))
        self.AddButton.clicked.connect(self.AddUserWindowShow)
        self.SyncButton = QPushButton('Sync', self.centralwidget)
        self.SyncButton.setGeometry(QRect(120, 10, 100, 23))
        self.SyncButton.clicked.connect(self.setManagerUi)

        COW.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(COW)
        self.menubar.setGeometry(QRect(0, 0, 932, 21))
        COW.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(COW)
        COW.setStatusBar(self.statusbar)

        self.SearchButton.clicked.connect(self.SearchClicked)

    def readExcel(self):
        f_list, phones, LINEs, IPs, real_phones, farms, secures_ip = readUser.readusers()
        self.IPs = IPs
        self.farms = f_list
        self.phones = phones
        self.Lines = LINEs

        return len(self.farms)

    def setManagerUi(self):
        COL = 6
        ROW = self.readExcel()

        self.tableWidget.setRowCount(ROW)

        for row in range(ROW):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setCheckState(Qt.Checked)
            self.tableWidget.setItem(row, 0, item)
            for col in range(COL):
                item = QTableWidgetItem()
                if 0 < col <= 4:
                    item.setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if col == 2:
                        item.setText(str(self.phones[row]))
                    if col == 1:
                        item.setText(str(self.farms[row]))
                    if col == 4:
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setText(str(len(self.IPs[row])))
                    self.tableWidget.setItem(row, col, item)
                if col == 3:
                    self.IPcomboBox = QComboBox()
                    self.IPcomboBox.addItems(self.IPs[row])
                    self.tableWidget.setCellWidget(row, 3, self.IPcomboBox)
                if col == 5:
                    self.CellButton = QPushButton("Connect")
                    self.CellButton.clicked.connect(self.handleButtonClicked)
                    self.tableWidget.setCellWidget(row, col, self.CellButton)

        if self.isSetManagerUiFirst:
            header = self.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(8, QHeaderView.ResizeToContents)

            self.isSetManagerUiFirst = False

    def SearchClicked(self):
        if self.SearchComboBox.currentIndex() == 0:
            col_index = 0
        elif self.SearchComboBox.currentIndex() == 1:
            col_index = 1
        else:
            col_index = 2
            # items = self.tableWidget.findItems(self.lineEdit.text(), Qt.MatchExactly)
            # if items:
            #     results = '\n'.join('row %d column %d' % (item.row() + 1, item.column() + 1) for item in items)
            # else:
            #     results = 'Found Nothing'
            # QMessageBox.information(self, 'Search Results', results)
        try:
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, col_index)
                if col_index != 2:
                    if item and item.data(Qt.DisplayRole) == self.SearcLineEdit.text():
                        # self.tableWidget.selectRow(self.tableWidget.indexFromItem(item))
                        self.tableWidget.selectRow(row)
                        # print(self.tableWidget.indexFromItem(item))
                else:
                    if self.IPs[row] == self.SearcLineEdit.text():
                        self.tableWidget.selectRow(self.tableWidget.indexFromItem(item))
                        # self.tableWidget.selectRow(self.tableWidget.indexFromItem(item))
            # return QMessageBox.information(self, 'Search Results', 'None')
            print('success')
        except:
            # return QMessageBox.information(self, 'Search Fail', 'None')
            print('fail')

    def handleButtonClicked(self):
        button = qApp.focusWidget()
        # or button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        if index.isValid():
            col = index.column()
            if col == 5:
                self.checkCCTV('cow', index.row())
            # elif col == 7:
            #     self.checkCCTV('people', index.row())
            # elif col == 8:
            #     self.checkCCTVs('draw', index.row())
            # print(index.row(), index.column())

    def AddUserWindowShow(self):
        self.AddUserWindow = QMainWindow()
        self.AddUserUi = Ui_AddUser()
        self.AddUserUi.setupUi(self.AddUserWindow)
        # self.AddUserWindow.setupUi(self.AddUserUi)
        self.AddUserWindow.show()

    # def FarmCCTVWindowShow(self, index):
    #     self.FarmCCTVWindow = MyWindow()
    #     self.FarmCCTVUi = Ui_FarmCCTV()
    #     IP = self.URLs
    #     name = self.phones[index]
    #     self.FarmCCTVWindow.setupUi(self.FarmCCTVUi)
    #     self.FarmCCTVUi.setupUi(self.FarmCCTVWindow, IP, name)
    #     self.FarmCCTVWindow.show()

    def FarmCCTVallWindowShow(self):
        # p = psutil.Process()
        # print('farm processes')
        # p.cpu_affinity([13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
        # print(p.cpu_affinity())

        self.FarmCCTVallWindow = MyWindow()
        self.FarmCCTVallUi = Ui_FarmCCTVall()
        self.FarmCCTVallWindow.setupUi(self.FarmCCTVallUi)
        print('Setting FarmCCTV...')
        # print(len(self.URLs))
        # print(len(self.phoneAll))
        # self.checkExit()
        self.FarmCCTVallUi.setupUi(self.FarmCCTVallWindow, self.URLs, self.phoneAll, self.cctv_n)
        self.FarmCCTVallWindow.show()

    # def SecureWindowShow(self, index):
    #     self.SecureWindow = MyWindow()
    #     self.SecureUi = Ui_Secure()
    #     # IP = self.IPs[index]
    #     name = self.phones[index]
    #     self.SecureWindow.setupUi(self.SecureUi)
    #     self.SecureUi.setupUi(self.SecureWindow, self.URLs, name)
    #     self.SecureWindow.show()
    #     print('Secure Window')

    def SecureAllWindowShow(self):
        # p = psutil.Process()
        # print('person processes')
        # p.cpu_affinity([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        # print(p.cpu_affinity())

        # self.runAllPeopleButton.setEnabled(False)
        self.SecureAllWindow = MyWindow()
        self.SecureAllUi = Ui_SecureAll()
        # IP = self.IPs[index]
        self.SecureAllWindow.setupUi(self.SecureAllUi)
        print('Setting SecureCCTV...')
        self.SecureAllUi.setupUi(self.SecureAllWindow, self.URLs, self.phoneAll, self.Lines)
        self.SecureAllWindow.show()
        print('SeureAll window')

    def checkExit(self):
        for u in self.URLs:
            print(u)
        import sys
        sys.exit()

    def checkAllCCTVs(self, mode):
        self.statusbar.showMessage('checking all CCTVs...')

        errorMessage, self.URLs, self.phoneAll, self.cctv_n = checkAllCCTVs(self.IPs, self.phones, mode)
        # print(errorMessage, self.URLs, self.phoneAll, self.cctv_n)
        # errorMessage = 'none'

        self.statusbar.showMessage('check all CCTVs completed')
        print('checked cctv')
        # print(errorMessage)

        if errorMessage != '':
            choice = QMessageBox.question(self.centralwidget, 'Error', '%s errored' % errorMessage,
                                          QMessageBox.Yes, QMessageBox.No)
            if choice == QMessageBox.Yes:
                if mode == 'cow':
                    self.FarmCCTVallWindowShow()
                elif mode == 'people':
                    self.SecureAllWindowShow()
        else:
            if mode == 'cow':
                # print(212112121)
                # self.checkExit()
                self.FarmCCTVallWindowShow()
            elif mode == 'people':
                self.SecureAllWindowShow()

    def checkCCTV(self, mode, index):
        self.statusbar.showMessage("check %s farm CCTVs" % self.farms[index])
        errorMessage, URLs = checkCCTVs(self.IPs[index], self.phones[index], 'all')

        if errorMessage != '':
            self.esmg.showMessage(errorMessage)

        try:
            vids = []
            for url in URLs:
                vids.append(cv2.VideoCapture(url))

            for i, vid in enumerate(vids):
                ret, frame = vid.read()
                if ret:
                    cv2.imshow(URLs[i], frame)

        except:
            self.esmg.showMessage('something wrong')


class MyWindow(QMainWindow):
    def setupUi(self, MyWindow):
        self.ui_parent = MyWindow

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '메세지', "정말 종료하기를 원하십니까?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.ui_parent.close2()
            print('app close')
        else:
            event.ignore()