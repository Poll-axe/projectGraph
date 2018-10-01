# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2351, 1352)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 170, 621, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menu1 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu1.setObjectName("menu1")
        self.verticalLayout.addWidget(self.menu1)
        self.menu2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu2.setObjectName("menu2")
        self.verticalLayout.addWidget(self.menu2)
        self.menu3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu3.setObjectName("menu3")
        self.verticalLayout.addWidget(self.menu3)
        self.menu4 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu4.setObjectName("menu4")
        self.verticalLayout.addWidget(self.menu4)
        self.menu5 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu5.setObjectName("menu5")
        self.verticalLayout.addWidget(self.menu5)
        self.menu6 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu6.setObjectName("menu6")
        self.verticalLayout.addWidget(self.menu6)

        self.menu7 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.menu7.setObjectName("menu7")
        self.verticalLayout.addWidget(self.menu7)

        self.runbut = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.runbut.setObjectName("runbut")
        self.verticalLayout.addWidget(self.runbut)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 600, 721, 571))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 70, 619, 101))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 0, 601, 51))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(740, 30, 1561, 1201))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 1170, 187, 57))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2351, 47))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu1.setText(_translate("MainWindow", "1. Информация по id"))
        self.menu2.setText(_translate("MainWindow", "2. Получить список друзей"))
        self.menu3.setText(_translate("MainWindow", "3. получить общих друзей"))
        self.menu4.setText(_translate("MainWindow", "4. Вывести список известных личностей"))
        self.menu5.setText(_translate("MainWindow", "5. построение графа"))
        self.menu6.setText(_translate("MainWindow", "6. друзья друзей"))

        self.menu7.setText(_translate("MainWindow", "7. сортировка друзей по колличеству общих"))

        self.runbut.setText(_translate("MainWindow", "Выполнить действие"))
        self.label.setText(_translate("MainWindow", "Введите id"))
        self.pushButton.setText(_translate("MainWindow", "очистить"))
