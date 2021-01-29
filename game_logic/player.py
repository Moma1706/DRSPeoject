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

    # pomera zmiju u pravcu koji je definisan pritisnutom tipkom
    def handle_movement(self, key, food_position, special_food_position):
        print('score: ', str(self.score))
        new_position = self.snakes[self.current_snake].handle_movement(key, food_position, special_food_position)
        if new_position['food_eaten']:
            self.score += 1
        return (new_position)

    # menja zmiju trenutnog igraca na drugu zmiju trenutnog igraca
    def change_snake(self):
        self.current_snake += 1
        if self.current_snake == self.number_of_snakes:
            self.current_snake = 0

        if self.current_snake > self.number_of_snakes:
            self.current_snake = 0

    # prolazi kroz niz kvadratica koji cine zmiju i vraca niz kvadratica tj. njohovih pozicija
    def get_rectangles(self):
        rectangles = []
        for snake in self.snakes:
            rectangles += snake.get_rectangles()
        return rectangles

    # uklanja kvadratic koji je udario u border ili u drugu zmiju
    def remove_rectangles(self, snake):
        if len(self.snakes) is 1:
            self.disabled = True
            self.snakes[self.current_snake].remove_rectangles()
            self.snakes.pop(snake)
        else:
            self.snakes[self.current_snake].remove_rectangles()
            self.snakes.pop(snake)
            self.number_of_snakes -= 1

    # proverava da li je igrac izasao izvan granica terena
    def is_border_collison(self, new_posiotion):
        for snake in self.snakes:
            return snake.is_border_collision(new_posiotion)

    # pomocna metoda koja se koristi za proveru da li je igrac i dalje ziv
    def is_disabled(self):
        return self.disabled

    # vraca poziciju zmijine glave
    def snake_position(self, snake):
        return self.snakes[snake].position()
