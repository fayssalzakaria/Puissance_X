# Importation des bibliothèques nécessaires
import numpy as np  # Pour la manipulation de la grille sous forme de matrice
import json  # Pour sauvegarder les résultats des matchs au format JSON
from game.game_logic import winning_move, get_next_open_row, drop_piece, is_valid_location  # Fonctions de logique du jeu
from game.ai import get_ai_move  # Fonction qui calcule le coup de l'IA en fonction de la difficulté

# Classe pour simuler et évaluer des matchs entre IA de différents niveaux de difficulté
class AIMatchTester:
    def __init__(self, rows=6, cols=7, win_condition=4, num_games=50):
        # Paramètres du plateau de jeu
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition
        self.num_games = num_games  # Nombre de matchs par duel de difficultés

        # Historique complet des matchs
        self.match_history = []

        # Dictionnaire pour suivre les performances par niveau de difficulté
        self.performance = {
            'easy': {'wins': 0, 'losses': 0, 'draws': 0},
            'medium': {'wins': 0, 'losses': 0, 'draws': 0},
            'hard': {'wins': 0, 'losses': 0, 'draws': 0}
        }

    # Fonction qui simule une série de matchs entre deux IA de difficulté donnée
    def run_match(self, difficulty1, difficulty2):
        wins_p1 = 0
        wins_p2 = 0
        draws = 0

        # Simulation des matchs
        for match_index in range(self.num_games):
            grid = np.zeros((self.rows, self.cols))  # Plateau vide
            game_over = False
            turn = 1 if match_index % 2 == 0 else 2  # Alterner le joueur qui commence

            moves = []  # Historique des coups de ce match

            while not game_over:
                # Sélection de la difficulté selon le joueur actif
                current_difficulty = difficulty1 if turn == 1 else difficulty2
                col = get_ai_move(grid, current_difficulty, self.win_condition)  # Coup joué par l'IA

                if is_valid_location(grid, col):  # Vérifie si la colonne est jouable
                    row = get_next_open_row(grid, col)  # Ligne disponible dans la colonne
                    drop_piece(grid, row, col, turn)  # Place le jeton du joueur
                    moves.append({'player': turn, 'row': row, 'col': col})  # Enregistre le coup

                    # Vérifie si le joueur courant a gagné
                    if winning_move(grid, turn, self.win_condition):
                        if turn == 1:
                            wins_p1 += 1
                            self.performance[difficulty1]['wins'] += 1
                            self.performance[difficulty2]['losses'] += 1
                        else:
                            wins_p2 += 1
                            self.performance[difficulty2]['wins'] += 1
                            self.performance[difficulty1]['losses'] += 1
                        game_over = True
                        winner = turn
                    elif np.all(grid != 0):  # Grille pleine → match nul
                        draws += 1
                        self.performance[difficulty1]['draws'] += 1
                        self.performance[difficulty2]['draws'] += 1
                        game_over = True
                        winner = 0
                    else:
                        turn = 2 if turn == 1 else 1  # Changement de joueur
                else:
                    # Cas rare : coup invalide (erreur IA)
                    draws += 1
                    self.performance[difficulty1]['draws'] += 1
                    self.performance[difficulty2]['draws'] += 1
                    winner = 0
                    break

            # Enregistrement du match dans l'historique
            self.match_history.append({
                'match_index': match_index,
                'difficulty1': difficulty1,
                'difficulty2': difficulty2,
                'starting_player': 1 if match_index % 2 == 0 else 2,
                'winner': winner,
                'moves': moves,
                'final_grid': grid.tolist()
            })

        return wins_p1, wins_p2, draws

    # Fonction qui organise tous les duels de difficulté et affiche les résultats
    def evaluate(self):
        matchups = [
            ('easy', 'easy'),
            ('medium', 'medium'),
            ('hard', 'hard'),
            ('easy', 'medium'),
            ('easy', 'hard'),
            ('medium', 'hard')
        ]

        print("=== RÉSULTATS DES MATCHS D'IA ===\n")
        for d1, d2 in matchups:
            p1_wins, p2_wins, draws = self.run_match(d1, d2)
            total = p1_wins + p2_wins + draws
            print(f"Match : {d1.upper()} vs {d2.upper()}")
            print(f"  IA 1 ({d1}) gagne : {p1_wins} ({p1_wins / total * 100:.1f}%)")
            print(f"  IA 2 ({d2}) gagne : {p2_wins} ({p2_wins / total * 100:.1f}%)")
            print(f"  Matchs nuls       : {draws} ({draws / total * 100:.1f}%)\n")

        # Sauvegarde des résultats et de l'historique des matchs dans un fichier JSON
        with open('match_results.json', 'w') as f:
            json.dump({
                'match_history': self.match_history,
                'performance': self.performance
            }, f, indent=2)

# Point d'entrée du script
if __name__ == "__main__":
    tester = AIMatchTester()
    tester.evaluate()
