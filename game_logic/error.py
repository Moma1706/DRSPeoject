from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QCheckBox
from game_logic.GameConfig import *


class ErrorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.par = parent

        self.__initUI__()

    def __initUI__(self):
        layout = QVBoxLayout(self)

        self.setLayout(layout)
        self.setWindowTitle("ERROR")
        self.setWindowIcon(QIcon('error.png'))


        self.label2 = QLabel("Number of players must be between 2 and 4!")
        self.label2.setStyleSheet("color: black;")
        layout.addWidget(self.label2)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.btnPressed)
        self.button.setStyleSheet("color: black;")
        layout.addWidget(self.button)
        self.show()

    def btnPressed(self):
        self.close()

