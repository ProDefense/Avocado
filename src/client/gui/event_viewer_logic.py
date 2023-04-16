from queue import Queue
from PyQt6.QtWidgets import QWidget
from client.gui.views.event_viewer import Ui_EventViewer

class EventViewer(QWidget, Ui_EventViewer):

    def __init__(self):
        super(EventViewer, self).__init__()
        self.setupUi(self)

        self.eventStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.eventStyleSheet)
        self.handleTest()

    def loadStyleSheet(self):
        eventStyleSheet = open("client/gui/resources/stylesheets/eventStyleSheet.css", "r")
        return eventStyleSheet.read()

    def handleTest(self):
        self.textEdit.append('Event Viewer logging..')

    def logToEventViewer(self, text):
        self.textEdit.append(text)

