# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Searching.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchingPage(object):
    def setupUi(self, SearchingPage):
        SearchingPage.setObjectName("SearchingPage")
        SearchingPage.resize(653, 249)
        SearchingPage.setAccessibleName("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SearchingPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(SearchingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.urlInput = QtWidgets.QLineEdit(SearchingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.urlInput.sizePolicy().hasHeightForWidth())
        self.urlInput.setSizePolicy(sizePolicy)
        self.urlInput.setMinimumSize(QtCore.QSize(0, 33))
        self.urlInput.setSizeIncrement(QtCore.QSize(0, 0))
        self.urlInput.setBaseSize(QtCore.QSize(0, 0))
        self.urlInput.setObjectName("urlInput")
        self.verticalLayout_2.addWidget(self.urlInput)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_yes = QtWidgets.QPushButton(SearchingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_yes.sizePolicy().hasHeightForWidth())
        self.btn_yes.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.btn_yes.setFont(font)
        self.btn_yes.setObjectName("btn_yes")
        self.horizontalLayout.addWidget(self.btn_yes)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(SearchingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 10)

        self.retranslateUi(SearchingPage)
        self.pushButton.clicked.connect(SearchingPage.close)
        QtCore.QMetaObject.connectSlotsByName(SearchingPage)

    def retranslateUi(self, SearchingPage):
        _translate = QtCore.QCoreApplication.translate
        SearchingPage.setWindowTitle(_translate("SearchingPage", "監控網址"))
        self.label.setText(_translate("SearchingPage", "請輸入首頁網址"))
        self.btn_yes.setText(_translate("SearchingPage", "確認"))
        self.pushButton.setText(_translate("SearchingPage", "取消"))

