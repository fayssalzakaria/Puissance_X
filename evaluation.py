import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Désactive l'affichage graphique

import pygame
import numpy as np
from game_screen import GameScreen
from game_logic import winning_move, get_next_open_row, drop_piece, is_valid_location
from ai import get_ai_move

class Evaluator:
    def __init__(self):
        pygame.init()
        self.results = {}
    
    def run_match(self, difficulty1: str, difficulty2: str, num_games: int = 50):
        wins_p1 = 0
        wins_p2 = 0
        draws = 0
        
        for match_index in range(num_games):
            # Configuration de base
            rows, cols, win_condition = 6, 7, 4
            grid = np.zeros((rows, cols))
            game_over = False

            # Alterner le joueur qui commence
            turn = 1 if match_index % 2 == 0 else 2
            
            while not game_over:
                # Tour de l'IA
                current_difficulty = difficulty1 if turn == 1 else difficulty2
                col = get_ai_move(grid, current_difficulty, win_condition)
                
                if is_valid_location(grid, col):
                    row = get_next_open_row(grid, col)
                    drop_piece(grid, row, col, turn)
                    
                    if winning_move(grid, turn, win_condition):
                        if turn == 1:
                            wins_p1 += 1
                        else:
                            wins_p2 += 1
                        game_over = True
                    elif np.all(grid != 0):
                        draws += 1
                        game_over = True
                    
                    turn = 2 if turn == 1 else 1
        
        return (wins_p1, wins_p2, draws)


    def evaluate(self):
        matchups = [
            ('easy', 'easy'),
            ('medium', 'medium'),
            ('hard', 'hard'),
            ('easy', 'medium'),
            ('easy', 'hard'),
            ('medium', 'hard')

        ]
        
        for matchup in matchups:
            d1, d2 = matchup
            results = self.run_match(d1, d2)
            total = sum(results)
            
            print(f"=== {d1.upper()} vs {d2.upper()} ===")
            print(f"Victoires {d1}: {results[0]} ({results[0]/total*100:.1f}%)")
            print(f"Victoires {d2}: {results[1]} ({results[1]/total*100:.1f}%)")
            print(f"Matchs nuls: {results[2]} ({results[2]/total*100:.1f}%)")
            print("------------------------")

if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate()