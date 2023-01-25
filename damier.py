import pygame

WIDTH, HEIGHT = 800, 800
LINES, COLS = 10, 10
SQUARE_SIZE = WIDTH//COLS

CASE_CLAIRE = (220,191,145)
CASE_SOMBRE = (138,88,41)

class Damier:
    
    def draw_cel(self, display):
        display.fill(CASE_SOMBRE) #
        for line in range(LINES):
            for col in range(line % 2, COLS, 2):
                pygame.draw.rect(display, CASE_CLAIRE, (line*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #


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
