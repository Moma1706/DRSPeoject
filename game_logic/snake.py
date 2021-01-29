import random
from PyQt5.QtCore import Qt


class Snake():
    class Rectangle():
        def __init__(self, color, position):
            self.x = position['x']
            self.y = position['y']
            self.width = 20
            self.height = 20
            self.color = color

    def __init__(self, color):
        self.rectangles = [self.Rectangle(color, {'x': random.randrange(50, 400, 20),
                                                  'y': random.randrange(50, 400, 20)})]
        self.prev_movement = None
        self.color = color

    def get_rectangles(self):
        array_of_rectangles = []
        for rect in self.rectangles:
            array_of_rectangles.append(rect.__dict__)
        return array_of_rectangles

    # brise kvadratic sa terena
    def remove_rectangles(self):
        self.rectangles.pop(0)

    """proverava da li je moguce napraviti potez koji je igrac uneo (ukoliko je zmija isla u desno,
       ne moze odmah kretati levo)"""
    def is_movement_legal(self, key):
        if (key == Qt.Key_A and self.prev_movement == Qt.Key_D) or \
            (key == Qt.Key_D and self.prev_movement == Qt.Key_A) or \
            (key == Qt.Key_W and self.prev_movement == Qt.Key_S) or \
            (key == Qt.Key_S and self.prev_movement == Qt.Key_W):
            print("illegal movement")
            return False
        return True

    # proverava da li je zmija izasla izvan granica terena i ispisuje kuda je otisla u konzoli
    def is_border_collision(self, new_position):
        if new_position['x'] < 30:
            print('otisao je lijevo od granice')
            return True
        if new_position['x'] > 510:
            print('otisao je desno od granice')
            return True
        if new_position['y'] < 50:
            print('otisao je gore od granice')
            return True
        if new_position['y'] > 550:
            print('otisao je dole od granice')
            return True

        return False

    """ definise kuda ce se zmija pomeriti na osnovu primljene informacije koje je tipka pritisnuta
        ukoliko je zmija pojela hranu, povecava je za jedno polje """
    def handle_movement(self, key, food_position, special_food_position):
        if self.is_movement_legal(key):
            new_position = {'x': self.rectangles[-1].x, 'y': self.rectangles[-1].y}

            if self.is_border_collision(new_position) is False:
                if key == Qt.Key_A:
                    new_position['x'] -= 20
                elif key == Qt.Key_D:
                    new_position['x'] += 20
                elif key == Qt.Key_W:
                    new_position['y'] -= 20
                elif key == Qt.Key_S:
                    new_position['y'] += 20

                self.prev_movement = key

                self.rectangles.append(self.Rectangle(self.color, new_position))

                if special_food_position['x'] == self.rectangles[-1].x and special_food_position['y'] == self.rectangles[-1].y:
                    self.special_food_eaten = True
                else:
                    self.special_food_eaten = False

                if food_position['x'] == self.rectangles[-1].x and food_position['y'] == self.rectangles[-1].y:
                    self.food_eaten = True
                    return ({'x': self.rectangles[-1].x, 'y': self.rectangles[-1].y, 'food_eaten': True, 'special_food_eaten': self.special_food_eaten})
                else:
                    self.rectangles.pop(0)

        return ({'x': self.rectangles[-1].x, 'y': self.rectangles[-1].y, 'food_eaten': False, 'special_food_eaten': self.special_food_eaten})

    ## vraca poziciju zmijine glave
    def position(self):
        return ({'x': self.rectangles[-1].x, 'y': self.rectangles[-1].y})