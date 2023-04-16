from PyQt6.QtWidgets import QMainWindow, QWidget, QDialog
from client.gui.views.generate_screen import Ui_GenerateScreen
from generate.generate import generate

# Screen for generating an implant
class GenerateScreen(QDialog, QWidget, Ui_GenerateScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connectScreenStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.connectScreenStyleSheet)

        self.genBtn.clicked.connect(self.generate)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("client/gui/resources/stylesheets/connectScreen.css", "r")
        return remoteMachinesStyleSheet.read()

    def generate(self):
        # get the text from each QTextEdit and save it to a variable
        host = self.Host.toPlainText()
        port = self.Port.toPlainText()
        self.port_text = self.Port.toPlainText()

        if (self.linuxBtn.isChecked()):
            target_os = "linux"
        elif (self.windowsBtn.isChecked()):
            target_os = "windows"

        generate(endpoint, target_os)
        self.close()
