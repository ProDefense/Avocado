# Form implementation generated from reading ui file 'gui/resources/ui/generate_screen.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GenerateScreen(object):
    def setupUi(self, GenerateScreen):
        GenerateScreen.setObjectName("GenerateScreen")
        GenerateScreen.resize(600, 350)
        GenerateScreen.setMinimumSize(QtCore.QSize(600, 350))
        GenerateScreen.setMaximumSize(QtCore.QSize(600, 350))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        GenerateScreen.setFont(font)
        GenerateScreen.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(GenerateScreen)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(GenerateScreen)
        self.widget.setObjectName("widget")
        self.Port = QtWidgets.QTextEdit(self.widget)
        self.Port.setGeometry(QtCore.QRect(150, 130, 341, 41))
        self.Port.setObjectName("Port")
        self.Host = QtWidgets.QTextEdit(self.widget)
        self.Host.setGeometry(QtCore.QRect(150, 60, 341, 41))
        self.Host.setObjectName("Host")
        self.genBtn = QtWidgets.QPushButton(self.widget)
        self.genBtn.setGeometry(QtCore.QRect(200, 270, 201, 51))
        self.genBtn.setObjectName("genBtn")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(70, 140, 58, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(70, 210, 58, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(70, 70, 58, 16))
        self.label_3.setObjectName("label_3")
        self.windownBtn = QtWidgets.QRadioButton(self.widget)
        self.windownBtn.setGeometry(QtCore.QRect(320, 210, 121, 20))
        self.windownBtn.setObjectName("windownBtn")
        self.linuxBtn = QtWidgets.QRadioButton(self.widget)
        self.linuxBtn.setGeometry(QtCore.QRect(190, 210, 121, 20))
        self.linuxBtn.setObjectName("linuxBtn")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(GenerateScreen)
        QtCore.QMetaObject.connectSlotsByName(GenerateScreen)

    def retranslateUi(self, GenerateScreen):
        _translate = QtCore.QCoreApplication.translate
        GenerateScreen.setWindowTitle(_translate("GenerateScreen", "Connect"))
        self.genBtn.setText(_translate("GenerateScreen", "Generate"))
        self.label.setText(_translate("GenerateScreen", "Port"))
        self.label_2.setText(_translate("GenerateScreen", "OS"))
        self.label_3.setText(_translate("GenerateScreen", "Host"))
        self.windownBtn.setText(_translate("GenerateScreen", "Windows"))
        self.linuxBtn.setText(_translate("GenerateScreen", "Linux"))
