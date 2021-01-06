from PyQt5.QtWidgets import QGraphicsItem

from Models.snake import Snake
from Models.player import Player
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
from multiprocessing import Process, Pipe
from Models.GameConfig import *
import random


class GameApplication(Process):
    def __init__(self, pipe):
        super().__init__(target=self.event_communication, args=[pipe])
        self.pipe = pipe
        config = GameConfig()
        self.number_of_players = 4
        self.number_of_snakes_per_player = 2
        self.timer = 0
        self.snake_size = 1
        self.current_player = 0
        self.end_game = False
        self.players = []
        self.food_position = {}
        self.steps = []
        self.steps_counter = 0

        self.colors = [QColor(200, 0, 0), QColor(0, 200, 0), QColor(0, 0, 200), QColor(128, 0, 128)]

    def event_communication(self, pipe: Pipe):
        movement_keys = [Qt.Key_A, Qt.Key_D, Qt.Key_W, Qt.Key_S]

        while True:
            receive = pipe.recv()

            if receive['event_type'] == 'start_game':
                config = receive['data']
                self.start_game(config)
            elif receive['event_type'] == 'key_pressed':
                if receive['data'] in movement_keys:
                    self.check_steps(receive['data'])

                elif receive['data'] == Qt.Key_Enter:
                    self.change_player()
                elif receive['data'] == Qt.Key_N:
                    self.change_snake()
            elif receive['event_type'] == 'next_player':
                self.change_player()

            elif receive['event_type'] == 'delete_all':
                self.end_game = True
            pipe.send({'event_type': 'rectangles', 'data': self.get_rectangles_to_draw()})

    def check_steps(self, movement):
        if self.steps[self.current_player] > self.steps_counter:
            self.steps_counter += 1
            self.handle_movement(movement)
            if self.steps_counter == self.steps[self.current_player]:
                self.change_player()

    def handle_movement(self, key):
        new_position = self.players[self.current_player].handle_movement(key, self.food_position)
        self.check_game_over(new_position)
        if new_position['food_eaten']:
            self.add_food()
            self.steps[self.current_player] += 1
            self.pipe.send({'event_type': 'score', 'data': self.current_player})

    def change_player(self):
        self.move_food()
        self.steps_counter = 0
        self.current_player += 1
        if self.current_player == self.number_of_players:
            self.current_player = 0

        if self.players[self.current_player].is_disabled() is False:
            self.pipe.send({'event_type': 'current_player', 'data': self.current_player})
        else:
            self.pipe.send({'event_type': 'current_player', 'data': 'reset_timer'})
            self.change_player()

    def change_snake(self):
        self.players[self.current_player].change_snake()

    def start_game(self, config: GameConfig):
        self.number_of_players = config.playerNumber
        self.number_of_snakes_per_player = config.snakeNumber
        self.timer = config.turnPlanTime
        for i in range(self.number_of_players):
            self.players.append(Player(self.number_of_snakes_per_player, self.colors[i]))

        self.add_food()

    def add_food(self):
        self.food_position['x'] = random.randrange(50, 400, 20)
        self.food_position['y'] = random.randrange(50, 400, 20)
        if not self.is_position_free({'x': self.food_position['x'],
                                      'y': self.food_position['y']}):
            self.add_food()

    def is_position_free(self, position):
        return self.number_of_elements_on_position(position) == 0

    def is_collision_on_position(self, position):
        return self.number_of_elements_on_position(position) >= 2

    def number_of_elements_on_position(self, position):
        number_of_occupied = 0
        rectangles = self.get_snake_rectangles()
        for rectangle in rectangles:
            if rectangle['x'] == position['x'] and rectangle['y'] == position['y']:
                number_of_occupied += 1
        return number_of_occupied
