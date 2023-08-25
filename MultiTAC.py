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
from PySide2 import QtWidgets
from BrushGui.axidraw import brush
from pyqtconsole.console import PythonConsole
import pandas as pd

from PyQt6 import QtWidgets, QtCore
from PyQt6.uic import loadUi
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QFileDialog


class AxiDraw:
    def __init__(self, q_in, q_out):
        self.serial_port = 'COM3'
        self.running = True
        self.serial_port = None
        self.serial_status = False
        self.running = True
        self.q_in = q_in
        self.q_out = q_out

    def connectDevice(self):
        port = brush.findPort()  # Success!! Axidraw founded in ComPort
        print(port)
        if port:
            self.serial_port, self.serial_status = brush.openPort(port)
            if self.serial_port:
                if self.serial_status:
                    self.q_out.put(self.serial_port.name, self.serial_status)
                    print(self.serial_port.name)
                else:
                    self.q_out.put(self.serial_port.name)
            else:
                print('Could not find a port with an AxiDraw connected')
                self.q_out.put('error_1')

    def stop(self):
        self.running = False
        # Here we need to close the serial port!
        print('Axidraw thread stopped')

    def run(self):
        while self.running:
            messages = ['open_port', 'close_port', 'brush_move', 'stop_move']
            message = self.q_in.get()

            if message == messages[1]:  # close port
                port = brush.findPort()
                if port:
                    self.serial_port = brush.closePort(port)
                    print('Closing port', port)
                else:
                    print('Could not find a port with an AxiDraw connected')
                    self.q_out.put('error_1')

            if message[:10] == messages[2]:  # brush movement
                brush.sendEnableMotors(self.serial_port, 2)
                time.sleep(0.1)
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

                self.q_out.put('Mov done')


class subjectFile():
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None
        self.hand = None


class experimentFile():
    def __init__(self):
        self.movement = None
        self.site = None
        self.speed = None
        self.distance = None
        self.trials = None
        self.vasTime = None
        self.interTime = None


class MultiTACGui(QMainWindow):
    def __init__(self):
        super(MultiTACGui, self).__init__()
        loadUi("gui/mainGui.ui", self)

        self.statusBar.showMessage('Ready')

        self.loadExperiment.triggered.connect(self.loadExperimentAction)
        self.saveExperiment.triggered.connect(self.saveExperimentAction)
        self.loadSubject.triggered.connect(self.loadSubjectAction)
        self.saveSubject.triggered.connect(self.saveSubjectAction)

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
        data = pd.read_csv(filename[0],header=None)
        self.updateExperiment(data)

    def updateExperiment(self,data):
        print(data[1])

        self.MovementDirection.setCurrentText(data[1][0])
        self.BodySite.setCurrentText(data[1][1])
        self.velocitiesInput.setText(data[1][2])
        self.distanceInput.setText(data[1][3])
        self.repetitionsInput.setText(data[1][4])
        self.intertrialIntput.setText(data[1][5])
        self.vastimeInput.setText(data[1][6])

    def saveExperimentAction(self):
        # save a experiment file
        data = [self.MovementDirection.currentText(), self.distanceInput.displayText()]
        self.printToConsole('Saving data')
        filename = QFileDialog.getSaveFileName(
            caption="Save Experiment",
            filter="Comma Separated Values CSV Files (*.csv)"
        )

        # self.markerModel.save(str(filename[0]))

    def loadSubjectAction(self):
        print('3')

    def saveSubjectAction(self):
        print('4')

        """
        self.ConnectButton.clicked.connect(self.stablishConnection)
        self.ResetButton.clicked.connect(self.resetPacient)
        self.BeginButton.clicked.connect(self.startExperiment)

        def printToConsole(self, text):
            self.ConsoleOutput.appendPlainText('- ' + text)

        def stablishConnection(self):
            self.printToConsole('Attempting to connect to device')
            AxiDraw.connectDevice(self)

        def resetPacient(self):
            self.printToConsole('reset')

        def startExperiment(self):
            self.printToConsole('Go')


        def exportData(self):
            print('hi')
            data = [self.MovementDirection.currentIndex(), self.distanceInput.displayText()]
            self.printToConsole(data)
        """


if __name__:

    app = QApplication(sys.argv)
    qt_app = MultiTACGui()
    qt_app.show()
    app.exec()

