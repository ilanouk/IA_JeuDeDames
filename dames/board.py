#représente le damier
import pygame
from .constants import *
from .piece import Piece

class Board:
    
    def __init__(self):

        self.board = []
        self.selected_piece = None #la pièce sélectionnée
        self.black_left = 20 #nombre de pièces
        self.white_left = 20
        self.create_board()

    #crée les cases du damier
    def draw_squares(self, win):

        win.fill(CASE_SOMBRE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, CASE_CLAIRE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) 

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 4:
                        self.board[row].append(Piece(row, col, NOIR))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, BLANC))
                    else:
                        # case vide
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    #permet de bouger une pièce
    def move(self, piece, row, col):
        #permuter case où on veut aller avec elle où se trouve la pièce
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]
