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
        self.mode_ia_vs_ia = False  # Nouveau mode IA vs IA
        # Update to use CSVStatsManager
        self.stats_manager = CSVStatsManager()
        self.temps_debut = time.time()
        self.coups_partie = []  # Pour enregistrer les coups de la partie en cours
        # Charger immédiatement les patterns appris des parties précédentes
        self.patterns_appris = self.stats_manager.analyser_historique_victoires()
        self.reinitialiser_jeu()

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
                    if self.joueur_actuel in patterns and pos in patterns[self.joueur_actuel]['frequence']:
                        bonus = patterns[self.joueur_actuel]['frequence'][pos] * 0.5
                        score += bonus
                        
                    # Malus si la position est souvent gagnante pour l'adversaire
                    adversaire = 'X' if self.joueur_actuel == 'O' else 'O'
                    if adversaire in patterns and pos in patterns[adversaire]['frequence']:
                        malus = patterns[adversaire]['frequence'][pos] * 0.8
                        score -= malus
                        
        # Vérifier les alignements partiels qui ont souvent conduit à des victoires
        for ligne in range(LIGNES-1):
            for col in range(COLONNES-1):
                if (self.plateau[ligne][col] == self.joueur_actuel and 
                    self.plateau[ligne+1][col] == self.joueur_actuel):
                    # Alignement vertical de 2
                    score += 2
                    
                if (col < COLONNES-2 and self.plateau[ligne][col] == self.joueur_actuel and 
                    self.plateau[ligne][col+1] == self.joueur_actuel):
                    # Alignement horizontal de 2
                    score += 2
                    
                if (ligne < LIGNES-2 and col < COLONNES-2 and 
                    self.plateau[ligne][col] == self.joueur_actuel and 
                    self.plateau[ligne+1][col+1] == self.joueur_actuel):
                    # Alignement diagonal \ de 2
                    score += 2
                    
                if (ligne > 0 and col < COLONNES-2 and ligne < LIGNES-1 and
                    self.plateau[ligne][col] == self.joueur_actuel and 
                    self.plateau[ligne-1][col+1] == self.joueur_actuel):
                    # Alignement diagonal / de 2
                    score += 2
        
        return score

    def choisir_meilleur_coup(self):
        """Choisit le meilleur coup pour l'IA en tenant compte des coups répétitifs de l'adversaire"""
        # Si c'est la première fois qu'on joue, priorité au centre
        if len(self.coups_partie) <= 2 and self.plateau[0][COLONNES // 2] == VIDE:
            return COLONNES // 2
            
        # Vérifier si un coup permet de gagner immédiatement
        for col in range(COLONNES):
            if self.plateau[0][col] == VIDE:  # Si la colonne n'est pas pleine
                # Simuler le coup pour voir s'il permet de gagner
                for ligne in range(LIGNES-1, -1, -1):
                    if self.plateau[ligne][col] == VIDE:
                        self.plateau[ligne][col] = self.joueur_actuel
                        victoire = self.verifier_victoire()
                        self.plateau[ligne][col] = VIDE  # Annuler le coup
                        if victoire:
                            return col

        # Vérifier si l'adversaire peut gagner au prochain coup et bloquer
        adversaire = JOUEUR_X if self.joueur_actuel == JOUEUR_O else JOUEUR_O
        joueur_actuel_backup = self.joueur_actuel
        self.joueur_actuel = adversaire  # Changer temporairement pour simuler
        
        for col in range(COLONNES):
            if self.plateau[0][col] == VIDE:  # Si la colonne n'est pas pleine
                # Simuler le coup de l'adversaire pour voir s'il permet de gagner
                for ligne in range(LIGNES-1, -1, -1):
                    if self.plateau[ligne][col] == VIDE:
                        self.plateau[ligne][col] = adversaire
                        victoire_adversaire = self.verifier_victoire()
                        self.plateau[ligne][col] = VIDE  # Annuler le coup
                        if victoire_adversaire:
                            self.joueur_actuel = joueur_actuel_backup  # Restaurer
                            return col
                        break
        
        # Restaurer le joueur actuel
        self.joueur_actuel = joueur_actuel_backup
        
        # Analyser les coups répétitifs du joueur
        coups_joueur = [coup for i, coup in enumerate(self.coups_partie) if i % 2 == 0]  # Coups du joueur (pairs)
        if len(coups_joueur) >= 2:
            derniers_coups_colonnes = [col for _, col in coups_joueur[-3:]]
            # Si le joueur a joué dans la même colonne 2 fois ou plus sur les 3 derniers coups
            colonne_repetee = None
            for col in range(COLONNES):
                if derniers_coups_colonnes.count(col) >= 2:
                    colonne_repetee = col
                    break
                    
            if colonne_repetee is not None:
                # Vérifier si nous pouvons bloquer cette colonne ou jouer juste à côté
                for col in [colonne_repetee-1, colonne_repetee+1, colonne_repetee]:
                    if 0 <= col < COLONNES and self.plateau[0][col] == VIDE:
                        # Vérifier si ce coup est sûr (ne donne pas une victoire à l'adversaire)
                        if not self.coup_donne_victoire_adversaire(col):
                            return col
        
        # Utiliser les patterns appris pour l'évaluation
        if self.patterns_appris:
            pattern_adversaire = 'X' if self.joueur_actuel == JOUEUR_O else 'O'
            if pattern_adversaire in self.patterns_appris and self.patterns_appris[pattern_adversaire]['frequence']:
                # Identifier les positions fréquemment utilisées par l'adversaire
                positions_frequentes = sorted(
                    self.patterns_appris[pattern_adversaire]['frequence'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]  # Top 5 des positions
                
                # Identifier les colonnes préférées de l'adversaire
                colonnes_frequentes = {}
                for pos_str, freq in positions_frequentes:
                    try:
                        # Extraire la colonne de la position (format: "(ligne, colonne)")
                        import ast
                        pos = ast.literal_eval(pos_str)
                        if isinstance(pos, tuple) and len(pos) == 2:
                            _, col = pos
                            if 0 <= col < COLONNES:
                                colonnes_frequentes[col] = colonnes_frequentes.get(col, 0) + freq
                    except:
                        continue
                
                # Si nous avons identifié des colonnes fréquentes, essayer de les bloquer
                if colonnes_frequentes:
                    colonne_preferee = max(colonnes_frequentes.items(), key=lambda x: x[1])[0]
                    if self.plateau[0][colonne_preferee] == VIDE and not self.coup_donne_victoire_adversaire(colonne_preferee):
                        return colonne_preferee
        
        # Si aucune stratégie spécifique n'a été utilisée, utiliser l'évaluation classique
        evaluations = {}
        for col in range(COLONNES):
            if self.plateau[0][col] == VIDE:  # Si la colonne n'est pas pleine
                score = self.evaluer_coup(col)
                evaluations[col] = score
                
        # Trouve le meilleur score
        if not evaluations:
            return None
            
        meilleur_score = max(evaluations.values())
        
        # Récupère tous les coups avec le meilleur score
        meilleurs_coups = [col for col, score in evaluations.items() if score == meilleur_score]
        
        # Choisit aléatoirement parmi les meilleurs coups
        return random.choice(meilleurs_coups) if meilleurs_coups else None

    def coup_donne_victoire_adversaire(self, colonne):
        """Vérifie si jouer dans cette colonne permet à l'adversaire de gagner au coup suivant"""
        if colonne < 0 or colonne >= COLONNES or self.plateau[0][colonne] != VIDE:
            return True  # Coup invalide
            
        # Trouver où le jeton va atterrir
        ligne_placement = -1
        for ligne in range(LIGNES-1, -1, -1):
            if self.plateau[ligne][colonne] == VIDE:
                ligne_placement = ligne
                break
                
        if ligne_placement == -1:
            return True  # Colonne pleine
            
        # Placer notre jeton
        self.plateau[ligne_placement][colonne] = self.joueur_actuel
        
        # Si c'est la ligne du haut, l'adversaire ne peut pas jouer au-dessus
        if ligne_placement == 0:
            self.plateau[ligne_placement][colonne] = VIDE
            return False
            
        # Sinon, vérifier si l'adversaire gagne en jouant au-dessus
        adversaire = JOUEUR_X if self.joueur_actuel == JOUEUR_O else JOUEUR_O
        self.plateau[ligne_placement-1][colonne] = adversaire
        
        victoire_adversaire = self.verifier_victoire()
        
        # Annuler les coups
        self.plateau[ligne_placement-1][colonne] = VIDE
        self.plateau[ligne_placement][colonne] = VIDE
        
        return victoire_adversaire

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

    def afficher_info_patterns(self):
        """Affiche des informations sur les patterns appris pour le débogage"""
        if not self.patterns_appris:
            print("Aucun pattern appris.")
            return
            
        print("----- INFORMATIONS SUR LES PATTERNS APPRIS -----")
        for joueur in ['X', 'O']:
            if joueur in self.patterns_appris and self.patterns_appris[joueur]['frequence']:
                print(f"Joueur {joueur} - {len(self.patterns_appris[joueur]['coups'])} coups enregistrés")
                print(f"Positions fréquentes (top 5):")
                # Trier par fréquence et afficher les 5 premières
                positions_frequentes = sorted(
                    self.patterns_appris[joueur]['frequence'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                for pos, freq in positions_frequentes:
                    print(f"  Position {pos}: utilisée {freq} fois")
            else:
                print(f"Joueur {joueur} - Aucun pattern appris")
        print("-------------------------------------------------")