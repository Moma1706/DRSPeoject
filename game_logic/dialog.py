from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QCheckBox
from game_logic.GameConfig import *


class StartDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.par = parent

        self.__initUI__()

    # definise izgled dijaloga za pocetak igre

    def __initUI__(self):
        layout = QVBoxLayout(self)

        self.setGeometry(550, 400, 250, 200)
        self.setLayout(layout)
        self.setWindowTitle("Settings")

        self.label2 = QLabel("Number of players:")
        self.label2.setStyleSheet("color: black;")
        layout.addWidget(self.label2)

        self.input2 = QLineEdit()
        self.input2.setText("2")
        self.input2.setStyleSheet("color: black;")
        layout.addWidget(self.input2)

        self.label3 = QLabel("Number of snakes:")
        self.label3.setStyleSheet("color: black;")
        layout.addWidget(self.label3)

        self.input3 = QLineEdit()
        self.input3.setText("1")
        self.input3.setStyleSheet("color: black;")
        layout.addWidget(self.input3)

        self.label6 = QLabel("Turn time:")
        self.label6.setStyleSheet("color: black;")
        layout.addWidget(self.label6)

        self.input6 = QLineEdit()
        self.input6.setText("10.0")
        self.input6.setStyleSheet("color: black;")
        layout.addWidget(self.input6)

        self.button = QPushButton("Start Game")
        self.button.clicked.connect(self.btnPressed)
        self.button.setStyleSheet("color: black;")
        layout.addWidget(self.button)

        self.show()

    # definise akciju koja se desava posle klika na dugme, preuzima unete podatke iz dijaloga
    def btnPressed(self):
        conf = GameConfig()

        conf.playerNumber = int(self.input2.text())
        conf.snakeNumber = int(self.input3.text())
        conf.turnPlanTime = float(self.input6.text())
        self.close()
        self.par.start_game_pressed(conf)

