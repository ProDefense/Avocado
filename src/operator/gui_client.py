#!/usr/bin/env python3

import os
import sys
import ast
import threading
from queue import Queue

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon, QAction

from gui.active_session_logic import TabWidget
from gui.remote_machines_logic import RemoteMachines
from gui.connect_screen_logic import ConnectScreen


from gui.views.main_window import Ui_MainWindow

from listener.listener import Listener
from src.operator.gui.event_viewer_logic import EventViewer


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
        tabwidget = TabWidget(self.listener, session_outputq)
        self.remote_machines = RemoteMachines(tabwidget)
        self.event_viewer = EventViewer()
        # layout.addWidget(self.event_viewer)

        hlay = QHBoxLayout()
        hlay.addWidget(self.remote_machines)
        hlay.addWidget(self.event_viewer)

        hWidget = QWidget()
        hWidget.setLayout(hlay)

        # Here, add a horizontal widget
        layout.addWidget(hWidget)

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
