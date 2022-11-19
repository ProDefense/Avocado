import sys

from PyQt6.QtWidgets import QApplication, QWidget
from active_session import Ui_Active_Session

class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.terminalInput.returnPressed.connect(self.inputHandler)

    
    def inputHandler(self):
        self.terminalOutput.appendPlainText("Hello World")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
