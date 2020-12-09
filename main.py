from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QMainWindow, QHBoxLayout, \
    QGraphicsScene, QGraphicsView, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QKeyEvent, QPen

from threading import Thread

import sys
from Models.snake import *
import multiprocessing as mp
import time

class SnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.snake = None
        self.playing = False
        self.score = 0
        self.particleSize = 10

    #window setup
        self.setCentralWidget(QWidget())
        self.setWindowTitle("\t\t\t\tTurnSnakeGdxGame")
        self.resize(1100, 750)

        self.move(200, 100)
        self.setWindowIcon(QIcon('snake.png'))

        horizontal = QHBoxLayout()
        self.setLayout(horizontal)
        self.setStyleSheet("background-image : url(galaxy.jpg);")

    #canvas
        self.canvas = QGraphicsScene(self)
        self.graphicsView = QGraphicsView(self.canvas, self)
        # Use all the QGraphicsView area
        self.canvas.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())
        self.canvas.setBackgroundBrush(QBrush(QColor(52, 56, 56), Qt.SolidPattern))
        self.graphicsView.setScene(self.canvas)
        self.graphicsView.resize(900, 700)

    # score label setup
        self.scoreLabel = QLabel(self)
        self.score = "Press <b>Enter</b> to start game"
        self.scoreLabel.setText(str(self.score))
        self.scoreLabel.resize(200, 200)
        self.scoreLabel.move(950, 10)
        self.scoreLabel.setStyleSheet("color: white;")

    #next player button
        #self.centralWidget().layout().addWidget()
        self.btn = QPushButton('Next Player', self)
        self.btn.setStyleSheet("background-color: purple; color: white;")

        self.btn.move(1000, 600)
        self.btn.resize(80, 80)
        #self.btn.clicked.connect(self.doAction)
        self.drawBorder()
        self.centerOnScreen()
        self.show()

    def startGame(self) -> None:
        """
        Starts a New Game every time the user press [Enter, Return]
        if a game has not started yet
        """
        self.playing = True

        # Reset the score
        self.score = 0
        self.scoreLabel.setText(str(self.score))

        # Add the new Snake object to the canvas
        self.snake = Snake(self)

        self.canvas.addItem(self.snake)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        start = [Qt.Key_Return, Qt.Key_Enter]
        # Game can be played using Arrow keys and WASD
        directions = [Qt.Key_Left, Qt.Key_A, Qt.Key_Right, Qt.Key_D, Qt.Key_Up, Qt.Key_W, Qt.Key_Down, Qt.Key_S]

        # Starts a new game if not already playingw
        if not self.playing and event.key() in start:
            self.startGame()

 # nzm sta
    def drawBorder(self) -> None:
        """
        Draw a decorative border in the perimeter of the QGraphicsView
        """
        # Remove the outline
        outline = QPen(Qt.NoPen)

        # Change the background color for the object being drawn
        background = QBrush(QColor(0, 95, 107), Qt.Dense3Pattern)

        # [0, 10, 20, 30, ... , self.canvas.width()] with particle size set to 10
        topBottom = range(0, int(self.canvas.width()), self.particleSize)

        # [10, 20, 30, 40, ... , self.canvas,height() - 10] with particle size set to 10
        leftRight = range(self.particleSize, int(self.canvas.height()) - self.particleSize, self.particleSize)

        size = self.particleSize
        width = 900 #self.canvas.width()
        height = 700 #self.canvas.height()

        # Top, Bottom, Left, Right borders (in that order)
        areas = [
            QRectF(-400, -334, width, size),
            QRectF(-400, 354, width, size),
            QRectF(-400, -325, size, height - size * 2),
            QRectF(490, -325, size, height - size * 2)
        ]

        for area in areas:
            self.canvas.addRect(area, outline, background)

    def centerOnScreen(self) -> None:
        """
        Centers the window on the screen keeping in mind the available space for
        the window to show
        """
        frameGeometry = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    rep = SnakeWindow()
    sys.exit(app.exec_())

