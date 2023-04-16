from PyQt6.QtWidgets import QMainWindow, QWidget
from gui.views.connect_screen import Ui_ConnectScreen

# Screen for connecting to C2 Server
class ConnectScreen(QWidget, Ui_ConnectScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connectScreenStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.connectScreenStyleSheet)



    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/connectScreen.css", "r")
        return remoteMachinesStyleSheet.read()
