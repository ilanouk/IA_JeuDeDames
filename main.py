import pygame, sys
from pygame.locals import *

WINDOWWIDTH=1100 #largeur fenetre
WINDOWHEIGHT=1100 #hauteur fenetre
SPACESIZE=50 #taille pour chaque espace
BOARDWIDTH=10 #nb de colonnes
BOARDHEIGHT=10 #nb de lignes
EMPTY_SPACE='EMPTY_SPACE'

#couleurs
BLANC = (255,255,255)
NOIR  = (0,0,0)
GRIS  = (155,155,155)

#fonction principale qui permet de lancer le programme
def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT

    pygame.init()

    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Jeu de dames')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    boardImage = pygame.image.load('nomImageDamier.png')###########peut etre ajouter un damier, pas sur
    #redimensionner l'image
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))

    while True:
        runGame()

def runGame():
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    drawBoard(mainBoard)

def getNewBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE]*BOARDHEIGHT)
    
    return board

def resetBoard(board): #A FAIRE : METTRE UNE CASE SUR 2 EN BLANC PUIS EN GRIS###############
    #crée le tableau
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y]=EMPTY_SPACE
    
    #A FAIRE : AJOUTER LES PIONS ############


def score():
    print('score')


if __name__=='__main__':
    main()