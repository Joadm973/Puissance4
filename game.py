import time
import random
import json
from datetime import datetime
from constants import *
# Fix the import statement to use CSVStatsManager instead of StatsManager
from stats import CSVStatsManager

class Puissance4:
    def __init__(self):
        # Initialize the game state
        self.scores = {JOUEUR_X: 0, JOUEUR_O: 0}
        self.mode_ia = False
        # Update to use CSVStatsManager
        self.stats_manager = CSVStatsManager()
        self.temps_debut = time.time()
        self.reinitialiser_jeu()
        self.coups_partie = []  # Pour enregistrer les coups de la partie en cours
        self.patterns_appris = None  # Pour stocker les patterns appris

    def reinitialiser_jeu(self):
        # Create an empty board
        self.plateau = []
        for _ in range(LIGNES):
            ligne = [VIDE] * COLONNES
            self.plateau.append(ligne)
        
        # Initialize game state
        self.joueur_actuel = JOUEUR_X
        # Always make sure temps_debut is set
        if not hasattr(self, 'temps_debut') or self.temps_debut is None:
            self.temps_debut = time.time()
        self.coups_partie = []  # Réinitialiser les coups de la partie

    def placer_jeton(self, colonne):
        """Place un jeton dans la colonne spécifiée"""
        # Make sure temps_debut is always set before any game-changing action
        if not hasattr(self, 'temps_debut') or self.temps_debut is None:
            self.temps_debut = time.time()
            
        if colonne < 0 or colonne >= COLONNES:
            return False
            
        for ligne in range(LIGNES-1, -1, -1):
            if self.plateau[ligne][colonne] == VIDE:
                self.plateau[ligne][colonne] = self.joueur_actuel
                # Enregistrer le coup
                self.coups_partie.append((ligne, colonne))
                
                # Vérifier si ce coup mène à une victoire
                if self.verifier_victoire():
                    return 'victoire'
                    
                # Vérifier si le plateau est plein
                if self.plateau_plein():
                    return 'nul'
                    
                return True
                
        return False

    def verifier_victoire(self):
        # Vérification horizontale
        for ligne in range(LIGNES):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne][col + 1] == 
                    self.plateau[ligne][col + 2] == self.plateau[ligne][col + 3]):
                    return True

        # Vérification verticale
        for ligne in range(LIGNES - 3):
            for col in range(COLONNES):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne + 1][col] == 
                    self.plateau[ligne + 2][col] == self.plateau[ligne + 3][col]):
                    return True

        # Vérification diagonale (/)
        for ligne in range(3, LIGNES):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne - 1][col + 1] == 
                    self.plateau[ligne - 2][col + 2] == self.plateau[ligne - 3][col + 3]):
                    return True

        # Vérification diagonale (\)
        for ligne in range(LIGNES - 3):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne + 1][col + 1] == 
                    self.plateau[ligne + 2][col + 2] == self.plateau[ligne + 3][col + 3]):
                    return True

        return False

    def trouver_jetons_gagnants(self):
        """Retourne les coordonnées des 4 jetons gagnants"""
        # Vérification horizontale
        for ligne in range(LIGNES):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne][col + 1] == 
                    self.plateau[ligne][col + 2] == self.plateau[ligne][col + 3]):
                    return [(ligne, col + i) for i in range(4)]

        # Vérification verticale
        for ligne in range(LIGNES - 3):
            for col in range(COLONNES):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne + 1][col] == 
                    self.plateau[ligne + 2][col] == self.plateau[ligne + 3][col]):
                    return [(ligne + i, col) for i in range(4)]

        # Vérification diagonale (/)
        for ligne in range(3, LIGNES):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne - 1][col + 1] == 
                    self.plateau[ligne - 2][col + 2] == self.plateau[ligne - 3][col + 3]):
                    return [(ligne - i, col + i) for i in range(4)]

        # Vérification diagonale (\)
        for ligne in range(LIGNES - 3):
            for col in range(COLONNES - 3):
                if (self.plateau[ligne][col] != VIDE and
                    self.plateau[ligne][col] == self.plateau[ligne + 1][col + 1] == 
                    self.plateau[ligne + 2][col + 2] == self.plateau[ligne + 3][col + 3]):
                    return [(ligne + i, col + i) for i in range(4)]

        return []

    def plateau_plein(self):
        return all(case != VIDE for ligne in self.plateau for case in ligne)

    def changer_joueur(self):
        self.joueur_actuel = JOUEUR_O if self.joueur_actuel == JOUEUR_X else JOUEUR_X

    def incrementer_score(self):
        self.scores[self.joueur_actuel] += 1
        return self.scores[self.joueur_actuel]

    def evaluer_coup(self, colonne):
        """Évalue un coup potentiel"""
        # Save the current state including temps_debut
        temps_debut_backup = self.temps_debut
        joueur_actuel_backup = self.joueur_actuel
        
        if not self.placer_jeton(colonne):
            self.temps_debut = temps_debut_backup  # Restore temps_debut
            return float('-inf')
            
        score = 0
        self.changer_joueur()
        
        # Vérifie si le coup mène à une victoire
        if self.verifier_victoire():
            score = 100
        else:
            # Évalue la position
            score = self.evaluer_position()
            
        # Annule le coup
        for ligne in range(LIGNES):
            if self.plateau[ligne][colonne] != VIDE:
                self.plateau[ligne][colonne] = VIDE
                break
                
        # IMPORTANT: Restore the original state including temps_debut
        self.temps_debut = temps_debut_backup
        self.joueur_actuel = joueur_actuel_backup
        
        return score

    def evaluer_position(self):
        """Évalue la position actuelle du plateau en tenant compte des patterns appris"""
        score = 0
        
        # Évaluation de base
        score += self._evaluer_position_base()
        
        # Bonus pour les patterns appris
        if self.patterns_appris:
            score += self._evaluer_patterns_appris()
        
        return score

    def _evaluer_position_base(self):
        """Évaluation de base de la position"""
        score = 0
        # Centre du plateau (priorité)
        centre = COLONNES // 2
        for ligne in range(LIGNES):
            if self.plateau[ligne][centre] == self.joueur_actuel:
                score += 3
                
        # Vérifie les alignements de 3
        for ligne in range(LIGNES):
            for col in range(COLONNES-2):
                if (self.plateau[ligne][col] == self.joueur_actuel and
                    self.plateau[ligne][col+1] == self.joueur_actuel and
                    self.plateau[ligne][col+2] == self.joueur_actuel):
                    score += 5
                    
        return score

    def _evaluer_patterns_appris(self):
        """Évalue la position en fonction des patterns appris"""
        score = 0
        patterns = self.patterns_appris
        
        if not patterns:
            return score
            
        # Vérifier si la position actuelle correspond à des patterns gagnants connus
        for ligne in range(LIGNES):
            for col in range(COLONNES):
                if self.plateau[ligne][col] == self.joueur_actuel:
                    pos = str((ligne, col))
                    # Bonus basé sur la fréquence du pattern
                    if pos in patterns[self.joueur_actuel]['frequence']:
                        score += patterns[self.joueur_actuel]['frequence'][pos] * 0.5
                        
                    # Malus si la position est souvent gagnante pour l'adversaire
                    adversaire = 'X' if self.joueur_actuel == 'O' else 'O'
                    if pos in patterns[adversaire]['frequence']:
                        score -= patterns[adversaire]['frequence'][pos] * 0.3
        
        return score

    def choisir_meilleur_coup(self):
        """Choisit le meilleur coup pour l'IA"""
        # Dictionnaire pour stocker les évaluations des coups
        evaluations = {}
        
        # Évalue chaque colonne possible
        for col in range(COLONNES):
            if self.plateau[0][col] == VIDE:  # Si la colonne n'est pas pleine
                score = self.evaluer_coup(col)
                evaluations[col] = score
                
        # Trouve le meilleur score
        meilleur_score = max(evaluations.values()) if evaluations else float('-inf')
        
        # Récupère tous les coups avec le meilleur score
        meilleurs_coups = [col for col, score in evaluations.items() if score == meilleur_score]
        
        # Choisit aléatoirement parmi les meilleurs coups
        return random.choice(meilleurs_coups) if meilleurs_coups else None

    def fin_partie(self, gagnant):
        # Always ensure we have a valid temps_debut
        if not hasattr(self, 'temps_debut') or self.temps_debut is None:
            self.temps_debut = time.time() - 1  # Default to 1 second duration
            duree = 1.0
        else:
            try:
                duree = round(time.time() - self.temps_debut, 2)
            except TypeError:
                duree = 0
        
        # Use the correct method name for CSVStatsManager
        stats = self.stats_manager.ajouter_partie(gagnant, duree, self.coups_partie)  # Changed from enregistrer_partie
        
        # Mettre à jour les patterns appris
        self.patterns_appris = self.stats_manager.analyser_historique_victoires()
        
        # Réinitialiser les coups de la partie
        self.coups_partie = []
        
        # Reset timer
        self.temps_debut = time.time()
        
        return stats