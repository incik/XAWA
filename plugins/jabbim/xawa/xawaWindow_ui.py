# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xawaWindow.ui'
#
# Created: Sun Oct 24 19:35:08 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 100, 75, 24))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 24))
        self.menubar.setObjectName("menubar")
        self.menuXAWA = QtGui.QMenu(self.menubar)
        self.menuXAWA.setObjectName("menuXAWA")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout_XAWA = QtGui.QAction(MainWindow)
        self.actionAbout_XAWA.setObjectName("actionAbout_XAWA")
        self.menuXAWA.addAction(self.actionAbout_XAWA)
        self.menubar.addAction(self.menuXAWA.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuXAWA.setTitle(QtGui.QApplication.translate("MainWindow", "XAWA", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_XAWA.setText(QtGui.QApplication.translate("MainWindow", "About XAWA", None, QtGui.QApplication.UnicodeUTF8))

