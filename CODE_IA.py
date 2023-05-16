import pygame, sys
from copy import deepcopy

LIGHT_SQUARE = (255,255,255) # couleur RGB pour les cases claires
DARK_SQUARE = (0,0,0) # couleur RGB pour les cases sombres

WHITE = (255, 255, 255) # couleur RGB pour les pièces blanches
BLACK = (155, 155, 155) # couleur RGB pour les pièces noires
YELLOW = (255,255,0) # couleur RGB pour les pièces reines

WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700 # dimensions de la fenêtre 
BOARD_LINES, BOARD_COLS = 10, 10 # nombre de lignes et de colonnes du damier
SQUARE_SIZE = WINDOW_WIDTH//BOARD_COLS # taille d'une case

# --------------------------------------------------------------------------- CLASSE PIECE ---------------------------------------------------------------------------
class Piece:
    """
    Classe représentant une pièce de jeu.
    
    """
    
    def __init__(self, line, col, color):
        """
        Initialise une nouvelle pièce.
        
        :param line: int, la ligne sur laquelle la pièce est positionnée.
        :param col: int, la colonne sur laquelle la pièce est positionnée.
        :param color: tuple, la couleur de la pièce au format (R, G, B).
        
        """
        self.line = line
        self.col = col
        self.x_pos = 0
        self.y_pos = 0
        self.calculate_position()
        self.color = color
        self.is_queen = False
        


    def calculate_position(self):
        """
        Calcule la position (x, y) de la pièce en fonction de sa ligne et colonne.
        
        """
        center_offset = SQUARE_SIZE // 2
        self.x_pos, self.y_pos = map(lambda coord: coord * SQUARE_SIZE + center_offset, (self.col, self.line))

    
    def draw(self, window):
        """
        Dessine la pièce sur la fenêtre de jeu.
        
        :param window: pygame.Surface, la fenêtre de jeu sur laquelle la pièce doit être dessinée.
        
        """
        if self.is_queen:
            pygame.draw.circle(window, YELLOW, (self.x_pos, self.y_pos) , 30)
            
        else:
            pygame.draw.circle(window, self.color, (self.x_pos, self.y_pos) , 30)

            
# --------------------------------------------------------------------------- CLASSE BOARD ---------------------------------------------------------------------------
class Board:
    """
    Classe représentant un plateau de jeu.
    
    """
    def __init__(self):
        """
        Initialise un nouveau plateau de jeu.
        
        """
        self.board = []
        self.black_pieces_left = 20
        self.white_pieces_left = 20
        self.black_queens = self.white_queens = 0
        self.generate_board()


    def move_piece(self, piece, lignes, col):
        """
        Déplace une pièce sur le plateau.

        :param piece: Piece, la pièce à déplacer.
        :param lignes: int, la ligne de destination.
        :param col: int, la colonne de destination.
        
        """
        start_lignes, start_col = piece.line, piece.col
        self.board[start_lignes][start_col], self.board[lignes][col] = self.board[lignes][col], self.board[start_lignes][start_col]
        piece.line = lignes
        piece.col = col
        piece.calculate_position()
        
        if piece.color == BLACK and lignes == BOARD_LINES - 1 or piece.color == WHITE and lignes == 0:
            piece.is_queen = True
            if piece.color == BLACK:
                self.black_queens += 1    
            else:
                self.white_queens += 1


    def get_piece_at(self, lignes, col):
        """
        Récupère la pièce à la position donnée.

        :param lignes: int, la ligne où chercher la pièce.
        :param col: int, la colonne où chercher la pièce.

        :return: Piece, la pièce trouvée ou None si aucune pièce à cette position.
        
        """
        for i, ligne_data in enumerate(self.board):
            if i == lignes:
                return ligne_data[col]


    def generate_board(self):
        """
        Génère le plateau initial avec les pièces placées.
        
        """
        black_lines = [[Piece(line, col, BLACK) if col % 2 == line % 2 else 0 for col in range(BOARD_COLS)] for line in range(4)]
        white_lines = [[Piece(line, col, WHITE) if col % 2 == line % 2 else 0 for col in range(BOARD_COLS)] for line in range(6, BOARD_LINES)]
        empty_lines = [[0] * BOARD_COLS for line in range(4, 6)]
        self.board = black_lines + empty_lines + white_lines

    
    def draw(self, window):
        """
        Dessine le plateau sur la fenêtre de jeu.

        :param window: pygame.Surface, la fenêtre de jeu sur laquelle le plateau doit être dessiné.
        
        """
        window.fill(LIGHT_SQUARE)
        square_coords = [(lines * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) for lines in range(BOARD_LINES) for col in range(lines % 2, BOARD_COLS, 2)]
        for coords in square_coords:
            pygame.draw.rect(window, DARK_SQUARE, coords)    
        piece_coords = [(line, col) for line in range(BOARD_LINES) for col in range(BOARD_COLS) if self.board[line][col] != 0]
        for line, col in piece_coords:
            self.board[line][col].draw(window)

    
    def remove_pieces(self, pieces):
        """
        Retire les pièces du plateau.

        :param pieces: list, les pièces à retirer.
        
        """
        remaining_pieces = list(filter(lambda x: x != 0, pieces))
        for piece in remaining_pieces:
            if piece.color == WHITE:
                self.white_pieces_left -= 1    
            else:
                self.black_pieces_left -= 1    
            self.board[piece.line][piece.col] = 0

    def get_winner(self):
        """
        Détermine le gagnant de la partie en fonction des pièces restantes et des coups disponibles pour chaque joueur.
        
        :return: BLACK si le joueur noir gagne, WHITE si le joueur blanc gagne, et None si il n'y a pas encore de gagnant.
        """
        white_moves_available = any(self.get_valid_moves(piece) for line in self.board for piece in line if piece and piece.color == WHITE)
        black_moves_available = any(self.get_valid_moves(piece) for line in self.board for piece in line if piece and piece.color == BLACK)
    
        if self.white_pieces_left <= 0 or (self.black_queens > self.white_queens and not white_moves_available):
            return BLACK
        elif self.black_pieces_left <= 0 or (self.white_queens > self.black_queens and not black_moves_available):
            return WHITE
        else:
            return None


    def get_winner(self):
        """
        Détermine le vainqueur de la partie.
    
        :return: tuple, la couleur du vainqueur (BLACK ou WHITE) ou None s'il n'y a pas encore de vainqueur.
        
        """
        if self.white_pieces_left <= 0:
            return BLACK  
        elif self.black_pieces_left <= 0:
            return WHITE 
        else:
            return None


    def get_valid_moves(self, piece):
        """
        Récupère les mouvements valides pour une pièce donnée.

        :param piece: Piece, la pièce pour laquelle calculer les mouvements valides.
        
        :return: dict, les mouvements valides sous la forme {(ligne, colonne): [pièces à sauter]}.
        
        """
        valid_moves = {}
        if piece.color == WHITE or piece.is_queen:
            for step, move_left in [(1, True), (1, False), (-1, True), (-1, False)]:
                valid_moves.update(self.get_diagonal_moves(piece.line - step, -step, max(piece.line - step - 2, -1), piece.color, piece.col - 1, piece.col + 1, move_left))
        if piece.color == BLACK or piece.is_queen:
            for step, move_left in [(-1, True), (-1, False), (1, True), (1, False)]:
                valid_moves.update(self.get_diagonal_moves(piece.line + step, step, min(piece.line + step + 2, BOARD_LINES), piece.color, piece.col - 1, piece.col + 1, move_left))
        return valid_moves


    def get_diagonal_moves(self, start_line, step, stop_line, color, left_col, right_col, move_left, jump=[]):
        """
        Récupère les mouvements en diagonale pour une pièce donnée.

        :param start_line: int, la ligne de départ pour chercher les mouvements diagonaux.
        :param step: int, le pas pour se déplacer en diagonale.
        :param stop_line: int, la ligne d'arrêt pour chercher les mouvements diagonaux.
        :param color: tuple, la couleur de la pièce (BLACK ou WHITE).
        :param left_col: int, la colonne de gauche pour chercher les mouvements diagonaux.
        :param right_col: int, la colonne de droite pour chercher les mouvements diagonaux.
        :param move_left: bool, True pour chercher les mouvements à gauche, False pour chercher les mouvements à droite.
        :param jump: list, les pièces déjà sautées lors de la recherche de mouvements.
        
        :return: dict, les mouvements diagonaux sous la forme {(ligne, colonne): [pièces à sauter]}.
    
        """
        diagonal_moves = {}
        last = []
        for line in range(start_line, stop_line, step):
            if move_left:
                if left_col < 0:
                    break
                current = self.board[line][left_col]
            else:
                if right_col >= BOARD_COLS:
                    break
                current = self.board[line][right_col]
            diagonal_moves, last, stop_iteration = self.process_current_position(diagonal_moves, current, last, jump, line, left_col, right_col, step, color, move_left)
            if stop_iteration:
                break
            if move_left:
                left_col -= 1
            else:
                right_col += 1
        return diagonal_moves


    def process_current_position(self, diagonal_moves, current, last, jump, line, left_col, right_col, step, color, move_left):
        """
        Traite la position actuelle pour calculer les mouvements diagonaux.

        :param diagonal_moves: dict, les mouvements diagonaux trouvés jusqu'à présent.
        :param current: Piece, la pièce à la position actuelle ou 0 si la case est vide.
        :param last: list, la dernière pièce rencontrée lors de la recherche de mouvements diagonaux.
        :param skipped: list, les pièces déjà sautées lors de la recherche de mouvements.
        :param line: int, la ligne de la position actuelle.
        :param left_col: int, la colonne de gauche pour chercher les mouvements diagonaux.
        :param right_col: int, la colonne de droite pour chercher les mouvements diagonaux.
        :param step: int, le pas pour se déplacer en diagonale.
        :param color: tuple, la couleur de la pièce (BLACK ou WHITE).
        :param move_left: bool, True pour chercher les mouvements à gauche, False pour chercher les mouvements à droite.
        
        :return: tuple, (diagonal_moves, last, stop_iteration) où diagonal_moves est un dictionnaire des mouvements diagonaux,
                 last est la dernière pièce rencontrée, et stop_iteration est un booléen indiquant si la recherche doit s'arrêter.
             
        """
        stop_iteration = False
        if current == 0:
            diagonal_moves, last = self.handle_empty_position(diagonal_moves, current, last, jump, line, left_col, right_col, step, color, move_left)
            stop_iteration = not last
        elif current.color == color:
            stop_iteration = True
        else:
            last = [current]
        return diagonal_moves, last, stop_iteration


    def handle_empty_position(self, diagonal_moves, current, last, jump, line, left_col, right_col, step, color, move_left):
        """
        Traite la position vide pour calculer les mouvements diagonaux.

        :param diagonal_moves: dict, les mouvements diagonaux trouvés jusqu'à présent.
        :param current: Piece, la pièce à la position actuelle ou 0 si la case est vide.
        :param last: list, la dernière pièce rencontrée lors de la recherche de mouvements diagonaux.
        :param skipped: list, les pièces déjà sautées lors de la recherche de mouvements.
        :param line: int, la ligne de la position actuelle.
        :param left_col: int, la colonne de gauche pour chercher les mouvements diagonaux.
        :param right_col: int, la colonne de droite pour chercher les mouvements diagonaux.
        :param step: int, le pas pour se déplacer en diagonale.
        :param color: tuple, la couleur de la pièce (BLACK ou WHITE).
        :param move_left: bool, True pour chercher les mouvements à gauche, False pour chercher les mouvements à droite.
        
        :return: tuple, (diagonal_moves, last) où diagonal_moves est un dictionnaire des mouvements diagonaux et last est la dernière pièce rencontrée.
    
        """
        if jump and not last:
            return diagonal_moves, None
        elif jump:
            if move_left:
                diagonal_moves[(line, left_col)] = last + jump
            else:
                diagonal_moves[(line, right_col)] = last + jump
        else:
            if move_left:
                diagonal_moves[(line, left_col)] = last
            else:
                diagonal_moves[(line, right_col)] = last
        if last:
            if step == -1:
                row_limit = max(line - 3, 0)
            else:
                row_limit = min(line + 3, BOARD_LINES)
            for next_step, next_move_left in [(1, True), (1, False), (-1, True), (-1, False)]:
                diagonal_moves.update(self.get_diagonal_moves(line + step, next_step, row_limit, color, left_col + (next_move_left * 2 - 1), right_col + (next_move_left * 2 - 1), next_move_left, jump = last))

        return diagonal_moves, last

    
# --------------------------------------------------------------------------- CLASSE PARTIE ---------------------------------------------------------------------------
class Partie:
    """
    Classe représentant une partie du jeu, gérant la logique du jeu, les tours, les mouvements valides et la sélection des pièces.
    
    """

    def __init__(self, window):
        """
        Initialise une nouvelle partie.

        :param window: Surface, la fenêtre Pygame où la partie sera dessinée.
        
        """
        self.selected_piece = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.window = window


    def get_winner(self):
        """
        Récupère le gagnant de la partie.

        :return: tuple, la couleur du gagnant (BLACK ou WHITE) ou None s'il n'y a pas encore de gagnant.
        
        """
        return self.board.get_winner()


    def select_piece(self, line, col):
        """
        Sélectionne une pièce à la position donnée (ligne, colonne) si elle est valide.

        :param line: int, la ligne où se trouve la pièce à sélectionner.
        :param col: int, la colonne où se trouve la pièce à sélectionner.
        
        :return: bool, True si la sélection a réussi, False sinon.
        
        """
        if self.selected_piece and (line, col) in self.valid_moves:
            self.board.move_piece(self.selected_piece,line, col)
            jump = self.valid_moves[(line, col)]
            if jump:
                self.board.remove_pieces(jump)
            self.selected_piece = None
            self.valid_moves = {}
            self.turn = WHITE if self.turn == BLACK else BLACK
        else:
            piece = self.board.get_piece_at(line, col)
            if piece != 0 and piece.color == self.turn:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        return False
    

    def draw_valid_moves(self, moves):
        """
        Dessine les mouvements valides sur la fenêtre Pygame.

        :param moves: dict, les mouvements valides à dessiner.
        
        """
        for move in moves:
            x, y = move
            start_x = y * SQUARE_SIZE
            start_y = x * SQUARE_SIZE
            end_x = start_x + SQUARE_SIZE
            end_y = start_y + SQUARE_SIZE
            pygame.draw.rect(self.window, (0, 255, 0), (start_x, start_y, SQUARE_SIZE, SQUARE_SIZE), 5)

            
# --------------------------------------------------------------------------- IA ---------------------------------------------------------------------------
def alpha_beta_search(position, depth, alpha, beta, max_player, game):
    """
    Effectue une recherche alpha-bêta pour déterminer le meilleur mouvement à partir de la position actuelle.

    :param position: Board, la position actuelle du plateau.
    :param depth: int, la profondeur de recherche dans l'arbre des mouvements.
    :param alpha: float, la borne inférieure de la recherche.
    :param beta: float, la borne supérieure de la recherche.
    :param max_player: bool, True si le joueur actuel est le joueur maximisant, False sinon.
    :param game: Partie, l'instance du jeu en cours.
    
    :return: tuple, le score du meilleur mouvement et le plateau correspondant.
    
    """
    if depth == 0 or position.get_winner() != None:
        black_score = position.black_pieces_left + (position.black_queens * 5)
        white_score = position.white_pieces_left + (position.white_queens * 5)
        return black_score - white_score, position
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, False, game)
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, True, game)
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def minimax(position, depth, alpha, beta, max_player, game):
    """
    Implémente l'algorithme Minimax avec élagage alpha-bêta.

    :param position: Board, la position actuelle du plateau.
    :param depth: int, la profondeur de recherche dans l'arbre des mouvements.
    :param alpha: float, la borne inférieure de la recherche.
    :param beta: float, la borne supérieure de la recherche.
    :param max_player: bool, True si le joueur actuel est le joueur maximisant, False sinon.
    :param game: Partie, l'instance du jeu en cours.
    
    :return: tuple, le score du meilleur mouvement et le plateau correspondant.
    
    """
    if max_player:
        return alpha_beta_search(position, depth, alpha, beta, True, game)
    else:
        return -alpha_beta_search(position, depth, -beta, -alpha, False, game)[0], None


def get_all_moves(board, color, game):
    """
    Génère tous les mouvements possibles pour une couleur donnée sur un plateau donné.

    :param board: Board, le plateau à analyser.
    :param color: tuple, la couleur des pièces pour lesquelles les mouvements doivent être générés (WHITE ou BLACK).
    :param game: Partie, l'instance du jeu en cours.
    
    :return: list, la liste des nouveaux plateaux après chaque mouvement valide.
    
    """
    all_moves = []
    for line in board.board:
        for piece in line:
            if piece and piece.color == color:
                valid_moves = board.get_valid_moves(piece)
                for move, jump in valid_moves.items():
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece_at(piece.line, piece.col)
                    temp_board.move_piece(temp_piece, move[0], move[1])
                    if jump:
                        temp_board.remove_pieces(jump)
                    new_board = temp_board
                    all_moves.append(new_board)
                    if jump:  # Si le mouvement saute sur une pièce ennemie, arrête de vérifier les mouvements de cette pièce
                        break
    return all_moves


def alpha_beta_search_2player(position, depth, alpha, beta, max_player, game, color):
    """
    Effectue une recherche alpha-bêta pour un jeu à deux joueurs à partir de la position actuelle.

    :param position: Board, la position actuelle du plateau.
    :param depth: int, la profondeur de recherche dans l'arbre des mouvements.
    :param alpha: float, la borne inférieure de la recherche.
    :param beta: float, la borne supérieure de la recherche.
    :param max_player: bool, True si le joueur actuel est le joueur maximisant, False sinon.
    :param game: Partie, l'instance du jeu en cours.
    :param color: tuple, la couleur du joueur actuel (WHITE ou BLACK).
    
    :return: tuple, le score du meilleur mouvement et le plateau correspondant.
    
    """
    if color == WHITE:
        if depth == 0 or position.get_winner() != None:
            white_score = position.white_pieces_left + (position.white_queens * 0.5)
            black_score = position.black_pieces_left + (position.black_queens * 0.5)
            return white_score - black_score, position
        if max_player:
            max_eval = float('-inf')
            best_move = None
            for move in get_all_moves(position, WHITE, game):
                evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, False, game)      
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break    
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in get_all_moves(position, BLACK, game):
                evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, True, game)
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break   
            return min_eval, best_move
    else:
        if depth == 0 or position.get_winner() != None:
            white_score = position.white_pieces_left + (position.white_queens * 0.5)
            black_score = position.black_pieces_left + (position.black_queens * 0.5)
            return black_score - white_score, position
        if max_player:
            max_eval = float('-inf')
            best_move = None
            for move in get_all_moves(position, BLACK, game):
                evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, False, game)
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in get_all_moves(position, WHITE, game):
                evaluation, _ = alpha_beta_search(move, depth-1, alpha, beta, True, game)
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

        
# --------------------------------------------------------------------------- PARTIE MAIN ---------------------------------------------------------------------------
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jeu de Dames')
get_coord = lambda pos: (pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE)

def main():
    """
    Fonction principale du programme, gère le déroulement du jeu de dames, les actions de l'utilisateur et les actions de l'IA.
    
    """
    partie = Partie(WINDOW)
    player1, player2, vs_ai, ai_level_1, ai_level_2, vs_ai_level, ia_vs_ia = get_game_settings()
    run1 = True

    while run1:
        if ia_vs_ia:
            if partie.turn == WHITE:
                if ai_level_1 == 1:
                    depth = 3
                elif ai_level_1 == 2:
                    depth = 4
                else:
                    depth = 5
                value, new_board = alpha_beta_search_2player(partie.board, depth, float('-inf'), float('inf'), True, partie, WHITE)
                partie.board = new_board
                partie.valid_moves = {}
                partie.turn = WHITE if partie.turn == BLACK else BLACK
            else:
                if ai_level_2 == 1:
                    depth = 3
                elif ai_level_2 == 2:
                    depth = 4
                else:
                    depth = 5
                value, new_board = alpha_beta_search_2player(partie.board, depth, float('-inf'), float('inf'), True, partie, BLACK)
                partie.board = new_board
                partie.valid_moves = {}
                partie.turn = WHITE if partie.turn == BLACK else BLACK
        if partie.turn == BLACK and vs_ai:
            if vs_ai_level == 1:
                depth = 3
            elif vs_ai_level == 2:
                depth = 4 
            else:
                depth = 5
            value, new_board = minimax(partie.board, depth, float('-inf'), float('inf'), True, partie)
            partie.board = new_board
            partie.valid_moves = {}
            partie.turn = BLACK if partie.turn == WHITE else WHITE
        elif partie.turn == BLACK and not vs_ai:
            run = handle_mouse_input(partie)
        elif partie.turn == WHITE:
            run = handle_mouse_input(partie)
        partie.board.draw(partie.window)
        partie.draw_valid_moves(partie.valid_moves)
        pygame.display.update()
    pygame.quit()


def get_game_settings():
    """
    Demande à l'utilisateur les paramètres de la partie et récupère les choix du joueur concernant le type de partie et le niveau de difficulté de l'IA.

    :return: tuple, contenant les paramètres de la partie : noms des joueurs, type de partie, niveaux de difficulté de l'IA.
    
    """
    vs_ai = False
    ia_vs_ia = False
    vs_ai_level = 1
    ai_level_1 = 1
    ai_level_2 = 1
    player1 = ""
    player2 = ""

    while True:
        choix = input("\n Choisissez une des options suivantes :\n\n - Jouer contre l'ordinateur : tapez 'o'\n - Jouer avec un autre humain : tapez 'n'\n - Faire jouer deux IA ensemble : tapez 'ia'\n\n Quel est votre choix ? ")
        if choix.lower() == 'o':
            vs_ai = True
            while True:
                vs_ai_level_input = input("\n Veuillez choisir le niveau de difficulté de la partie :\n\n - Facile : tapez (1)\n - Intermédiaire : tapez (2)\n - Difficile : tapez (3)\n\n Quel est votre choix ? ")
                try:
                    vs_ai_level = int(vs_ai_level_input)
                    if vs_ai_level in [1, 2, 3]:
                        break
                    else:
                        print("\n Choix invalide. Veuillez saisir 1, 2 ou 3.")
                except:
                    print("\n Choix invalide. Veuillez saisir 1, 2 ou 3.")
            break
        elif choix.lower() == 'n':
            break
        elif choix.lower() == 'ia':
            ia_vs_ia = True

            while True:
                ai_level_1_input = input("\n Veuillez choisir le niveau de difficulté de la 1ère (blanc) IA :\n\n - Facile : tapez (1)\n - Intermédiaire : tapez (2)\n - Difficile : tapez (3)\n\n Quel est votre choix ? ")
                ai_level_2_input = input("\n Veuillez choisir le niveau de difficulté de la 2ème (noir) IA :\n\n - Facile : tapez (1)\n - Intermédiaire : tapez (2)\n - Difficile : tapez (3)\n\n Quel est votre choix ? ")
                try:
                    ai_level_1 = int(ai_level_1_input)
                    ai_level_2 = int(ai_level_2_input)
                    if (ai_level_1 and ai_level_2) in [1, 2, 3]:
                        break
                    else:
                        print("\n Choix invalide. Veuillez saisir 1, 2 ou 3.")
                except:
                    print("\n Choix invalide. Veuillez saisir 1, 2 ou 3.")
            break  
        else:
            print("\n Choix invalide. Veuillez saisir 'O' ou 'N' ou 'IA'.")
    if not (vs_ai or ia_vs_ia):
        player1 = input("\n Nom du joueur 1 : ")
        player2 = input(" Nom du joueur 2 : ")
    return player1, player2, vs_ai, ai_level_1, ai_level_2, vs_ai_level, ia_vs_ia


def handle_mouse_input(partie):
    """
    Gère les événements liés à la souris (clics) pour sélectionner et déplacer les pièces.

    :param partie: Partie, l'instance du jeu en cours.
    :return: bool, True si le jeu doit continuer à tourner, False sinon (si l'utilisateur a quitté la fenêtre).
    
    """
    run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            line, col = get_coord(pos)
            partie.select_piece(line,col)
    return run


main()
