from PyQt6 import QtCore, QtWidgets
from gui.views.remote_machines import Ui_RemoteMachines
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWidgets import QWidget, QAbstractItemView, QHeaderView

DisplayRole = Qt.ItemDataRole.DisplayRole
Horizontal = Qt.Orientation.Horizontal

class RemoteMachinesModel(QAbstractTableModel):
    def __init__(self, machines, headers):
        super(RemoteMachinesModel, self).__init__()
        self.machines = machines
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.machines)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=DisplayRole):
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

    def getId(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][0])
    def getOs(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][3])

    def getUser(self, index, role=DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.machines[index.row()][5])

class RemoteMachines(QWidget, Ui_RemoteMachines):
    def __init__(self, tabwidget):
        self.tabwidget = tabwidget
        super(RemoteMachines, self).__init__()
        self.setupUi(self)

        self.implant_list: list = []
        self.header = ["id", "host", "port", "os", "pid", "user"]

        self._remoteMachinesModel = RemoteMachinesModel(self.implant_list, self.header)

        self.implants.setModel(self._remoteMachinesModel)
        self.remoteMachinesStyleSheet = self.loadStyleSheet()
        self.implants.setStyleSheet(self.remoteMachinesStyleSheet)
        self.implants.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.implants.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.implants.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.implants.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.implants.verticalHeader().setVisible(False)

        self.implants.doubleClicked.connect(self.interact)

    def interact(self, index):
        id = self.implants.model().getId(index).value()
        user = self.implants.model().getUser(index).value()
        os = self.implants.model().getOs(index).value()
        self.tabwidget.newTab(id, user, os)

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/remoteMachineStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()

    def addImplant(self, new_implant):
        self.implant_list.append(new_implant)
        self.implants.model().layoutChanged.emit()
