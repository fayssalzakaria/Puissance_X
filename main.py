import pygame
from menu.main_menu import MainMenu
from settings.constants import *
from settings.settings_screen import SettingsScreen
from game.game_screen import GameScreen
from ui.credits_screen import CreditsScreen

class Game:
    """
    Classe principale qui gère tout le cycle de vie du jeu, y compris l'affichage, les évènements
    et les transitions entre les scènes.

    Elle gère :
    - L'initialisation de Pygame
    - La boucle principale du jeu
    - Le changement d'écrans (menu, paramètres, jeu)
    - La communication entre les composants principaux (MainMenu, SettingsScreen, GameScreen)
    """

    def __init__(self):
        """Initialise le jeu, les écrans, la fenêtre d'affichage et les paramètres par défaut."""
        pygame.init()
        self.running = True # Indique si le jeu est en cours d'execution
        self.fullscreen = False # Indique si le jeu est en plein écran
        self.current_screen_size = (BASE_WIDTH, BASE_HEIGHT) # Taille de la fenêtre du jeu (en pixel)
        self.screen = pygame.display.set_mode(self.current_screen_size) # Fenêtre redimensionnable
        pygame.display.set_caption("Puissance X") # Titre du jeu 
        
        self.clock = pygame.time.Clock() # Contrôle le framerate pour éviter les latences
        self.current_screen = "menu" # Ecran actuelle (menu principal au lancement)
        self.game_mode = None # Mode de jeu actuel
        
        # Initialisation des écrans
        self.main_menu = MainMenu(self.show_settings_screen, self.show_credits) # Initialisation du menu principal
        self.credits_screen = None  # Écran des crédits, à afficher via un bouton
        self.game_screen = None # Ecran du jeu (pas chargé par défaut)
        self.difficulty = "easy"  # Difficulté par défaut
    
    def show_settings_screen(self, mode: str):
        """
        Aller à l'écran de la configuration de la partie (lorsque l'on clique sur
        "Joueur vs Joueur", "Joueur vs IA" ou "Tournois IA").

        Args:
            mode (str): Le mode de jeu sélectionné ("pvp (supprimé)", "pvia", "ai_vs_ai")
        """
        self.game_mode = mode # Stock le mode de jeu séléctionné ("Joueur vs Joueur" ou "Joueur vs IA")
        self.current_screen = "settings" # changement de l'écran actuel ("configuration")
        self.settings_screen = SettingsScreen(self.start_game, self.return_to_menu, mode=mode) # Initialisation de l'écran de configuration
        print(f"Passage à l'écran des paramètres pour le mode {mode}")  # Debug
    
    def start_game(self, rows: int, cols: int, win_condition: int, difficulty: str, starting_player: int = 1, difficulty2: str=None):
        """
        Lance le jeu avec la configuration choisie par le joueur.

        Args:
            rows (int): Nombre de lignes de la grille
            cols (int): Nombre de colonnes de la grille
            win_condition (int): Nombre de pions alignés pour gagner
            difficulty (str): Difficulté de l'IA principale
            starting_player (int): Le joueur qui commence (1 ou 2), défaut = 1
            difficulty2 (str): Difficulté de la deuxième IA (en mode IA vs IA)
        """
        print(f"Démarrage du jeu {rows}x{cols}, victoire à {win_condition}, difficulté: {difficulty}, joueur qui commence: {starting_player}") #debug
        self.current_screen = "game"
        
        self.game_screen = GameScreen(rows, cols, win_condition, difficulty, difficulty2, self.return_to_menu, starting_player) # paramètre difficulty2 ajouté à la version du 08/04 pour l'instanciation

    def return_to_menu(self):
        """
        Retourne au menu principal après une partie (ou pendant par le menu pause). Réinitialise l'écran de jeu.
        """
        self.current_screen = "menu" # changement de l'écran actuel ("menu pause" ou "menu de fin de partie")
        self.game_screen = None # Réinitialise l'écran du jeu (pour une nouvelle partie)
    
    def handle_events(self):
        """
        Gère les événements sans bloquer :
        - Quitter le jeu
        - Interaction avec les boutons/menu
        - Propagation des événements à l'écran actif
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # Ferme le jeu si l'on clique sur la croix (éviter la fermeture brut)
            
            '''
            !!! Toggle plein écran (Supprimé pour éviter des conflits de responsivité) !!!
            
            elif event.type == pygame.VIDEORESIZE:
                #self.handle_resize(event.size) # Gère le redimensionnement de la fenêtre
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen() # Activer ou désactiver le plein écran avec F11
            '''

            # Transmission des évènements aux autres classes (MainMenu, GameScreen, ..)
            if self.current_screen == "menu":
                self.main_menu.handle_event(event)
            elif self.current_screen == "settings":
                if self.settings_screen:
                    self.settings_screen.ui.handle_event(event)
            elif self.current_screen == "game":
                if self.game_screen:
                    self.game_screen.handle_event(event)
            elif self.current_screen == "credits":
                if self.credits_screen:
                    self.credits_screen.handle_event(event)

    
    def draw_current_screen(self):
        """
        Dessine l'écran actuel (Menu, Configuration ou Jeu) en appelant les méthodes draw() de chaque classe.
        """
        self.screen.fill(BLACK) # Tous les écrans ont un fond noir (actuellement)
        
        # Appel de la méthode draw() au différentes classes
        if self.current_screen == "menu":
            self.main_menu.draw(self.screen)
        elif self.current_screen == "settings":
            if self.settings_screen:
                self.settings_screen.draw(self.screen)
        elif self.current_screen == "game":
            if self.game_screen:
                self.game_screen.draw(self.screen)
        elif self.current_screen == "credits":
            if self.credits_screen:
                self.credits_screen.draw(self.screen)

    
    def update(self):
        """
        Mise à jour de la logique du jeu. Actuellement vide mais peut servir à ajouter des fonctionnalités comme des sauvegardes.
        """
        if self.current_screen == "game" and self.game_screen:
            pass
    
    def handle_resize(self, new_size):
        """
        Met à jour l'affichage en cas de redimensionnement
        !!! Inutile si la responsivité a été desactivée !!!

        Args:
            new_size (tuple[int, int]): Nouvelle taille de la fenêtre (largeur, hauteur)
        """
        self.current_screen_size = new_size
        self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)

        # Adapter les différents écran aux nouvelles dimensions définies (Responsivité)
        if self.current_screen == "menu":
            self.main_menu.ui.update_layout(new_size)
        elif self.current_screen == "settings" and self.settings_screen:
            self.settings_screen.ui.update_layout(new_size)
        elif self.current_screen == "game" and self.game_screen:
            self.game_screen.ui.update_layout(new_size)

    def run(self):
        """
        Boucle principale non bloquante.
        Gère les événements, met à jour la logique, et redessine les écrans.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw_current_screen()
            pygame.display.flip() # Rafraîchit l'affichage (évitant des latences)
            self.clock.tick(FPS) # Limite le framerate (évitant des latences également)
        
        pygame.quit() # Quit Pygame avant la fermeture de la fenêtre (si self.running devient false, éviter la manière brut)

    def show_credits(self):
        """Affiche l'écran des crédits"""
        self.current_screen = "credits"
        self.credits_screen = CreditsScreen(self.return_to_menu)


if __name__ == "__main__":
    """Execute le jeu seulement si ce fichier est lancé"""
    game = Game()
    game.run()