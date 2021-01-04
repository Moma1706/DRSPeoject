from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QHBoxLayout, QCheckBox, QVBoxLayout
from Models.GameConfig import *


class EndGameDialog(QDialog):

    def __init__(self, parent, player: int):
        super().__init__(parent)
        self.par = parent
        self.player = player

        self.__initUI__()

    def __initUI__(self):
        layout = QHBoxLayout(self)
        layout2 = QVBoxLayout(self)

        self.setLayout(layout)
        self.setWindowTitle("End game")

        self.label2 = QLabel("Player")
        self.label2.setStyleSheet("color: black;")
        layout.addWidget(self.label2)

        self.label3 = QLabel(str(self.player))
        self.label3.setStyleSheet("color: black;")
        layout.addWidget(self.label3)

        self.label4 = QLabel("won")
        self.label4.setStyleSheet("color: black;")
        layout.addWidget(self.label4)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.btnPressed)
        self.button.setStyleSheet("color: black;")

        layout.addWidget(self.button)
        self.resize(250, 100)

        self.show()

    def btnPressed(self):
        self.par.end_game(self.player)
        self.close()
