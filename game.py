import sys
import pygame
from constants import SQUARESIZE, PLAYER_PIECE, AI_PIECE
from game_logic import create_board, is_valid_location, get_next_open_row, drop_piece, winning_move
from ai import get_ai_move
from interface import draw_board

def handle_player_turn(board, col, piece, game_screen):
    """Gère le tour du joueur et vérifie s'il gagne."""
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)
        draw_board(board, game_screen)
        return winning_move(board, piece)
    return False

def run_game(game_mode, difficulty, font, game_screen):
    """Exécute une partie complète de Puissance 4."""
    board = create_board()
    draw_board(board, game_screen)

    game_over = False
    turn = 0
    winner_message = ""

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARESIZE  # Conversion en colonne
                if turn == 0:  # Joueur 1
                    if handle_player_turn(board, col, PLAYER_PIECE, game_screen):
                        winner_message = "Joueur 1 gagne!"
                        game_over = True
                elif turn == 1 and game_mode == "pvp":  # Joueur 2
                    if handle_player_turn(board, col, AI_PIECE, game_screen):
                        winner_message = "Joueur 2 gagne!"
                        game_over = True
                if not game_over:
                    turn = (turn + 1) % 2  # Changer de tour

        # Tour de l'IA (si en mode PvAI)
        if game_mode == "pvai" and turn == 1 and not game_over:
            pygame.time.wait(500)  # Pause pour lisibilité
            col = get_ai_move(board, difficulty)
            if handle_player_turn(board, col, AI_PIECE, game_screen):
                winner_message = "L'IA gagne!"
                game_over = True
            if not game_over:
                turn = (turn + 1) % 2

    return winner_message
