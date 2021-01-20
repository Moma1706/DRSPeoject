from PyQt5.QtCore import QRectF, QBasicTimer, QTime, QTimerEvent, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QHBoxLayout, QGraphicsScene, QGraphicsView, QLabel, \
    QAction, QPushButton
from PyQt5.QtGui import QPainter, QColor, QIcon, QBrush, QPen, QPixmap, QPolygon
import sys
from threading import Thread

import multiprocessing as mp

from game_logic.dialog import StartDialog
from game_logic.error import ErrorDialog
from game_logic.game_application import GameApplication
from game_logic.GameConfig import *
from game_logic.endGameDialog import *
import time


class Example(QMainWindow):
    def __init__(self, pipe):
        super().__init__()

        self.pipe = pipe

        self.gameConfig = GameConfig()
        self.playing = False
        self.game_over = []
        self.all_die = 0
        self.currentPlayer = 0

        self.timer = QBasicTimer()  # Used for controlling the game speed, and the canvas update
        self.speed = 100
        self.timeCounter = 0
        self.playtime = QTime()
        self.counter = []

        self.rectangles_to_draw = []
        self.playerLabels = []
        self.scoreLabels = []
        self.sec_counter = 1
        self.special_food_border = False
        self.special_food = False
        self.score = [0, 0, 0, 0]
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 900, 600)
        self.setWindowTitle("TurnSnakeGdxGame")
        self.setWindowIcon(QIcon('snake.png'))
        self.setStyleSheet("background-image : url(rsz_snake_background.png);")

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

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_rectangles(qp)

        if self.playing is True:
            if self.special_food_border is False:
                if self.sec_counter % 17 == 0:
                    self.draw_border()
                    self.special_food_border = True
        qp.end()

        painter = QPainter(self)

        painter.setPen(QPen(Qt.darkGreen,  20, Qt.SolidLine))
        painter.drawRect(20, 40, 520, 540)

    def draw_rectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        for rect in self.rectangles_to_draw:
            qp.setBrush(rect['color'])
            qp.drawRect(rect['x'], rect['y'], rect['width'], rect['height'])

    def draw_border(self):
        painter = QPainter(self)

        painter.setPen(QPen(Qt.darkGreen, 5, Qt.SolidLine))
        painter.drawRect(450, 500, 60, 60)

    def set_labels(self):
        for i in range(self.gameConfig.playerNumber):
            space = 15 + i*50
            self.playerLabels.append(QLabel(self))
            self.player = "Player {}:".format(i+1)
            self.playerLabels[i].setText(str(self.player))
            self.playerLabels[i].setGeometry(600, space, 100, 50)
            self.playerLabels[i].setStyleSheet("color: black;")
            self.playerLabels[i].show()

            self.scoreLabels.append(QLabel(self))
            self.score[i] = 0
            self.scoreLabels[i].setText(str(self.score[3]))
            self.scoreLabels[i].setGeometry(660, space, 200, 50)
            self.scoreLabels[i].setStyleSheet("color: black;")
            self.scoreLabels[i].show()

    def hide_labels(self):
        for i in range(self.gameConfig.playerNumber):
            self.playerLabels[i].hide()
            self.scoreLabels[i].hide()

    def change_label_color(self):
        for i in range(self.gameConfig.playerNumber):
            self.playerLabels[i].setStyleSheet("color: black;")

        if self.currentPlayer == 0:
            self.playerLabels[0].setStyleSheet("color: red;")
        elif self.currentPlayer == 1:
            self.playerLabels[1].setStyleSheet("color: green;")
        elif self.currentPlayer == 2:
            self.playerLabels[2].setStyleSheet("color: blue;")
        elif self.currentPlayer == 3:
            self.playerLabels[3].setStyleSheet("color: purple;")

    def next_player(self):
        if self.playing is True:
            self.pipe.send({'event_type': 'next_player', 'data': 'next_player'})
            time.sleep(0.1)

    def keyPressEvent(self, e):
        if self.playing is True:
            self.pipe.send({'event_type': 'key_pressed', 'data': e.key()})
            time.sleep(0.2)

    def listen(self):
        while True:
            try:
                receive = self.pipe.recv()

                if receive['event_type'] == 'rectangles':
                    self.rectangles_to_draw = receive['data']
                    self.update()

                elif receive['event_type'] == 'score':
                    self.update_score(receive['data'], 1)
                elif receive['event_type'] == 'special_score':
                    self.update_score(receive['data'], receive['score_type'])
                    self.update_spec_food_value()
                elif receive['event_type'] == 'end_game':
                    self.all_die += 1
                    self.set_game_over(receive['data'])

                elif receive['event_type'] == 'current_player':
                    self.gameConfig.turnPlanTime = self.timeCounter
                    self.timerCounterLabel.setText(str(self.timeCounter))
                    self.currentPlayer = receive['data']
                    self.change_label_color()

            except BrokenPipeError as e:
                print(e)
                print('Broken pipe error')
                break
            except EOFError as e:
                print(e)
                print('EOFError')
                break

    def update_spec_food_value(self):
        self.special_food = False
        self.special_food_border = False
        self.sec_counter = 1

    def do_action(self, config: GameConfig):
        self.pipe.send({'event_type': 'start_game', 'data': config})
        # start thread which listens on the child_connection
        t = Thread(target=self.listen)
        t.start()

    def start(self):
        dialog = StartDialog(self)
        dialog.exec()

    def reset_value(self):
        for i in range(self.gameConfig.playerNumber):
            self.game_over.append(1)
        for i in range(self.gameConfig.playerNumber):
            self.counter.append(0)

        self.playing = True

        self.timeCounter = self.gameConfig.turnPlanTime
        self.speed = 100
        self.playtime.start()
        self.timer.start(self.speed, Qt.PreciseTimer, self)

    def start_game_pressed(self, gameConfig: GameConfig):
        self.menuBar().setDisabled(True)
        self.gameConfig = gameConfig
        if self.gameConfig.playerNumber > 4 or self.gameConfig.playerNumber < 2:
            dialog = ErrorDialog(self)
            dialog.exec()
            self.start()
        else:
            self.reset_value()
            self.set_labels()
            self.change_label_color()

            self.do_action(self.gameConfig)

    def show_dialog(self, player: int):
        end_dialog = EndGameDialog(self, player)
        end_dialog.exec()

    def show_special_food(self):
        self.pipe.send({'event_type': 'special_food', 'data': 'next_player'})
        time.sleep(0.1)
        self.special_food = True

    def timerEvent(self, event: QTimerEvent) -> None:
        """
        In charge of, in this case, update the game and check the
        conditions to continue playing, grow, spawn food and special item
        """
        if self.playtime.elapsed() > 1000:
            self.sec_counter += 1
            self.gameConfig.turnPlanTime -= 1.0
            self.timerCounterLabel.setText(str(self.gameConfig.turnPlanTime))
            self.playtime.restart()
            if self.gameConfig.turnPlanTime == 0:
                self.next_player()
                self.gameConfig.turnPlanTime = self.timeCounter
                self.timerCounterLabel.setText(str(self.timeCounter))

        if self.sec_counter % 17 == 0:
            self.update()

        if self.sec_counter % 19 == 0 and self.special_food is False:
            self.show_special_food()

        # Check if the event if from the self.timer
        if event.timerId() is self.timer.timerId():
            if self.playing is True:
                if self.all_die == self.gameConfig.playerNumber - 1:
                    winner = self.winner()
                    self.playing = False
                    self.show_dialog(winner)
                    self.timer.stop()
                    return

        else:
            super(Example, self).timerEvent(event)

    def winner(self):
        for i in range(len(self.game_over)):
            if self.game_over[i] == 1:
                return i+1

    def end_game(self, winner: int):
        self.pipe.send({'event_type': 'delete_all', 'data': winner})
        self.hide_labels()

    def set_game_over(self, player: int):
        for i in range(self.gameConfig.playerNumber):
            if player == i:
                self.score[i] = "Game over"
                self.scoreLabels[i].setText(str(self.score[i]))
                self.game_over[i] = 0

    def update_score(self, player: int, points: int):
        for i in range(self.gameConfig.playerNumber):
            if player == i:
                self.score[i] = self.score[i] + points
                self.scoreLabels[i].setText(str(self.score[i]))

    def closeEvent(self, event):
        self.pipe.send({'event_type': 'close_app'})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex_pipe, in_pipe = mp.Pipe()
    ex = Example(in_pipe)
    process = GameApplication(ex_pipe)  # second process
    process.start()
    sys.exit(app.exec_())
