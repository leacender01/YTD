# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Command.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Command(object):
    def setupUi(self, Command):
        Command.setObjectName("Command")
        Command.resize(400, 300)
        Command.setAccessibleName("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Command)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Command)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 228))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.pushButton = QtWidgets.QPushButton(Command)
        self.pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 1)

        self.retranslateUi(Command)
        QtCore.QMetaObject.connectSlotsByName(Command)

    def retranslateUi(self, Command):
        _translate = QtCore.QCoreApplication.translate
        Command.setWindowTitle(_translate("Command", "任務視窗"))
        self.label.setText(_translate("Command", "開始執行"))
        self.pushButton.setText(_translate("Command", "執行中"))

