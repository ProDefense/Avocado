import os

from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avocado C2")

app = QApplication(sys.argv)
app.setApplicationName("Avocado")
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'assets/avocadologo.png')
app.setWindowIcon(QIcon(path))
window = Window()
window.show()
sys.exit(app.exec())

