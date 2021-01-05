from PyQt5.QtCore import QRectF, QBasicTimer, QTime, QTimerEvent, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QHBoxLayout, QGraphicsScene, QGraphicsView, QLabel, \
    QAction, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QIcon, QBrush, QPen, QPixmap, QPolygon, QKeyEvent
import sys
from threading import Thread

import multiprocessing as mp
from Models.food import *
from Models.dialog import *
from Models.error import *
from Models.endGameDialog import *
from Models.GameConfig import *
from Models.snake import Snake


class SnakeWindow(QMainWindow):
    def __init__(self, pipe):
        super().__init__()

        self.pipe = pipe

        self.gameConfig = GameConfig()
        self.playing = False
        self.ate_food_happen = []
        self.game_over = []
        self.game_over_winner = []
        self.all_die = 0
        self.currentPlayer = 0

        self.timer = QBasicTimer()  # Used for controlling the game speed, and the canvas update
        self.speed = 100
        self.timeCounter = 0
        self.playtime = QTime()

        self.rectangles_to_draw = []
        self.playerLabels = []
        self.scoreLabels = []

        self.score = [0, 0, 0, 0]
        self.initUI()

    def initUi(self):
        # window setup
        self.setGeometry(200, 200, 900, 600)
        self.setWindowTitle("TurnSnakeGdxGame")
        self.setWindowIcon(QIcon('snake.png'))
        self.setStyleSheet("background-image : url(rsz_snake_background.png);")

        self.playerLabels.append(QLabel(self))
        self.player1 = "Player1:"
        self.playerLabels[0].setText(str(self.player1))
        self.playerLabels[0].setGeometry(600, 15, 100, 50)
        self.playerLabels[0].setStyleSheet("color: black;")

        self.scoreLabels.append(QLabel(self))
        self.score[0] = 0
        self.scoreLabels[0].setText(str(self.score[0]))
        self.scoreLabels[0].setGeometry(660, 15, 200, 50)
        self.scoreLabels[0].setStyleSheet("color: black;")

        self.playerLabels.append(QLabel(self))
        self.player2 = "Player2:"
        self.playerLabels[1].setText(str(self.player2))
        self.playerLabels[1].setGeometry(600, 65, 100, 50)
        self.playerLabels[1].setStyleSheet("color: black;")

        self.scoreLabels.append(QLabel(self))
        self.score[1] = 0
        self.scoreLabels[1].setText(str(self.score[1]))
        self.scoreLabels[1].setGeometry(660, 65, 200, 50)
        self.scoreLabels[1].setStyleSheet("color: black;")

        self.playerLabels.append(QLabel(self))
        self.player3 = "Player3:"
        self.playerLabels[2].setText(str(self.player3))
        self.playerLabels[2].setGeometry(600, 115, 100, 50)
        self.playerLabels[2].setStyleSheet("color: black;")

        self.scoreLabels.append(QLabel(self))
        self.score[2] = 0
        self.scoreLabels[2].setText(str(self.score[2]))
        self.scoreLabels[2].setGeometry(660, 115, 200, 50)
        self.scoreLabels[2].setStyleSheet("color: black;")

        self.playerLabels.append(QLabel(self))
        self.player4 = "Player4:"
        self.playerLabels[3].setText(str(self.player4))
        self.playerLabels[3].setGeometry(600, 165, 100, 50)
        self.playerLabels[3].setStyleSheet("color: black;")

        self.scoreLabels.append(QLabel(self))
        self.score[3] = 0
        self.scoreLabels[3].setText(str(self.score[3]))
        self.scoreLabels[3].setGeometry(660, 165, 200, 50)
        self.scoreLabels[3].setStyleSheet("color: black;")

        self.set_labels()
        self.change_label_color()

        self.timerLabel = QLabel(self)
        self.timeElapsed = "Time Elapsed:"
        self.timerLabel.setText(str(self.timeElapsed))
        self.timerLabel.resize(100, 50)
        self.timerLabel.move(600, 450)
        self.timerLabel.setStyleSheet("color: black;")

        self.timerCounterLabel = QLabel(self)
        self.timeCounter = 0
        self.timerCounterLabel.setText(str(self.timeCounter))
        self.timerCounterLabel.resize(50, 50)
        self.timerCounterLabel.move(700, 450)
        self.timerCounterLabel.setStyleSheet("color: black;")

        # next player button
        self.btn = QPushButton('Next Player', self)
        self.btn.setStyleSheet("background-color: purple; color: white;")
        self.btn.clicked.connect(self.next_player)
        self.btn.setGeometry(600, 520, 270, 50)

        menu = self.menuBar().addMenu("New game")
        self.menuBar().setStyleSheet("color: black;")
        self.hostAct = QAction("&Start Game", self)
        self.hostAct.triggered.connect(self.start)
        menu.addAction(self.hostAct)
        self.show()

    def set_labels(self):
        if self.gameConfig.playerNumber == 4:
            for j in range(4):
                self.playerLabels[j].show()
                self.scoreLabels[j].show()
        elif self.gameConfig.playerNumber == 3:
            for j in range(3):
                self.playerLabels[j].show()
                self.scoreLabels[j].show()
            self.playerLabels[3].hide()
            self.scoreLabels[3].hide()
        elif self.gameConfig.playerNumber == 2:
            for j in range(2):
                self.playerLabels[j].show()
                self.scoreLabels[j].show()
            self.playerLabels[3].hide()
            self.scoreLabels[3].hide()
            self.playerLabels[2].hide()
            self.scoreLabels[2].hide()
        else:
            for j in range(4):
                self.playerLabels[j].hide()
                self.scoreLabels[j].hide()

    def change_label_color(self):
        for i in range(self.gameConfig.playerNumber):
            self.playerLabels[i].setStyleSheet("color: black;")
        if self.currentPlayer == 0:
            self.playerLabels[0].setStyleSheet("color: red;")
        if self.currentPlayer == 1:
            self.playerLabels[1].setStyleSheet("color: green;")
        if self.currentPlayer == 2:
            self.playerLabels[2].setStyleSheet("color: blue;")
        if self.currentPlayer == 3:
            self.playerLabels[3].setStyleSheet("color: purple;")

    def paintEvent(self, e):
        painter = QPainter(self)

        painter.setPen(QPen(Qt.darkGreen, 20, Qt.SolidLine))
        painter.drawRect(20, 40, 520, 540)

    def startGame(self, config: GameConfig) -> None:
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
                    self.playingArray[i] = True
                    self.color = self.color1
                elif i == 1:
                    self.playingArray[i] = True
                    self.color = self.color2
                elif i == 2:
                    self.playingArray[i] = True
                    self.color = self.color3
                else:
                    self.playingArray[i] = True
                    self.color = self.color4
                self.snakeArray.append(Snake(self, self.color))
                self.canvas.addItem(self.snakeArray[i])
        else:
            for i in range(self.gameConfig.playerNumber * self.gameConfig.snakeNumber):
                if i == 0 or i == 1:
                    self.playingArray[0] = True
                    self.color = self.color1
                elif i == 2 or i == 3:
                    self.playingArray[1] = True
                    self.color = self.color2
                elif i == 4 or i == 5:
                    self.playingArray[2] = True
                    self.color = self.color3
                else:
                    self.playingArray[3] = True
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
                if self.playing and self.playingArray[0] and event.key() in directions:
                    self.snakeArray[0].update()
                    self.snakeArray[0].changeDirection(event.key())
                if self.playing and self.playingArray[0] and event.key() in directions2:
                    self.snakeArray[1].update()
                    self.snakeArray[1].changeDirection(event.key())
                self.playerLabel1.setStyleSheet("color: yellow;")

            elif self.currentPlayer == 2:
                if self.playing and self.playingArray[1] and event.key() in directions:
                    self.snakeArray[2].update()
                    self.snakeArray[2].changeDirection(event.key())
                if self.playing and self.playingArray[1] and event.key() in directions2:
                    self.snakeArray[3].update()
                    self.snakeArray[3].changeDirection(event.key())
                self.playerLabel2.setStyleSheet("color: red;")

            elif self.currentPlayer == 3:
                if self.playing and self.playingArray[2] and event.key() in directions:
                    self.snakeArray[4].update()
                    self.snakeArray[4].changeDirection(event.key())
                if self.playing and self.playingArray[2] and event.key() in directions2:
                    self.snakeArray[5].update()
                    self.snakeArray[5].changeDirection(event.key())
                self.playerLabel3.setStyleSheet("color: green;")
            else:
                if self.playing and self.playingArray[3] and event.key() in directions:
                    self.snakeArray[6].update()
                    self.snakeArray[6].changeDirection(event.key())
                if self.playing and self.playingArray[3] and event.key() in directions2:
                    self.snakeArray[7].update()
                    self.snakeArray[7].changeDirection(event.key())
                self.playerLabel4.setStyleSheet("color: blue;")
        else:
            if self.currentPlayer == 1:
                if self.playing and self.playingArray[0] and event.key() in directions:
                    self.snakeArray[0].update()
                    self.snakeArray[0].changeDirection(event.key())
                    self.playerLabel1.setStyleSheet("color: yellow;")

            elif self.currentPlayer == 2:
                if self.playing and self.playingArray[1] and event.key() in directions:
                    self.snakeArray[1].update()
                    self.snakeArray[1].changeDirection(event.key())
                    self.playerLabel2.setStyleSheet("color: red;")

            elif self.currentPlayer == 3:
                if self.playing and self.playingArray[2] and event.key() in directions:
                    self.snakeArray[2].update()
                    self.snakeArray[2].changeDirection(event.key())
                    self.playerLabel3.setStyleSheet("color: green;")
            else:
                if self.playing and self.playingArray[3] and event.key() in directions:
                    self.snakeArray[3].update()
                    self.snakeArray[3].changeDirection(event.key())
                    self.playerLabel4.setStyleSheet("color: blue;")

    def listen(self):
        while True:
            receive = self.pipe.recv()

            if receive['event_type'] == 'rectangles':
                self.rectangles_to_draw = receive['data']
                self.update()

            elif receive['event_type'] == 'score':
                for i in range(len(self.ate_food_happen)):
                    if receive['data'] == i:
                        self.ate_food_happen[i] = True


            elif receive['event_type'] == 'enter_pressed':
                self.gameConfig.turnPlanTime = self.timeCounter
                self.timerCounterLabel.setText(str(self.timeCounter))



    def do_action(self, config: GameConfig):
        self.pipe.send({'event_type': 'start_game', 'data': config})
        # start thread which listens on the child_connection
        t = Thread(target=self.listen)
        t.start()

    def start(self):
        dialog = StartDialog(self)
        dialog.exec()

    def start_game_pressed(self, gameConfig: GameConfig):
        self.gameConfig = gameConfig
        if self.gameConfig.playerNumber > 4 or self.gameConfig.playerNumber < 2:
            dialog = ErrorDialog(self)
            dialog.exec()
            self.start()
        else:
            self.set_labels()

            for i in range(self.gameConfig.playerNumber):
                self.ate_food_happen.append(False)

            for i in range(self.gameConfig.playerNumber):
                self.game_over.append(False)

            for i in range(self.gameConfig.playerNumber):
                self.game_over_winner.append(True)

            self.playing = True

            self.timeCounter = self.gameConfig.turnPlanTime
            self.speed = 100
            self.playtime.start()
            self.timer.start(self.speed, Qt.PreciseTimer, self)

            self.do_action(self.gameConfig)

    def show_dialog(self, player: int):
        end_dialog = EndGameDialog(self, player)
        end_dialog.exec()

    def nextPlayer(self):
        self.playerLabel1.setStyleSheet("color: white;")
        self.playerLabel2.setStyleSheet("color: white;")
        self.playerLabel3.setStyleSheet("color: white;")
        self.playerLabel4.setStyleSheet("color: white;")

        if self.gameConfig.playerNumber == self.currentPlayer:
            if self.playingArray[0] is True:
                self.currentPlayer = 1
                self.playerLabel1.setStyleSheet("color: yellow;")
            elif self.playingArray[1] is True:
                self.currentPlayer = 2
                self.playerLabel2.setStyleSheet("color: red;")
            elif self.playingArray[2] is True:
                self.currentPlayer = 3
                self.playerLabel3.setStyleSheet("color: green;")
            elif self.playingArray[3] is True:
                self.currentPlayer = 4
                self.playerLabel4.setStyleSheet("color: blue;")
        else:
            self.currentPlayer = self.currentPlayer + 1
            if self.currentPlayer == 2 and self.playingArray[1] is True:
                self.playerLabel2.setStyleSheet("color: red;")
            elif self.currentPlayer == 2 and self.playingArray[1] is False:
                self.currentPlayer = 3
                self.playerLabel3.setStyleSheet("color: green;")
            elif self.currentPlayer == 3 and self.playingArray[2] is True:
                self.playerLabel3.setStyleSheet("color: green;")
            elif self.currentPlayer == 3 and self.playingArray[2] is False:
                self.currentPlayer = 4
                self.playerLabel4.setStyleSheet("color: blue;")
            elif self.currentPlayer == 4 and self.playingArray[3] is True:
                self.playerLabel4.setStyleSheet("color: blue;")
            elif self.currentPlayer == 4 and self.playingArray[3] is False:
                self.playerLabel1.setStyleSheet("color: yellow;")
                self.currentPlayer = 1

    def updateScore(self, player: int, points: int):
        for i in range(self.gameConfig.playerNumber):
            if player == i:
                self.score[i] = self.score[i] + points
                self.scoreLabels[i].setText(str(self.score[i]))
                self.ate_food_happen[i] = False

    def timerEvent(self, event: QTimerEvent) -> None:
        """
        In charge of, in this case, update the game and check the
        conditions to continue playing, grow, spawn food and special item
        """
        if self.playtime.elapsed() > 1000:
            self.gameConfig.turnPlanTime -= 1.0
            self.timerCounterLabel.setText(str(self.gameConfig.turnPlanTime))
            self.playtime.restart()
            if self.gameConfig.turnPlanTime == 0:
                self.next_player()
                self.gameConfig.turnPlanTime = self.timeCounter
                self.timerCounterLabel.setText(str(self.timeCounter))

        # Check if the event if from the self.timer
        if event.timerId() is self.timer.timerId():
            # Check if the Snake ate the food
            for i in range(len(self.ate_food_happen)):
                if self.ate_food_happen[i] is True:
                    self.update_score(i, 1)

            # Same process for the Special food
            for i in range(self.gameConfig.snakeNumber * self.gameConfig.playerNumber):
                if self.snakeArray[i].ateFood(self.special):
                    self.updateScore(5)
                    self.special = None
                    self.food = Food(self)
                    self.canvas.addItem(self.food)

            # Check if Snake is out of bounds, or its head collided with
            # its body
            for i in range(self.gameConfig.snakeNumber * self.gameConfig.playerNumber):
                if self.snakeArray[i].outOfBounds() and self.playingArray[i] is True:
                    self.endGame(self.currentPlayer)
        else:
            super(SnakeWindow, self).timerEvent(event)

    def update_score(self, player: int, points: int):
        for i in range(self.gameConfig.playerNumber):
            if player == i:
                self.score[i] = self.score[i] + points
                self.scoreLabels[i].setText(str(self.score[i]))
                self.ate_food_happen[i] = False

    def endGame(self, player: int) -> None:
        """
        Handles the event when the Snake dies
        """
        #self.playing = False
        if player == 1 and self.playingArray[0]:
            point = "point" if self.score1 == 1 else "points"
            self.scoreLabel1.setText("Game Over. You scored <b>%d</b> %s" % (self.score1, point))
            self.canvas.removeItem(self.snakeArray[0])
            self.playingArray[0] = False
        elif player == 2 and self.playingArray[1]:
            point = "point" if self.score2 == 1 else "points"
            self.scoreLabel2.setText("Game Over. You scored <b>%d</b> %s" % (self.score2, point))
            self.canvas.removeItem(self.snakeArray[1])
            self.playingArray[1] = False
        elif player == 3 and self.playingArray[2]:
            point = "point" if self.score3 == 1 else "points"
            self.scoreLabel3.setText("Game Over. You scored <b>%d</b> %s" % (self.score3, point))
            self.canvas.removeItem(self.snakeArray[2])
            self.playingArray[2] = False
        elif player == 4 and self.playingArray[3]:
            point = "point" if self.score4 == 1 else "points"
            self.scoreLabel4.setText("Game Over. You scored <b>%d</b> %s" % (self.score4, point))
            self.canvas.removeItem(self.snakeArray[3])
            self.playingArray[3] = False

        self.counter = 0
        for i in range(len(self.playingArray)):
            if self.playingArray[i] is False:
                self.counter = self.counter + 1
        if self.counter == self.gameConfig.playerNumber - 1:
            self.playing = False
            self.timer.stop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex_pipe, in_pipe = mp.Pipe()
    ex = Example(in_pipe)
    process = GameApplication(ex_pipe)  # second process
    process.start()
    sys.exit(app.exec_())
