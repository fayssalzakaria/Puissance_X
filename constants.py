import pygame
from typing import Tuple

# Screen
BASE_WIDTH = 1280
BASE_HEIGHT = 720
FPS = 60 # Images par secodne pour le rafraichissement (inutile retiré après la deuxième version)

# Colors
BLACK = (0, 0, 0) # Utilisé pour le fond d'écran
WHITE = (255, 255, 255) # Utilisé pour la couleur du texte
BLUE = (30, 144, 255) # Utilisé pour la couleur des boutons
HOVER_BLUE = (100, 149, 237) # Utilisé pour la couleur des boutons au survol de la souris
DARK_GREY = (40, 40, 40) # Non utilisé actuellement

# UI
BUTTON_WIDTH_RATIO = 0.2  # largeur des boutons (20% de la largeur de l'écran)
BUTTON_HEIGHT = 60 # Hauteur fixe en pixels pour les boutons
BUTTON_SPACING_RATIO = 0.05  # Espacement vertical entre boutons (5% de la hauteur de l'écran)
TITLE_TOP_MARGIN_RATIO = 0.1  # Marge du haut pour le titre (10% de la hauteur)

DROPDOWN_WIDTH = 0.15  # 15% de la largeur d'écran
DROPDOWN_HEIGHT = 0.06  # 6% de la hauteur d'écran
SLIDER_WIDTH = 0.3
SLIDER_HEIGHT = 0.04
TEXT_MARGIN = 0.02  # 2% d'espace entre les élément

# Couleurs
RED = (255, 0, 0)      # Pion joueur
YELLOW = (255, 255, 0) # Pion IA

# Pièces
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 2

# Configuration IA
WINDOW_LENGTH = 4  # Pour Puissance 4

# Fonts
pygame.font.init() # Intialisation du module "font" de pygame
TITLE_FONT = pygame.font.Font(None, 72)  # Choisir une police et une taille pour le texte
BUTTON_FONT = pygame.font.Font(None, 36)  # Choisir une police et une taille pour le texte
SETTINGS_FONT = pygame.font.Font(None, 24)  # Choisir une police et une taille pour le texte

AI_DELAY = 1000  # en millisecondes (1 seconde)
AI_MOVE_EVENT = pygame.USEREVENT + 1  # Événement personnalisé