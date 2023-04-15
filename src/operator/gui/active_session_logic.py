import sys
import socket
import threading

from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QDialog
from gui.views.active_session import Ui_Active_Session

from pb import operatorpb_pb2

class TabWidget(QDialog):
    def __init__(self, listener, outputq, session_outputq, sessionq):
        super().__init__()

        self.tab_id = {}
        self.listener = listener
        self.outputq = outputq
        #self.session_outputq = session_outputq
        self.sessionq = sessionq
        #threading.Thread(target=self.sessionHandler, args=(sessionq,)).start()

        self.tabwidget = QTabWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)
        self.setLayout(vbox)

    #    threading.Thread(target=self.outputHandler, args=(outputq,)).start()
        threading.Thread(target=self.sessionOutputHandler, args=(session_outputq,)).start()

    def newTab(self, id, user, os):
        self.listener.send(f"use {id}")

        tab = self.tabwidget.addTab(ActiveSession(self.listener, id, self.tab_id, self.tabwidget,f"{user}/{os}"), f"{user}/{os}")

        self.tab_id[id] = tab

    '''
    # handle new session connections
    def sessionHandler(self, sessionq):
        while True:
            new_session = sessionq.get()

            if new_session:
                print(f"Connected to session {new_session.addr}")

            else:
                break

    # prints output messages received from the server
    def outputHandler(self, outputq):
        while True:
            #output, id = outputq.get()
            output = outputq.get()

            if not output:
                break

            else:
                #self.guiPrint(output)
                pass
    '''

    # prints output messages received from the server
    def sessionOutputHandler(self, session_outputq):
        while True:
            output, id = session_outputq.get()

            if not output:
                continue

            else:
                tab = self.tab_id[id]

                self.tabwidget.widget(tab).terminalOutput.appendPlainText(output)
                self.tabwidget.widget(tab).terminalOutput.verticalScrollBar().setValue(self.tabwidget.widget(tab).terminalOutput.verticalScrollBar().maximum())

    def guiPrint(self, text):
        self.terminalOutput.appendPlainText(text)
        self.terminalOutput.verticalScrollBar().setValue(self.terminalOutput.verticalScrollBar().maximum())


class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, listener, id, tab_id, tabwidget, title, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id = id
        self.tab_id = tab_id


        self.machineName.setText(title)
        self.terminalInput.returnPressed.connect(self.inputHandler)

        self.activeSessionStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.activeSessionStyleSheet)
        self.listener = listener
        self.tabwidget = tabwidget


    def inputHandler(self):
        msg = self.terminalInput.text()
        self.terminalInput.clear()
        self.listener.sendSession(msg, self.id)

        if msg.lower() == "exit":
            index = self.tabwidget.indexOf(self)
            self.tabwidget.removeTab(index)
            del self.tab_id[self.id]

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/activeSessionStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
