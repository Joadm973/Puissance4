import time
import random
import json
from datetime import datetime
from constants import *
# Use the CSVStatsManager from stats.py with the correct method name
from stats import CSVStatsManager

class Connect4:
    def __init__(self):
        # Initialize the game state
        self.scores = {PLAYER_X: 0, PLAYER_O: 0}
        self.ai_mode = False
        self.ai_vs_ai_mode = False
        self.ai_level = 1  # Default AI level: 1 = moderate, 2 = advanced
        # Update to use CSVStatsManager
        self.stats_manager = CSVStatsManager()
        self.start_time = time.time()
        self.game_moves = []  # To record moves of the current game
        # Immediately load patterns learned from previous games
        try:
            self.learned_patterns = self.stats_manager.analyser_historique_victoires()
        except Exception as e:
            print(f"Error loading learned patterns: {e}")
            self.learned_patterns = {
                'X': {'coups': [], 'frequence': {}},
                'O': {'coups': [], 'frequence': {}}
            }
        self.reset_game()

    def reset_game(self):
        # Create an empty board
        self.board = []
        for _ in range(ROWS):
            row = [EMPTY] * COLUMNS
            self.board.append(row)
        
        # Initialize game state
        self.current_player = PLAYER_X
        # Always make sure start_time is set
        if not hasattr(self, 'start_time') or self.start_time is None:
            self.start_time = time.time()
        self.game_moves = []  # Reset moves of the current game

    def place_token(self, column):
        """Place a token in the specified column"""
        # Make sure start_time is always set before any game-changing action
        if not hasattr(self, 'start_time') or self.start_time is None:
            self.start_time = time.time()
            
        if column < 0 or column >= COLUMNS:
            return False
            
        for row in range(ROWS-1, -1, -1):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = self.current_player
                # Record the move
                self.game_moves.append((row, column))
                
                # Check if this move leads to a victory
                if self.check_victory():
                    return 'victory'
                    
                # Check if the board is full
                if self.is_board_full():
                    return 'draw'
                    
                return True
                
        return False

    def check_victory(self):
        # Horizontal check
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row][col + 1] == 
                    self.board[row][col + 2] == self.board[row][col + 3]):
                    return True

        # Vertical check
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row + 1][col] == 
                    self.board[row + 2][col] == self.board[row + 3][col]):
                    return True

        # Diagonal check (/)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row - 1][col + 1] == 
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3]):
                    return True

        # Diagonal check (\)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row + 1][col + 1] == 
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                    return True

        return False

    def find_winning_tokens(self):
        """Returns the coordinates of the 4 winning tokens"""
        # Horizontal check
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row][col + 1] == 
                    self.board[row][col + 2] == self.board[row][col + 3]):
                    return [(row, col + i) for i in range(4)]

        # Vertical check
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row + 1][col] == 
                    self.board[row + 2][col] == self.board[row + 3][col]):
                    return [(row + i, col) for i in range(4)]

        # Diagonal check (/)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row - 1][col + 1] == 
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3]):
                    return [(row - i, col + i) for i in range(4)]

        # Diagonal check (\)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] != EMPTY and
                    self.board[row][col] == self.board[row + 1][col + 1] == 
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                    return [(row + i, col + i) for i in range(4)]

        return []

    def is_board_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def change_player(self):
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def increment_score(self):
        self.scores[self.current_player] += 1
        return self.scores[self.current_player]

    def evaluate_move(self, column):
        """Evaluates a potential move"""
        # Save the current state including start_time
        start_time_backup = self.start_time
        current_player_backup = self.current_player
        
        if not self.place_token(column):
            self.start_time = start_time_backup  # Restore start_time
            return float('-inf')
            
        score = 0
        self.change_player()
        
        # Check if the move leads to a victory
        if self.check_victory():
            score = 100
        else:
            # Evaluate the position
            score = self.evaluate_position()
            
        # Undo the move
        for row in range(ROWS):
            if self.board[row][column] != EMPTY:
                self.board[row][column] = EMPTY
                break
                
        # IMPORTANT: Restore the original state including start_time
        self.start_time = start_time_backup
        self.current_player = current_player_backup
        
        return score

    def evaluate_position(self):
        """Evaluates the current board position using learned patterns"""
        score = 0
        
        # Basic evaluation
        score += self._evaluate_base_position()
        
        # Bonus for learned patterns
        if self.learned_patterns:
            score += self._evaluate_learned_patterns()
        
        return score

    def _evaluate_base_position(self):
        """Basic evaluation of the position"""
        score = 0
        # Center of the board (priority)
        center = COLUMNS // 2
        for row in range(ROWS):
            if self.board[row][center] == self.current_player:
                score += 3
                
        # Check for alignments of 3
        for row in range(ROWS):
            for col in range(COLUMNS-2):
                if (self.board[row][col] == self.current_player and
                    self.board[row][col+1] == self.current_player and
                    self.board[row][col+2] == self.current_player):
                    score += 5
                    
        return score

    def _evaluate_learned_patterns(self):
        """Evaluates the position based on learned patterns"""
        score = 0
        patterns = self.learned_patterns
        
        if not patterns:
            return score
            
        # Check if the current position matches known winning patterns
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board[row][col] == self.current_player:
                    pos = str((row, col))
                    # Bonus based on pattern frequency
                    if self.current_player in patterns and pos in patterns[self.current_player]['frequence']:
                        bonus = patterns[self.current_player]['frequence'][pos] * 0.5
                        score += bonus
                        
                    # Penalty if position is often winning for opponent
                    opponent = 'X' if self.current_player == 'O' else 'O'
                    if opponent in patterns and pos in patterns[opponent]['frequence']:
                        penalty = patterns[opponent]['frequence'][pos] * 0.8
                        score -= penalty
                        
        # Check partial alignments that often lead to victories
        for row in range(ROWS-1):
            for col in range(COLUMNS-1):
                if (self.board[row][col] == self.current_player and 
                    self.board[row+1][col] == self.current_player):
                    # Vertical alignment of 2
                    score += 2
                    
                if (col < COLUMNS-2 and self.board[row][col] == self.current_player and 
                    self.board[row][col+1] == self.current_player):
                    # Horizontal alignment of 2
                    score += 2
                    
                if (row < ROWS-2 and col < COLUMNS-2 and 
                    self.board[row][col] == self.current_player and 
                    self.board[row+1][col+1] == self.current_player):
                    # Diagonal \ alignment of 2
                    score += 2
                    
                if (row > 0 and col < COLUMNS-2 and row < ROWS-1 and
                    self.board[row][col] == self.current_player and 
                    self.board[row-1][col+1] == self.current_player):
                    # Diagonal / alignment of 2
                    score += 2
        
        return score

    def choose_best_move(self):
        """Chooses the best move for the AI based on the AI level"""
        if self.ai_level == 1:
            return self._choose_moderate_move()  # Niveau modéré - logique de base
        else:
            return self._choose_advanced_move()  # Niveau avancé - avec analyse des parties
            
    def _choose_moderate_move(self):
        """
        Chooses the best move using only basic game logic (moderate level).
        This AI uses a simpler approach without learning from past games.
        """
        # If it's the first time we play, priority to the center
        if len(self.game_moves) <= 2 and self.board[0][COLUMNS // 2] == EMPTY:
            return COLUMNS // 2
            
        # Check if a move allows to win immediately
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                # Simulate the move to see if it leads to a victory
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = self.current_player
                        victory = self.check_victory()
                        self.board[row][col] = EMPTY  # Undo the move
                        if victory:
                            return col

        # Check if the opponent can win on the next move and block
        opponent = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        current_player_backup = self.current_player
        self.current_player = opponent  # Temporarily change to simulate
        
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                # Simulate the opponent's move to see if it leads to a victory
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = opponent
                        opponent_victory = self.check_victory()
                        self.board[row][col] = EMPTY  # Undo the move
                        if opponent_victory:
                            self.current_player = current_player_backup  # Restore
                            return col
                        break
        
        # Restore the current player
        self.current_player = current_player_backup
        
        # If no obvious move, use basic evaluation (without patterns)
        evaluations = {}
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                # Use a simplified evaluation that only considers basic position
                score = self._evaluate_basic_position(col)
                evaluations[col] = score
                
        # Find the best score
        if not evaluations:
            return None
            
        best_score = max(evaluations.values())
        
        # Get all moves with the best score
        best_moves = [col for col, score in evaluations.items() if score == best_score]
        
        # Choose randomly among the best moves with some randomness for moderate difficulty
        if random.random() < 0.2:  # 20% of the time, pick a random valid move
            valid_moves = [col for col in range(COLUMNS) if self.board[0][col] == EMPTY]
            if valid_moves:
                return random.choice(valid_moves)
        
        # Otherwise choose among the best moves
        return random.choice(best_moves) if best_moves else None

    def _evaluate_basic_position(self, column):
        """
        Simplified evaluation for the moderate AI level.
        Only considers basic strategy without pattern learning.
        """
        # Save the current state
        start_time_backup = self.start_time
        current_player_backup = self.current_player
        
        # Try to place the token
        placement_row = -1
        for row in range(ROWS-1, -1, -1):
            if self.board[row][column] == EMPTY:
                placement_row = row
                self.board[row][column] = self.current_player
                break
                
        if placement_row == -1:
            # Column is full
            return float('-inf')
            
        score = 0
        
        # Check if this creates any potential alignments
        
        # Check horizontal potential (how many tokens could be aligned)
        for c in range(max(0, column-3), min(COLUMNS-3, column+1)):
            window = [self.board[placement_row][c+i] for i in range(4)]
            score += self._evaluate_window(window)
            
        # Check vertical potential
        if placement_row <= ROWS-4:
            window = [self.board[placement_row+i][column] for i in range(4)]
            score += self._evaluate_window(window)
            
        # Check diagonal potentials
        # Diagonal \
        for r, c in zip(range(max(0, placement_row-3), min(ROWS-3, placement_row+1)), 
                         range(max(0, column-3), min(COLUMNS-3, column+1))):
            window = [self.board[r+i][c+i] for i in range(4)]
            score += self._evaluate_window(window)
            
        # Diagonal /
        for r, c in zip(range(min(ROWS-1, placement_row+3), max(3, placement_row), -1),
                         range(max(0, column-3), min(COLUMNS-3, column+1))):
            window = [self.board[r-i][c+i] for i in range(4)]
            score += self._evaluate_window(window)
        
        # Prefer center columns
        center_preference = [1, 2, 3, 4, 3, 2, 1]  # Higher values for central columns
        score += center_preference[column]
        
        # Undo the move
        self.board[placement_row][column] = EMPTY
        
        # Restore original state
        self.start_time = start_time_backup
        self.current_player = current_player_backup
        
        return score
        
    def _evaluate_window(self, window):
        """
        Helper function to evaluate a window of 4 positions.
        Used by the moderate AI level.
        """
        score = 0
        # Count player tokens and empty spaces
        player_count = window.count(self.current_player)
        empty_count = window.count(EMPTY)
        opponent = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        opponent_count = window.count(opponent)
        
        if player_count == 4:
            score += 100  # Winning move
        elif player_count == 3 and empty_count == 1:
            score += 5  # Good potential
        elif player_count == 2 and empty_count == 2:
            score += 2  # Some potential
            
        # Prevent opponent from winning
        if opponent_count == 3 and empty_count == 1:
            score -= 10  # Block opponent's potential win
            
        return score

    def _choose_advanced_move(self):
        """
        Chooses the best move using advanced strategy and pattern learning.
        This AI uses all available information including past game data.
        """
        # If it's the first time we play, priority to the center
        if len(self.game_moves) <= 2 and self.board[0][COLUMNS // 2] == EMPTY:
            return COLUMNS // 2
            
        # Check if a move allows to win immediately
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                # Simulate the move to see if it leads to a victory
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = self.current_player
                        victory = self.check_victory()
                        self.board[row][col] = EMPTY  # Undo the move
                        if victory:
                            return col

        # Check if the opponent can win on the next move and block
        opponent = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        current_player_backup = self.current_player
        self.current_player = opponent  # Temporarily change to simulate
        
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                # Simulate the opponent's move to see if it leads to a victory
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = opponent
                        opponent_victory = self.check_victory()
                        self.board[row][col] = EMPTY  # Undo the move
                        if opponent_victory:
                            self.current_player = current_player_backup  # Restore
                            return col
                        break
        
        # Restore the current player
        self.current_player = current_player_backup
        
        # Analyze repetitive moves of the player
        player_moves = [move for i, move in enumerate(self.game_moves) if i % 2 == 0]  # Player moves (even)
        if len(player_moves) >= 2:
            last_moves_columns = [col for _, col in player_moves[-3:]]
            # If the player has played in the same column 2 or more times in the last 3 moves
            repeated_column = None
            for col in range(COLUMNS):
                if last_moves_columns.count(col) >= 2:
                    repeated_column = col
                    break
                    
            if repeated_column is not None:
                # Check if we can block this column or play right next to it
                for col in [repeated_column-1, repeated_column+1, repeated_column]:
                    if 0 <= col < COLUMNS and self.board[0][col] == EMPTY:
                        # Check if this move is safe (doesn't give a victory to the opponent)
                        if not self.move_gives_opponent_victory(col):
                            return col
        
        # Use learned patterns for evaluation
        if self.learned_patterns:
            pattern_opponent = 'X' if self.current_player == 'O' else 'O'
            if pattern_opponent in self.learned_patterns and self.learned_patterns[pattern_opponent]['frequence']:
                # Identify positions frequently used by the opponent
                frequent_positions = sorted(
                    self.learned_patterns[pattern_opponent]['frequence'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]  # Top 5 positions
                
                # Identify preferred columns of the opponent
                frequent_columns = {}
                for pos_str, freq in frequent_positions:
                    try:
                        # Extract the column from the position (format: "(row, column)")
                        import ast
                        pos = ast.literal_eval(pos_str)
                        if isinstance(pos, tuple) and len(pos) == 2:
                            _, col = pos
                            if 0 <= col < COLUMNS:
                                frequent_columns[col] = frequent_columns.get(col, 0) + freq
                    except:
                        continue
                
                # If we have identified frequent columns, try to block them
                if frequent_columns:
                    preferred_column = max(frequent_columns.items(), key=lambda x: x[1])[0]
                    if self.board[0][preferred_column] == EMPTY and not self.move_gives_opponent_victory(preferred_column):
                        return preferred_column
        
        # If no specific strategy was used, use advanced evaluation with learned patterns
        evaluations = {}
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:  # If the column is not full
                score = self.evaluate_move(col)
                evaluations[col] = score
                
        # Find the best score
        if not evaluations:
            return None
            
        best_score = max(evaluations.values())
        
        # Get all moves with the best score
        best_moves = [col for col, score in evaluations.items() if score == best_score]
        
        # Choose randomly among the best moves
        return random.choice(best_moves) if best_moves else None

    def move_gives_opponent_victory(self, column):
        """Check if playing in this column allows the opponent to win on the next move"""
        if column < 0 or column >= COLUMNS or self.board[0][column] != EMPTY:
            return True  # Invalid move
            
        # Find where the token will land
        placement_row = -1
        for row in range(ROWS-1, -1, -1):
            if self.board[row][column] == EMPTY:
                placement_row = row
                break
                
        if placement_row == -1:
            return True  # Column full
            
        # Place our token
        self.board[placement_row][column] = self.current_player
        
        # If it's the top row, the opponent can't play above
        if placement_row == 0:
            self.board[placement_row][column] = EMPTY
            return False
            
        # Otherwise, check if the opponent wins by playing above
        opponent = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
        self.board[placement_row-1][column] = opponent
        
        opponent_victory = self.check_victory()
        
        # Undo the moves
        self.board[placement_row-1][column] = EMPTY
        self.board[placement_row][column] = EMPTY
        
        return opponent_victory

    def end_game(self, winner):
        # Always ensure we have a valid start_time
        if not hasattr(self, 'start_time') or self.start_time is None:
            self.start_time = time.time() - 1  # Default to 1 second duration
            duration = 1.0
        else:
            try:
                duration = round(time.time() - self.start_time, 2)
            except TypeError:
                duration = 0
        
        # Add the game to statistics
        stats = self.stats_manager.ajouter_partie(winner, duration, self.game_moves)
        
        # Update learned patterns
        self.learned_patterns = self.stats_manager.analyze_victory_history()
        
        # Reset the moves of the game
        self.game_moves = []
        
        # Reset timer
        self.start_time = time.time()
        
        return stats

    def display_pattern_info(self):
        """Displays information about learned patterns for debugging"""
        if not self.learned_patterns:
            print("No learned patterns.")
            return
            
        print("----- LEARNED PATTERNS INFORMATION -----")
        for player in ['X', 'O']:
            if player in self.learned_patterns and self.learned_patterns[player]['frequence']:
                print(f"Player {player} - {len(self.learned_patterns[player]['coups'])} recorded moves")
                print(f"Frequent positions (top 5):")
                # Sort by frequency and display the top 5
                frequent_positions = sorted(
                    self.learned_patterns[player]['frequence'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                for pos, freq in frequent_positions:
                    print(f"  Position {pos}: used {freq} times")
            else:
                print(f"Player {player} - No learned patterns")
        print("-------------------------------------------------")