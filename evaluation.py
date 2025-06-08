# Désactive l'affichage graphique de Pygame (utile pour l'exécution sur un serveur ou en test automatique)
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Utilise un pilote vidéo fictif

# Importation des bibliothèques
import pygame
import numpy as np  # Pour gérer la grille du jeu comme une matrice
from game_screen import GameScreen  # (Import inutilisé ici, peut être supprimé)
from game_logic import winning_move, get_next_open_row, drop_piece, is_valid_location  # Fonctions du moteur du jeu
from ai import get_ai_move  # Fonction pour obtenir le coup d'une IA selon sa difficulté

# Classe permettant d'évaluer les performances des IA en les faisant s'affronter
class Evaluator:
    def __init__(self):
        pygame.init()  # Initialisation de Pygame (même sans affichage visible)
        self.results = {}  # Dictionnaire pour stocker les résultats (pas utilisé ici, mais utile pour extensions)
    
    # Fonction pour exécuter une série de matchs entre deux IA de difficultés données
    def run_match(self, difficulty1: str, difficulty2: str, num_games: int = 50):
        wins_p1 = 0  # Nombre de victoires de l'IA 1
        wins_p2 = 0  # Nombre de victoires de l'IA 2
        draws = 0    # Nombre de matchs nuls
        
        for match_index in range(num_games):
            # Configuration de la grille de jeu pour chaque match
            rows, cols, win_condition = 6, 7, 4
            grid = np.zeros((rows, cols))  # Grille vide initiale (0 = case vide)
            game_over = False  # Indicateur de fin de jeu

            # Alterne le joueur qui commence selon l’indice du match
            turn = 1 if match_index % 2 == 0 else 2
            
            while not game_over:
                # Détermination de la difficulté de l’IA pour le joueur en cours
                current_difficulty = difficulty1 if turn == 1 else difficulty2
                
                # L’IA choisit une colonne où jouer
                col = get_ai_move(grid, current_difficulty, win_condition)
                
                # Vérifie si la colonne est valide (non pleine)
                if is_valid_location(grid, col):
                    row = get_next_open_row(grid, col)  # Trouve la prochaine ligne disponible dans la colonne
                    drop_piece(grid, row, col, turn)    # Place le pion du joueur en cours
                    
                    # Vérifie s’il y a une victoire après ce coup
                    if winning_move(grid, turn, win_condition):
                        if turn == 1:
                            wins_p1 += 1
                        else:
                            wins_p2 += 1
                        game_over = True  # Fin du match
                    elif np.all(grid != 0):  # Vérifie si la grille est pleine (match nul)
                        draws += 1
                        game_over = True
                    
                    # Change de joueur pour le prochain tour
                    turn = 2 if turn == 1 else 1
        
        # Retourne les résultats sous forme de tuple (victoires IA1, victoires IA2, nuls)
        return (wins_p1, wins_p2, draws)

    # Méthode principale pour évaluer toutes les combinaisons de difficulté entre les IA
    def evaluate(self):
        matchups = [
            ('easy', 'easy'),
            ('medium', 'medium'),
            ('hard', 'hard'),
            ('easy', 'medium'),
            ('easy', 'hard'),
            ('medium', 'hard')
        ]
        
        # Pour chaque affrontement, lancer des matchs et afficher les résultats
        for matchup in matchups:
            d1, d2 = matchup  # Difficultés des deux IA
            results = self.run_match(d1, d2)  # Résultats du duel
            total = sum(results)  # Total des matchs joués
            
            # Affichage formaté des résultats
            print(f"=== {d1.upper()} vs {d2.upper()} ===")
            print(f"Victoires {d1}: {results[0]} ({results[0]/total*100:.1f}%)")
            print(f"Victoires {d2}: {results[1]} ({results[1]/total*100:.1f}%)")
            print(f"Matchs nuls: {results[2]} ({results[2]/total*100:.1f}%)")
            print("------------------------")

# Point d’entrée du script
if __name__ == "__main__":
    evaluator = Evaluator()  # Création de l’instance
    evaluator.evaluate()     # Lancement de l’évaluation des IA
