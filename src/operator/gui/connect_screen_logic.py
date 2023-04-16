from PyQt6.QtWidgets import QMainWindow, QWidget, QDialog
from gui.views.connect_screen import Ui_ConnectScreen

# Screen for connecting to C2 Server
class ConnectScreen(QDialog, QWidget, Ui_ConnectScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.hostname = None
        self.name = None
        self.port = None

        self.connectScreenStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.connectScreenStyleSheet)

        self.connectButton.clicked.connect(self.saveServerInfo)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/connectScreen.css", "r")
        return remoteMachinesStyleSheet.read()

    def saveServerInfo(self):
        # get the text from each QTextEdit and save it to a variable
        self.hostname_text = self.Host.toPlainText()
        self.name_text = self.Name.toPlainText()
        self.port_text = self.Port.toPlainText()
        self.close()



