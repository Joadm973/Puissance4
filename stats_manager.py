import os
import pandas as pd
import csv

class CSVStatsManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_stats(self):
        """Load stats from CSV file"""
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def analyze_victory_history(self):
        """
        Analyzes victory history from the CSV file and returns patterns.
        """
        patterns = {}
        
        try:
            # Check if the history file exists
            if os.path.exists(self.file_path):
                data = pd.read_csv(self.file_path)
                
                if not data.empty:
                    # Example pattern analysis - adjust based on your actual data structure
                    if 'winning_column' in data.columns:
                        patterns['preferred_columns'] = data['winning_column'].value_counts().to_dict()
                    
                    # Initialize patterns structure for both players
                    patterns = {
                        'X': {'coups': [], 'frequence': {}},  # Player X patterns
                        'O': {'coups': [], 'frequence': {}}   # Player O patterns
                    }
                    
                    # Analyze each winning game
                    for _, row in data.iterrows():
                        if row['gagnant'] in ['X', 'O'] and 'coups' in row:
                            try:
                                # Convert from string to list if necessary
                                coups = row['coups']
                                
                                # Check coups type
                                if isinstance(coups, (float, int)) or coups == 'nan':
                                    continue
                                    
                                if isinstance(coups, str):
                                    try:
                                        import ast
                                        coups = ast.literal_eval(coups)
                                        if not isinstance(coups, list):
                                            continue
                                    except (SyntaxError, ValueError):
                                        print(f"Invalid coups format: {coups}")
                                        continue
                                
                                # Now we have a valid list, process the moves
                                patterns[row['gagnant']]['coups'].extend(coups)
                                
                                # Count frequency of winning positions
                                for coup in coups:
                                    pos = str(coup)  # Convert position to string for the key
                                    patterns[row['gagnant']]['frequence'][pos] = \
                                        patterns[row['gagnant']]['frequence'].get(pos, 0) + 1
                                        
                            except Exception as e:
                                print(f"Error analyzing moves: {e}")
        except Exception as e:
            print(f"Error analyzing victory history: {e}")
            
        return patterns