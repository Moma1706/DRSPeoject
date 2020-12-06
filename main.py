from PyQt5.QtWidgets import QWidget, QProgressBar,QPushButton, QApplication , QLabel, QMainWindow, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap

from threading import Thread

import sys
import multiprocessing as mp
import time

class SnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    #window setup
        self.setCentralWidget(QWidget())
        self.setWindowTitle("\t\t\t\tTurnSnakeGdxGame")
        self.resize(1000, 700)
        self.move(200, 100)
        self.setWindowIcon(QIcon('snake.png'))

        horizontal = QHBoxLayout()
        self.setLayout(horizontal)
        self.setStyleSheet("background-color: #79d2a6;")

    #grass pic
        label = QLabel(self)
        pixmap = QPixmap('grass.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)

    #next player button
        #self.centralWidget().layout().addWidget()
        self.btn = QPushButton('Next Player', self)
        self.btn.move(900, 600)
        self.btn.resize(80,80)
        #self.btn.clicked.connect(self.doAction)

        self.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    rep = SnakeWindow()
    sys.exit(app.exec_())

