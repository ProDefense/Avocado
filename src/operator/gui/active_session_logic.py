import sys
import socket
import threading

from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QDialog
from gui.views.active_session import Ui_Active_Session

from pb import operatorpb_pb2

class TabWidget(QDialog):
    def __init__(self, listener,outputq,sessionq):
        super().__init__()

        self.listener = listener
        self.outputq = outputq
        self.sessionq = sessionq
        threading.Thread(target=self.sessionHandler, args=(outputq,sessionq,)).start()

        self.tabwidget = QTabWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)
        self.setLayout(vbox)

    def newTab(self, id, user, os):
        self.listener.send(f"use {id}")
        self.tab = self.tabwidget.addTab(ActiveSession(self.listener,self.outputq,self.sessionq, self.tabwidget,f"{user}/{os}"), f"{user}/{os}")

    # handle new session connections
    def sessionHandler(self, outputq, sessionq):
        while True:
            new_session = sessionq.get()

            if new_session:
                print(f"Connected to session {new_session.addr}")

            else:
                break


class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, listener, outputq, sessionq, tabwidget, title, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        self.machineName.setText(title)
        self.terminalInput.returnPressed.connect(self.inputHandler)

        self.activeSessionStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.activeSessionStyleSheet)
        self.listener = listener
        self.tabwidget = tabwidget

        self.stop_thread = False

        self.thread = threading.Thread(target=self.outputHandler, args=(outputq,))
        self.thread.start()



    # prints output messages received from the server
    def outputHandler(self, outputq):
        while not self.stop_thread:
            output = outputq.get()

            if not output:
                break

            else:
                self.guiPrint(output)

    def guiPrint(self, text):
        self.terminalOutput.appendPlainText(text)
        self.terminalOutput.verticalScrollBar().setValue(self.terminalOutput.verticalScrollBar().maximum())



    def inputHandler(self):
        msg = self.terminalInput.text()
        self.terminalInput.clear()
        self.listener.send(msg)

        if msg.lower() == "exit":
            self.stop_thread = True

            index = self.tabwidget.indexOf(self)
            self.tabwidget.removeTab(index)

            self.listener.send("---") # workaround to ensure the output thread is closed


    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/activeSessionStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
