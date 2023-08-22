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
from ui import mainGui
from axidraw import brush
from PySide2 import QtWidgets


class Axidraw(threading.Thread):
    def __init__(self, q_in, q_out):
        threading.Thread.__init__(self)
        self.serial_port = None
        self.running = True
        self.q_in = q_in
        self.q_out = q_out
        self.dir_default = 'to_R'
        print('Axidraw thread started')

    def stop(self):
        self.running = False
        # Here we need to close the serial port!
        print('Axidraw thread stopped')

    def run(self):
        while self.running:
            #  Message from events (associated with the GUI, for example
            #  a button was clicked
            msg = self.q_in.get()

            if msg == 'open_port':
                p = brush.findPort()
                if p is None:
                    print('Could not find a port with an AxiDraw connected')
                else:
                    print('AxiDraw found at port', p)  # Success!! Axidraw founded in ComPort
                    self.serial_port = brush.openPort(p)
                    if self.serial_port is None:
                        print('Could not open the port.')
                        self.q_out.put('error_2')  # Port not available, error 2
                    elif self.serial_port == "OFF":
                        self.q_out.put('error_3')  # Power off, error3
                    else:
                        self.q_out.put(self.serial_port.name)

            if msg == 'close_port':
                p = brush.findPort()
                if p is None:
                    print('Could not find a port with an AxiDraw connected')
                    self.q_out.put('error_1')
                else:
                    print('Closing port', p)
                    self.serial_port = brush.closePort(p)

            if msg[:4] == 'move':
                brush.sendEnableMotors(self.serial_port, 2)
                time.sleep(0.1)
                action = msg.split('_')[1]
                if action == 'front':
                    brush.to_the_front(self.serial_port, 1000, 200)
                elif action == 'back':
                    brush.to_the_back(self.serial_port, 1000, 200)
                elif action == 'left':
                    brush.to_the_left(self.serial_port, 1000, 200)
                elif action == 'right':
                    brush.to_the_right(self.serial_port, 1000, 200)
                elif action == 'brush-up':
                    brush.pen_up(self.serial_port)
                elif action == 'brush-down':
                    brush.pen_down(self.serial_port)
                time.sleep(0.5)
                brush.sendDisableMotors(self.serial_port)
                self.q_out.put('OK')

            if msg[:5] == 'brush':
                trial = eval(msg.split('_')[1])
                length, speed, direction = trial

                print(f'Brushing trial {trial}', flush=True)
                sys.stdout.flush()  # To allow printing while threading

                brush.sendEnableMotors(self.serial_port, 2)
                # time.sleep(0.5)
                if self.dir_default == 'to_R':
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
                else:
                    if direction == 'R':
                        brush.move_x(self.serial_port, -length, 3)
                        brush.pen_down(self.serial_port)
                        brush.move_x(self.serial_port, length, speed)
                        brush.pen_up(self.serial_port)
                    elif direction == 'L':
                        brush.pen_down(self.serial_port)
                        brush.move_x(self.serial_port, -length, speed)
                        brush.pen_up(self.serial_port)
                        brush.move_x(self.serial_port, length, 3)
                brush.sendDisableMotors(self.serial_port)

                self.q_out.put('OK')


"""-----------------------------------------------------------"""
q_to_ad = queue.Queue()
q_from_ad = queue.Queue()
axidraw = Axidraw(q_to_ad, q_from_ad)

axidraw.daemon = True
axidraw.start()

Connected = False
Powered = False
debug = True

"""_----------------------------------------------------------"""


class MyMainWindow(mainGui.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

        self.ConsoleOutput.setPlainText("hello")
        self.ConnectButton.clicked.connect(self.connectTac)

    def connectTac(self):
        self.ConsoleOutput.setPlainText("Attempting connection...")
        q_to_ad.put('open_port')
        answer = q_from_ad.get()
        if answer not in 'error_3':
            # window['status2'].Update(f'MultiTAC Power ON')
            Powered = True
        else:
            self.ConsoleOutput.setPlainText('Failed to connect: MultiTAC power OFF')
            # window['status2'].Update(f'MultiTAC Power OFF', text_color='DarkRed')
        if answer not in ('error_1', 'error_2', 'error_3'):
            # window['status'].Update(f'Connected to {answer}', text_color='Blue')
            # window['status2'].Update(f'MultiTAC Power ON', text_color='Blue')
            # q_to_ad.put('query_power')
            Connected = True

if __name__:
    app = QtWidgets.QApplication()
    qt_app = MyMainWindow()
    qt_app.show()
    app.exec_()
