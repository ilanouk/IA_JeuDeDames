# fonction qui permet savoir à quel joueur c'est le tour de jouer, si une pièce est sélectionnée, et si le joueur a gagné

import pygame
from dames.board import Board
from .constants import *

class Jeu:

    def __init__(self, win):
        self._init()
        self.win = win

    # màj de l'affichage du jeu
    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    # remet à zéro le jeu
    def reset(self):
        self._init()

    # permet de laisser ces méthodes privées
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLANC
        self.valid_moves = {}

    # permet de sélectionner une pièce
    # si c'est possible, ca renvoie True
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            # si le mouvement n'est pas valide, on déselectionne la pièce
            if not result:
                self.selected = None
                self.select(row, col)

        else:
            piece = self.board.get_piece(row, col)
            # si la pièce est de la bonne couleur, on la sélectionne
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False
    
    # permet de bouger une pièce
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # si la case est vide, on bouge la pièce
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False
        return True
    
    # permet de changer de joueur
    def change_turn(self):
        if self.turn == BLANC:
            self.turn = NOIR
        else:
            self.turn = BLANC