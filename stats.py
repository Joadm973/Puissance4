import json
import os
from datetime import datetime
import csv
import pandas as pd

class StatsManager:
    def __init__(self, filename="stats.json"):
        self.filename = filename
        self.stats = self.charger_stats()

    def charger_stats(self):
        """Charge les statistiques depuis le fichier JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.creer_stats_par_defaut()
        return self.creer_stats_par_defaut()

    def creer_stats_par_defaut(self):
        """Crée un dictionnaire de statistiques par défaut"""
        return {
            "parties_jouees": 0,
            "victoires_joueur": 0,
            "victoires_ia": 0,
            "matchs_nuls": 0,
            "historique": [],
            "derniere_mise_a_jour": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def sauvegarder_stats(self):
        """Sauvegarde les statistiques dans le fichier JSON"""
        self.stats["derniere_mise_a_jour"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, 'w') as f:
            json.dump(self.stats, f, indent=4)

    def ajouter_partie(self, gagnant, duree, coups=None):
        """Ajoute une nouvelle partie aux statistiques avec les coups joués"""
        nouvelle_partie = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gagnant": gagnant,
            "duree": duree
        }
        
        # Ajouter les coups si disponibles
        if coups:
            nouvelle_partie["coups"] = coups

        self.stats["parties_jouees"] += 1
        
        if gagnant == "X":
            self.stats["victoires_joueur"] += 1
        elif gagnant == "O":
            self.stats["victoires_ia"] += 1
        else:
            self.stats["matchs_nuls"] += 1

        # Ajouter à l'historique
        self.stats["historique"].append(nouvelle_partie)

        # Garder seulement les 100 dernières parties
        if len(self.stats["historique"]) > 100:
            self.stats["historique"] = self.stats["historique"][-100:]

        self.sauvegarder_stats()

    def get_statistiques(self):
        """Retourne les statistiques actuelles"""
        return {
            "parties_jouees": self.stats["parties_jouees"],
            "victoires_joueur": self.stats["victoires_joueur"],
            "victoires_ia": self.stats["victoires_ia"],
            "matchs_nuls": self.stats["matchs_nuls"],
            "pourcentage_victoires_joueur": round((self.stats["victoires_joueur"] / self.stats["parties_jouees"] * 100) if self.stats["parties_jouees"] > 0 else 0, 2),
            "pourcentage_victoires_ia": round((self.stats["victoires_ia"] / self.stats["parties_jouees"] * 100) if self.stats["parties_jouees"] > 0 else 0, 2),
            "pourcentage_matchs_nuls": round((self.stats["matchs_nuls"] / self.stats["parties_jouees"] * 100) if self.stats["parties_jouees"] > 0 else 0, 2),
            "derniere_mise_a_jour": self.stats["derniere_mise_a_jour"]
        }

    def get_historique(self, limit=10):
        """Retourne l'historique des parties (par défaut les 10 dernières)"""
        return self.stats["historique"][-limit:]

    def reinitialiser_stats(self):
        """Réinitialise toutes les statistiques"""
        self.stats = self.creer_stats_par_defaut()
        self.sauvegarder_stats()
        return self.stats 

    def analyser_historique_victoires(self):
        """Analyse l'historique des parties pour identifier les patterns gagnants"""
        historique = self.stats['historique']
        patterns = {
            'X': {'coups': [], 'frequence': {}},  # Patterns du joueur
            'O': {'coups': [], 'frequence': {}}   # Patterns de l'IA
        }
        
        # Analyser chaque partie gagnante
        for partie in historique:
            if partie['gagnant'] in ['X', 'O']:
                # Ajouter l'analyse des coups de cette partie
                if 'coups' in partie:  # Si les coups ont été enregistrés
                    try:
                        # Convertir de string à liste si nécessaire
                        coups = partie['coups']
                        
                        # Vérifier le type de coups
                        if isinstance(coups, (float, int)) or coups == 'nan':
                            # Skip this entry - it's a number or NaN, not a list
                            continue
                            
                        if isinstance(coups, str):
                            # Le format sera quelque chose comme "[(0, 1), (1, 2), ...]"
                            try:
                                import ast
                                coups = ast.literal_eval(coups)
                                # Vérifier que c'est bien une liste
                                if not isinstance(coups, list):
                                    continue
                            except (SyntaxError, ValueError):
                                # Si la conversion échoue, ignorer cette entrée
                                print(f"Format de coups invalide: {coups}")
                                continue
                        
                        # Maintenant que nous avons une liste valide, traiter les coups
                        patterns[partie['gagnant']]['coups'].extend(coups)
                        
                        # Compter la fréquence des positions gagnantes
                        for coup in coups:
                            pos = str(coup)  # Convertir la position en string pour la clé
                            patterns[partie['gagnant']]['frequence'][pos] = \
                                patterns[partie['gagnant']]['frequence'].get(pos, 0) + 1
                                
                    except Exception as e:
                        print(f"Erreur lors de l'analyse des coups: {e}, valeur: {partie.get('coups', 'Non défini')}")
        
        return patterns

class CSVStatsManager:
    def __init__(self, filename="stats.csv"):
        self.filename = filename
        self.stats = {
            'parties_jouées': 0,
            'victoires_joueur': 0,
            'victoires_ia': 0,
            'matchs_nuls': 0,
            'historique': []
        }
        self.charger_stats()
        
    def charger_stats(self):
        """Charge les statistiques depuis le fichier CSV"""
        if not os.path.exists(self.filename):
            # Créer le fichier CSV avec les en-têtes
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'gagnant', 'duree', 'coups'])
            return
            
        try:
            # Lire le fichier CSV avec pandas
            df = pd.read_csv(self.filename)
            
            # Mettre à jour les statistiques générales
            self.stats['parties_jouées'] = len(df)
            self.stats['victoires_joueur'] = len(df[df['gagnant'] == 'X'])
            self.stats['victoires_ia'] = len(df[df['gagnant'] == 'O'])
            self.stats['matchs_nuls'] = len(df[df['gagnant'] == 'N'])
            
            # Convertir l'historique en format liste
            self.stats['historique'] = df.to_dict('records')
            
        except Exception as e:
            print(f"Erreur lors du chargement des statistiques: {e}")
            # Recréer le fichier en cas d'erreur
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'gagnant', 'duree', 'coups'])
                
    def sauvegarder_stats(self):
        """Sauvegarde les statistiques dans le fichier CSV"""
        try:
            # Convertir l'historique en DataFrame
            df = pd.DataFrame(self.stats['historique'])
            
            # Sauvegarder dans le fichier CSV
            df.to_csv(self.filename, index=False)
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des statistiques: {e}")
            
    def ajouter_partie(self, gagnant, duree, coups=None):
        """Ajoute une nouvelle partie aux statistiques"""
        nouvelle_partie = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'gagnant': gagnant,
            'duree': duree
        }
        
        # Ajouter les coups si disponibles
        if coups:
            nouvelle_partie['coups'] = str(coups)  # Convertir la liste en string pour CSV
        
        self.stats['historique'].append(nouvelle_partie)
        self.stats['parties_jouées'] += 1
        
        if gagnant == 'X':
            self.stats['victoires_joueur'] += 1
        elif gagnant == 'O':
            self.stats['victoires_ia'] += 1
        else:
            self.stats['matchs_nuls'] += 1
            
        self.sauvegarder_stats()
        return self.get_statistiques()
        
    def get_statistiques(self):
        """Retourne les statistiques générales"""
        return {
            'parties_jouées': self.stats['parties_jouées'],
            'victoires_joueur': self.stats['victoires_joueur'],
            'victoires_ia': self.stats['victoires_ia'],
            'matchs_nuls': self.stats['matchs_nuls'],
            'pourcentage_victoires_joueur': round((self.stats['victoires_joueur'] / self.stats['parties_jouées'] * 100) if self.stats['parties_jouées'] > 0 else 0, 1),
            'pourcentage_victoires_ia': round((self.stats['victoires_ia'] / self.stats['parties_jouées'] * 100) if self.stats['parties_jouées'] > 0 else 0, 1),
            'pourcentage_matchs_nuls': round((self.stats['matchs_nuls'] / self.stats['parties_jouées'] * 100) if self.stats['parties_jouées'] > 0 else 0, 1)
        }
        
    def get_historique(self, n=10):
        """Retourne les n dernières parties"""
        return self.stats['historique'][-n:] if n > 0 else self.stats['historique']
        
    def reinitialiser_stats(self):
        """Réinitialise toutes les statistiques"""
        self.stats = {
            'parties_jouées': 0,
            'victoires_joueur': 0,
            'victoires_ia': 0,
            'matchs_nuls': 0,
            'historique': []
        }
        self.sauvegarder_stats()
        
    def analyser_historique_victoires(self):
        """Analyse l'historique des parties pour identifier les patterns gagnants"""
        historique = self.stats['historique']
        patterns = {
            'X': {'coups': [], 'frequence': {}},  # Patterns du joueur
            'O': {'coups': [], 'frequence': {}}   # Patterns de l'IA
        }
        
        # Analyser chaque partie gagnante
        for partie in historique:
            if partie['gagnant'] in ['X', 'O']:
                # Ajouter l'analyse des coups de cette partie
                if 'coups' in partie:  # Si les coups ont été enregistrés
                    try:
                        # Convertir de string à liste si nécessaire
                        coups = partie['coups']
                        
                        # Vérifier le type de coups
                        if isinstance(coups, (float, int)) or coups == 'nan':
                            # Skip this entry - it's a number or NaN, not a list
                            continue
                            
                        if isinstance(coups, str):
                            # Le format sera quelque chose comme "[(0, 1), (1, 2), ...]"
                            try:
                                import ast
                                coups = ast.literal_eval(coups)
                                # Vérifier que c'est bien une liste
                                if not isinstance(coups, list):
                                    continue
                            except (SyntaxError, ValueError):
                                # Si la conversion échoue, ignorer cette entrée
                                print(f"Format de coups invalide: {coups}")
                                continue
                        
                        # Maintenant que nous avons une liste valide, traiter les coups
                        patterns[partie['gagnant']]['coups'].extend(coups)
                        
                        # Compter la fréquence des positions gagnantes
                        for coup in coups:
                            pos = str(coup)  # Convertir la position en string pour la clé
                            patterns[partie['gagnant']]['frequence'][pos] = \
                                patterns[partie['gagnant']]['frequence'].get(pos, 0) + 1
                                
                    except Exception as e:
                        print(f"Erreur lors de l'analyse des coups: {e}, valeur: {partie.get('coups', 'Non défini')}")
        
        return patterns