# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainGui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1106, 763)
        MainWindow.setMinimumSize(QSize(1106, 763))
        MainWindow.setMaximumSize(QSize(1106, 763))
        MainWindow.setMouseTracking(False)
        icon = QIcon()
        icon.addFile(u"ui/handIcon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.System = QFrame(self.centralwidget)
        self.System.setObjectName(u"System")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.System.sizePolicy().hasHeightForWidth())
        self.System.setSizePolicy(sizePolicy1)
        self.System.setMinimumSize(QSize(0, 0))
        self.System.setMaximumSize(QSize(250, 16777215))
        self.System.setFrameShape(QFrame.StyledPanel)
        self.System.setFrameShadow(QFrame.Sunken)
        self.System.setLineWidth(1)
        self.ConnectButton = QPushButton(self.System)
        self.ConnectButton.setObjectName(u"ConnectButton")
        self.ConnectButton.setGeometry(QRect(10, 560, 221, 31))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ConnectButton.setFont(font)
        self.WelcomeText = QLabel(self.System)
        self.WelcomeText.setObjectName(u"WelcomeText")
        self.WelcomeText.setGeometry(QRect(10, 0, 231, 81))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        font1.setWeight(75)
        self.WelcomeText.setFont(font1)
        self.WelcomeText.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.WelcomeText.setWordWrap(True)
        self.WelcomeText2 = QLabel(self.System)
        self.WelcomeText2.setObjectName(u"WelcomeText2")
        self.WelcomeText2.setGeometry(QRect(20, 70, 211, 251))
        self.WelcomeText2.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.WelcomeText2.setWordWrap(True)
        self.SystemStatusText = QLabel(self.System)
        self.SystemStatusText.setObjectName(u"SystemStatusText")
        self.SystemStatusText.setGeometry(QRect(10, 370, 231, 31))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setWeight(75)
        self.SystemStatusText.setFont(font2)
        self.line = QFrame(self.System)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 350, 251, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layoutWidget = QWidget(self.System)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 420, 211, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.layoutWidget)
        self.label_25.setObjectName(u"label_25")
        font3 = QFont()
        font3.setPointSize(16)
        self.label_25.setFont(font3)

        self.horizontalLayout_2.addWidget(self.label_25)

        self.connectedBox = QCheckBox(self.layoutWidget)
        self.connectedBox.setObjectName(u"connectedBox")
        self.connectedBox.setEnabled(True)
        self.connectedBox.setFocusPolicy(Qt.StrongFocus)
        self.connectedBox.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.connectedBox.setAcceptDrops(False)
        self.connectedBox.setIconSize(QSize(80, 80))
        self.connectedBox.setCheckable(False)
        self.connectedBox.setTristate(False)

        self.horizontalLayout_2.addWidget(self.connectedBox)

        self.layoutWidget1 = QWidget(self.System)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 460, 211, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.layoutWidget1)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font3)

        self.horizontalLayout_3.addWidget(self.label_26)

        self.poweredBox = QCheckBox(self.layoutWidget1)
        self.poweredBox.setObjectName(u"poweredBox")
        self.poweredBox.setCheckable(False)

        self.horizontalLayout_3.addWidget(self.poweredBox)


        self.horizontalLayout.addWidget(self.System)

        self.Experiment = QFrame(self.centralwidget)
        self.Experiment.setObjectName(u"Experiment")
        self.Experiment.setFrameShape(QFrame.StyledPanel)
        self.Experiment.setFrameShadow(QFrame.Sunken)
        self.gridLayout = QGridLayout(self.Experiment)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Setup = QFrame(self.Experiment)
        self.Setup.setObjectName(u"Setup")
        self.Setup.setFrameShape(QFrame.StyledPanel)
        self.Setup.setFrameShadow(QFrame.Sunken)
        self.label_15 = QLabel(self.Setup)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 0, 381, 31))
        self.label_15.setFont(font2)
        self.layoutWidget2 = QWidget(self.Setup)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 40, 381, 286))
        self.gridLayout_3 = QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.BeginButton = QPushButton(self.layoutWidget2)
        self.BeginButton.setObjectName(u"BeginButton")
        self.BeginButton.setFont(font)

        self.gridLayout_3.addWidget(self.BeginButton, 10, 2, 1, 1)

        self.label_16 = QLabel(self.layoutWidget2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 3, 0, 1, 2)

        self.label_17 = QLabel(self.layoutWidget2)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 3, 3, 1, 1)

        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 2)

        self.label_8 = QLabel(self.layoutWidget2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 2)

        self.label_13 = QLabel(self.layoutWidget2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_3.addWidget(self.label_13, 2, 3, 1, 1)

        self.label_20 = QLabel(self.layoutWidget2)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 6, 0, 1, 2)

        self.VelocitiesInput = QLineEdit(self.layoutWidget2)
        self.VelocitiesInput.setObjectName(u"VelocitiesInput")

        self.gridLayout_3.addWidget(self.VelocitiesInput, 2, 2, 1, 1)

        self.BodySite = QComboBox(self.layoutWidget2)
        self.BodySite.addItem("")
        self.BodySite.addItem("")
        self.BodySite.addItem("")
        self.BodySite.addItem("")
        self.BodySite.addItem("")
        self.BodySite.setObjectName(u"BodySite")

        self.gridLayout_3.addWidget(self.BodySite, 1, 2, 1, 1)

        self.label_9 = QLabel(self.layoutWidget2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 7, 0, 1, 2)

        self.label_11 = QLabel(self.layoutWidget2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 7, 3, 1, 1)

        self.label_12 = QLabel(self.layoutWidget2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 8, 3, 1, 1)

        self.label_14 = QLabel(self.layoutWidget2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 9, 0, 1, 4)

        self.label_10 = QLabel(self.layoutWidget2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 8, 0, 1, 2)

        self.label_6 = QLabel(self.layoutWidget2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setLineWidth(1)
        self.label_6.setMidLineWidth(0)

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 2)

        self.MovementDirection = QComboBox(self.layoutWidget2)
        self.MovementDirection.addItem("")
        self.MovementDirection.addItem("")
        self.MovementDirection.addItem("")
        self.MovementDirection.setObjectName(u"MovementDirection")

        self.gridLayout_3.addWidget(self.MovementDirection, 0, 2, 1, 1)

        self.label_18 = QLabel(self.layoutWidget2)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 11, 0, 1, 4)

        self.distanceInput = QLineEdit(self.layoutWidget2)
        self.distanceInput.setObjectName(u"distanceInput")

        self.gridLayout_3.addWidget(self.distanceInput, 3, 2, 1, 1)

        self.repetitionsInput = QLineEdit(self.layoutWidget2)
        self.repetitionsInput.setObjectName(u"repetitionsInput")

        self.gridLayout_3.addWidget(self.repetitionsInput, 6, 2, 1, 1)

        self.VastimeInput = QLineEdit(self.layoutWidget2)
        self.VastimeInput.setObjectName(u"VastimeInput")

        self.gridLayout_3.addWidget(self.VastimeInput, 7, 2, 1, 1)

        self.intertrialIntput = QLineEdit(self.layoutWidget2)
        self.intertrialIntput.setObjectName(u"intertrialIntput")

        self.gridLayout_3.addWidget(self.intertrialIntput, 8, 2, 1, 1)


        self.gridLayout.addWidget(self.Setup, 0, 0, 1, 1)

        self.Subject = QFrame(self.Experiment)
        self.Subject.setObjectName(u"Subject")
        self.Subject.setFrameShape(QFrame.StyledPanel)
        self.Subject.setFrameShadow(QFrame.Sunken)
        self.label = QLabel(self.Subject)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 381, 31))
        self.label.setFont(font2)
        self.ResetButton = QPushButton(self.Subject)
        self.ResetButton.setObjectName(u"ResetButton")
        self.ResetButton.setGeometry(QRect(320, 270, 75, 23))
        self.ResetButton.setFont(font)
        self.layoutWidget3 = QWidget(self.Subject)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(11, 40, 381, 111))
        self.gridLayout_2 = QGridLayout(self.layoutWidget3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ageInput = QLineEdit(self.layoutWidget3)
        self.ageInput.setObjectName(u"ageInput")

        self.gridLayout_2.addWidget(self.ageInput, 1, 1, 1, 1)

        self.subjectInput = QLineEdit(self.layoutWidget3)
        self.subjectInput.setObjectName(u"subjectInput")

        self.gridLayout_2.addWidget(self.subjectInput, 0, 1, 1, 1)

        self.genderInput = QComboBox(self.layoutWidget3)
        self.genderInput.addItem("")
        self.genderInput.addItem("")
        self.genderInput.addItem("")
        self.genderInput.addItem("")
        self.genderInput.addItem("")
        self.genderInput.setObjectName(u"genderInput")

        self.gridLayout_2.addWidget(self.genderInput, 2, 1, 1, 1)

        self.label_5 = QLabel(self.layoutWidget3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)

        self.handInput = QComboBox(self.layoutWidget3)
        self.handInput.addItem("")
        self.handInput.addItem("")
        self.handInput.addItem("")
        self.handInput.setObjectName(u"handInput")

        self.gridLayout_2.addWidget(self.handInput, 4, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_19 = QLabel(self.layoutWidget3)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 1, 2, 1, 1)

        self.label_3 = QLabel(self.layoutWidget3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.Subject, 0, 1, 1, 1)

        self.Output = QTabWidget(self.Experiment)
        self.Output.setObjectName(u"Output")
        sizePolicy1.setHeightForWidth(self.Output.sizePolicy().hasHeightForWidth())
        self.Output.setSizePolicy(sizePolicy1)
        self.Output.setTabShape(QTabWidget.Rounded)
        self.Page1 = QWidget()
        self.Page1.setObjectName(u"Page1")
        self.progressBar = QProgressBar(self.Page1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 290, 781, 23))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.ConsoleOutput = QPlainTextEdit(self.Page1)
        self.ConsoleOutput.setObjectName(u"ConsoleOutput")
        self.ConsoleOutput.setGeometry(QRect(10, 10, 781, 271))
        self.ConsoleOutput.setReadOnly(True)
        self.Output.addTab(self.Page1, "")
        self.Page2 = QWidget()
        self.Page2.setObjectName(u"Page2")
        self.demoButton = QPushButton(self.Page2)
        self.demoButton.setObjectName(u"demoButton")
        self.demoButton.setGeometry(QRect(320, 270, 471, 23))
        self.Output.addTab(self.Page2, "")
        self.Page3 = QWidget()
        self.Page3.setObjectName(u"Page3")
        self.AboutText = QLabel(self.Page3)
        self.AboutText.setObjectName(u"AboutText")
        self.AboutText.setGeometry(QRect(10, 20, 451, 121))
        self.AboutText.setWordWrap(True)
        self.label_21 = QLabel(self.Page3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(670, 90, 121, 91))
        self.label_21.setPixmap(QPixmap(u"thumbnail.svg"))
        self.label_21.setScaledContents(True)
        self.label_22 = QLabel(self.Page3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(520, 90, 121, 91))
        self.label_22.setPixmap(QPixmap(u"thumbnail.svg"))
        self.label_22.setScaledContents(True)
        self.label_23 = QLabel(self.Page3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(520, 210, 121, 91))
        self.label_23.setPixmap(QPixmap(u"thumbnail.svg"))
        self.label_23.setScaledContents(True)
        self.label_24 = QLabel(self.Page3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(670, 210, 121, 91))
        self.label_24.setPixmap(QPixmap(u"thumbnail.svg"))
        self.label_24.setScaledContents(True)
        self.Output.addTab(self.Page3, "")

        self.gridLayout.addWidget(self.Output, 1, 0, 1, 2)


        self.horizontalLayout.addWidget(self.Experiment)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 1106, 21))
        self.menubar.setDefaultUp(False)
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.Output.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MultiTAC", None))
        self.ConnectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.WelcomeText.setText(QCoreApplication.translate("MainWindow", u"Welcome to MultiTAC User Interface", None))
        self.WelcomeText2.setText(QCoreApplication.translate("MainWindow", u"\n"
"What is MultiTAC?\n"
"\n"
"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\n"
"", None))
        self.SystemStatusText.setText(QCoreApplication.translate("MainWindow", u"System Status", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Connected", None))
        self.connectedBox.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Powered", None))
        self.poweredBox.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Experiment Setup", None))
        self.BeginButton.setText(QCoreApplication.translate("MainWindow", u"Go!", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Distance", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Body Site", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Velocities", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"cm/s", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Repetitions per velocity", None))
        self.VelocitiesInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1;3;10;...", None))
        self.BodySite.setItemText(0, QCoreApplication.translate("MainWindow", u"Forearm", None))
        self.BodySite.setItemText(1, QCoreApplication.translate("MainWindow", u"Upper Back", None))
        self.BodySite.setItemText(2, QCoreApplication.translate("MainWindow", u"Lower Back", None))
        self.BodySite.setItemText(3, QCoreApplication.translate("MainWindow", u"Thigh", None))
        self.BodySite.setItemText(4, QCoreApplication.translate("MainWindow", u"Calf", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Maximum time for VAS response", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.label_14.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"InterTrial time interval", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Brush Movement", None))
        self.MovementDirection.setItemText(0, QCoreApplication.translate("MainWindow", u"Linear", None))
        self.MovementDirection.setItemText(1, QCoreApplication.translate("MainWindow", u"Circular", None))
        self.MovementDirection.setItemText(2, QCoreApplication.translate("MainWindow", u"Oval", None))

        self.label_18.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subject Information", None))
        self.ResetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.genderInput.setItemText(0, QCoreApplication.translate("MainWindow", u"Woman", None))
        self.genderInput.setItemText(1, QCoreApplication.translate("MainWindow", u"Man", None))
        self.genderInput.setItemText(2, QCoreApplication.translate("MainWindow", u"Transgender", None))
        self.genderInput.setItemText(3, QCoreApplication.translate("MainWindow", u"Non-binary/non-conforming", None))
        self.genderInput.setItemText(4, QCoreApplication.translate("MainWindow", u"Prefer not to respond", None))

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Handedness", None))
        self.handInput.setItemText(0, QCoreApplication.translate("MainWindow", u"Left", None))
        self.handInput.setItemText(1, QCoreApplication.translate("MainWindow", u"Right ", None))
        self.handInput.setItemText(2, QCoreApplication.translate("MainWindow", u"Ambidextrous", None))

        self.handInput.setCurrentText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Subject", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"years old", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Age", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Gender Identity", None))
#if QT_CONFIG(accessibility)
        self.Page1.setAccessibleName(QCoreApplication.translate("MainWindow", u"Page1", None))
#endif // QT_CONFIG(accessibility)
        self.Output.setTabText(self.Output.indexOf(self.Page1), QCoreApplication.translate("MainWindow", u"Console Ouput", None))
        self.demoButton.setText(QCoreApplication.translate("MainWindow", u"Execute demo!", None))
        self.Output.setTabText(self.Output.indexOf(self.Page2), QCoreApplication.translate("MainWindow", u"Demo", None))
        self.AboutText.setText(QCoreApplication.translate("MainWindow", u"Created By: Edgardo Silva - Universidad de Valpara\u00edso\n"
"Contact: edgardo.silva@uv.cl\n"
"\n"
"MultiTAC Project: Edgardo Silva; Grace Whitaker; Alejandro Weinstein; Wael El-Deredy; Francis McGlone\n"
"\n"
"Selected publications: ", None))
        self.label_21.setText("")
        self.label_22.setText("")
        self.label_23.setText("")
        self.label_24.setText("")
        self.Output.setTabText(self.Output.indexOf(self.Page3), QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

