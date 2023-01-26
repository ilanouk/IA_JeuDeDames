import pygame

#largeur et hauteur de l'image
WIDTH, HEIGHT = 800, 800

#nb de lignes et de colonnes
LINES, COLS = 10, 10

#taille d'une case
SQUARE_SIZE = WIDTH//COLS


#création pion
#PION_BLANC = pygame.draw.circle(pygame.display.set_mode((WIDTH, HEIGHT)), (255,255,255), (100,100), 0)

#couleurs des 2 types de cases
CASE_CLAIRE = (220,191,145)
CASE_SOMBRE = (138,88,41)

#classe pour le damier
class Damier:
    
    #fonction qui permet de dessiner le DAMIER
    def draw_cel(self, display):
        #créé une image de couleur "CASE_SOMBRE"
        display.fill(CASE_SOMBRE)
        
        #boucles permettant de dessiner les cases de couleur "CASE_CLAIRE"
        for line in range(LINES):
            #intervalle partant de "line % 2" jusqu'à "COLS" avec un pas de 2
            for col in range(line % 2, COLS, 2):
                #(line*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) = les 4 coordonnées du carré représentant une case
                pygame.draw.rect(display, CASE_CLAIRE, (line*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    #fonction qui permet de dessiner les PIONS
    def draw_pion(self, display):
        
        #boucles permettant de dessiner les pions NOIRS
        for line in range(LINES+1):
            #intervalle partant de "line % 2" jusqu'à "COLS" avec un pas de 2
            for col in range(line%2, COLS-6, 2):
                #pygame.draw.circle(surface, color, pos, radius, width=0)
                pygame.draw.circle(display, (0,0,0), ((line*SQUARE_SIZE)-40, (col*SQUARE_SIZE)+40), 20)

        #boucles permettant de dessiner les pions BLANCS
        for line in range(LINES+1):
            #intervalle partant de "line % 2" jusqu'à "COLS" avec un pas de 2
            for col in range((line%2)+6, COLS, 2):
                #pygame.draw.circle(surface, color, pos, radius, width=0)
                pygame.draw.circle(display, (255,255,255), ((line*SQUARE_SIZE)-40, (col*SQUARE_SIZE)+40), 20)
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
            
            #si on clique sur la souris
            if pygame.mouse.get_pressed()[0]:
                location = pygame.mouse.get_pos()
                print(location)
                
        Damier.draw_cel(None,DISPLAYSURF)
        Damier.draw_pion(None,DISPLAYSURF)
        pygame.display.update()
    
    pygame.quit()

main()
