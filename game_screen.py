import pygame
from constants import *
import numpy as np
from game_logic import *
from ai import *
from interface import Button, Label

class GameScreen:
    """Classe gérant l'affichage du jeu, les interactions avec la grille, et les tours de jeu"""

    def __init__(self, rows, cols, win_condition, difficulty, difficulty2, return_to_menu_callback, starting_player):
        """
        Initialise l'écran de jeu avec la configuration de la grille et les paramètres du jeu.

        Args:
            rows (int): Nombre de lignes du plateau.
            cols (int): Nombre de colonnes du plateau.
            win_condition (int): Nombre de pions alignés nécessaires pour gagner.
            difficulty (str): Difficulté de l'IA (si présente).
            difficulty2 (str): Difficulté de la deuxième IA (pour mode IA vs IA).
            return_to_menu_callback (function): Fonction pour retourner au menu principal.
            starting_player (int): Joueur qui commence (1 pour l'humain, 2 pour IA).
        """
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition
        self.difficulty = difficulty
        self.difficulty2 = difficulty2  # Nouvelle difficulté pour l'IA 2 (si besoin)
        self.return_to_menu_callback = return_to_menu_callback

        self.grid = np.zeros((rows, cols))
        self.game_over = False
        self.turn = starting_player
        self.winner = None
        self.is_paused = False  # Variable pour indiquer si le jeu est en pause

        self.cell_size = min((BASE_WIDTH - 100) // self.cols, (BASE_HEIGHT - 100) // self.rows)

        # Boutons pour l'écran de fin et le menu pause
        self.replay_button = Button((0.4, 0.6), (0.2, 0.1), "Rejouer", self.reset_game)
        self.menu_button = Button((0.4, 0.8), (0.2, 0.1), "Menu Principal", self.return_to_menu_callback)
        self.resume_button = Button((0.4, 0.45), (0.2, 0.1), "Reprendre", self.toggle_pause)

        # Création des labels pour les écrans de pause et de fin de jeu
        self.pause_label = Label((0.375, 0.15), "Jeu en Pause", TITLE_FONT, relative=True)
        self.winner_label = Label((0.375, 0.25), "", TITLE_FONT, relative=True)

        # Si mode IA vs IA, programmer le premier coup automatiquement
        if self.difficulty2 is not None:
            pygame.time.set_timer(AI_MOVE_EVENT, AI_DELAY)

        # Si l'IA doit commencer (dans n'importe quel mode)
        if self.turn == 2:
            pygame.time.set_timer(AI_MOVE_EVENT, AI_DELAY)

    def handle_event(self, event):
        """
        Gère les événements liés au clavier, à la souris et à l'IA.

        Args:
            event (pygame.Event): Événement capturé par Pygame.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()

        if self.is_paused:
            self.resume_button.handle_event(event)
            self.replay_button.handle_event(event)
            self.menu_button.handle_event(event)
            return

        if self.game_over:
            self.replay_button.handle_event(event)
            self.menu_button.handle_event(event)
            return

        # Seulement pour le mode Joueur vs IA
        if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 1 and self.difficulty2 is None:
            posx = event.pos[0]
            start_x = (pygame.display.get_surface().get_width() - self.cols * self.cell_size) // 2
            col = int((posx - start_x) // self.cell_size)

            if 0 <= col < self.cols and is_valid_location(self.grid, col):
                row = get_next_open_row(self.grid, col)
                drop_piece(self.grid, row, col, PLAYER_PIECE)

                if winning_move(self.grid, PLAYER_PIECE, self.win_condition):
                    self.game_over = True
                    self.winner = "Le Joueur gagne !"
                elif np.all(self.grid != 0):
                    self.game_over = True
                    self.winner = "Match nul !"
                    return

                self.turn = 2
                pygame.time.set_timer(AI_MOVE_EVENT, AI_DELAY)

        if event.type == AI_MOVE_EVENT:
            pygame.time.set_timer(AI_MOVE_EVENT, 0)
            self.ai_move()

    def ai_move(self):
        """
        Exécute un coup pour l'IA en fonction de la difficulté définie.
        """
        if not self.game_over:
            if self.difficulty2 is None:
                current_difficulty = self.difficulty  # Mode Joueur vs IA
            else:
                current_difficulty = self.difficulty if self.turn == 1 else self.difficulty2
            col = get_ai_move(self.grid, current_difficulty, self.win_condition)

            if is_valid_location(self.grid, col):
                row = get_next_open_row(self.grid, col)
                piece = self.turn

                drop_piece(self.grid, row, col, piece)

                if winning_move(self.grid, piece, self.win_condition):
                    self.game_over = True
                    if self.difficulty2:  # Mode IA vs IA
                        self.winner = f"IA {self.turn} gagne !"
                    else:  # Mode Joueur vs IA
                        self.winner = "L'IA gagne !"
                elif np.all(self.grid != 0):
                    self.game_over = True
                    self.winner = "Match nul !"
                    return

                self.turn = 2 if self.turn == 1 else 1

                if self.difficulty2 is not None and not self.game_over:
                    pygame.time.set_timer(AI_MOVE_EVENT, AI_DELAY)

    def toggle_pause(self):
        """Bascule entre l'état de pause et l'état de jeu"""
        self.is_paused = not self.is_paused

    def draw_overlay(self, screen, alpha=100):
        """
        Dessine un overlay semi-transparent par-dessus l'écran pour simuler l'opacité.

        Args:
            screen (pygame.Surface): Surface d'affichage.
            alpha (int): Valeur de transparence (0 à 255).
        """
        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        overlay.fill((0, 0, 0))  # Remplir d'une couleur noire
        overlay.set_alpha(alpha)  # Appliquer la transparence
        screen.blit(overlay, (0, 0))  # Dessiner l'overlay sur l'écran

    def draw(self, screen):
        """
        Affiche le plateau de jeu et les éléments d'interface selon l'état (jeu, pause ou fin).

        Args:
            screen (pygame.Surface): Surface d'affichage.
        """
        screen.fill(BLACK)

        # Appliquer un overlay si le jeu est en pause ou en fin de partie
        if self.is_paused or self.game_over:
            self.draw_overlay(screen, alpha=150)  # Un alpha plus élevé pour l'écran de fin ou pause

        start_x = (screen.get_width() - self.cols * self.cell_size) // 2
        start_y = (screen.get_height() - self.rows * self.cell_size) // 2

        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    start_x + col * self.cell_size,
                    start_y + row * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, BLUE, rect, 2)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == PLAYER_PIECE:
                    pygame.draw.circle(screen, RED, 
                                       (start_x + col * self.cell_size + self.cell_size // 2, 
                                        start_y + row * self.cell_size + self.cell_size // 2), 
                                       self.cell_size // 2 - 5)
                elif self.grid[row][col] == AI_PIECE:
                    pygame.draw.circle(screen, YELLOW, 
                                       (start_x + col * self.cell_size + self.cell_size // 2, 
                                        start_y + row * self.cell_size + self.cell_size // 2), 
                                       self.cell_size // 2 - 5)

        if self.game_over:
            self.draw_end_screen(screen)
        elif self.is_paused:
            self.draw_pause_screen(screen)

        pygame.display.update()

    def draw_end_screen(self, screen):
        """
        Affiche l'écran de fin avec le gagnant et les options de redémarrage/menu.

        Args:
            screen (pygame.Surface): Surface d'affichage.
        """
        # Dessiner un overlay semi-transparent pour améliorer la lisibilité
        self.draw_overlay(screen, alpha=120)
        self.winner_label.set_text(self.winner)

        self.winner_label.draw(screen)
        
        # Dessiner les boutons Rejouer et Retourner au Menu
        self.replay_button.draw(screen)
        self.menu_button.draw(screen)

    def draw_pause_screen(self, screen):
        """Affiche l'écran de pause avec les boutons pour reprendre ou revenir au menu"""
        # Dessiner un overlay semi-transparent pour améliorer la lisibilité
        self.draw_overlay(screen, alpha=120)
        
        self.pause_label.draw(screen)

        # S'assurer que le bouton "Reprendre" est visible et interactif pendant la pause
        self.resume_button.visible = True  # Le rendre visible quand en pause
        self.resume_button.draw(screen)

        # Dessiner les boutons Rejouer et Retourner au Menu
        self.replay_button.draw(screen)
        self.menu_button.draw(screen)

    def reset_game(self):
        """Réinitialise la partie"""
        self.grid = np.zeros((self.rows, self.cols))
        self.game_over = False
        self.turn = 1
        self.winner = None
        self.is_paused = False  # Réinitialiser l'état de pause lorsque le jeu est réinitialisé