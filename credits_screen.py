import pygame
from constants import *
from interface import Label, Button, UIManager

class CreditsScreen:
    def __init__(self, return_callback):
        self.ui = UIManager()
        self.return_callback = return_callback

        # Titre centré
        title_text = "Crédits"
        title_surface = TITLE_FONT.render(title_text, True, WHITE)
        title_width = title_surface.get_width()
        title_x = 0.5 - (title_width / BASE_WIDTH / 2)
        self.title = Label((title_x, 0.15), title_text, TITLE_FONT, WHITE, relative=True)

        # Texte principal en deux lignes, centrées manuellement
        credit_lines = [
            "Ce jeu a été développé par Nicolas Adamczyk et Fayssal Zakaria",
            "dans le cadre du module d'intelligence artificielle."
        ]

        self.credit_labels = []
        line_height = SETTINGS_FONT.get_height() + 0.5
        start_y = 0.4  # Position verticale de la première ligne

        for i, line in enumerate(credit_lines):
            surface = SETTINGS_FONT.render(line, True, WHITE)
            width = surface.get_width()
            x = 0.5 - (width / BASE_WIDTH / 2)
            y = start_y + i * (line_height / BASE_HEIGHT)
            label = Label((x, y), line, SETTINGS_FONT, WHITE, relative=True)
            self.credit_labels.append(label)
            self.ui.add_element(label)

        # Bouton retour centré
        self.back_button = Button(
            (0.5 - 0.1, 0.75),
            (0.2, 0.08),
            "Retour",
            self.return_callback,
            relative=True
        )

        # Ajout à l'UI
        self.ui.add_element(self.title)
        self.ui.add_element(self.back_button)

    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, screen):
        screen.fill(BLACK)
        self.ui.draw(screen)