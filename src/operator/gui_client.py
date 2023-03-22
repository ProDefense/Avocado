#!/usr/bin/env python3

import os
import socket
import sys
import threading
from queue import Queue

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QStyle, QVBoxLayout, QWidget, QMenu
from PyQt6.QtGui import QIcon, QAction

from gui.active_session_logic import ActiveSession
from gui.views.main_window import Ui_MainWindow
from gui.views.remote_machines import Ui_RemoteMachines
from gui.views.connect_screen import Ui_ConnectScreen

from listener.listener import Listener

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
        return 4

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

        self.implant_list: list = []
        self.header = ["addr", "os", "pid", "user"]

        self._remoteMachinesModel = RemoteMachinesModel(self.implant_list, self.header)

        self.implants.setModel(self._remoteMachinesModel)
        self.remoteMachinesStyleSheet = self.loadStyleSheet()
        self.implants.setStyleSheet(self.remoteMachinesStyleSheet)
        self.implants.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.implants.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.implants.resizeColumnsToContents()
        self.implants.verticalHeader().setVisible(False)


    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/remoteMachineStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()

    def addImplant(self, new_implant):
        self.implant_list.append(new_implant)
        # Update the model with the new data
        self._remoteMachinesModel.beginInsertRows(QtCore.QModelIndex(), len(self.implant_list) - 1, len(self.implant_list) - 1)
        self._remoteMachinesModel.endInsertRows()

        # Resize the columns to fit the data 
        # TODO: figure out why it's not resizing properly
        self.implants.setModel(self._remoteMachinesModel)
        self.implants.resizeColumnsToContents()


# Screen for connecting to C2 Server
class ConnectScreen(QMainWindow, Ui_ConnectScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connectScreenStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.connectScreenStyleSheet)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/connectScreen.css", "r")
        return remoteMachinesStyleSheet.read()

# Main app that connects widgets into one window
class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # set up connection w/ server
        hostname = "127.0.0.1"
        port = 12345

        implantq = Queue()
        sessionq = Queue()
        outputq = Queue()

        listener = Listener(hostname, port, outputq, implantq, sessionq)

        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # add connect button to Avocado menu bar
        openConnectScreen = QAction(self)
        openConnectScreen.setText("Connect")
        openConnectScreen.triggered.connect(self.connectScreen)
        self.menuAvocado.addAction(openConnectScreen)

        layout = QVBoxLayout()
        # add active session and remote machines table to one widget
        self.remote_machines = RemoteMachines()

        layout.addWidget(self.remote_machines)
        layout.addWidget(ActiveSession(listener, outputq))
        # widget holds layout
        widget = QWidget()
        widget.setLayout(layout)
        # stylesheet
        self.mainAppStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.mainAppStyleSheet)

        self.setCentralWidget(widget)

        threading.Thread(target=self.implantHandler, args=(implantq,)).start()
        threading.Thread(target=self.sessionHandler, args=(sessionq,)).start()

    # handle new implants
    def implantHandler(self,implantq):
        while True:
            new_implant = implantq.get()

            if new_implant:
                self.remote_machines.addImplant([
                    new_implant.addr,
                    new_implant.os,
                    new_implant.pid,
                    new_implant.user.name])

            else:
                break

    # handle new session connections
    def sessionHandler(self, sessionq):
        while True:
            new_session = sessionq.get()

            if new_session:
                print(f"Connected to session {new_session.addr}")
                #threading.Thread(target=inputHandler, args=(listener, output_received, session_closed, "Session")).start()

            else:
                break

    def connectScreen(self):
        self.w = ConnectScreen()
        self.w.show()

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/mainWindowStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Avocado")
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "assets/avocadologo.png")
    app.setWindowIcon(QIcon(path))

    window = MainApp()
    window.show()

    sys.exit(app.exec())
