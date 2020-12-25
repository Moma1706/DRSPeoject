from random import choice

from PyQt5 import QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtWidgets import QWidget
from Models.food import *

class Snake(QGraphicsItem):

    def __init__(self, parent: object, color: QColor) -> None:
        super(Snake, self).__init__()
        self.parent = parent.canvas
        self.color = color
        self.particleSize = parent.particleSize

        # Random direction at the start
        #directions = [[self.particleSize, 0], [-self.particleSize, 0], [0, self.particleSize], [0, -self.particleSize]]
        self.direction = [self.particleSize, 0] #choice(directions)

        # Initial position of the Snake head
        positions = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 540, 600, 650, 700, 750, 800, 850]

        width = range(-390, choice(positions) - self.particleSize * 2, self.particleSize)
        height = range(-322, choice(positions) - self.particleSize * 2, self.particleSize)
        self.body = [[width[int(len(width) / 2)], height[int(len(height) / 2)]]]

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        brush = QBrush(self.color, Qt.Dense3Pattern)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        for i in range(len(self.body)):
            painter.drawRect(self.body[i][0], self.body[i][1], self.particleSize, self.particleSize)

        # Move Snake
        # Take head and move it around according to the direction
        head = [sum(x) for x in zip(self.body[0], self.direction)]
        # Remove the last element of the list
        self.body.pop()
        # Insert the new head
        self.body.insert(0, head)

    def boundingRect(self) -> QRectF:
        return QRectF(-400, -335, 900, 700)

    def changeDirection(self, key: int) -> None:
        """
        Change the Snake's direction according to the key the user has pressed
        """
        if key in [Qt.Key_A, Qt.Key_J] and self.direction != [self.particleSize, 0]:
            self.direction = [-self.particleSize, 0]
        elif key in [Qt.Key_D, Qt.Key_L] and self.direction != [-self.particleSize, 0]:
            self.direction = [self.particleSize, 0]
        elif key in [Qt.Key_S, Qt.Key_K] and self.direction != [0, -self.particleSize]:
            self.direction = [0, self.particleSize]
        elif key in [Qt.Key_W, Qt.Key_I] and self.direction != [0, self.particleSize]:
            self.direction = [0, -self.particleSize]

    def ateFood(self, food: Food) -> bool:
        """
        Compare the snake's head position with the food
        """
        head = self.body[0]

        if food is not None and food.x() == head[0] and food.y() == head[1]:
            self.grow()
            self.parent.removeItem(food)
            return True

        return False

    def grow(self) -> None:
        """
        Take the last element of the list, and reinsert it as the last element
        """
        self.body.append(self.body[-1])

    def outOfBounds(self) -> bool:
        """
        Check if the snake collided with the boundaries
        """
        head = self.body[0]

        return head[0] > (500 - self.particleSize * 2) or \
               head[0] < -390 or \
               head[1] > (368 - self.particleSize * 2) or \
               head[1] < -322
