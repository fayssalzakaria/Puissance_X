import pygame
from interface import get_game_mode, get_difficulty, display_end_screen
from game import run_game  # On importe maintenant `run_game` depuis game.py

def main():
    """Gère le menu et le lancement du jeu."""
    pygame.init()
    font_menu = pygame.font.SysFont("Arial", 36)
    font = pygame.font.SysFont("Arial", 40)

    while True:
        # Affichage du menu
        menu_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Puissance 4 - Menu")
        game_mode = get_game_mode(menu_screen, font_menu)
        difficulty = get_difficulty(menu_screen, font_menu) if game_mode == "pvai" else None

        # Lancement du jeu
        game_screen = pygame.display.set_mode((700, 700))  # Adapter à ton plateau
        winner_message = run_game(game_mode, difficulty, font, game_screen)

        # Affichage de l'écran de fin avec possibilité de rejouer
        while True:
            result = display_end_screen(game_screen, font, winner_message)
            if result == "menu":
                break  # Retour au menu principal
            elif result == "replay":
                winner_message = run_game(game_mode, difficulty, font, game_screen)

if __name__ == "__main__":
    main()
