# Created by "EdgardoCS" at 22-Aug-23
__github__ = "https://github.com/EdgardoCS"
__email__ = "edgardo.silva@uv.cl"

import os
import sys
import random
import time
import queue
import threading
import screeninfo
# from PySide2 import QtWidgets
from BrushGui.axidraw import brush
from pyqtconsole.console import PythonConsole
import pandas as pd

from PyQt6 import QtWidgets, QtCore
from PyQt6.uic import loadUi
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QFileDialog


class AxiDraw(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.serial_port = 'COM3'
        self.running = True
        self.serial_status = False
        self.running = True
        # self.q_in = q_in
        # self.q_out = q_out

    def stop(self):
        self.running = False
        # Here we need to close the serial port!
        print('Axidraw thread stopped')

    def run(self):
        while self.running:
            continue

    def connectDevice(self):
        port = brush.findPort()  # Success!! Axidraw founded in ComPort
        print(port)
        if port:
            self.serial_port, self.serial_status = brush.openPort(port)
            if self.serial_port:
                if self.serial_status:
                    return self.serial_port.name
                    # self.q_out.put(self.serial_port.name, self.serial_status)
                    # print(self.serial_port.name)
                else:
                    return self.serial_port.name
                    # self.q_out.put(self.serial_port.name)
            else:
                print('Could not find a port with an AxiDraw connected')
                # self.q_out.put('error_1')
        else:
            print('Could not find a port with an AxiDraw connected')
            # self.q_out.put('error_1')

    def startDevice(self, data):
        print(self)
        print(self.serial_port)
        print(data)
        # brush.sendEnableMotors(self.serial_port, 2)
        # time.sleep(0.1)
        # print(data)
        """
        trial = eval(message.split('_')[1])
        length, speed, direction = trial
        print(f'Brushing trial {trial}')

        # linear movement
        if direction == 'R':
            brush.pen_down(self.serial_port)
            brush.move_x(self.serial_port, length, speed)
            brush.pen_up(self.serial_port)
            brush.move_x(self.serial_port, -length, 3)
        elif direction == 'L':
            brush.pen_down(self.serial_port)
            brush.move_x(self.serial_port, -length, 3)
            brush.pen_up(self.serial_port)
            brush.move_x(self.serial_port, length, speed)

        # circular movement
        elif direction == 'CW':
            brush.pen_down(self.serial_port)
            brush.move_circular(self.serial_port, speed, 0.67, 1, direction)
            brush.pen_up(self.serial_port)
        elif direction == 'ACW':
            brush.pen_down(self.serial_port)
            brush.move_circular(self.serial_port, speed, 0.67, 1, direction)
            brush.pen_up(self.serial_port)
        brush.sendDisableMotors(self.serial_port)
        """


axidraw = AxiDraw()

axidraw.daemon = True
axidraw.start()


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("gui/mainGui.ui", self)

        self.statusBar.showMessage('Ready')

        self.loadExperiment.triggered.connect(self.loadExperimentAction)
        self.saveExperiment.triggered.connect(self.saveExperimentAction)
        self.loadSubject.triggered.connect(self.loadSubjectAction)
        self.saveSubject.triggered.connect(self.saveSubjectAction)
        self.ResetButton.clicked.connect(self.resetSubject)
        self.BeginButton.clicked.connect(self.startExperiment)
        self.ConnectButton.clicked.connect(self.connectDevice)
        self.actionExit.triggered.connect(QtWidgets.QApplication.quit)

    def printToConsole(self, text):
        self.ConsoleOutput.appendPlainText('- ' + text)

    def loadExperimentAction(self):
        # load a experiment file
        filename = QFileDialog.getOpenFileName(self,
                                               caption="Open Experiment",
                                               filter="Comma Separated Values CSV Files (*.csv)"
                                               )

        if filename[0] == "":
            return
        data = pd.read_csv(filename[0], header=None)
        self.updateExperiment(data)

    def updateExperiment(self, data):
        self.MovementDirection.setCurrentText(data[1][0])
        self.BodySite.setCurrentText(data[1][1])
        self.velocitiesInput.setText(data[1][2])
        self.distanceInput.setText(data[1][3])
        self.repetitionsInput.setText(data[1][4])
        self.intertrialIntput.setText(data[1][5])
        self.vastimeInput.setText(data[1][6])

    def saveExperimentAction(self):
        # save a experiment file
        data = [self.MovementDirection.currentText(),
                self.BodySite.currentText(),
                self.velocitiesInput.displayText(),
                self.distanceInput.displayText(),
                self.repetitionsInput.displayText(),
                self.intertrialIntput.displayText(),
                self.vastimeInput.displayText()]

        self.printToConsole('Saving data')
        filename = QFileDialog.getSaveFileName(
            caption="Save Experiment",
            filter="Comma Separated Values CSV Files (*.csv)",
            initialFilter="csv"
        )

        if filename[0] == "":
            return

        indexRow = ["Movement", "Site",
                    "Velocity", "Distance",
                    "Repetitions", "VasTime",
                    "InterTime"]
        dataToCsv = pd.DataFrame(data, index=indexRow)
        dataToCsv.to_csv(str(filename[0]), header=False)

    def loadSubjectAction(self):
        # load a subject file
        filename = QFileDialog.getOpenFileName(self,
                                               caption="Open Experiment",
                                               filter="Comma Separated Values CSV Files (*.csv)"
                                               )

        if filename[0] == "":
            return

        data = pd.read_csv(filename[0], header=None)
        self.updateSubject(data)

    def saveSubjectAction(self):
        # save a subject file
        data = [self.subjectInput.displayText(),
                self.ageInput.displayText(),
                self.genderInput.currentText(),
                self.handInput.currentText()]

        self.printToConsole('Saving data')
        filename = QFileDialog.getSaveFileName(
            caption="Save Experiment",
            filter="Comma Separated Values CSV Files (*.csv)",
            initialFilter="csv"
        )

        if filename[0] == "":
            return

        indexRow = ["Subject", "Age",
                    "Gender", "Handeness"]
        dataToCsv = pd.DataFrame(data, index=indexRow)
        dataToCsv.to_csv(str(filename[0]), header=False)

    def updateSubject(self, data):
        self.subjectInput.setText(data[1][0])
        self.ageInput.setText(data[1][1])
        self.genderInput.setCurrentText(data[1][2])
        self.handInput.setCurrentText(data[1][3])

    def resetSubject(self):
        self.subjectInput.setText("")
        self.ageInput.setText("")
        self.genderInput.setCurrentIndex(0)
        self.handInput.setCurrentIndex(0)

    def connectDevice(self):
        self.printToConsole('Attempting to connect...')
        AxiDraw.connectDevice(axidraw)

    def startExperiment(self):
        self.printToConsole('Starting Experiment')
        data = self.getExperimentData()
        AxiDraw.startDevice(axidraw, data)

    def getExperimentData(self):
        self.printToConsole('Starting Experiment')
        data = [self.MovementDirection.currentText(),
                self.BodySite.currentText(),
                self.velocitiesInput.displayText(),
                self.distanceInput.displayText(),
                self.repetitionsInput.displayText(),
                self.intertrialIntput.displayText(),
                self.vastimeInput.displayText()]
        return data

        """
        q_to_ad.put('open_port')
        answer = q_from_ad.get()
        if answer not in 'error_3':
            window['status2'].Update(f'MultiTAC Power ON')
            Powered = True
        else:
            print('Failed to connect: MultiTAC power OFF')
            window['status2'].Update(f'MultiTAC Power OFF', text_color='DarkRed')
        if answer not in ('error_1', 'error_2', 'error_3'):
            window['status'].Update(f'Connected to {answer}', text_color='Blue')
            window['status2'].Update(f'MultiTAC Power ON', text_color='Blue')
            # q_to_ad.put('query_power')
            Connected = True
        """


if __name__:
    app = QApplication(sys.argv)
    qt_app = MainUI()
    qt_app.show()
    app.exec()
