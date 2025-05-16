from interface import UIManager, Button, Slider, Label, Dropdown
from constants import *
import pygame

class SettingsScreen:
    """Cette classe représente l'écran de configuration d'une partie"""
    def __init__(self, on_confirm: callable, on_back: callable, mode="pvp"):
        self.ui = UIManager()
        self.on_confirm = on_confirm # fonction de callback appelé lorsque l'utilisateur valide les paramètres (ensuite se faire rediriger vers la partie par la classe Game)
        self.on_back = on_back  # fonction de callback appelé lorsque l'utilisteur veut revenir au menu principal (ensuite revenir au menu principal par la classe Game)
        self.rows = 6 # Nombre de lignes (par défaut 6 comme dans le jeu Puissance 4)
        self.cols = 7 # Nombre de colonnes (par défaut 7 comme dans le jeu Puissance 4)
        self.win_condition = 4 # Nombre de pions à aligner pour gagner
        
        # Définition des positions de base (en coordonnées relatives)
        self.title_y = 0.1  # Position verticale du titre
        self.first_row_y = 0.2  # Position verticale de la première ligne de réglages
        self.row_gap = 0.08  # Espace vertical entre chaque ligne
        
        # Position horizontale pour la colonne de texte et celle des contrôles
        self.label_x = 0.3 # Position horizontale pour les textes des réglages (gauche)
        self.control_x = 0.55 # Position horizontale pour les contrôles des réglages (droite)
        self.mode = mode  # "pvp" ou "pvia"
        self.create_ui() # Appel directement à la création de l'interface (définie dans la première méthode)


    
    def create_ui(self):
        """Cette méthode ajoute tous les éléments d'interface (définis dans le fichier interface.py) à l'écran."""
        # Les méthodes add_title(), add_text(), add_button(), add_slider(), add_dropdown() sont définies ci-dessous de cette méthode
        # Titre
        self.add_title() 
        
        # 1 : Configuration du nombre de lignes
        current_y = self.first_row_y
        self.add_text("Nombre de lignes:", (self.label_x, current_y))
        self.rows_dropdown = self.add_dropdown(
            (self.control_x, current_y),
            [str(i) for i in range(5, 11)],  # Le nombre de lignes possible va de 5 à 10
            1  # Default: 6 (comme dans Puissance 4)
        )

        # 2 : Configuration du nombre de colonnes
        current_y += self.row_gap
        self.add_text("Nombre de colonnes:", (self.label_x, current_y))
        self.cols_dropdown = self.add_dropdown(
            (self.control_x, current_y),
            [str(i) for i in range(5, 11)],  # Le nombre de colonnes possible va de 5 à 10
            2  # Default: 7 (comme dans Puissance 4)
        )

        # 3 : Configuration de la difficulté de l'IA
        current_y += self.row_gap
        self.add_text("Difficulté de l'IA:", (self.label_x, current_y))
        self.difficulty_dropdown = self.add_dropdown(
            (self.control_x, current_y),
            ['Facile', 'Moyen', 'Difficile'], 
            1  # Moyen par défaut
        )

        # 3b : Afficher IA 2 seulement en mode tournoi IA
        if self.mode == "ai_vs_ai":
            current_y += self.row_gap
            self.add_text("Difficulté de l'IA 2:", (self.label_x, current_y))
            self.difficulty2_dropdown = self.add_dropdown(
                (self.control_x, current_y),
                ['Facile', 'Moyen', 'Difficile'],
                1
            )
            self.difficulty2_dropdown.set_enabled(True)  # S'assurer qu'il est activé
            
            # Ajout du choix de qui commence en mode IA vs IA
            current_y += self.row_gap
            self.add_text("Qui commence:", (self.label_x, current_y))
            self.starting_player_dropdown = self.add_dropdown(
                (self.control_x, current_y),
                ['IA 1', 'IA 2'],
                0  # IA 1 par défaut
            )
        else:
            self.difficulty2_dropdown = None  # Pas affiché ni utilisé
            # Ajout du choix de qui commence en mode PvIA
            current_y += self.row_gap
            self.add_text("Qui commence:", (self.label_x, current_y))
            self.starting_player_dropdown = self.add_dropdown(
                (self.control_x, current_y),
                ['Joueur', 'IA'],
                0  # Joueur par défaut
            )
        
        # 4 : Configuration des pions à aligner pour gagner
        current_y += self.row_gap
        self.add_text("Pions à aligner:", (self.label_x, current_y))
        self.win_condition_slider = self.add_slider(
            (self.control_x, current_y),
            3, 9, 4
        )
        
        # Ligne 5 : Bouton pour commencer la partie
        current_y += self.row_gap
        self.add_button("Commencer", (0.5, current_y), self.on_confirm_click)
        
        # Ligne 6 : Bouton pour revenir au menu principal
        current_y += self.row_gap * 1.2
        self.add_button("Retour", (0.5, current_y), self.on_back_click)

    
    def add_title(self):
        """Ajoute le titre centré en haut de l'écran"""
        title = Button(
            (0.5, self.title_y),
            (0, 0.1),
            "CONFIGURATION DE LA PARTIE",
            None,
            relative=True
        )
        title.visible = True  # Visible mais non cliquable
        self.ui.add_element(title)
    
    def add_text(self, text: str, position: tuple):
        """Ajoute un texte statique (label)"""
        label = Label(
            position,
            text,
            BUTTON_FONT,
            WHITE,
            relative=True
        )
        self.ui.add_element(label)
    
    def add_dropdown(self, position: tuple, options: list, default_index: int = 0):
        """Ajoute un menu déroulant"""
        dropdown = Dropdown(
            position,
            (DROPDOWN_WIDTH, DROPDOWN_HEIGHT),
            options,
            default_index,
            relative=True
        )
        self.ui.add_element(dropdown)
        return dropdown
    
    def add_slider(self, position: tuple, min_val: int, max_val: int, default_val: int):
        """Ajoute un slider"""
        slider = Slider(
            position,
            (SLIDER_WIDTH, SLIDER_HEIGHT),
            min_val,
            max_val,
            default_val,
            relative=True
        )
        self.ui.add_element(slider)
        return slider
    
    def add_button(self, text: str, position: tuple, callback):
        """Ajoute un bouton centré horizontalement"""
        button = Button(
            (position[0] - (0.2 / 2), position[1]),  # Centrage horizontal
            (0.2, 0.08),  # Taille du bouton
            text,
            callback,
            relative=True
        )
        self.ui.add_element(button)
        return button
        
    def on_confirm_click(self):
        self.rows = int(self.rows_dropdown.selected_value)
        self.cols = int(self.cols_dropdown.selected_value)
        self.win_condition = self.win_condition_slider.get_value()
        self.difficulty = ['easy', 'medium', 'hard'][self.difficulty_dropdown.selected_index]
        
        # Qui commence
        if self.mode == "ai_vs_ai":
            self.starting_player = self.starting_player_dropdown.selected_index + 1  # 1 ou 2
        else:
            self.starting_player = self.starting_player_dropdown.selected_index + 1  # 1 ou 2
        
        # IA 2 seulement si mode "ai_vs_ai"
        if self.mode == "ai_vs_ai":
            self.difficulty2 = ['easy', 'medium', 'hard'][self.difficulty2_dropdown.selected_index]
        else:
            self.difficulty2 = None

        # Callback enrichi
        self.on_confirm(self.rows, self.cols, self.win_condition, self.difficulty, self.starting_player, self.difficulty2) # Une fois que tous les paramètres sont configurés via l'interface graphique, on passe toutes les valeurs (stockés dans leur attributs respectifs) au callback pour lancer la partie

    
    def on_back_click(self):
        """Retour au menu principal"""
        self.on_back()

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Mise à jour dynamique du slider
        current_rows = int(self.rows_dropdown.selected_value)
        current_cols = int(self.cols_dropdown.selected_value)
        new_max = min(current_rows, current_cols)
        self.win_condition_slider.max_val = new_max
        
        current_value = self.win_condition_slider.get_value()
        if current_value > new_max:
            self.win_condition_slider.set_value(new_max)
        
        # Dessiner tous les éléments de l'interface
        self.ui.draw(screen)
        
        # Ajouter le dropdown de la deuxième IA à la liste
        dropdowns = [
            self.rows_dropdown, 
            self.cols_dropdown, 
            self.difficulty_dropdown,
            self.difficulty2_dropdown,  # Ajouté ici
            self.starting_player_dropdown
        ]
        
        # Dessiner les options des dropdowns ouverts
        for dropdown in dropdowns:
            if dropdown and dropdown.is_open:  # Vérifier si le dropdown existe
                dropdown.draw_options(screen)