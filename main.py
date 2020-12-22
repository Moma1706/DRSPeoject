import sys

from PyQt5.QtCore import QBasicTimer, QTime, QTimerEvent
from PyQt5.QtGui import QIcon, QKeyEvent, QPen
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QMainWindow, QHBoxLayout, \
    QGraphicsScene, QGraphicsView, QDesktopWidget, QAction

from Models.food import Food
from Models.snake import *
from Models.dialog import *
from Models.GameConfig import *


class SnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.snakeArray = []
        self.gameConfig = None
        self.food = None
        self.special = None
        self.playing = False
        self.score = 0
        self.particleSize = 10
        self.currentPlayer = 0
        self.color1 = QColor(245, 245, 15)
        self.color2 = QColor(247, 5, 5)
        self.color3 = QColor(10, 138, 3)
        self.color4 = QColor(40, 10, 163)
        self.color = QColor()
        self.timer = QBasicTimer()  # Used for controlling the game speed, and the canvas update
        self.speed = 100
        self.playtime = QTime()

        # window setup
        self.setCentralWidget(QWidget())
        self.setWindowTitle("\t\t\t\tTurnSnakeGdxGame")
        self.resize(1120, 750)

        self.move(200, 50)
        self.setWindowIcon(QIcon('snake.png'))

        horizontal = QHBoxLayout()
        self.setLayout(horizontal)
        self.setStyleSheet("background-image : url(galaxy.jpg);")

        # canvas
        self.canvas = QGraphicsScene(self)
        self.graphicsView = QGraphicsView(self.canvas, self)
        # Use all the QGraphicsView area
        self.graphicsView.resize(905, 705)
        self.graphicsView.move(5, 25)
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
        self.score1 = 0
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
        self.score2 = 0
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
        self.score3 = 0
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
        self.score4 = 0
        self.scoreLabel4.setText(str(self.score4))
        self.scoreLabel4.resize(100, 50)
        self.scoreLabel4.move(1000, 160)
        self.scoreLabel4.setStyleSheet("color: white;")

        menu = self.menuBar().addMenu("New game")
        self.menuBar().setStyleSheet("color: white;")
        self.hostAct = QAction("&Start Game", self)
        self.hostAct.triggered.connect(self.host)
        menu.addAction(self.hostAct)

        # next player button
        # self.centralWidget().layout().addWidget()
        self.btn = QPushButton('Next Player', self)
        self.btn.setStyleSheet("background-color: purple; color: white;")
        self.btn.clicked.connect(self.nextPlayer)
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
        self.currentPlayer = 1
        self.speed = 100
        self.playtime.start()
        self.timer.start(self.speed, Qt.PreciseTimer, self)

        if self.gameConfig.snakeNumber == 1:
            for i in range(self.gameConfig.playerNumber):
                if i == 0:
                    self.color = self.color1
                elif i == 1:
                    self.color = self.color2
                elif i == 2:
                    self.color = self.color3
                else:
                    self.color = self.color4
                self.snakeArray.append(Snake(self, self.color))
                self.canvas.addItem(self.snakeArray[i])
        else:
            for i in range(self.gameConfig.playerNumber * self.gameConfig.snakeNumber):
                if i == 0 or i == 1:
                    self.color = self.color1
                elif i == 2 or i == 3:
                    self.color = self.color2
                elif i == 4 or i == 5:
                    self.color = self.color3
                else:
                    self.color = self.color4
                self.snakeArray.append(Snake(self, self.color))
                self.canvas.addItem(self.snakeArray[i])

        self.food = Food(self)
        self.canvas.addItem(self.food)
        self.playerLabel1.setStyleSheet("color: yellow;")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        start = [Qt.Key_Return, Qt.Key_Enter]
        # Game can be played using Arrow keys and WASD
        directions = [Qt.Key_A, Qt.Key_D, Qt.Key_W, Qt.Key_S]
        directions2 = [Qt.Key_I,  Qt.Key_L, Qt.Key_J, Qt.Key_K]


        # Change the Snake's movement direction
        if self.gameConfig.snakeNumber == 2:
            if self.currentPlayer == 1:
                if self.playing and event.key() in directions:
                    self.snakeArray[0].update()
                    self.snakeArray[0].changeDirection(event.key())
                if self.playing and event.key() in directions2:
                    self.snakeArray[1].update()
                    self.snakeArray[1].changeDirection(event.key())
                self.playerLabel1.setStyleSheet("color: yellow;")

            elif self.currentPlayer == 2:
                if self.playing and event.key() in directions:
                    self.snakeArray[2].update()
                    self.snakeArray[2].changeDirection(event.key())
                if self.playing and event.key() in directions2:
                    self.snakeArray[3].update()
                    self.snakeArray[3].changeDirection(event.key())
                self.playerLabel2.setStyleSheet("color: red;")

            elif self.currentPlayer == 3:
                if self.playing and event.key() in directions:
                    self.snakeArray[4].update()
                    self.snakeArray[4].changeDirection(event.key())
                if self.playing and event.key() in directions2:
                    self.snakeArray[5].update()
                    self.snakeArray[5].changeDirection(event.key())
                self.playerLabel3.setStyleSheet("color: green;")
            else:
                if self.playing and event.key() in directions:
                    self.snakeArray[6].update()
                    self.snakeArray[6].changeDirection(event.key())
                if self.playing and event.key() in directions2:
                    self.snakeArray[7].update()
                    self.snakeArray[7].changeDirection(event.key())
                self.playerLabel4.setStyleSheet("color: blue;")
        else:
            if self.currentPlayer == 1:
                if self.playing and event.key() in directions:
                    self.snakeArray[0].update()
                    self.snakeArray[0].changeDirection(event.key())
                    self.playerLabel1.setStyleSheet("color: yellow;")

            elif self.currentPlayer == 2:
                if self.playing and event.key() in directions:
                    self.snakeArray[1].update()
                    self.snakeArray[1].changeDirection(event.key())
                    self.playerLabel2.setStyleSheet("color: red;")

            elif self.currentPlayer == 3:
                if self.playing and event.key() in directions:
                    self.snakeArray[2].update()
                    self.snakeArray[2].changeDirection(event.key())
                    self.playerLabel3.setStyleSheet("color: green;")
            else:
                if self.playing and event.key() in directions:
                    self.snakeArray[3].update()
                    self.snakeArray[3].changeDirection(event.key())
                    self.playerLabel4.setStyleSheet("color: blue;")

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

    def host(self):
        dialog = HostDialog(self)
        dialog.exec()

    def hostPressed(self, gameConfig: GameConfig):
        self.gameConfig = gameConfig
        self.startGame()

    def nextPlayer(self):
        self.playerLabel1.setStyleSheet("color: white;")
        self.playerLabel2.setStyleSheet("color: white;")
        self.playerLabel3.setStyleSheet("color: white;")
        self.playerLabel4.setStyleSheet("color: white;")

        if self.gameConfig.playerNumber == self.currentPlayer:
            self.currentPlayer = 1
            self.playerLabel1.setStyleSheet("color: yellow;")
        else:
            self.currentPlayer = self.currentPlayer + 1
            if self.currentPlayer == 2:
                self.playerLabel2.setStyleSheet("color: red;")
            elif self.currentPlayer == 3:
                self.playerLabel3.setStyleSheet("color: green;")
            elif self.currentPlayer == 4:
                self.playerLabel4.setStyleSheet("color: blue;")

    def updateScore(self, points: int) -> None:
        if self.currentPlayer == 1:
            self.score1 += points
            self.scoreLabel1.setText(str(self.score1))
        elif self.currentPlayer == 2:
            self.score2 += points
            self.scoreLabel2.setText(str(self.score2))
        elif self.currentPlayer == 3:
            self.score3 += points
            self.scoreLabel3.setText(str(self.score3))
        else:
            self.score4 += points
            self.scoreLabel4.setText(str(self.score4))

    def timerEvent(self, event: QTimerEvent) -> None:
        """
        In charge of, in this case, update the game and check the
        conditions to continue playing, grow, spawn food and special item
        """

        # Check if the event if from the self.timer
        if event.timerId() is self.timer.timerId():
            # Check if the Snake ate the food
            for i in range(self.gameConfig.snakeNumber * self.gameConfig.playerNumber):
                if self.snakeArray[i].ateFood(self.food):
                    self.updateScore(1)
                    self.food = Food(self)
                    self.canvas.addItem(self.food)

            # Same process for the Special food
            for i in range(self.gameConfig.snakeNumber * self.gameConfig.playerNumber):
                if self.snakeArray[i].ateFood(self.special):
                    self.updateScore(5)
                    self.special = None
                    self.food = Food(self)
                    self.canvas.addItem(self.food)

            # Check if Snake is out of bounds, or its head collided with
            # its body
            #if self.snake.outOfBounds() or self.snake.headInsideOfTail():
            #    self.endGame()
        else:
            super(SnakeWindow, self).timerEvent(event)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    rep = SnakeWindow()
    sys.exit(app.exec_())
