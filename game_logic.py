import numpy as np

def create_board(rows, cols):
    """
    Crée un plateau de jeu vide.

    Args:
        rows (int): Nombre de lignes.
        cols (int): Nombre de colonnes.

    Returns:
        ndarray: Plateau de jeu initialisé à 0.
    """
    return np.zeros((rows, cols))  # Crée un plateau de jeu vide (rempli de 0) de dimensions (rows * cols, défini dans la classe SettingsScreen)

def is_valid_location(board, col):
    """
    Vérifie si une colonne est jouable (c'est-à-dire que la première case en haut est vide).

    Args:
        board (ndarray): Plateau de jeu.
        col (int): Colonne à vérifier.

    Returns:
        bool: True si la colonne est valide, False sinon.
    """
    return board[0][col] == 0  # Vérifie si la case du haut est vide

def get_next_open_row(board, col):
    """
    POUR l'IA : Trouver la prochaine ligne vide dans une colonne.

    Args:
        board (ndarray): Plateau de jeu.
        col (int): Colonne où chercher.

    Returns:
        int: Index de la première ligne libre en partant du bas.
    """
    for r in range(len(board)-1, -1, -1):  # Parcourt les lignes de bas en haut
        if board[r][col] == 0:  # Chercher la première case vide
            return r  # Retourne l'index de la ligne vide

def drop_piece(board, row, col, piece):
    """
    Déposer un pion dans une colonne.

    Args:
        board (ndarray): Plateau de jeu.
        row (int): Ligne cible.
        col (int): Colonne cible.
        piece (int): Valeur représentant le joueur (ex: 1 pour humain, 2 pour IA).
    """
    board[row][col] = piece  # Place la pièce (dépend du joueur 1 (humain) ou 2 (IA)) à l'endroit spécifié

def winning_move(board, piece, win_condition=4):
    """
    Vérifie si un joueur a gagné en alignant 'win_condition' pions.

    Args:
        board (ndarray): Plateau de jeu.
        piece (int): Pièce du joueur à vérifier.
        win_condition (int): Nombre de pièces alignées nécessaires pour gagner.

    Returns:
        bool: True si une condition de victoire est remplie, False sinon.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    # Vérifie les victoires horizontales
    for r in range(rows):
        for c in range(cols - (win_condition - 1)):
            if all(board[r][c+i] == piece for i in range(win_condition)):
                return True
            
    # Vérifie les victoires verticales
    for r in range(rows - (win_condition - 1)):
        for c in range(cols):
            if all(board[r+i][c] == piece for i in range(win_condition)):
                return True
            
    # Vérifie les victoires diagonales (haut-gauche à bas-droit)
    for r in range(rows - (win_condition - 1)):
        for c in range(cols - (win_condition - 1)):
            if all(board[r+i][c+i] == piece for i in range(win_condition)):
                return True
            
    # Vérifie les victoires diagonales (haut-droit à bas-gauche)
    for r in range(win_condition - 1, rows):
        for c in range(cols - (win_condition - 1)):
            if all(board[r-i][c+i] == piece for i in range(win_condition)):
                return True
                
    return False