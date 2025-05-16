from interface import UIManager, Button, Title
from constants import *

class MainMenu:
    """Classe principale du menu avec tous les boutons"""
    def __init__(self, show_settings_callback, show_credits_callback):
        self.ui = UIManager()  # Crée le gestionnaire UI
        self.title = Title("Puissance X")  # Crée le titre
        self.show_settings = show_settings_callback
        self.show_credits = show_credits_callback
        self.create_buttons()  # Initialise les boutons, appeler juste en dessous

    def create_buttons(self):
        """Initialisation des boutons avec le positionnement relatif"""
        button_width = BUTTON_WIDTH_RATIO  # Largeur relative
        start_y = 0.4  # Position verticale de départ (40%)

        # Bouton Joueur vs Joueur
        self.btn_pvp = Button(
            (0.5 - button_width / 2, start_y),  # Centré horizontalement
            (button_width, BUTTON_HEIGHT / BASE_HEIGHT),  # Taille relative
            "Joueur vs IA",
            self.on_pvp,
            relative=True
        )

        # Bouton Joueur vs IA (positionné en dessous)
        self.btn_ai = Button(
            (0.5 - button_width / 2, start_y + (BUTTON_SPACING_RATIO + BUTTON_HEIGHT / BASE_HEIGHT)),
            (button_width, BUTTON_HEIGHT / BASE_HEIGHT),
            "Tournois IA",
            self.on_ai_tournament,
            relative=True
        )

        # Bouton Paramètres (en bas de l'écran)
        self.btn_settings = Button(
            (0.5 - button_width / 2,
             start_y + 2 * (BUTTON_SPACING_RATIO + BUTTON_HEIGHT / BASE_HEIGHT)),
            (button_width, BUTTON_HEIGHT / BASE_HEIGHT),  # Bouton plus petit
            "Crédits",
            self.on_credits,
            relative=True
        )

        self.ui.add_element(self.title)
        self.ui.add_element(self.btn_pvp)
        self.ui.add_element(self.btn_ai)
        self.ui.add_element(self.btn_settings)

    def on_pvp(self):
        self.show_settings("pvp")  # joueur vs joueur (plus utilisé)

    def on_pvai(self):
        self.show_settings("pvia")  # joueur vs IA

    def on_ai_tournament(self):
        self.show_settings("ai_vs_ai")  # IA vs IA

    def on_credits(self):
        """Callback pour les paramètres (faire passer le joueur a l'écran des paramètres par la classe Game)"""
        self.show_credits()

    def handle_event(self, event):
        """Transmet les événements au gestionnaire UI"""
        return self.ui.handle_event(event)

    def draw(self, screen):
        """Dessin du menu"""
        screen.fill(BLACK)
        self.ui.draw(screen)