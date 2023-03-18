import pygame

# constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def minimax( pos, depth, max_player, jeu ):
    if depth == 0 or jeu.game_over():
        return jeu.evaluate(), pos
    
    # Maximiser le score
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in jeu.get_valid_moves():
            evaluation = minimax( move, depth - 1, False, jeu )[0]
            max_eval = max( max_eval, evaluation )
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move

    # Minimiser le score
    else: 
        min_eval = float('inf')
        best_move = None
        for move in jeu.get_valid_moves():
            evaluation = minimax( move, depth - 1, True, jeu )[0]
            min_eval = min( min_eval, evaluation )
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move