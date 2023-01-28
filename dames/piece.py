import pygame
from .constants import *


class Piece:

    DECALAGE = 15 #decalage du pion par rapport au bordure de la case
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if self.color == CASE_SOMBRE:
            self.direction = 1
        else:
            self.direction = -1

        self.x = 0
        self.y = 0
        self.calc_pos()

    # permet de mettre les pions au centre des cases
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        rayon = SQUARE_SIZE // 2 - self.DECALAGE
        pygame.draw.circle(win, self.color, (self.x, self.y), rayon + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), rayon)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()