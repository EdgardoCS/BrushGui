# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vas.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(581, 190)
        icon = QIcon()
        icon.addFile(u"icons/VASIcon.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 579, 183))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.vasCurrent = QLCDNumber(self.frame)
        self.vasCurrent.setObjectName(u"vasCurrent")
        self.vasCurrent.setProperty("intValue", 1)

        self.horizontalLayout.addWidget(self.vasCurrent)


        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.vasSlider = QSlider(self.frame)
        self.vasSlider.setObjectName(u"vasSlider")
        self.vasSlider.setMinimum(-10)
        self.vasSlider.setMaximum(10)
        self.vasSlider.setOrientation(Qt.Horizontal)
        self.vasSlider.setTickPosition(QSlider.TicksBelow)
        self.vasSlider.setTickInterval(1)

        self.gridLayout.addWidget(self.vasSlider, 3, 0, 1, 3)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(14)
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 3)

        self.vasSubmit = QPushButton(self.frame)
        self.vasSubmit.setObjectName(u"vasSubmit")

        self.gridLayout_2.addWidget(self.vasSubmit, 3, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"VAS Input", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Current Selection", None))
        self.label.setText(QCoreApplication.translate("Form", u"Visual Analogue Scale ", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Neutral", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Pleasant", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Unpleasant", None))
        self.label_6.setText("")
        self.vasSubmit.setText(QCoreApplication.translate("Form", u"Submit", None))
    # retranslateUi

