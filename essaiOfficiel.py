# Description: Jeu de dames en python, en JvsJ, ou contre une IA à différents niveaux,
#              utilisant l'algorithme de l'élagage alpha-beta.
#
# Author: @Ilan' DAUMONT-OUK
#         @Sam 

import pygame

#CONSTANTE  ----------------------------------------------------------------

WIDTH, HEIGHT = 800, 800
LIGNES, COLS = 10, 10
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
YELLOW = (255,255,0)
CASE_CLAIRE = (220,191,145)
CASE_SOMBRE = (138,88,41)


# CLASSE PIECE ---------------------------------------------------------------------------
class Piece:

    def __init__(self, lignes, col, color):
        self.lignes = lignes
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.position()

    def position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.lignes + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
        
    def draw(self, win):
        #radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y) , 30)
        if self.king:
            pygame.draw.circle(win, YELLOW, (self.x, self.y) , 30)

    def move(self, lignes, col):
        self.lignes = lignes
        self.col = col
        self.position()

# CLASSE BOARD ---------------------------------------------------------------------------

class Board:
    def __init__(self):
        self.board = []
        self.black_left = 20
        self.white_left = 20
        self.black_kings = self.white_kings = 0
        self.create_board()

    def move(self, piece, lignes, col):
        
        self.board[piece.lignes][piece.col],  self.board[lignes][col] = self.board[lignes][col], self.board[piece.lignes][piece.col]
        
        piece.move(lignes, col)

        if lignes == LIGNES - 1 or lignes == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 

    def get_piece(self, lignes, col):
        return self.board[lignes][col]

    def create_board(self):
        for lignes in range(LIGNES):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((lignes +  1) % 2):
                    #créé les pions blanc pour les 4 premières lignes
                    if lignes < 4:
                        self.board[lignes].append(Piece(lignes, col, WHITE))
                    #créé les pions noir de la 7 ème ligne jusqu'à la fin du damier
                    elif lignes > 5:
                        self.board[lignes].append(Piece(lignes, col, BLACK))
                    #créé des cases libres entre les pions blanc et noir (5e et 6e lignes)
                    else:
                        self.board[lignes].append(0)
                #créé des cases libres entre chaque pions
                else:
                    self.board[lignes].append(0)
        
    def draw(self, win):
        win.fill(CASE_SOMBRE)
        for lignes in range(LIGNES):
            for col in range(lignes % 2, COLS, 2):
                pygame.draw.rect(win, CASE_CLAIRE, (lignes*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
        for lignes in range(LIGNES):
            for col in range(COLS):
                piece = self.board[lignes][col]
                #si la case n'est pas libre, alors on dessine le pion
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.lignes][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        lignes = piece.lignes

        if piece.color == BLACK or piece.king:
            moves.update(self.diagonale_poss(lignes -1, max(lignes-3, -1), -1, piece.color, left, right, True))
            moves.update(self.diagonale_poss(lignes -1, max(lignes-3, -1), -1, piece.color, left, right, False))
            
        if piece.color == WHITE or piece.king:
            moves.update(self.diagonale_poss(lignes +1, min(lignes+3, LIGNES), 1, piece.color, left, right, True))
            moves.update(self.diagonale_poss(lignes +1, min(lignes+3, LIGNES), 1, piece.color, left, right, False))
    
        return moves
    
    def diagonale_poss(self, start, stop, step, color, left, right, bool, skipped = []):
        moves = {}
        last = []

        for i in range(start, stop, step):
            if bool:
                if left < 0:
                    break
                current = self.board[i][left]
            else:
                if right >= COLS:
                    break
                current = self.board[i][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    if bool:
                        moves[(i, left)] = last + skipped
                    else:
                         moves[(i, right)] = last + skipped
                else:
                    if bool:
                        moves[(i, left)] = last
                    else:
                        moves[(i, right)] = last
                
                if last:
                    if step == -1:
                        lignes = max(i-3, 0)
                    else:
                        lignes = min(i+3, LIGNES)
                    if bool:
                        moves.update(self.diagonale_poss(i+step, lignes, step, color, left-1, right, True, skipped=last))
                        moves.update(self.diagonale_poss(i+step, lignes, step, color, left+1, right, False, skipped=last))
                    else:
                        moves.update(self.diagonale_poss(i+step, lignes, step, color, left, right-1, True, skipped=last))
                        moves.update(self.diagonale_poss(i+step, lignes, step, color, left,right+1, False, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            if bool:
                left -= 1
            else:
                right += 1
               
        return moves
        
# CLASSE GAME ----------------------------------------------------------------

class Partie:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def select(self, lignes, col):
        if self.selected:
            result = self._move(lignes, col)
            if not result:
                self.selected = None
                self.select(lignes, col)
        
        piece = self.board.get_piece(lignes, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def select(self, lignes, col):
        if self.selected:
            piece = self.board.get_piece(lignes, col)
            if self.selected and piece == 0 and (lignes, col) in self.valid_moves:
                self.board.move(self.selected, lignes, col)
                skipped = self.valid_moves[(lignes, col)]
                if skipped:
                    self.board.remove(skipped)
                self.change_turn()
            else:
                result = False
            result = True
            
            if not result:
                self.selected = None
                self.select(lignes, col)
        
        piece = self.board.get_piece(lignes, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            lignes, col = move
            pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, lignes * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

# CLASSE PRINCIPALE ------------------------------------------------------------

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de Dames')

def get_row_col_from_mouse(pos):
    x, y = pos
    lignes = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return lignes, col

def main():
    run = True
    clock = pygame.time.Clock()
    partie = Partie(WIN)

    while run:

        if partie.winner() != None:
            print(partie.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                lignes, col = get_row_col_from_mouse(pos)
                partie.select(lignes, col)

        partie.update()
    
    pygame.quit()

main()
