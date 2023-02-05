#!/usr/bin/env python3

import os
import socket
import sys

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QStyle, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from active_session_logic import ActiveSession
from main_window import Ui_MainWindow
from remote_machines import Ui_RemoteMachines

DisplayRole = Qt.ItemDataRole.DisplayRole
Horizontal = Qt.Orientation.Horizontal


class RemoteMachinesModel(QAbstractTableModel):
    def __init__(self, machines, headers):
        super(RemoteMachinesModel, self).__init__()
        self.machines = machines
        self.headers = headers

    def rowCount(self, parent):
        return len(self.machines)

    def columnCount(self, parent):
        return len(self.machines[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][index.column()])

    def headerData(self, section, orientation, role=DisplayRole):
        if role != DisplayRole:
            return QtCore.QVariant()
        if orientation == Horizontal:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant(int(section + 1))


class RemoteMachines(QWidget, Ui_RemoteMachines):

    def __init__(self):
        super(RemoteMachines, self).__init__()
        self.setupUi(self)

        # test data
        data: list = [
            ["178.01.02", "54.01.02", "subaru", "win03", 4098, 38],
            ["156.01.02", "255.01.02", "teamc2", "win10", 4098, 40],

        ]
        header = ["external", "internal", "user", "name", "pid", "last"]
        self._remoteMachinesModel = RemoteMachinesModel(data, header)
        self.implants.setModel(self._remoteMachinesModel)
        self.remoteMachinesStyleSheet = self.loadStyleSheet()
        self.implants.setStyleSheet(self.remoteMachinesStyleSheet)
        self.implants.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.implants.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.implants.resizeColumnsToContents()
        self.implants.verticalHeader().setVisible(False)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("stylesheets/remoteMachineStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


# Main app that connects widgets into one window
class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # set up client connection
        host = "127.0.0.1"
        port = 12345
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,port))

        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        layout = QVBoxLayout()
        # add active session and remote machines table to one widget
        layout.addWidget(RemoteMachines())
        layout.addWidget(ActiveSession(s))
        # widget holds layout
        widget = QWidget()
        widget.setLayout(layout)
        # stylesheet
        self.mainAppStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.mainAppStyleSheet)

        self.setCentralWidget(widget)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("stylesheets/mainWindowStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


app = QApplication(sys.argv)
app.setApplicationName("Avocado")
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "assets/avocadologo.png")
app.setWindowIcon(QIcon(path))

window = MainApp()
window.show()

sys.exit(app.exec())
