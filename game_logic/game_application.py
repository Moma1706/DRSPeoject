from PyQt5.QtWidgets import QGraphicsItem

from game_logic.snake import Snake
from .player import Player
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
from multiprocessing import Process, Pipe
from game_logic.GameConfig import *
import random
import time


class GameApplication(Process):
    def __init__(self, pipe):
        super().__init__(target=self.event_communication, args=[pipe])
        self.pipe = pipe
        config = GameConfig()
        self.current_player = 0
        self.end_game = False
        self.players = []
        self.food_position = {}
        self.special_food_position = {'x': 0, 'y': 0}
        self.steps = []
        self.steps_counter = 0
        self.special_food = False
        self.number_of_players = 0
        self.number_of_snakes_per_player = 0
        self.timer = 0

        self.colors = [QColor(200, 0, 0), QColor(0, 200, 0), QColor(0, 0, 200), QColor(128, 0, 128)]

    def event_communication(self, pipe: Pipe):
        movement_keys = [Qt.Key_A, Qt.Key_D, Qt.Key_W, Qt.Key_S]

        while True:

            try:
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
                elif receive['event_type'] == 'special_food':
                    self.add_special_food()
                elif receive['event_type'] == 'close_app':
                    break

                pipe.send({'event_type': 'rectangles', 'data': self.get_rectangles_to_draw()})

            except BrokenPipeError as e:
                print(e)
                print('Broken pipe error')
                break

            except EOFError as e:
                print(e)
                print('EOFError - game_APP')
                break

    def check_steps(self, movement):
        if self.steps[self.current_player] > self.steps_counter:
            self.steps_counter += 1
            self.handle_movement(movement)
            if self.steps_counter == self.steps[self.current_player]:
                self.change_player()

    def handle_movement(self, key):
        new_position = self.players[self.current_player].handle_movement(key, self.food_position, self.special_food_position)
        self.check_game_over(new_position)
        move = random.randint(1, 2)
        if new_position['food_eaten']:
            self.add_food()
            self.steps[self.current_player] += 1
            self.pipe.send({'event_type': 'score', 'data': self.current_player})

        if new_position['special_food_eaten']:
            self.special_food_position = {'x': 0, 'y': 0}
            if move is 1:
                self.steps[self.current_player] += 3
                self.pipe.send({'event_type': 'special_score', 'data': self.current_player, 'score_type': 3})
            else:
                self.steps[self.current_player] -= 1
                self.pipe.send({'event_type': 'special_score', 'data': self.current_player, 'score_type': -1})

    def is_surrounded(self, position):
        counter = 0

        if not self.is_position_free({'x': position['x'] - 20, 'y': position['y']}):
            counter += 1

        if not self.is_position_free({'x': position['x'] + 20, 'y': position['y']}):
            counter += 1

        if not self.is_position_free({'x': position['x'], 'y': position['y'] - 20}):
            counter += 1

        if not self.is_position_free({'x': position['x'], 'y': position['y'] + 20}):
            counter += 1

        if counter is 4:
            return True

    def change_player(self):
        self.move_food()
        self.steps_counter = 0
        self.current_player += 1
        if self.current_player == self.number_of_players:
            self.current_player = 0

        if self.players[self.current_player].is_disabled() is False:
            self.pipe.send({'event_type': 'current_player', 'data': self.current_player})
            time.sleep(0.1)

            for i in range(len(self.players[self.current_player].snakes)):
                position = self.players[self.current_player].snake_position(i)
                if self.is_surrounded(position):
                    if len(self.players[self.current_player].snakes) is 1:
                        self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                        print("Game Over")
                        self.pipe.send({'event_type': 'end_game', 'data': self.current_player})
                        time.sleep(0.1)
                        self.change_player()
                        # self.game_over()
                    else:
                        self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                        self.change_snake()
                        # self.remove_snake()
        else:
            self.change_player()

    def check_game_over(self, new_position):
        if self.is_border_collision(new_position):
            if len(self.players[self.current_player].snakes) is 1:
                print("Game Over")
                self.pipe.send({'event_type': 'end_game', 'data': self.current_player})
                time.sleep(0.1)
                self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                self.change_player()
                # self.game_over()
            else:
                self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                self.change_snake()
                # self.remove_snake()
            return True

        elif self.is_collision_on_position(new_position):
            if len(self.players[self.current_player].snakes) is 1:
                self.pipe.send({'event_type': 'end_game', 'data': self.current_player})
                time.sleep(0.1)
                self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                self.change_player()
                # self.game_over()
            else:
                self.players[self.current_player].remove_rectangles(self.players[self.current_player].current_snake)
                self.change_snake()
                # self.remove_snake()
            return True

        return False

    def start_game(self, config: GameConfig):
        self.number_of_players = config.playerNumber
        self.number_of_snakes_per_player = config.snakeNumber
        self.timer = config.turnPlanTime
        for i in range(self.number_of_players):
            self.players.append(Player(self.number_of_snakes_per_player, self.colors[i]))
            self.steps.append(5)

        self.add_food()

    def move_food(self):
        move = random.randint(1, 3)
        position = random.randint(1, 2)  # x ili y
        direction = random.randint(1, 2)  # left or right
        if direction is 1:  # right
            if position is 1:  # x
                new_position = move * 20
                if self.is_collision({'x': new_position + self.food_position['x'],
                                      'y': self.food_position['y']}):
                    self.add_food()
                else:
                    self.food_position['x'] += new_position

            elif position is 2:  # y
                new_position = move * 20
                if self.is_collision({'x': self.food_position['x'],
                                      'y': new_position + self.food_position['y']}):
                    self.add_food()
                else:
                    self.food_position['y'] += new_position

        elif direction is 2:  # left
            if position is 1:  # x
                new_position = move * 20
                if self.is_collision({'x': self.food_position['x'] - new_position,
                                      'y': self.food_position['y']}):
                    self.add_food()
                else:
                    self.food_position['x'] -= new_position

            elif position is 2:  # y
                new_position = move * 20
                if self.is_collision({'x': self.food_position['x'],
                                      'y': self.food_position['y'] - new_position}):
                    self.add_food()
                else:
                    self.food_position['y'] -= new_position

    def is_collision(self, f_position):
        if f_position['x'] < 30:
            print('left collision')
            return True
        elif f_position['x'] > 510:
            print('right collision')
            return True
        elif f_position['y'] < 50:
            print('up collision')
            return True
        elif f_position['y'] > 550:
            print('down collision')
            return True
        elif self.number_of_elements_on_position(f_position) is not 0:
            print('food - snake collision')
            return True

        return False

    def change_snake(self):
        self.players[self.current_player].change_snake()

    def get_rectangles_to_draw(self):
        if self.end_game is False:
            rectangles = self.get_snake_rectangles()
            food_rectangle = {'x': self.food_position['x'], 'y': self.food_position['y'], 'width': 20, 'height': 20,
                              'color': QColor(128, 128, 128)}
            rectangles.append(food_rectangle)
            if self.special_food is True:
                special_food_rectangle = {'x': self.special_food_position['x'], 'y': self.special_food_position['y'],
                                          'width': 20, 'height': 20, 'color': QColor(0, 0, 0)}
                rectangles.append(special_food_rectangle)

        else:
            rectangles = []

        return rectangles

    def get_snake_rectangles(self):
        rectangles = []
        for player in self.players:
            rectangles += player.get_rectangles()
        return rectangles

    def add_food(self):
        self.food_position['x'] = random.randrange(50, 400, 20)
        self.food_position['y'] = random.randrange(50, 400, 20)
        if not self.is_position_free({'x': self.food_position['x'],
                                      'y': self.food_position['y']}):
            self.add_food()

    def add_special_food(self):
        self.special_food = True
        self.special_food_position['x'] = 470
        self.special_food_position['y'] = 510
        if not self.is_position_free({'x': self.food_position['x'],
                                      'y': self.food_position['y']}):
            self.add_special_food()

    def is_position_free(self, position):
        return self.number_of_elements_on_position(position) == 0

    def is_collision_on_position(self, position):
        return self.number_of_elements_on_position(position) >= 2

    def is_border_collision(self, position):
        if self.players[self.current_player].is_border_collison(position):
            return True
        return False

    def number_of_elements_on_position(self, position):
        number_of_occupied = 0
        rectangles = self.get_snake_rectangles()
        for rectangle in rectangles:
            if rectangle['x'] == position['x'] and rectangle['y'] == position['y']:
                number_of_occupied += 1
        return number_of_occupied
