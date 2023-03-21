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

#C:/Users/iland/OneDrive/Images/Captures d’écran/Oui.png
#/Users/samlelouey/Desktop/crown.png
#CROWN = pygame.transform.scale(pygame.image.load('C:/Users/iland/OneDrive/Images/Captures d’écran/Oui.png'), (44, 25))

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
        for row in range(LIGNES):
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
                    #créé les pions blanc pour les 4 premières lignes
                    #if lignes < 4:
                        #self.board[lignes].append(Piece(lignes, col, WHITE))
                    #créé les pions noir de la 7 ème ligne jusqu'à la fin du damier
                    #elif lignes > 5:
                        #self.board[lignes].append(Piece(lignes, col, BLACK))
                    #créé des cases libres entre les pions blanc et noir (5e et 6e lignes)
                    #else:
                        #self.board[lignes].append(0)
                #créé des cases libres entre chaque pions
                #else:
                    #self.board[lignes].append(0)

    #Dans cette version, j'ai créé une liste de listes remplie de zéros en utilisant la multiplication d'une liste par un entier.
    #Ensuite, j'ai modifié la boucle pour itérer sur toutes les colonnes de chaque ligne.
    #J'ai également utilisé l'opérateur modulo pour déterminer le début de la série de cases noires ou blanches sur chaque ligne.
    #Enfin, j'ai remplacé la méthode "append" par l'indexation directe pour remplir la liste de pièces ou de cases libres.

    #EXPLICATION :
    #Cette fonction create_board crée un plateau de jeu pour le jeu de dames. Le plateau est représenté par une liste de listes appelée self.board.
    #Chaque élément de la liste intérieure représente une case sur le plateau et peut être soit un objet de pièce, soit un entier 0 pour indiquer une case vide.
    #La fonction utilise une boucle pour parcourir chaque rangée du plateau (LIGNES), puis utilise une autre boucle pour parcourir chaque colonne (COLS) de cette rangée.
    #La variable start_col est initialisée à 0 ou 1, en fonction du numéro de rangée.
    #Cela est fait pour que le motif d'échiquier soit créé sur le plateau, c'est-à-dire que les cases noires et blanches soient alternées.
    #Pour chaque case du plateau, la fonction vérifie d'abord si la rangée est l'une des quatre premières (pour les pièces blanches) ou les quatre dernières (pour les pièces noires).
    #Si c'est le cas, la case est initialisée avec un objet de pièce, avec une position de rangée et de colonne correspondante, ainsi que la couleur de la pièce (BLANCHE ou NOIRE).
    #Sinon, la case est simplement initialisée à 0 pour indiquer une case vide.
    #Ainsi, à la fin de la fonction, le plateau est créé avec toutes les cases initialisées avec des objets de pièce pour les joueurs blancs et noirs aux positions de départ,
    #et toutes les autres cases initialisées avec 0 pour indiquer des cases vides.
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
        
    #Au lieu de deux boucles imbriquées, cette alternative utilise une liste en compréhension pour générer toutes les coordonnées de cases en une seule ligne de code.
    #La liste en compréhension est une méthode compacte pour générer des listes à partir d'expressions.
    #Ensuite, la fonction utilise une seule boucle pour dessiner toutes les cases, en passant chaque ensemble de coordonnées
    #à la fonction pygame.draw.rect pour dessiner le rectangle correspondant à la case.

    #EXPLICATION
    #La fonction "draw" prend deux paramètres : "self" et "win". Le premier paramètre "self" fait référence à l'instance de la classe qui appelle cette méthode,
    #tandis que le deuxième paramètre "win" représente la fenêtre où le dessin sera affiché.
    #Dans cette fonction, la première étape consiste à remplir la fenêtre "win" avec une couleur sombre définie par la constante "CASE_SOMBRE".
    #Ensuite, la fonction utilise une liste en compréhension pour générer les coordonnées de chaque case. Cette liste de coordonnées est stockée dans la variable "case_coords".
    #Les coordonnées sont calculées en fonction du nombre de lignes et de colonnes définis dans les constantes "LIGNES" et "COLS",
    #ainsi que de la taille de chaque case définie dans la constante "SQUARE_SIZE".
    #Enfin, la fonction utilise une boucle "for" pour dessiner toutes les cases en utilisant les coordonnées stockées dans la liste "case_coords".
    #Pour chaque case, la fonction "pygame.draw.rect()" est appelée pour dessiner un rectangle sur la fenêtre "win".
    #Le premier paramètre de cette fonction spécifie la couleur de remplissage de la case, définie par la constante "CASE_CLAIRE",
    #et le deuxième paramètre spécifie les coordonnées de la case à dessiner.
    #En résumé, la fonction "draw" dessine un plateau de jeu sous forme de cases rectangulaires en utilisant la bibliothèque Pygame.
    def draw(self, win):
        win.fill(CASE_SOMBRE)
        # Liste en compréhension pour générer les coordonnées de chaque case
        case_coords = [(lignes * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        for lignes in range(LIGNES)
                        for col in range(lignes % 2, COLS, 2)]
        # Dessine toutes les cases en une seule fois
        for coords in case_coords:
            pygame.draw.rect(win, CASE_CLAIRE, coords)

        # Liste en compréhension pour générer toutes les pièces non nulles
        piece_coords = [(ligne, col) for ligne in range(LIGNES) for col in range(COLS) if self.board[ligne][col] != 0]
        # Dessine toutes les pièces en une seule fois
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
    
    #La première ligne teste si le nombre de pions noirs restants est inférieur ou égal à zéro.
    #Si c'est le cas, la fonction renvoie la constante "WHITE" pour indiquer que les blancs ont gagné.
    #Sinon, la deuxième ligne teste si le nombre de pions blancs restants est inférieur ou égal à zéro.
    #Si c'est le cas, la fonction renvoie la constante "BLACK" pour indiquer que les noirs ont gagné.
    #Enfin, si aucun des deux joueurs n'a encore gagné, la troisième ligne renvoie None.
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
        # Dessine le plateau de jeu sur la fenêtre
        self.board.draw(self.win)
        # Dessine les mouvements valides sur le plateau
        self.draw_valid_moves(self.valid_moves)
        # Actualise l'affichage de la fenêtre
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
    #La fonction prend en entrée les coordonnées d'une case sur le plateau de jeu (lignes et col).
    #Elle commence par vérifier si une pièce est déjà sélectionnée en testant la valeur de l'attribut "selected" de l'objet.
    #Si une pièce est sélectionnée, la fonction tente de déplacer cette pièce vers la case spécifiée par les coordonnées en utilisant la méthode "move" de l'objet "board".
    #Si le mouvement est valide, la fonction supprime éventuellement une pièce adverse sautée lors du déplacement et passe le tour au joueur suivant en appelant la méthode "change_turn".
    #Si le mouvement n'est pas valide, la fonction renvoie False. Dans tous les cas, la fonction renvoie True.
    #Si aucune pièce n'est sélectionnée, la fonction vérifie si une pièce existe sur la case spécifiée par les coordonnées et si elle appartient au joueur en cours. Si c'est le cas, la fonction sélectionne cette pièce, récupère ses mouvements valides à l'aide de la méthode "get_valid_moves" de l'objet "board" et renvoie True. Sinon, la fonction renvoie False.La fonction prend en entrée les coordonnées d'une case sur le plateau de jeu (lignes et col). Elle commence par vérifier si une pièce est déjà sélectionnée en testant la valeur de l'attribut "selected" de l'objet. Si une pièce est sélectionnée, la fonction tente de déplacer cette pièce vers la case spécifiée par les coordonnées en utilisant la méthode "move" de l'objet "board". Si le mouvement est valide, la fonction supprime éventuellement une pièce adverse sautée lors du déplacement et passe le tour au joueur suivant en appelant la méthode "change_turn". Si le mouvement n'est pas valide, la fonction renvoie False. Dans tous les cas, la fonction renvoie True.
    #Si aucune pièce n'est sélectionnée, la fonction vérifie si une pièce existe sur la case spécifiée par les coordonnées et si elle appartient au joueur en cours. Si c'est le cas, la fonction sélectionne cette pièce, récupère ses mouvements valides à l'aide de la méthode "get_valid_moves" de l'objet "board" et renvoie True. Sinon, la fonction renvoie False.

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
    #Cette nouvelle version de la fonction "_move" suit la même logique que l'originale, mais utilise des noms de variables différents et une structure de code légèrement différente.
    #Les commentaires ont également été supprimés pour rendre le code plus concis.
    #La principale différence entre les deux versions est que la nouvelle version stocke les informations du mouvement retournées par
    #la méthode "move" de l'objet "board" dans une variable "move_info", plutôt que de stocker séparément la pièce sautée dans une variable "skipped" comme dans l'originale.
    #La nouvelle version utilise également des noms de variables plus descriptifs pour améliorer la lisibilité du code.

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
    #Cette nouvelle version de la fonction "draw_valid_moves" fait essentiellement la même chose que l'originale, mais utilise des noms de variables différents
    #et une structure de code légèrement différente. Les commentaires ont également été supprimés pour rendre le code plus concis.

    #La principale différence entre les deux versions est que la nouvelle version utilise des noms de variables plus descriptifs pour améliorer la lisibilité du code,
    #comme "x" et "y" pour représenter les coordonnées de la case, et "center_x" et "center_y" pour représenter les coordonnées du centre du cercle dessiné.
    #La nouvelle version utilise également une variable "color" pour stocker la couleur utilisée pour dessiner le cercle, ce qui rend le code plus facile
    #à modifier si la couleur doit être changée plus tard.

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

#fonction minimax qui utilise alpha beta, on aurait donc pu l'appeler alphabeta
def minimax(position, depth, alpha, beta, max_player, game):
    #si la profondeur est atteinte ou si la partie est terminée, on retourne l'évaluation de la position
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    #si c'est au joueur de maximiser son score
    if max_player:
        maxEval = float('-inf')
        best_move = None
        #on parcourt toutes les positions possibles à partir de la position actuelle
        for move in get_all_moves(position, WHITE, game):
            #on calcule l'évaluation de la position
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            #la meilleure évalutation choisi est celle qui maximise l'évaluation
            maxEval = max(maxEval, evaluation)
            #si l'évaluation maximale est égale à l'évaluation actuelle, on stocke la position actuelle comme la meilleure position
            if maxEval == evaluation:
                best_move = move
            #alpha est la meilleure évaluation maximale pour le joueur MAX
            alpha = max(alpha, maxEval)
            #si alpha est supérieur ou égal à beta, on arrête la recherche
            if beta <= alpha:
                break
        
        return maxEval, best_move
    #si c'est au joueur de minimiser son score
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
#La fonction main() a pour rôle de permettre à l'utilisateur de jouer au jeu d'échecs contre un adversaire, qui peut être soit un autre joueur soit l'ordinateur.
#Le jeu utilise la bibliothèque Pygame pour afficher le plateau de jeu et les pièces, et pour gérer les interactions avec l'utilisateur.
#La première partie de la fonction demande à l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur. Si l'utilisateur choisit de jouer contre l'ordinateur,
#la fonction lui demande ensuite de choisir le niveau de difficulté de l'ordinateur (facile, moyen ou difficile).
#Le niveau facile a une pronfondeur de recherche de 3, le niveau moyen a une profondeur de recherche de 4, et le niveau difficile a une profondeur de recherche de 5.
#Ensuite, la fonction entre dans une boucle principale qui gère le déroulement du jeu. Si c'est le tour de l'ordinateur et que l'utilisateur a choisi de jouer contre l'ordinateur,
#la fonction utilise l'algorithme Minimax pour déterminer le meilleur coup à jouer, en utilisant le niveau de difficulté choisi par l'utilisateur
#pour régler la profondeur de recherche de l'algorithme. Sinon, si c'est le tour d'un joueur, la fonction attend que le joueur sélectionne une pièce à déplacer
#en cliquant dessus avec la souris, puis attend qu'il sélectionne la case de destination en cliquant à nouveau avec la souris.
#La fonction met également à jour le plateau de jeu à chaque tour, vérifie s'il y a un gagnant, et affiche le résultat final lorsque la partie est terminée.
#Enfin, la fonction termine en appelant la fonction pygame.quit() pour fermer la fenêtre du jeu.

def main():

    #run est un booléen qui permet de contrôler la boucle principale de la fonction.
    run = True
    #partie est une instance de la classe Partie qui représente l'état du plateau de jeu et permet de gérer les déplacements des pièces.
    partie = Partie(WIN)
    vs_ai = False  # variable pour indiquer si l'utilisateur joue contre l'ordinateur ou contre un autre joueur
    ia_vs_ia = False # variable pour indiquer si l'utilisateur veut que l'ordinateur joue contre lui-même
    ai_level = 1  # niveau de difficulté de l'ordinateur, 1 pour facile, 2 pour moyen, 3 pour difficile
    player1 = ""
    player2 = ""

    # demander à l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur
    #Cette boucle permet de demander à l'utilisateur s'il veut jouer contre l'ordinateur ou contre un autre joueur.
    while True:
        choix = input("Voulez-vous jouer contre l'ordinateur ou IAvsIA? (O/N/IA) : ")

        #Si l'utilisateur choisit de jouer contre l'ordinateur, la variable vs_ai est mise à True.
        if choix.lower() == 'o':
            vs_ai = True
            while True:
                ai_level_input = input("Niveau de difficulté de l'ordinateur (1 pour facile, 2 pour moyen, 3 pour difficile) : ")
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

        #IAvsIA
        elif choix.lower() == 'ia':
            ia_vs_ia = True
            while True:
                ai_level_input = input("Niveau de difficulté de l'IA, l'autre est niveau moyen (1 pour facile, 2 pour moyen, 3 pour difficile) : ")
                try:
                    ai_level = int(ai_level_input)
                    if ai_level in [1, 2, 3]:
                        break
                    else:
                        print("Choix invalide. Veuillez saisir 1, 2 ou 3.")
                except:
                    print("Choix invalide. Veuillez saisir 1, 2 ou 3.")
            break

        #Si l'utilisateur saisit autre chose que 'O' ou 'N', un message d'erreur est affiché et la boucle continue.
        else:
            print("Choix invalide. Veuillez saisir 'O' ou 'N' ou 'IA'.")

    # si l'utilisateur joue contre un autre joueur, demander les noms des joueurs
    if not (vs_ai or ia_vs_ia):
        player1 = input("Nom du joueur 1 : ")
        player2 = input("Nom du joueur 2 : ")


    #Cette partie de la boucle gère les tours de jeu.
    while run:

        #lorsqu'une ia joue contre une autre ia, il faut qu'a chaque tour, une ia joue puis l'autre
        if ia_vs_ia:
            if partie.turn == WHITE:
                if ai_level == 1:
                    value, new_board = minimax(partie.get_board(), 3, float('-inf'), float('inf'), True, partie)
                elif ai_level == 2:
                    value, new_board = minimax(partie.get_board(), 4, float('-inf'), float('inf'), True, partie)
                else:
                    value, new_board = minimax(partie.get_board(), 5, float('-inf'), float('inf'), True, partie)
                
            else:
                if ai_level == 1:
                    value, new_board = minimax(partie.get_board(), 3, float('-inf'), float('inf'), True, partie)
                elif ai_level == 2:
                    value, new_board = minimax(partie.get_board(), 4, float('-inf'), float('inf'), True, partie)
                else:
                    value, new_board = minimax(partie.get_board(), 5, float('-inf'), float('inf'), True, partie)
                
            partie.ai_move(new_board)


        #Si c'est le tour de l'ordinateur et que l'utilisateur joue contre l'ordinateur (vs_ai == True),
        #la fonction minimax() est appelée pour déterminer le meilleur coup à jouer, et le coup est joué en appelant la méthode ai_move() de l'objet partie.
        if partie.turn == WHITE and vs_ai:
            
            if ai_level == 1:
                value, new_board = minimax(partie.get_board(), 3, float('-inf'), float('inf'), True, partie)
            
            elif ai_level == 2:
                value, new_board = minimax(partie.get_board(), 4, float('-inf'), float('inf'), True, partie)
            
            else:
                value, new_board = minimax(partie.get_board(), 5, float('-inf'), float('inf'), True, partie)
            partie.ai_move(new_board)
            
        #Si c'est le tour d'un joueur et que l'utilisateur joue contre un autre joueur (vs_ai == False),
        #la fonction attend que le joueur sélectionne une pièce à déplacer en cliquant dessus avec la souris,
        #puis attend qu'il sélectionne la case de destination en cliquant à nouveau avec la souris.
        elif partie.turn == WHITE and not vs_ai:
            # l'utilisateur joue avec les pièces blanches
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    lignes, col = get_row_col_from_mouse(pos)
                    partie.select(lignes, col)

        elif partie.turn == BLACK:
            # l'utilisateur joue avec les pièces noires
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    lignes, col = get_row_col_from_mouse(pos)
                    partie.select(lignes, col)


        #Cette partie du code vérifie si un joueur a gagné la partie en appelant la méthode winner() de l'objet partie.
        #Si la méthode retourne une valeur différente de None, cela signifie qu'un joueur a gagné, et le nom du gagnant
        #est imprimé sur la console à l'aide de la fonction print(). Ensuite, la variable run est définie à False,
        #ce qui arrête la boucle principale et permet à l'utilisateur de quitter le jeu en appuyant sur la croix de la fenêtre.
        if partie.winner() != None:
            print(partie.winner())

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
