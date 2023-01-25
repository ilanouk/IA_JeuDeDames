import pygame

#largeur et hauteur de l'image
WIDTH, HEIGHT = 800, 800

#nb de lignes et de colonnes
LINES, COLS = 10, 10

#taille d'une case
SQUARE_SIZE = WIDTH//COLS

#couleurs des 2 types de cases
CASE_CLAIRE = (220,191,145)
CASE_SOMBRE = (138,88,41)

#classe pour le damier
class Damier:
    
    #fonction qui permet de dessiner le damier
    def draw_cel(self, display):
        #créé une image de couleur "CASE_SOMBRE"
        display.fill(CASE_SOMBRE)
        
        #boucles permettant de dessiner les cases de couleur "CASE_CLAIRE"
        for line in range(LINES):
            #intervalle partant de "line % 2" jusqu'à "COLS" avec un pas de 2
            for col in range(line % 2, COLS, 2):
                #(line*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) = les 4 coordonnées du carré représentant une case
                pygame.draw.rect(display, CASE_CLAIRE, (line*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
 #


# CLASSE PRINCIPALE ------------------------------------------------------------

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de dames')



def main():

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        Damier.draw_cel(None,DISPLAYSURF)
        pygame.display.update()
    
    pygame.quit()

main()
