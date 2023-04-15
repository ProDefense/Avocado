from PyQt6.QtWidgets import QWidget

from src.operator.gui.views.event_viewer import Ui_EventViewer


class EventViewer(QWidget, Ui_EventViewer):

    def __init__(self):
        # self.tabwidget = tabwidget
        super(EventViewer, self).__init__()
        self.setupUi(self)

        self.eventStyleSheet = self.loadStyleSheet()
        self.setStyleSheet(self.eventStyleSheet)
        self.handleTest()

    def loadStyleSheet(self):
        eventStyleSheet = open("gui/resources/stylesheets/eventStyleSheet.css", "r")
        return eventStyleSheet.read()

    def handleTest(self):
        self.textEdit.append('Event Viewer logging..')

    def logToEventViewer(self, text):
        self.textEdit.append(text)

