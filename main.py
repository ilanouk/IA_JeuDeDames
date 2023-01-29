# Description: Jeu de dames en python, en JvsJ, ou contre une IA à différents niveaux,
#              utilisant l'algorithme de l'élagage alpha-beta.
#
# Author: @Ilan' DAUMONT-OUK
#         @Sam 

import pygame
from dames.constants import *
from dames.jeu import *

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de dames')

#permet d'obtenir la case sur laquelle on clique
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

#----------------MAIN----------------

def main():
    run = True
    clock = pygame.time.Clock()
    jeu = Jeu(WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                jeu.select(row, col)

        jeu.update()

    pygame.quit()

main()