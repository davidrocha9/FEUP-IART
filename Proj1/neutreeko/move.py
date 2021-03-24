from .constants import WHITE, LIGHTBLUE, SQUARE_SIZE
import pygame

class Move:
    PADDING = 37.5
    BORDER = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()


    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (160 + self.x, 160 + self.y), radius)
        pygame.draw.circle(win, self.color, (160 + self.x, 160 + self.y), radius + self.BORDER)

    def __repr__(self):
        return str(self.color)