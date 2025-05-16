import numpy as np
import json
from game_logic import winning_move, get_next_open_row, drop_piece, is_valid_location
from ai import get_ai_move

class AIMatchTester:
    def __init__(self, rows=6, cols=7, win_condition=4, num_games=50):
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition
        self.num_games = num_games
        self.match_history = []
        self.performance = {
            'easy': {'wins': 0, 'losses': 0, 'draws': 0},
            'medium': {'wins': 0, 'losses': 0, 'draws': 0},
            'hard': {'wins': 0, 'losses': 0, 'draws': 0}
        }

    def run_match(self, difficulty1, difficulty2):
        wins_p1 = 0
        wins_p2 = 0
        draws = 0

        for match_index in range(self.num_games):
            grid = np.zeros((self.rows, self.cols))
            game_over = False
            turn = 1 if match_index % 2 == 0 else 2  # Alterner qui commence

            moves = []  # Historique des coups pour ce match

            while not game_over:
                current_difficulty = difficulty1 if turn == 1 else difficulty2
                col = get_ai_move(grid, current_difficulty, self.win_condition)

                if is_valid_location(grid, col):
                    row = get_next_open_row(grid, col)
                    drop_piece(grid, row, col, turn)
                    moves.append({'player': turn, 'row': row, 'col': col})

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
                    elif np.all(grid != 0):
                        draws += 1
                        self.performance[difficulty1]['draws'] += 1
                        self.performance[difficulty2]['draws'] += 1
                        game_over = True
                        winner = 0
                    else:
                        turn = 2 if turn == 1 else 1
                else:
                    # Colonne invalide (devrait pas arriver)
                    draws += 1
                    self.performance[difficulty1]['draws'] += 1
                    self.performance[difficulty2]['draws'] += 1
                    winner = 0
                    break

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

        # Sauvegarde de l'historique
        with open('match_results.json', 'w') as f:
            json.dump({
                'match_history': self.match_history,
                'performance': self.performance
            }, f, indent=2)

if __name__ == "__main__":
    tester = AIMatchTester()
    tester.evaluate()
