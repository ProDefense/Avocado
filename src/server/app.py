#!/usr/bin/env python3

import os

from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6.QtGui import QIcon
from main_window import Ui_MainWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication(sys.argv)
app.setApplicationName("Avocado")
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "assets/avocadologo.png")
app.setWindowIcon(QIcon(path))

window = Window()
window.show()

sys.exit(app.exec())
