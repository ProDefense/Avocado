import sys
import socket

from PyQt6.QtWidgets import QApplication, QWidget
from gui.views.active_session import Ui_Active_Session

class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, s, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.terminalInput.returnPressed.connect(self.inputHandler)
        self.activeSessionStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.activeSessionStyleSheet)
        self.s = s


    def guiPrint(self, text):
        self.terminalOutput.appendPlainText(text)

    def inputHandler(self):
        msg = self.terminalInput.text()
        self.terminalInput.clear()

        self.s.send(msg.encode('ascii'))
        data = self.s.recv(1024)

        if msg.lower() == "exit":
            self.guiPrint("[+]Connection Terminated")
            self.s.close() 
            exit()

        elif (not data):
            self.guiPrint("no data")
        else:
            self.guiPrint("[+]Recv: " + str(data.decode('ascii')))


    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/activeSessionStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
