from PyQt6.QtWidgets import QMainWindow, QWidget, QDialog
from client.gui.views.connect_screen import Ui_ConnectScreen

# Screen for connecting to C2 Server
class ConnectScreen(QDialog, QWidget, Ui_ConnectScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connectScreenStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.connectScreenStyleSheet)

        self.connectButton.clicked.connect(self.saveServerInfo)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("client/gui/resources/stylesheets/connectScreen.css", "r")
        return remoteMachinesStyleSheet.read()

    def saveServerInfo(self):
        # get the text from each QTextEdit and save it to a variable
        self.hostname_text = self.Host.toPlainText()
        self.port_text = self.Port.toPlainText()
        self.close()



