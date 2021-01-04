from .snake import Snake


class Player():
    def __init__(self, number_of_snakes, color):
        self.number_of_snakes = number_of_snakes
        self.color = color
        self.snakes = []
        self.current_snake = 0
        self.score = 0
        self.disabled = False

        for i in range(number_of_snakes):
            self.snakes.append(Snake(color))