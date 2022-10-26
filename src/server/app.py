#!/usr/bin/env python3

import os

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QStyle
import sys
from PyQt6.QtGui import QIcon
DisplayRole = Qt.ItemDataRole.DisplayRole
Horizontal = Qt.Orientation.Horizontal


from main_window import Ui_MainWindow


class RemoteMachinesModel(QAbstractTableModel):
    def __init__(self, machines, headers):
        super(RemoteMachinesModel, self).__init__()
        self.machines = machines
        self.headers = headers

    def rowCount(self, parent):
        return len(self.machines)

    def columnCount(self, parent):
        return len(self.machines[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][index.column()])

    def headerData(self, section, orientation, role=DisplayRole):
        if role != DisplayRole:
            return QtCore.QVariant()
        if orientation == Horizontal:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant(int(section + 1))


remoteMachineStyleSheet = """
QWidget {
    background-color: #24273A;
    color: "white";
}
QPushButton {
    font-size: 16px;
    background-color: "darkblue"
}
QLineEdit {
    background-color: "white";
    color: "black";
}
"""

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # test data
        data: list = [
            ["178.01.02", "54.01.02", "subaru", "win03", 4098, 38],
            ["156.01.02", "255.01.02", "teamc2", "win10", 4098, 40],

        ]
        header = ["external", "internal", "user", "name", "pid", "last"]

        self._remoteMachinesModel = RemoteMachinesModel(data, header)
        self.implants.setModel(self._remoteMachinesModel)

        self.implants.setStyleSheet(remoteMachineStyleSheet)
        self.implants.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.implants.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.implants.resizeColumnsToContents()


app = QApplication(sys.argv)
app.setApplicationName("Avocado")
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "assets/avocadologo.png")
app.setWindowIcon(QIcon(path))

window = MainWindow()
window.show()

sys.exit(app.exec())
