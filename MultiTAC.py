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
import numpy as np

from PyQt6 import QtWidgets, QtCore
from PyQt6.uic import loadUi
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QFileDialog


class AxiDraw(threading.Thread):
    def __init__(self, q_in, q_out):
        threading.Thread.__init__(self)
        self.serial_port = None
        self.running = True
        self.serial_status = False
        self.running = True
        self.q_in = q_in
        self.q_out = q_out

    def stop(self):
        self.running = False
        # Here we need to close the serial port!
        print('Axidraw thread stopped')

    def run(self):
        while self.running:
            msg = self.q_in.get()
            if msg == 'open_port':
                port = brush.findPort()  # Success!! Axidraw founded in COMPort
                if port:
                    self.serial_port, self.serial_status = brush.openPort(port)
                    if self.serial_port:
                        if self.serial_status:
                            self.q_out.put(self.serial_port.name, self.serial_status)
                            # return self.serial_port.name
                        else:
                            self.q_out.put(self.serial_port.name)
                            # return self.serial_port.name
                    else:
                        print('Could not find a port with an AxiDraw connected')
                        self.q_out.put('OK')
                else:
                    print('Could not find a port with an AxiDraw connected')
                    self.q_out.put('OK')

            if msg == 'close_port':
                port = brush.findPort()
                if port is None:
                    print('Could not find a port with an AxiDraw connected')
                else:
                    print('Closing port', port)
                    self.serial_port = brush.closePort(port)

            if msg[0] == 'execute order 66':
                brush.sendEnableMotors(self.serial_port, 2)
                speed = msg[1]
                direction = msg[2]
                distance = msg[3]
                # print('Brushing at ' + str(speed) + ' cm/s')
                if direction == 'Left to Right':
                    brush.pen_down(self.serial_port)
                    brush.move_x(self.serial_port, distance, speed)
                    brush.pen_up(self.serial_port)
                    brush.move_x(self.serial_port, -distance, 3)
                elif direction == 'Right to Left':
                    brush.pen_down(self.serial_port)
                    brush.move_x(self.serial_port, -distance, 3)
                    brush.pen_up(self.serial_port)
                    brush.move_x(self.serial_port, distance, speed)

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
                self.q_out.put('OK')


q_to_ad = queue.Queue()
q_from_ad = queue.Queue()
axidraw = AxiDraw(q_to_ad, q_from_ad)

axidraw.daemon = True
axidraw.start()


class vasPage(QMainWindow):
    def __init__(self):
        super(vasPage, self).__init__()
        loadUi("gui/vas.ui", self)
        self.vasSlider.valueChanged.connect(self.updateDisplay)
        self.vasSubmit.clicked.connect(self.getValues)

    def getValues(self):
        print(self.vasSlider.value())
        self.close()

    def updateDisplay(self):
        self.vasCurrent.display(self.vasSlider.value())


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
        self.movementPath.setCurrentText(data[1][0])
        self.bodySite.setCurrentText(data[1][1])
        self.movementDirection.setCurrentText(data[1][2])
        self.velocitiesInput.setText(data[1][3])
        self.distanceInput.setText(data[1][4])
        self.repetitionsInput.setText(data[1][5])
        self.intertrialIntput.setText(data[1][6])
        self.vastimeInput.setText(data[1][7])

    def saveExperimentAction(self):
        # save a experiment file
        data = [self.movementPath.currentText(),
                self.bodySite.currentText(),
                self.movementDirection.currentText(),
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

        indexRow = ["Path", "Site",
                    "Movement", "Velocity",
                    "Distance", "Repetitions",
                    "VasTime", "InterTime"]
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
        q_to_ad.put('open_port')
        answer = q_from_ad.get()
        print(answer)

    def startExperiment(self):
        trialsRnd = []
        data = self.getExperimentData()

        direction = data[2]
        trials = data[3].split(";")
        distance = int(data[4])
        reps = int(data[5])
        interTime = int(data[6])
        VasTime = int(data[7])

        trials = [eval(i) for i in trials]
        for i in range(0, reps):
            trialsRnd.append(random.sample(trials, len(trials)))
        """
        trialsRnd
        timeCount = len(trials) * reps
        count = 0

        for cycle in trialsRnd:
            for trial in cycle:
                self.printToConsole('Brushed at ' + str(trial) + ' cm/s')
                q_to_ad.put(['execute order 66', trial, direction, distance])
                answer = q_from_ad.get()
                print(answer)
        """
    def getExperimentData(self):
        # self.printToConsole('Starting Experiment')
        data = [self.movementPath.currentText(),
                self.bodySite.currentText(),
                self.movementDirection.currentText(),
                self.velocitiesInput.displayText(),
                self.distanceInput.displayText(),
                self.repetitionsInput.displayText(),
                self.intertrialIntput.displayText(),
                self.vastimeInput.displayText()]
        return data

    def getVas(self):
        self.main = vasPage()
        self.main.show()


if __name__:
    debugger = True

    if debugger:
        app = QApplication(sys.argv)
        qt_app = MainUI()
        qt_app.show()
        app.exec()
