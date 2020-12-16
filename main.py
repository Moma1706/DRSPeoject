import sys

from PyQt5.QtCore import QBasicTimer, QTime, QTimerEvent
from PyQt5.QtGui import QIcon, QKeyEvent, QPen
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QMainWindow, QHBoxLayout, \
    QGraphicsScene, QGraphicsView, QDesktopWidget

from Models.food import Food
from Models.snake import *


class SnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.snake = None
        self.snake2 = None
        self.food = None
        self.playing = False
        self.score = 0
        self.particleSize = 10

        # window setup
        self.setCentralWidget(QWidget())
        self.setWindowTitle("\t\t\t\tTurnSnakeGdxGame")
        self.resize(1120, 750)

        self.move(200, 100)
        self.setWindowIcon(QIcon('snake.png'))

        horizontal = QHBoxLayout()
        self.setLayout(horizontal)
        self.setStyleSheet("background-image : url(galaxy.jpg);")

        # canvas
        self.canvas = QGraphicsScene(self)
        self.graphicsView = QGraphicsView(self.canvas, self)
        # Use all the QGraphicsView area
        self.graphicsView.resize(905, 705)
        self.canvas.setSceneRect(0, 0, (self.canvas.width()), (self.canvas.height()))
        self.canvas.setBackgroundBrush(QBrush(QColor(52, 56, 56), Qt.SolidPattern))
        self.graphicsView.setScene(self.canvas)

        # score labels setup

        self.playerLabel1 = QLabel(self)
        self.player1 = "Player1:"
        self.playerLabel1.setText(str(self.player1))
        self.playerLabel1.resize(100, 50)
        self.playerLabel1.move(930, 15)
        self.playerLabel1.setStyleSheet("color: white;")

        self.scoreLabel1 = QLabel(self)
        self.score1 = "Press <b>Enter</b> to start game"
        self.scoreLabel1.setText(str(self.score1))
        self.scoreLabel1.resize(100, 50)
        self.scoreLabel1.move(1000, 15)
        self.scoreLabel1.setStyleSheet("color: white;")

        self.playerLabel2 = QLabel(self)
        self.player2 = "Player2:"
        self.playerLabel2.setText(str(self.player2))
        self.playerLabel2.resize(100, 50)
        self.playerLabel2.move(930, 65)
        self.playerLabel2.setStyleSheet("color: white;")

        self.scoreLabel2 = QLabel(self)
        self.score2 = "0"
        self.scoreLabel2.setText(str(self.score2))
        self.scoreLabel2.resize(100, 50)
        self.scoreLabel2.move(1000, 65)
        self.scoreLabel2.setStyleSheet("color: white;")

        self.playerLabel3 = QLabel(self)
        self.player3 = "Player3:"
        self.playerLabel3.setText(str(self.player3))
        self.playerLabel3.resize(100, 50)
        self.playerLabel3.move(930, 110)
        self.playerLabel3.setStyleSheet("color: white;")

        self.scoreLabel3 = QLabel(self)
        self.score3 = "0"
        self.scoreLabel3.setText(str(self.score3))
        self.scoreLabel3.resize(100, 50)
        self.scoreLabel3.move(1000, 110)
        self.scoreLabel3.setStyleSheet("color: white;")

        self.playerLabel4 = QLabel(self)
        self.player4 = "Player4:"
        self.playerLabel4.setText(str(self.player4))
        self.playerLabel4.resize(100, 50)
        self.playerLabel4.move(930, 160)
        self.playerLabel4.setStyleSheet("color: white;")

        self.scoreLabel4 = QLabel(self)
        self.score4 = "0"
        self.scoreLabel4.setText(str(self.score4))
        self.scoreLabel4.resize(100, 50)
        self.scoreLabel4.move(1000, 160)
        self.scoreLabel4.setStyleSheet("color: white;")

        # next player button
        # self.centralWidget().layout().addWidget()
        self.btn = QPushButton('Next Player', self)
        self.btn.setStyleSheet("background-color: purple; color: white;")

        self.btn.move(1000, 600)
        self.btn.resize(80, 80)
        self.drawBorder()
        self.show()

    def startGame(self) -> None:
        """
        Starts a New Game every time the user press [Enter, Return]
        if a game has not started yet
        """
        self.playing = True

        # Reset the score
        self.score1 = 0
        self.scoreLabel1.setText(str(self.score1))

        # Add the new Snake object to the canvas
        self.snake = Snake(self)
        self.snake2 = Snake(self)
        self.canvas.addItem(self.snake)
        self.canvas.addItem(self.snake2)

        self.food = Food(self)
        self.canvas.addItem(self.food)


    def keyPressEvent(self, event: QKeyEvent) -> None:
        start = [Qt.Key_Return, Qt.Key_Enter]
        # Game can be played using Arrow keys and WASD
        directions = [Qt.Key_A, Qt.Key_D, Qt.Key_W, Qt.Key_S]
        directions2 = [Qt.Key_I,  Qt.Key_L, Qt.Key_J, Qt.Key_K]
        # Starts a new game if not already playing
        if not self.playing and event.key() in start:
            self.startGame()

        # Change the Snake's movement direction
        if self.playing and event.key() in directions:
            self.snake.update()
            self.snake.changeDirection(event.key())

        if self.playing and event.key() in directions2:
            self.snake2.update()
            self.snake2.changeDirection(event.key())

    # border
    def drawBorder(self) -> None:
        """
        Draw a decorative border in the perimeter of the QGraphicsView
        """
        # Remove the outline
        outline = QPen(Qt.NoPen)

        # Change the background color for the object being drawn
        background = QBrush(QColor(0, 95, 107), Qt.Dense3Pattern)

        size = self.particleSize
        width = 900  # self.canvas.width()
        height = 700  # self.canvas.height()

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
