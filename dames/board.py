# représente le damier
import pygame
from .constants import *
from .piece import Piece

class Board:
    
    def __init__(self):

        self.board = []
        self.black_left = 20 # nombre de pièces
        self.white_left = 20
        self.create_board()

    # crée les cases du damier
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

    # permet de bouger une pièce
    def move(self, piece, row, col):
        #permuter case où on veut aller avec elle où se trouve la pièce
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]
    
    # méthode privée qui permet de savoir si on peut bouger une pièce vers la gauche
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []

        for row in range(start, stop, step):
            # si on est hors du damier, on arrête
            if left < 0:
                break

            current = self.board[row][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, left)] = last + skipped
                else:
                    moves[(row, left)] = last

                if last:
                    if step == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, ROWS)
                    moves.update(self._traverse_left(row + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(row + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

    #                         debut et fin, pas(haut/bas), couleur, direction, sauté
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        pass

    # permet d'obtenir les cases où on peut aller
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLANC:
            # on vérifie jusqu'à 3 cases en haut
            #                                debut et        fin, pas(haut/bas), couleur, gauche
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        
        elif piece.color == NOIR:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves # retourne les cases où on peut aller
