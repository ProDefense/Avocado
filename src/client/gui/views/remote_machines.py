# Form implementation generated from reading ui file 'ui/remote_machines.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RemoteMachines(object):
    def setupUi(self, RemoteMachines):
        RemoteMachines.setObjectName("RemoteMachines")
        RemoteMachines.resize(632, 422)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        RemoteMachines.setFont(font)
        RemoteMachines.setStyleSheet("background-color:#171724")
        self.gridLayout = QtWidgets.QGridLayout(RemoteMachines)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.implants = QtWidgets.QTableView(RemoteMachines)
        self.implants.setObjectName("implants")
        self.gridLayout.addWidget(self.implants, 0, 0, 1, 1)

        self.retranslateUi(RemoteMachines)
        QtCore.QMetaObject.connectSlotsByName(RemoteMachines)

    def retranslateUi(self, RemoteMachines):
        _translate = QtCore.QCoreApplication.translate
        RemoteMachines.setWindowTitle(_translate("RemoteMachines", "Form"))
