import sys
import socket
import threading

from PyQt6.QtWidgets import QApplication, QWidget
from gui.views.active_session import Ui_Active_Session

from pb import operatorpb_pb2

class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, listener, outputq, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.terminalInput.returnPressed.connect(self.inputHandler)
        self.activeSessionStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.activeSessionStyleSheet)
        self.listener = listener

        threading.Thread(target=self.outputHandler, args=(outputq,)).start()

    # prints output messages received from the server
    def outputHandler(self, outputq):
        while True:
            output = outputq.get()

            if not output:
                break

            else:
                self.guiPrint(output)

    def guiPrint(self, text):
        self.terminalOutput.appendPlainText(text)


    def inputHandler(self):
        msg = self.terminalInput.text()
        self.terminalInput.clear()
        self.listener.send(msg)

        if msg.lower() == "exit":
            self.guiPrint("[+]Connection Terminated")
            exit()

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/activeSessionStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
