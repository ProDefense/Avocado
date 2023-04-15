#!/usr/bin/env python3

import os
import sys
import ast
import threading
from queue import Queue

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QIcon, QAction

from gui.active_session_logic import TabWidget
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


    def rowCount(self, parent=QModelIndex()):
        return len(self.machines)

    def columnCount(self, parent=QModelIndex()):
        return 6

    def data(self, index, role=DisplayRole):
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

    def getId(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][0])
    def getOs(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][3])

    def getUser(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][5])

class RemoteMachines(QWidget, Ui_RemoteMachines):
    def __init__(self, tabwidget):
        self.tabwidget = tabwidget
        super(RemoteMachines, self).__init__()
        self.setupUi(self)

        self.implant_list: list = []
        self.header = ["id", "host", "port", "os", "pid", "user"]

        self._remoteMachinesModel = RemoteMachinesModel(self.implant_list, self.header)

        self.implants.setModel(self._remoteMachinesModel)
        self.remoteMachinesStyleSheet = self.loadStyleSheet()
        self.implants.setStyleSheet(self.remoteMachinesStyleSheet)
        self.implants.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.implants.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.implants.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.implants.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.implants.verticalHeader().setVisible(False)

        self.implants.doubleClicked.connect(self.interact)



    def interact(self, index):
        id = self.implants.model().getId(index).value()
        user = self.implants.model().getUser(index).value()
        os = self.implants.model().getOs(index).value()
        self.tabwidget.newTab(id, user, os)



    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/remoteMachineStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()

    def addImplant(self, new_implant):
        self.implant_list.append(new_implant)
        self.implants.model().layoutChanged.emit()


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
        session_outputq = Queue()
        self.listener = Listener(hostname, port, session_outputq, implantq)

        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.generateAction.triggered.connect(lambda: self.listener.send("generate"))

        # add connect button to Avocado menu bar
        openConnectScreen = QAction(self)
        openConnectScreen.setText("Connect")
        openConnectScreen.triggered.connect(self.connectScreen)
        self.menuAvocado.addAction(openConnectScreen)

        layout = QVBoxLayout()

        # add active session and remote machines table to one widget
        tabwidget = TabWidget(self.listener,session_outputq)
        self.remote_machines = RemoteMachines(tabwidget)

        layout.addWidget(self.remote_machines)
        layout.addWidget(tabwidget)
        # widget holds layout
        widget = QWidget()
        widget.setLayout(layout)
        # stylesheet
        self.mainAppStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.mainAppStyleSheet)

        self.setCentralWidget(widget)

        threading.Thread(target=self.implantHandler, args=(implantq,)).start()

    def closeEvent(self, event):
        self.listener.terminate()
        event.accept()

    # handle new implants
    def implantHandler(self,implantq):
        while True:
            new_implant = implantq.get()
            if new_implant:
                self.remote_machines.addImplant([
                    new_implant.id,
                    ast.literal_eval(new_implant.addr)[0],
                    ast.literal_eval(new_implant.addr)[1],
                    new_implant.os,
                    new_implant.pid,
                    new_implant.user.name])

            else:
                break

    def connectScreen(self):
        self.w = ConnectScreen()
        self.w.show()

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/mainWindowStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Avocado")
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "assets/avocadologo.png")
    app.setWindowIcon(QIcon(path))

    window = MainApp()
    window.show()

    sys.exit(app.exec())
