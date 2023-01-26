import pygame
from damier import Damier, Pion

#largeur et hauteur de l'image
WIDTH, HEIGHT = 800, 800

#nb de lignes et de colonnes
LINES, COLS = 10, 10

#taille d'une case
SQUARE_SIZE = WIDTH//COLS

#couleurs des 2 types de cases
CASE_CLAIRE = (220,191,145)
CASE_SOMBRE = (138,88,41)

# CLASSE PRINCIPALE ------------------------------------------------------------
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de dames')



def main():

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #si on clique sur la souris et ca renvoie un tuple avec les coordonnées du clic
            if pygame.mouse.get_pressed()[0]:
                location = pygame.mouse.get_pos()
                print(location)
                
        Damier.draw_cel(None,DISPLAYSURF)
        Pion.draw_pion(None,DISPLAYSURF)
        pygame.display.update()
    
    pygame.quit()

main()