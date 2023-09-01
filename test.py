from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from PyQt5.QtCore import QTimer
from random import randint


class AnotherWindow(QWidget):
    """
    This "&quot";window&"quot"; is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)
        timer = QTimer()  # set up your QTimer
        timer.timeout.connect(self.show_new_window)  # connect it to your update function
        timer.start(5000)
    def show_new_window(self):
        print('h')
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()