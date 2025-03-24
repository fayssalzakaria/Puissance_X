import math
import numpy as np
from game_logic import is_valid_location, get_next_open_row, drop_piece, winning_move
from constants import ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH, PLAYER_PIECE, AI_PIECE

def evaluate_window(window, piece):
    """Évalue une fenêtre de 4 cases en fonction de la présence de jetons du joueur ou de l'IA.

    Args:
        window (list): Une fenêtre de 4 cases à évaluer.
        piece (int): La pièce pour laquelle on évalue la fenêtre (IA ou joueur).

    Returns:
        int: Le score de la fenêtre, positif si favorable pour la pièce, négatif si favorable pour l'adversaire.
    """
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # Score élevé pour 4 jetons alignés de la même couleur
    if window.count(piece) == 4:
        score += 100000
    # Score élevé pour 3 jetons alignés avec un emplacement vide
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 1000
    # Score modéré pour 2 jetons alignés avec deux emplacements vides
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 50

    # Pénalisation pour les configurations adverses
    if window.count(opp_piece) == 4:
        score -= 100000
    elif window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 1200  # Pénalisation plus forte pour une menace immédiate
    elif window.count(opp_piece) == 2 and window.count(0) == 2:
        score -= 50

    return score

def score_position(board, piece):
    """Évalue la position globale sur le plateau en tenant compte du contrôle du centre et des alignements sur toutes les directions (horizontale, verticale, diagonale).

    Args:
        board (ndarray): Le plateau de jeu sous forme de matrice (rows x columns).
        piece (int): La pièce à évaluer (IA ou joueur).

    Returns:
        int: Le score global pour la pièce donnée sur le plateau.
    """
    score = 0

    # Prioriser le contrôle du centre (cette zone est plus stratégique)
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 8  # Pondération plus forte pour le centre du plateau

    # Vérification horizontale
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vérification verticale
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vérification des diagonales positives (de bas à gauche à haut à droite)
    for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Vérification des diagonales négatives (de bas à droite à haut à gauche)
    for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):
    """Retourne une liste des colonnes où un coup est possible (i.e., où il y a de l'espace dans la colonne).

    Args:
        board (ndarray): Le plateau de jeu sous forme de matrice (rows x columns).

    Returns:
        list: Liste des indices des colonnes valides où il est possible de jouer.
    """
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
    """Algorithme Minimax avec élagage alpha-bêta pour déterminer le meilleur coup à jouer.

    Args:
        board (ndarray): Le plateau de jeu.
        depth (int): La profondeur de recherche pour l'algorithme.
        alpha (int): La valeur alpha pour l'élagage alpha-bêta.
        beta (int): La valeur bêta pour l'élagage alpha-bêta.
        maximizingPlayer (bool): Indique si c'est le tour du joueur maximisant ou minimisant.

    Returns:
        tuple: La colonne choisie et la valeur d'évaluation associée au coup.
    """
    valid_locations = get_valid_locations(board)
    terminal = winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(valid_locations) == 0

    # Si on atteint la profondeur maximale ou que la partie est terminée, on retourne le score
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000)  # L'IA gagne
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000)  # Le joueur gagne
            else:
                return (None, 0)  # Match nul
        return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Élagage bêta
        return best_col, value

    else:
        value = math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Élagage alpha
        return best_col, value

def get_ai_move(board, difficulty):
    """Retourne le meilleur coup pour l'IA en fonction de la difficulté.

    Args:
        board (ndarray): Le plateau de jeu.
        difficulty (str): La difficulté choisie ('easy', 'medium', 'hard').

    Returns:
        int: La colonne où l'IA devrait jouer.
    """
    # Définir la profondeur de recherche selon la difficulté
    difficulty_depth = {
        'easy': 1,
        'medium': 3,
        'hard': 5  
    }
    depth = difficulty_depth.get(difficulty, 4)

    # Vérifier si l'IA peut gagner immédiatement
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, AI_PIECE)
        if winning_move(temp_board, AI_PIECE):
            return col

    # Vérifier si le joueur peut gagner au prochain coup et bloquer
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, PLAYER_PIECE)
        if winning_move(temp_board, PLAYER_PIECE):
            return col

    # Si aucune victoire ou blocage immédiat, utiliser l'algorithme Minimax pour choisir le meilleur coup
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col
