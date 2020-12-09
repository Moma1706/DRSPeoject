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

class Snake(QGraphicsItem):

    def __init__(self, parent: object) -> None:
        super(Snake, self).__init__()
        self.parent = parent.graphicsView
        self.particleSize = parent.particleSize

        # Random direction at the start
        directions = [[self.particleSize, 0], [-self.particleSize, 0], [0, self.particleSize], [0, -self.particleSize]]
        self.direction = choice(directions)

        # Initial position of the Snake head
        positions = [0, 50, 150, 400, -50, -200, -300]
        width = range(self.particleSize, self.particleSize * 2, self.particleSize)
        height = range(self.particleSize, self.particleSize * 2, self.particleSize)
        self.body = [[width[int(len(width) / 2)], height[int(len(height) / 2)]]]
     

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        brush = QBrush(QColor(76, 175, 79), Qt.Dense3Pattern)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        for i in range(len(self.body)):
            painter.drawRect(self.body[i][0], self.body[i][1], self.particleSize, self.particleSize)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 400, 400)