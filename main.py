import pygame, sys
from pygame.locals import *

WINDOWWIDTH=1300
WINDOWHEIGHT=1300
CELLSIZE=50
assert WINDOWWIDTH % CELLSIZE==0, "la largeur de la fenetre doit etre un multiple de la taille de la cellule"
assert WINDOWHEIGHT % CELLSIZE==0, "la hauteur de la fenetre doit etre un multiple de la taille de la cellule"

#couleur
BLANC = (255,255,255)
NOIR  = (0,0,0)
GRIS  = (155,155,155)

#fonction principale qui permet de lancer le programme
def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(WINDOWWIDTH,WINDOWHEIGHT)
    BASICFONT = pygame.font.Font(GRILLE)
    pygame.display.set_caption('Jeu de dames')

    affichage()
    while True:
        runGame()


def affichage():
    titre=pygame.font.Font()


def score():
    print('score')


if __name__=='__main__':
    main()