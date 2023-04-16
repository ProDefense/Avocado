import sys
import threading

from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QDialog
from gui.views.active_session import Ui_Active_Session
from PyQt6.QtCore import QTimer


class TabWidget(QDialog):
    def __init__(self, listener, session_outputq):
        super().__init__()

        self.tab_id = {}
        self.listener = listener


        self.tabwidget = QTabWidget()
        self.tabwidget.setTabsClosable(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabwidget)
        self.setLayout(vbox)

        self.tabwidget.currentChanged.connect(self.onChange)
        self.tabwidget.tabCloseRequested.connect(self.onClose)

        threading.Thread(target=self.sessionOutputHandler, args=(session_outputq,)).start()

    def onClose(self, index):
        widget = self.tabwidget.widget(index)
        del self.tab_id[widget.id]
        widget.deleteLater()
        self.tabwidget.removeTab(index)

    def onChange(self, index):
        if (index != -1):
            QTimer.singleShot(0, lambda: self.tabwidget.widget(index).terminalInput.setFocus())

    def newTab(self, id, user, os):
        if id in self.tab_id:
            self.tabwidget.setCurrentIndex(self.tab_id[id])
            return

        tab = self.tabwidget.addTab(ActiveSession(self.listener, id, self.tab_id, self.tabwidget,f"{user}/{os}"), f"{user}/{os}")

        self.tab_id[id] = tab

        self.tabwidget.setCurrentIndex(tab)

    # prints output messages received from the server
    def sessionOutputHandler(self, session_outputq):
        while True:
            out = session_outputq.get()

            if not out:
                break

            elif out[0]:
                output, id = out
                tab = self.tab_id[id]
                self.tabwidget.widget(tab).terminalOutput.appendPlainText(output)
                self.tabwidget.widget(tab).terminalOutput.verticalScrollBar().setValue(self.tabwidget.widget(tab).terminalOutput.verticalScrollBar().maximum())


class ActiveSession(QWidget, Ui_Active_Session):
    def __init__(self, listener, id, tab_id, tabwidget, title, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id = id
        self.tab_id = tab_id

        self.machineName.setText(title)
        self.terminalInput.returnPressed.connect(self.inputHandler)

        self.activeSessionStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.activeSessionStyleSheet)
        self.listener = listener
        self.tabwidget = tabwidget

    def inputHandler(self):
        msg = self.terminalInput.text()
        self.terminalInput.clear()
        self.listener.sendSession(msg, self.id)

        if msg.lower() == "exit":
            index = self.tab_id[self.id]
            self.tabwidget.removeTab(index)
            del self.tab_id[self.id]

    def loadStyleSheet(self):
        remoteMachinesStyleSheet = open("gui/resources/stylesheets/activeSessionStyleSheet.css", "r")
        return remoteMachinesStyleSheet.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ActiveSession()
    widget.show()
    sys.exit(app.exec())
