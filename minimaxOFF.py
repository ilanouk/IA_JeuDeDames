import pygame
from copy import deepcopy

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

CROWN = pygame.transform.scale(pygame.image.load('/Users/samlelouey/Desktop/crown.png'), (44, 25))

# CLASSE PIECE ---------------------------------------------------------------------------
class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, lignes, col, color):
        self.lignes = lignes
        self.col = col
        self.color = color
        self.king = False
        self.x_coord = 0
        self.y_coord = 0
        self.position()

    def position(self):
        self.x_coord = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y_coord = SQUARE_SIZE * self.lignes + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        #radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x_coord, self.y_coord) , 30)
        if self.king:
            pygame.draw.circle(win, YELLOW, (self.x_coord, self.y_coord) , 30)

    def move(self, lignes, col):
        self.lignes = lignes
        self.col = col
        self.position()

    def __repr__(self):
        return str(self.color)

# CLASSE BOARD ---------------------------------------------------------------------------
class Board:
    def __init__(self):
        self.board = []
        self.black_left = 20
        self.white_left = 20
        self.black_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, lignes, col):

        start_lignes, start_col = piece.lignes, piece.col

        # Swap the positions of the pieces on the board
        self.board[start_lignes][start_col], self.board[lignes][col] = self.board[lignes][col], self.board[start_lignes][start_col]
        
        #self.board[piece.lignes][piece.col],  self.board[lignes][col] = self.board[lignes][col], self.board[piece.lignes][piece.col]

        # Move the piece to the new position
        piece.move(lignes, col)

        if piece.color == WHITE and lignes == LIGNES - 1 or piece.color == BLACK and lignes == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 

    def get_piece(self, lignes, col):
        return self.board[lignes][col]

    #def create_board(self):
        #for lignes in range(LIGNES):
            #self.board.append([])
            #for col in range(COLS):
                #if col % 2 == ((lignes +  1) % 2):
                    #cr???? les pions blanc pour les 4 premi??res lignes
                    #if lignes < 4:
                        #self.board[lignes].append(Piece(lignes, col, WHITE))
                    #cr???? les pions noir de la 7 ??me ligne jusqu'?? la fin du damier
                    #elif lignes > 5:
                        #self.board[lignes].append(Piece(lignes, col, BLACK))
                    #cr???? des cases libres entre les pions blanc et noir (5e et 6e lignes)
                    #else:
                        #self.board[lignes].append(0)
                #cr???? des cases libres entre chaque pions
                #else:
                    #self.board[lignes].append(0)

    #Dans cette version, j'ai cr???? une liste de listes remplie de z??ros en utilisant la multiplication d'une liste par un entier.
    #Ensuite, j'ai modifi?? la boucle pour it??rer sur toutes les colonnes de chaque ligne.
    #J'ai ??galement utilis?? l'op??rateur modulo pour d??terminer le d??but de la s??rie de cases noires ou blanches sur chaque ligne.
    #Enfin, j'ai remplac?? la m??thode "append" par l'indexation directe pour remplir la liste de pi??ces ou de cases libres.

    #EXPLICATION :
    #Cette fonction create_board cr??e un plateau de jeu pour le jeu de dames. Le plateau est repr??sent?? par une liste de listes appel??e self.board.
    #Chaque ??l??ment de la liste int??rieure repr??sente une case sur le plateau et peut ??tre soit un objet de pi??ce, soit un entier 0 pour indiquer une case vide.
    #La fonction utilise une boucle pour parcourir chaque rang??e du plateau (LIGNES), puis utilise une autre boucle pour parcourir chaque colonne (COLS) de cette rang??e.
    #La variable start_col est initialis??e ?? 0 ou 1, en fonction du num??ro de rang??e.
    #Cela est fait pour que le motif d'??chiquier soit cr???? sur le plateau, c'est-??-dire que les cases noires et blanches soient altern??es.
    #Pour chaque case du plateau, la fonction v??rifie d'abord si la rang??e est l'une des quatre premi??res (pour les pi??ces blanches) ou les quatre derni??res (pour les pi??ces noires).
    #Si c'est le cas, la case est initialis??e avec un objet de pi??ce, avec une position de rang??e et de colonne correspondante, ainsi que la couleur de la pi??ce (BLANCHE ou NOIRE).
    #Sinon, la case est simplement initialis??e ?? 0 pour indiquer une case vide.
    #Ainsi, ?? la fin de la fonction, le plateau est cr???? avec toutes les cases initialis??es avec des objets de pi??ce pour les joueurs blancs et noirs aux positions de d??part,
    #et toutes les autres cases initialis??es avec 0 pour indiquer des cases vides.
    def create_board(self):
        for lignes in range(LIGNES):
            self.board.append([0] * COLS)
            start_col = lignes % 2

            for col in range(start_col, COLS, 2):
                if lignes < 4:
                    self.board[lignes][col] = Piece(lignes, col, WHITE)
                elif lignes > 5:
                    self.board[lignes][col] = Piece(lignes, col, BLACK)
                else:
                    self.board[lignes][col] = 0
        
    #Au lieu de deux boucles imbriqu??es, cette alternative utilise une liste en compr??hension pour g??n??rer toutes les coordonn??es de cases en une seule ligne de code.
    #La liste en compr??hension est une m??thode compacte pour g??n??rer des listes ?? partir d'expressions.
    #Ensuite, la fonction utilise une seule boucle pour dessiner toutes les cases, en passant chaque ensemble de coordonn??es
    #?? la fonction pygame.draw.rect pour dessiner le rectangle correspondant ?? la case.

    #EXPLICATION
    #La fonction "draw" prend deux param??tres : "self" et "win". Le premier param??tre "self" fait r??f??rence ?? l'instance de la classe qui appelle cette m??thode,
    #tandis que le deuxi??me param??tre "win" repr??sente la fen??tre o?? le dessin sera affich??.
    #Dans cette fonction, la premi??re ??tape consiste ?? remplir la fen??tre "win" avec une couleur sombre d??finie par la constante "CASE_SOMBRE".
    #Ensuite, la fonction utilise une liste en compr??hension pour g??n??rer les coordonn??es de chaque case. Cette liste de coordonn??es est stock??e dans la variable "case_coords".
    #Les coordonn??es sont calcul??es en fonction du nombre de lignes et de colonnes d??finis dans les constantes "LIGNES" et "COLS",
    #ainsi que de la taille de chaque case d??finie dans la constante "SQUARE_SIZE".
    #Enfin, la fonction utilise une boucle "for" pour dessiner toutes les cases en utilisant les coordonn??es stock??es dans la liste "case_coords".
    #Pour chaque case, la fonction "pygame.draw.rect()" est appel??e pour dessiner un rectangle sur la fen??tre "win".
    #Le premier param??tre de cette fonction sp??cifie la couleur de remplissage de la case, d??finie par la constante "CASE_CLAIRE",
    #et le deuxi??me param??tre sp??cifie les coordonn??es de la case ?? dessiner.
    #En r??sum??, la fonction "draw" dessine un plateau de jeu sous forme de cases rectangulaires en utilisant la biblioth??que Pygame.
    def draw(self, win):
        win.fill(CASE_SOMBRE)
        # Liste en compr??hension pour g??n??rer les coordonn??es de chaque case
        case_coords = [(lignes * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        for lignes in range(LIGNES)
                        for col in range(lignes % 2, COLS, 2)]
        # Dessine toutes les cases en une seule fois
        for coords in case_coords:
            pygame.draw.rect(win, CASE_CLAIRE, coords)

        # Liste en compr??hension pour g??n??rer toutes les pi??ces non nulles
        piece_coords = [(ligne, col) for ligne in range(LIGNES) for col in range(COLS) if self.board[ligne][col] != 0]
        # Dessine toutes les pi??ces en une seule fois
        for ligne, col in piece_coords:
            self.board[ligne][col].draw(win)

    #def draw(self, win):
        #win.fill(CASE_SOMBRE)
        #for lignes in range(LIGNES):
            #for col in range(lignes % 2, COLS, 2):
                #pygame.draw.rect(win, CASE_CLAIRE, (lignes*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
        #for lignes in range(LIGNES):
            #for col in range(COLS):
                #piece = self.board[lignes][col]
                #si la case n'est pas libre, alors on dessine le pion
                #if piece != 0:
                    #piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
                self.board[piece.lignes][piece.col] = 0



    #def remove(self, pieces):
        #for piece in pieces:
            #self.board[piece.lignes][piece.col] = 0
            #if piece != 0:
                #if piece.color == BLACK:
                    #self.black_left -= 1
                #else:
                    #self.white_left -= 1
    
    #La premi??re ligne teste si le nombre de pions noirs restants est inf??rieur ou ??gal ?? z??ro.
    #Si c'est le cas, la fonction renvoie la constante "WHITE" pour indiquer que les blancs ont gagn??.
    #Sinon, la deuxi??me ligne teste si le nombre de pions blancs restants est inf??rieur ou ??gal ?? z??ro.
    #Si c'est le cas, la fonction renvoie la constante "BLACK" pour indiquer que les noirs ont gagn??.
    #Enfin, si aucun des deux joueurs n'a encore gagn??, la troisi??me ligne renvoie None.
    def winner(self):
        return WHITE if self.black_left <= 0 else BLACK if self.white_left <= 0 else None


    #def winner(self):
        #if self.black_left <= 0:
            #return WHITE
        #elif self.white_left <= 0:
            #return BLACK
        
        #return None 
    
    def get_valid_moves(self, piece):
        available_moves = {}
        left = piece.col - 1
        right = piece.col + 1
        lignes = piece.lignes

        if piece.color == BLACK or piece.king:
            available_moves.update(self.diagonale_poss(lignes -1, max(lignes-3, -1), -1, piece.color, left, right, True))
            available_moves.update(self.diagonale_poss(lignes -1, max(lignes-3, -1), -1, piece.color, left, right, False))
            
        if piece.color == WHITE or piece.king:
            available_moves.update(self.diagonale_poss(lignes +1, min(lignes+3, LIGNES), 1, piece.color, left, right, True))
            available_moves.update(self.diagonale_poss(lignes +1, min(lignes+3, LIGNES), 1, piece.color, left, right, False))
    
        return available_moves

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
        # Dessine le plateau de jeu sur la fen??tre
        self.board.draw(self.win)
        # Dessine les mouvements valides sur le plateau
        self.draw_valid_moves(self.valid_moves)
        # Actualise l'affichage de la fen??tre
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    #def select(self, lignes, col):
        #if self.selected:
            #result = self._move(lignes, col)
            #if not result:
                #self.selected = None
                #self.select(lignes, col)
        
        #piece = self.board.get_piece(lignes, col)
        #if piece != 0 and piece.color == self.turn:
            #self.selected = piece
            #self.valid_moves = self.board.get_valid_moves(piece)
            #return True
            
        #return False

    #EXPLICATION :
    #La fonction prend en entr??e les coordonn??es d'une case sur le plateau de jeu (lignes et col).
    #Elle commence par v??rifier si une pi??ce est d??j?? s??lectionn??e en testant la valeur de l'attribut "selected" de l'objet.
    #Si une pi??ce est s??lectionn??e, la fonction tente de d??placer cette pi??ce vers la case sp??cifi??e par les coordonn??es en utilisant la m??thode "move" de l'objet "board".
    #Si le mouvement est valide, la fonction supprime ??ventuellement une pi??ce adverse saut??e lors du d??placement et passe le tour au joueur suivant en appelant la m??thode "change_turn".
    #Si le mouvement n'est pas valide, la fonction renvoie False. Dans tous les cas, la fonction renvoie True.
    #Si aucune pi??ce n'est s??lectionn??e, la fonction v??rifie si une pi??ce existe sur la case sp??cifi??e par les coordonn??es et si elle appartient au joueur en cours. Si c'est le cas, la fonction s??lectionne cette pi??ce, r??cup??re ses mouvements valides ?? l'aide de la m??thode "get_valid_moves" de l'objet "board" et renvoie True. Sinon, la fonction renvoie False.La fonction prend en entr??e les coordonn??es d'une case sur le plateau de jeu (lignes et col). Elle commence par v??rifier si une pi??ce est d??j?? s??lectionn??e en testant la valeur de l'attribut "selected" de l'objet. Si une pi??ce est s??lectionn??e, la fonction tente de d??placer cette pi??ce vers la case sp??cifi??e par les coordonn??es en utilisant la m??thode "move" de l'objet "board". Si le mouvement est valide, la fonction supprime ??ventuellement une pi??ce adverse saut??e lors du d??placement et passe le tour au joueur suivant en appelant la m??thode "change_turn". Si le mouvement n'est pas valide, la fonction renvoie False. Dans tous les cas, la fonction renvoie True.
    #Si aucune pi??ce n'est s??lectionn??e, la fonction v??rifie si une pi??ce existe sur la case sp??cifi??e par les coordonn??es et si elle appartient au joueur en cours. Si c'est le cas, la fonction s??lectionne cette pi??ce, r??cup??re ses mouvements valides ?? l'aide de la m??thode "get_valid_moves" de l'objet "board" et renvoie True. Sinon, la fonction renvoie False.

    def select(self, lignes, col):
        if self.selected:
            piece = self.board.get_piece(lignes, col)
            if self.selected and piece == 0 and (lignes, col) in self.valid_moves:
                self.board.move(self.selected, lignes, col)
                skipped = self.valid_moves[(lignes, col)]
                if skipped:
                    self.board.remove(skipped)
                #self.change_turn()
                #fonction change_turn() DIRECTEMENT ICI-----------
                self.valid_moves = {}
                self.turn = WHITE if self.turn == BLACK else BLACK
                #-----------------------------------------
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


    #def _move(self, row, col):
        #piece = self.board.get_piece(row, col)
        #if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #self.board.move(self.selected, row, col)
            #skipped = self.valid_moves[(row, col)]
            #if skipped:
                #self.board.remove(skipped)
            #self.change_turn()
        #else:
            #return False

        #return True

    #CHANGEMENT :
    #Cette nouvelle version de la fonction "_move" suit la m??me logique que l'originale, mais utilise des noms de variables diff??rents et une structure de code l??g??rement diff??rente.
    #Les commentaires ont ??galement ??t?? supprim??s pour rendre le code plus concis.
    #La principale diff??rence entre les deux versions est que la nouvelle version stocke les informations du mouvement retourn??es par
    #la m??thode "move" de l'objet "board" dans une variable "move_info", plut??t que de stocker s??par??ment la pi??ce saut??e dans une variable "skipped" comme dans l'originale.
    #La nouvelle version utilise ??galement des noms de variables plus descriptifs pour am??liorer la lisibilit?? du code.

    def _move(self, row, col):
        target_piece = self.board.get_piece(row, col)
        if self.selected_piece and target_piece == 0 and (row, col) in self.valid_moves:
            move_info = self.board.move(self.selected_piece, row, col)
            if move_info['skipped_piece']:
                self.board.remove(move_info['skipped_piece'])
            self.change_turn()
            return True
        else:
            return False


    #def draw_valid_moves(self, moves):
        #for move in moves:
            #lignes, col = move
            #pygame.draw.circle(self.win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE//2, lignes * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    #CHANGEMENT :
    #Cette nouvelle version de la fonction "draw_valid_moves" fait essentiellement la m??me chose que l'originale, mais utilise des noms de variables diff??rents
    #et une structure de code l??g??rement diff??rente. Les commentaires ont ??galement ??t?? supprim??s pour rendre le code plus concis.

    #La principale diff??rence entre les deux versions est que la nouvelle version utilise des noms de variables plus descriptifs pour am??liorer la lisibilit?? du code,
    #comme "x" et "y" pour repr??senter les coordonn??es de la case, et "center_x" et "center_y" pour repr??senter les coordonn??es du centre du cercle dessin??.
    #La nouvelle version utilise ??galement une variable "color" pour stocker la couleur utilis??e pour dessiner le cercle, ce qui rend le code plus facile
    #?? modifier si la couleur doit ??tre chang??e plus tard.

    def draw_valid_moves(self, moves):
        for move in moves:
            x, y = move
            center_x = x * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = y * SQUARE_SIZE + SQUARE_SIZE // 2
            radius = 15
            color = RED
            pygame.draw.circle(self.win, color, (center_y, center_x), radius)

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        #self.change_turn()
        #FONCTION CHANGE_TURN DIRECTEMENT ICI
        self.valid_moves = {}
        self.turn = WHITE if self.turn == BLACK else BLACK


# -------------------------- MINIMAX ---------------------------------

#RED = (255,0,0)
#WHITE = (255, 255, 255)

#def minimax(position, depth, max_player, game):
    #if depth == 0 or position.winner() != None:
        #return position.evaluate(), position
    
    #if max_player:
        #maxEval = float('-inf')
        #best_move = None
        #for move in get_all_moves(position, WHITE, game):
            #evaluation = minimax(move, depth-1, False, game)[0]
            #maxEval = max(maxEval, evaluation)
            #if maxEval == evaluation:
                #best_move = move
        
        #return maxEval, best_move
    #else:
        #minEval = float('inf')
        #best_move = None
        #for move in get_all_moves(position, BLACK, game):
            #evaluation = minimax(move, depth-1, True, game)[0]
            #minEval = min(minEval, evaluation)
            #if minEval == evaluation:
                #best_move = move
        
        #return minEval, best_move


def minimax(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        
        return minEval, best_move






def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board




def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.lignes, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


#def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    #board.draw(game.win)
    #pygame.draw.circle(game.win, (0,255,0), (piece.x_coord, piece.y_coord), 50, 5)
    #game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)


# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
#--------------------------- MAIN --------------------------



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de Dames')

def get_row_col_from_mouse(pos):
    x, y = pos
    lignes = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return lignes, col



#FONCTIONNEMENT :
#La fonction main2() a pour r??le de permettre ?? l'utilisateur de jouer au jeu d'??checs contre un adversaire, qui peut ??tre soit un autre joueur soit l'ordinateur.
#Le jeu utilise la biblioth??que Pygame pour afficher le plateau de jeu et les pi??ces, et pour g??rer les interactions avec l'utilisateur.
#La premi??re partie de la fonction demande ?? l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur. Si l'utilisateur choisit de jouer contre l'ordinateur,
#la fonction lui demande ensuite de choisir le niveau de difficult?? de l'ordinateur (facile, moyen ou difficile).
#Ensuite, la fonction entre dans une boucle principale qui g??re le d??roulement du jeu. Si c'est le tour de l'ordinateur et que l'utilisateur a choisi de jouer contre l'ordinateur,
#la fonction utilise l'algorithme Minimax pour d??terminer le meilleur coup ?? jouer, en utilisant le niveau de difficult?? choisi par l'utilisateur
#pour r??gler la profondeur de recherche de l'algorithme. Sinon, si c'est le tour d'un joueur, la fonction attend que le joueur s??lectionne une pi??ce ?? d??placer
#en cliquant dessus avec la souris, puis attend qu'il s??lectionne la case de destination en cliquant ?? nouveau avec la souris.
#La fonction met ??galement ?? jour le plateau de jeu ?? chaque tour, v??rifie s'il y a un gagnant, et affiche le r??sultat final lorsque la partie est termin??e.
#Enfin, la fonction termine en appelant la fonction pygame.quit() pour fermer la fen??tre du jeu.

def main():
    #run est un bool??en qui permet de contr??ler la boucle principale de la fonction.
    run = True
    #partie est une instance de la classe Partie qui repr??sente l'??tat du plateau de jeu et permet de g??rer les d??placements des pi??ces.
    partie = Partie(WIN)
    vs_ai = False  # variable pour indiquer si l'utilisateur joue contre l'ordinateur ou contre un autre joueur
    ai_level = 1  # niveau de difficult?? de l'ordinateur, 1 pour facile, 2 pour moyen, 3 pour difficile
    player1 = ""
    player2 = ""

    # demander ?? l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur
    #Cette boucle permet de demander ?? l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur.
    while True:
        choix = input("Voulez-vous jouer contre l'ordinateur ? (O/N) : ")
        #Si l'utilisateur choisit de jouer contre l'ordinateur, la variable vs_ai est mise ?? True.
        if choix.lower() == 'o':
            vs_ai = True
            while True:
                ai_level_input = input("Niveau de difficult?? de l'ordinateur (1 pour facile, 2 pour moyen, 3 pour difficile) : ")
                try:
                    ai_level = int(ai_level_input)
                    if ai_level in [1, 2, 3]:
                        break
                    else:
                        print("Choix invalide. Veuillez saisir 1, 2 ou 3.")
                except:
                    print("Choix invalide. Veuillez saisir 1, 2 ou 3.")
            break
        #Sinon, si l'utilisateur choisit de jouer contre un autre joueur, la boucle se termine.
        elif choix.lower() == 'n':
            break
        #Si l'utilisateur saisit autre chose que 'O' ou 'N', un message d'erreur est affich?? et la boucle continue.
        else:
            print("Choix invalide. Veuillez saisir 'O' ou 'N'.")
     # si l'utilisateur joue contre un autre joueur, demander les noms des joueurs
    if not vs_ai:
        player1 = input("Nom du joueur 1 : ")
        player2 = input("Nom du joueur 2 : ")

    #Cette partie de la boucle g??re les tours de jeu.
    while run:
        #Si c'est le tour de l'ordinateur et que l'utilisateur joue contre l'ordinateur (vs_ai == True),
        #la fonction minimax() est appel??e pour d??terminer le meilleur coup ?? jouer, et le coup est jou?? en appelant la m??thode ai_move() de l'objet partie.
        if partie.turn == WHITE and vs_ai:
            if ai_level == 1:
                value, new_board = minimax(partie.get_board(), 3, float('-inf'), float('inf'), True, partie)
            elif ai_level == 2:
                value, new_board = minimax(partie.get_board(), 4, float('-inf'), float('inf'), True, partie)
            else:
                value, new_board = minimax(partie.get_board(), 5, float('-inf'), float('inf'), True, partie)
            partie.ai_move(new_board)
            
        #Si c'est le tour d'un joueur et que l'utilisateur joue contre un autre joueur (vs_ai == False),
        #la fonction attend que le joueur s??lectionne une pi??ce ?? d??placer en cliquant dessus avec la souris,
        #puis attend qu'il s??lectionne la case de destination en cliquant ?? nouveau avec la souris.
        elif partie.turn == WHITE and not vs_ai:
            # l'utilisateur joue avec les pi??ces blanches
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    lignes, col = get_row_col_from_mouse(pos)
                    partie.select(lignes, col)
        elif partie.turn == BLACK:
            # l'utilisateur joue avec les pi??ces noires
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    lignes, col = get_row_col_from_mouse(pos)
                    partie.select(lignes, col)

        #Cette partie du code v??rifie si un joueur a gagn?? la partie en appelant la m??thode winner() de l'objet partie.
        #Si la m??thode retourne une valeur diff??rente de None, cela signifie qu'un joueur a gagn??, et le nom du gagnant
        #est imprim?? sur la console ?? l'aide de la fonction print(). Ensuite, la variable run est d??finie ?? False,
        #ce qui arr??te la boucle principale et permet ?? l'utilisateur de quitter le jeu en appuyant sur la croix de la fen??tre.
        if partie.winner() != None:
            #print(partie.winner())

            # afficher le nom du gagnant s'il y en a un, sinon afficher "Match nul"
            winner = partie.winner()
            if winner == "blanc":
                print("Le gagnant est :", player1)
            elif winner == "noir":
                print("Le gagnant est :", player2)
            
            run = False

        partie.update()
    
    pygame.quit()

main()
