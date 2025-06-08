# Importation des bibliothèques nécessaires
import pygame
from constants import *  # Contient les constantes globales comme les couleurs, dimensions, polices, etc.
from interface import Label, Button, UIManager  # Composants d’interface utilisateur personnalisés

# Classe représentant l'écran de crédits du jeu
class CreditsScreen:
    def __init__(self, return_callback):
        # UIManager gère tous les éléments visuels (labels, boutons, etc.)
        self.ui = UIManager()
        
        # Callback pour revenir au menu précédent (par exemple, écran principal)
        self.return_callback = return_callback

        # ----- Création du titre "Crédits" centré en haut -----
        title_text = "Crédits"
        title_surface = TITLE_FONT.render(title_text, True, WHITE)  # Rend le texte pour obtenir ses dimensions
        title_width = title_surface.get_width()
        
        # Calcul de la position x relative pour centrer le texte horizontalement
        title_x = 0.5 - (title_width / BASE_WIDTH / 2)
        
        # Création du label du titre
        self.title = Label((title_x, 0.15), title_text, TITLE_FONT, WHITE, relative=True)

        # ----- Création des lignes de texte de crédits centrées manuellement -----
        credit_lines = [
            "Ce jeu a été développé par Nicolas Adamczyk et Fayssal Zakaria",
            "dans le cadre du module d'intelligence artificielle."
        ]

        self.credit_labels = []  # Stockage des labels de texte
        line_height = SETTINGS_FONT.get_height() + 0.5  # Espacement entre les lignes
        start_y = 0.4  # Position verticale de départ pour la première ligne

        for i, line in enumerate(credit_lines):
            surface = SETTINGS_FONT.render(line, True, WHITE)  # Rendu pour calcul de la largeur
            width = surface.get_width()
            
            # Calcul de la position x pour centrer la ligne horizontalement
            x = 0.5 - (width / BASE_WIDTH / 2)
            
            # Calcul de la position y relative
            y = start_y + i * (line_height / BASE_HEIGHT)
            
            # Création et ajout du label
            label = Label((x, y), line, SETTINGS_FONT, WHITE, relative=True)
            self.credit_labels.append(label)
            self.ui.add_element(label)  # Ajout à l’UI manager

        # ----- Création du bouton "Retour" centré en bas -----
        self.back_button = Button(
            (0.5 - 0.1, 0.75),  # Position centrée (largeur du bouton = 0.2)
            (0.2, 0.08),        # Taille du bouton
            "Retour",           # Texte affiché
            self.return_callback,  # Action à effectuer lors du clic
            relative=True       # Coordonnées relatives
        )

        # ----- Ajout des éléments à l’UI manager -----
        self.ui.add_element(self.title)
        self.ui.add_element(self.back_button)

    # Gestion des événements utilisateur (clics, survols, etc.)
    def handle_event(self, event):
        self.ui.handle_event(event)

    # Affichage de l'écran
    def draw(self, screen):
        screen.fill(BLACK)  # Fond noir
        self.ui.draw(screen)  # Dessin de tous les éléments de l'interface
