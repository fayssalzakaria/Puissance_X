import pygame
from typing import Callable, Optional, Tuple
from constants import *


class UIElement:
    """Classe de base (abstraite) pour tous les éléments d'interface utilisateur"""
    def __init__(self, position: Tuple[float, float], size: Tuple[float, float], relative: bool = True) :
        """
        position: (x, y) en pourcentages si relative=True, sinon en pixels
        size: (width, height) en pourcentages si relative=True, sinon en pixels
        relative : si True, les valeurs sont des ratios entre 0 et 1 (pourcentage)
        """
        self.relative = relative
        self._position = position # Privé : Position stockée
        self._size = size # Privé : Taille stockée
        self.rect = pygame.Rect(0, 0, 0, 0) # Rectangle (Rect) de Pygame pour la gestion des collisions
        self.visible = True # Visibilité de l'élément
        self.screen_size = (BASE_WIDTH, BASE_HEIGHT) # Taille de l'écran actuelle
        self.update_position(self.screen_size)
    
    def update_position(self, screen_size : Tuple[int, int]) :
        """Met à jour la position et la taille selon les dimensions de l'écran"""
        self.screen_size = screen_size
        if self.relative: # Si les coordonnées sont relatives
            x = self._position[0] * screen_size[0] # Conversion de % en pixels
            y = self._position[1] * screen_size[1]
            w = self._size[0] * screen_size[0]
            h = self._size[1] * screen_size[1]
            self.rect = pygame.Rect(int(x), int(y), int(w), int(h))
        else: # Si les coordonnées sont abosolues (en pixels)
            self.rect = pygame.Rect(*self._position, *self._size)
    
    def handle_event(self, event: pygame.event.Event):
        """Gère les événements, retourne True si l'événement est traité"""
        return False
    
    def draw(self, screen: pygame.Surface):
        """Utilisée plus tard pour dessiner le terrain de jeu"""
        pass

class Button(UIElement):
    """Classe fille de UIElement. Bouton cliquable avec effet de survol"""
    PADDING_X = 20  # Padding horizontal (gauche/droite)
    PADDING_Y = 10  # Padding vertical (haut/bas)

    def __init__(self, position: Tuple[float, float], size: Optional[Tuple[float, float]],
                 text: str, callback: Optional[Callable] = None,
                 relative: bool = True):
        """
        text : texte à afficher
        callback : fonction à appeler lors du clic de la souris
        """
        # Calcul automatique de la taille en fonction du texte si `size` est None
        text_surf = BUTTON_FONT.render(text, True, WHITE)
        text_width, text_height = text_surf.get_size()

        if size is None:
            size = (text_width + self.PADDING_X * 2, text_height + self.PADDING_Y * 2)

        super().__init__(position, size, relative)  # Initialise la classe parent (UIElement)
        
        self.text = text
        self.callback = callback
        self.hovered = False  # État de survol de la souris

    def handle_event(self, event: pygame.event.Event):
        """Gère les événements de souris"""
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEMOTION:  # Mouvement de souris
            self.hovered = self.rect.collidepoint(event.pos)  # Vérifie une collision
            return self.hovered
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            if self.hovered and self.callback:
                self.callback()  # Appelle la fonction callback()
                return True
        return False

    def draw(self, screen: pygame.Surface):
        """Dessine le bouton avec son état actuel"""
        if not self.visible:
            return

        # Couleur dépendant du survol de la souris
        color = HOVER_BLUE if self.hovered else BLUE
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Rendu du texte centré dans le bouton
        text_surf = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class Title(UIElement):
    """Titre du jeu (actuellement "Puissance X") centré en haut de l'écran"""
    def __init__(self, text: str):
        self.text = text
        super().__init__((0.5, TITLE_TOP_MARGIN_RATIO), (0, 0)) # Initialisation de la classe parente (Position relative)

    
    def update_position(self, screen_size: Tuple[int, int]):
        """Met à jour la position du titre"""
        super().update_position(screen_size)
        text_surf = TITLE_FONT.render(self.text, True, WHITE)
        # Centre horizontalement uniquement, la position verticale est fixe
        self.rect = text_surf.get_rect(center=(screen_size[0]//2, int(screen_size[1] * TITLE_TOP_MARGIN_RATIO)))
    
    def draw(self, screen: pygame.Surface) :
        """Dessine le titre"""
        text_surf = TITLE_FONT.render(self.text, True, WHITE)
        screen.blit(text_surf, self.rect)

class UIManager:
    """Gestionnaire de tous les éléments de la classe UIElement (et de ses sous-classes)"""
    def __init__(self):
        self.elements = [] # List des éléments UI
        self.screen_size = (BASE_WIDTH, BASE_HEIGHT) # Taille actuelle de l'écran
    
    def add_element(self, element: UIElement):
        """Ajoute une élément et met à jour sa position"""
        element.update_position(self.screen_size)
        self.elements.append(element)
    
    def handle_event(self, event: pygame.event.Event):
        """Transmet les évemements aux éléments (du dernier au premier)"""
        cursor_changed = False  # Suivi du changement de curseur

        for element in reversed(self.elements):  # Parcours inversé pour gérer la priorité d'affichage
            if element.handle_event(event):  
                if isinstance(element, (Button, Slider, Dropdown)):  # Vérifie si l'élément est interactif
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Curseur en mode pointeur
                    cursor_changed = True
                return True  

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Curseur par défaut
        
        return False
    
    def update_layout(self, new_size: Tuple[int, int]):
        """Met à jour toutes les positions après un redimensionnement"""
        self.screen_size = new_size
        for element in self.elements:
            element.update_position(new_size)
    
    def draw(self, screen: pygame.Surface):
        """Dessine tous les éléments visibles"""
        for element in self.elements:
            if element.visible:
                element.draw(screen)

class Slider(UIElement):
    def __init__(self, position: Tuple[float, float], size: Tuple[float, float],
                 min_value: int, max_value: int, default_value: int, relative: bool = True):
        super().__init__(position, size, relative)
        self.min = min_value
        self.max = max_value
        self.value = default_value
        self.dragging = False
        self.handle_radius = 12  # Augmenté de 10 à 12 pixels
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self.update_value(mouse_pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(mouse_pos[0])
            return True
        return False
    
    def update_value(self, x_pos: int):
        relative_x = max(0, min(x_pos - self.rect.left, self.rect.width))
        self.value = int(self.min + (relative_x / self.rect.width) * (self.max - self.min))
        self.value = max(self.min, min(self.max, self.value))

    def draw(self, screen: pygame.Surface):
        # Barre de fond
        pygame.draw.rect(screen, DARK_GREY, self.rect, border_radius=3)
        
        # Position du curseur
        handle_x = self.rect.left + (self.value - self.min) / (self.max - self.min) * self.rect.width
        handle_pos = (int(handle_x), self.rect.centery)
        
        # Dessin du cercle plus gros
        pygame.draw.circle(screen, BLUE, handle_pos, self.handle_radius)
        
        # Affichage de la valeur (avec une police légèrement plus petite si nécessaire)
        font = pygame.font.SysFont(None, 30)
        text_surf = font.render(str(self.value), True, WHITE)
        text_rect = text_surf.get_rect(center=handle_pos)
        screen.blit(text_surf, text_rect)
        
    def get_value(self):
        return self.value

    def set_value(self, value: int):
        self.value = max(self.min, min(value, self.max))
        
    def get_value(self):
        return self.value

    def set_value(self, value: int):
        self.value = max(self.min, min(value, self.max))

class Label(UIElement):
    """Classe permettant d'afficher un texte statique à l'écran"""
    
    def __init__(self, position: Tuple[float, float], text: str, font: pygame.font.Font, color: Tuple[int, int, int] = WHITE, relative: bool = True):
        """
        position : Position du texte (en % si relative=True, sinon en pixels)
        text : Contenu du texte
        font : Police utilisée pour le texte
        color : Couleur du texte
        relative : Définit si la position est relative (True) ou absolue (False)
        """
        self.text = text
        self.font = font
        self.color = color
        self.text_surf = font.render(text, True, color)  # Rendu du texte
        size = self.text_surf.get_size()  # Calcul automatique de la taille

        super().__init__(position, size, relative)  # Appel du constructeur parent

    def update_position(self, screen_size: Tuple[int, int]):
        """Met à jour la position du label"""
        super().update_position(screen_size)
        self.text_surf = self.font.render(self.text, True, self.color)  # Rendu du texte
        self.rect = self.text_surf.get_rect(topleft=(self.rect.x, self.rect.y))  # Mise à jour de la position

    def draw(self, screen: pygame.Surface):
        """Dessine le texte à l'écran"""
        if self.visible:
            screen.blit(self.text_surf, self.rect)
    
    def set_text(self, new_text: str):
        """Change le texte affiché et met à jour la taille"""
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, self.color)
        self.rect.size = self.text_surf.get_size()  # Ajuste la taille du rect automatiquement

class Dropdown(UIElement):  # Implémente le menu déroulant, Hérite de UIElement
    def __init__(self, position: Tuple[float, float], size: Tuple[float, float],
                 options: list, default_index: int = 0, relative: bool = True):
        super().__init__(position, size, relative)  # Initialise la classe parente
        self.options = options  # liste d'options disponibles
        self.selected_index = default_index  # Index de l'option sélectionnée par défaut
        self.is_open = False  # Indique si le menu est actuellement ouvert ou fermé
        self.hovered_index = -1  # Index de l'option survolée par la souris

    @property
    def selected_value(self):
        """Permet d'accéder directement à la valeur de l'option sélectionnée"""
        return self.options[self.selected_index]

    def handle_event(self, event: pygame.event.Event):
        """Gérer les événements liés à la souris"""
        if not self.visible:
            return False

        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si le clic est dans le bouton principal du dropdown
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                return True
            elif self.is_open:
                # Parcours des options affichées à droite
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(
                        self.rect.right,  # À droite du bouton principal
                        self.rect.top + i * self.rect.height,  # Correction de l'offset Y pour aligner avec le bouton
                        self.rect.width,  # Même largeur que le bouton principal
                        self.rect.height  # Même hauteur que le bouton principal
                    )
                    if option_rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        self.is_open = False
                        return True
                # Si le clic est en dehors, on ferme le menu
                self.is_open = False
                return True

        if event.type == pygame.MOUSEMOTION and self.is_open:
            self.hovered_index = -1
            for i in range(len(self.options)):
                option_rect = pygame.Rect(
                    self.rect.right,
                    self.rect.top + i * self.rect.height,  # Correction de l'offset Y
                    self.rect.width,
                    self.rect.height
                )
                if option_rect.collidepoint(mouse_pos):
                    self.hovered_index = i
            return True

        return False

    def draw_main(self, screen):
        """Dessine le bouton principal du dropdown."""
        if not self.visible:
            return
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=5)
        text_surf = BUTTON_FONT.render(str(self.selected_value), True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def draw_options(self, screen):
        """Dessine les options du dropdown si ouvert."""
        if not self.visible or not self.is_open:
            return
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.rect.right,
                self.rect.top + i * self.rect.height,
                self.rect.width,
                self.rect.height
            )
            color = HOVER_BLUE if i == self.hovered_index else BLUE
            pygame.draw.rect(screen, color, option_rect, border_radius=5)
            opt_text = BUTTON_FONT.render(str(option), True, WHITE)
            opt_text_rect = opt_text.get_rect(center=option_rect.center)
            screen.blit(opt_text, opt_text_rect)
        
    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.color = DARK_GREY if not enabled else WHITE

    def draw(self, screen):
        """Dessine le bouton principal. Les options sont gérées séparément."""
        self.draw_main(screen)
