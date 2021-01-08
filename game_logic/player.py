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

    def handle_movement(self, key, food_position):
        print('score: ', str(self.score))
        new_position = self.snakes[self.current_snake].handle_movement(key, food_position)
        if new_position['food_eaten']:
            self.score += 1
        return (new_position)

    def change_snake(self):
        self.current_snake += 1
        if self.current_snake == self.number_of_snakes:
            self.current_snake = 0

    def get_rectangles(self):
        rectangles = []
        for snake in self.snakes:
            rectangles += snake.get_rectangles()
        return rectangles

    def remove_rectangles(self):
        self.disabled = True
        for snake in self.snakes:
            snake.remove_rectangles()

    def is_border_collison(self, new_posiotion):
        for snake in self.snakes:
            return snake.is_border_collision(new_posiotion)

    def is_disabled(self):
        return self.disabled
