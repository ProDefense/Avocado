# Form implementation generated from reading ui file 'gui/resources/ui/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(717, 572)
        font = QtGui.QFont()
        font.setFamily("Academy Engraved LET")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
"background-color:#16161D\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 717, 24))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuImplant = QtWidgets.QMenu(self.menubar)
        self.menuImplant.setObjectName("menuImplant")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setCheckable(False)
        self.actionAbout.setChecked(False)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionQuit_Avocado = QtGui.QAction(MainWindow)
        self.actionQuit_Avocado.setObjectName("actionQuit_Avocado")
        self.actionPlaceholder = QtGui.QAction(MainWindow)
        self.actionPlaceholder.setObjectName("actionPlaceholder")
        self.actionPlaceholder_2 = QtGui.QAction(MainWindow)
        self.actionPlaceholder_2.setObjectName("actionPlaceholder_2")
        self.generateAction = QtGui.QAction(MainWindow)
        self.generateAction.setObjectName("generateAction")
        self.actionPlaceholder_4 = QtGui.QAction(MainWindow)
        self.actionPlaceholder_4.setObjectName("actionPlaceholder_4")
        self.actionPlaceholder_5 = QtGui.QAction(MainWindow)
        self.actionPlaceholder_5.setObjectName("actionPlaceholder_5")
        self.menuImplant.addAction(self.generateAction)
        self.menubar.addAction(self.menuImplant.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Avocado 🥑"))
        self.menuImplant.setTitle(_translate("MainWindow", "Implant"))
        self.actionAbout.setText(_translate("MainWindow", "About Avocado"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))
        self.actionQuit_Avocado.setText(_translate("MainWindow", "Quit Avocado"))
        self.actionPlaceholder.setText(_translate("MainWindow", "Placeholder"))
        self.actionPlaceholder_2.setText(_translate("MainWindow", "Placeholder"))
        self.generateAction.setText(_translate("MainWindow", "Generate"))
        self.actionPlaceholder_4.setText(_translate("MainWindow", "Placeholder"))
        self.actionPlaceholder_5.setText(_translate("MainWindow", "Placeholder"))
