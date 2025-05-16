import random
import numpy as np
from game_logic import (
    is_valid_location,
    get_next_open_row,
    drop_piece,
    winning_move
)
from constants import PLAYER_PIECE, AI_PIECE

def get_valid_locations(board):
    """
    Retourne la liste des colonnes valides où un coup peut encore être joué.

    Args:
        board (ndarray): Plateau de jeu.

    Returns:
        list: Indices de colonnes jouables.
    """
    return [col for col in range(board.shape[1]) if is_valid_location(board, col)]

def evaluate_window(window, piece):
    """
    Évalue un ensemble de 4 cases (une "fenêtre") pour en déterminer la valeur stratégique.

    Args:
        window (list): Liste de 4 cases (ligne, colonne ou diagonale).
        piece (int): Pièce du joueur évalué (AI_PIECE ou PLAYER_PIECE).

    Returns:
        int: Score attribué à la fenêtre.
    """
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 80  # Défense forte contre menace adverse

    return score

def score_position(board, piece):
    """
    Calcule un score global du plateau pour un joueur donné.

    Args:
        board (ndarray): Plateau de jeu.
        piece (int): Pièce du joueur.

    Returns:
        int: Score global du plateau.
    """
    score = 0
    rows, cols = board.shape

    # Contrôle central : favorise le centre du plateau
    center_col = cols // 2
    center_array = [int(board[r][center_col]) for r in range(rows)]
    score += center_array.count(piece) * 3

    # Évaluations horizontales
    for r in range(rows):
        row_array = list(board[r])
        for c in range(cols - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Évaluations verticales
    for c in range(cols):
        col_array = [board[r][c] for r in range(rows)]
        for r in range(rows - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Évaluations diagonales ↘
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Évaluations diagonales ↙
    for r in range(3, rows):
        for c in range(cols - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def simulate_move(board, row, col, piece):
    """Joue un coup de manière temporaire sur le plateau."""
    board[row][col] = piece

def undo_move(board, row, col):
    """Annule un coup précédemment simulé."""
    board[row][col] = 0

def score_simulated_move(board, col, piece):
    """
    Simule un coup dans une colonne donnée et retourne le score associé.

    Args:
        board (ndarray): Plateau de jeu.
        col (int): Colonne à simuler.
        piece (int): Pièce du joueur.

    Returns:
        int: Score du plateau après simulation.
    """
    row = get_next_open_row(board, col)
    simulate_move(board, row, col, piece)
    score = score_position(board, piece)
    undo_move(board, row, col)
    return score

def minimax(board, depth, alpha, beta, maximizing_player, win_condition):
    """
    Algorithme Minimax avec élagage alpha-bêta.

    Args:
        board (ndarray): Plateau de jeu.
        depth (int): Profondeur maximale de recherche.
        alpha (float): Meilleur score pour le joueur maximisant.
        beta (float): Meilleur score pour le joueur minimisé.
        maximizing_player (bool): True si c’est à l’IA de jouer.
        win_condition (int): Nombre de pièces alignées pour gagner.

    Returns:
        tuple: (colonne choisie, score associé)
    """
    valid_locations = get_valid_locations(board)
    is_terminal = (
        not valid_locations or 
        winning_move(board, PLAYER_PIECE, win_condition) or 
        winning_move(board, AI_PIECE, win_condition)
    )

    if depth == 0 or is_terminal:
        if winning_move(board, AI_PIECE, win_condition):
            return (None, float("inf"))
        elif winning_move(board, PLAYER_PIECE, win_condition):
            return (None, float("-inf"))
        elif not valid_locations:
            return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = float("-inf")
        best_col = random.choice(valid_locations)

        # Exploration plus intelligente : les coups prometteurs en premier
        valid_locations.sort(key=lambda col: score_simulated_move(board, col, AI_PIECE), reverse=True)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            simulate_move(board, row, col, AI_PIECE)
            _, new_score = minimax(board, depth - 1, alpha, beta, False, win_condition)
            undo_move(board, row, col)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Élagage beta
        return best_col, value

    else:
        value = float("inf")
        best_col = random.choice(valid_locations)

        valid_locations.sort(key=lambda col: score_simulated_move(board, col, PLAYER_PIECE))

        for col in valid_locations:
            row = get_next_open_row(board, col)
            simulate_move(board, row, col, PLAYER_PIECE)
            _, new_score = minimax(board, depth - 1, alpha, beta, True, win_condition)
            undo_move(board, row, col)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Élagage alpha
        return best_col, value

def get_ai_move(board, difficulty, win_condition=4):
    """
    Calcule le meilleur coup à jouer selon le niveau de difficulté.

    Args:
        board (ndarray): Plateau de jeu.
        difficulty (str): "easy", "medium", ou "hard".
        win_condition (int): Nombre de pièces alignées pour gagner.

    Returns:
        int or None: Colonne choisie pour le coup de l'IA, ou None si aucune possible.
    """
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return None

    # Vérifie s'il existe un coup gagnant immédiat
    for col in valid_locations:
        row = get_next_open_row(board, col)
        simulate_move(board, row, col, AI_PIECE)
        if winning_move(board, AI_PIECE, win_condition):
            undo_move(board, row, col)
            return col
        undo_move(board, row, col)

    # Détermine la profondeur de recherche selon la difficulté
    depth = {"easy":0, "medium":3 , "hard": 4}.get(difficulty, 2)

    try:
        best_col, _ = minimax(board, depth, float("-inf"), float("inf"), True, win_condition)
        return best_col if best_col in valid_locations else random.choice(valid_locations)
    except Exception as e:
        print(f"Erreur dans l'IA : {e}")
        return random.choice(valid_locations)