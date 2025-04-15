import tkinter as tk
from tkinter import messagebox, ttk
import random
import traceback
from constants import *
from game import Puissance4
from visualisation import VisualisationStats

class Puissance4GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        self.window.configure(bg=COULEURS['fond'])
        
        # Style global
        style = ttk.Style()
        style.configure('TButton', **STYLE_BOUTON)
        style.configure('TLabel', **STYLE_LABEL)
        
        self.jeu = Puissance4()
        # Initialisons temps_debut lors de la création de l'instance
        import time
        self.jeu.temps_debut = time.time()
        self.visualisation = VisualisationStats(self.jeu.stats_manager)
        
        # Frame principale avec ombre
        self.frame_principal = tk.Frame(self.window, bg=COULEURS['fond'], padx=30, pady=30)
        self.frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # Titre du jeu
        self.label_titre = tk.Label(
            self.frame_principal,
            text="PUISSANCE 4",
            **STYLE_TITRE
        )
        self.label_titre.pack(pady=(0, 20))
        
        # Frame pour le score et les stats avec fond légèrement plus clair
        self.frame_score = tk.Frame(
            self.frame_principal,
            bg=COULEURS['fond_stats'],
            padx=20,
            pady=15,
            relief='flat',
            borderwidth=1
        )
        self.frame_score.pack(fill=tk.X, pady=(0, 20))
        
        # Labels pour le score avec style amélioré
        score_x_style = STYLE_LABEL.copy()
        score_x_style['fg'] = COULEURS[JOUEUR_X]
        self.label_score_x = tk.Label(
            self.frame_score,
            text=f"Joueur {JOUEUR_X}: 0",
            **score_x_style
        )
        self.label_score_x.pack(side=tk.LEFT, padx=20)
        
        score_o_style = STYLE_LABEL.copy()
        score_o_style['fg'] = COULEURS[JOUEUR_O]
        self.label_score_o = tk.Label(
            self.frame_score,
            text=f"Joueur {JOUEUR_O}: 0",
            **score_o_style
        )
        self.label_score_o.pack(side=tk.LEFT, padx=20)

        # Frame pour les boutons d'action
        self.frame_actions = tk.Frame(self.frame_score, bg=COULEURS['fond_stats'])
        self.frame_actions.pack(side=tk.RIGHT, padx=20)

        # Bouton Statistiques avec icône
        self.bouton_stats = tk.Button(
            self.frame_actions,
            text="📊 Statistiques",
            command=self.afficher_stats,
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['bouton'],
            activebackground=COULEURS['bouton_hover'],
            activeforeground=COULEURS['fond']
        )
        self.bouton_stats.pack(side=tk.LEFT, padx=5)
        
        # Bouton Graphiques avec icône
        self.bouton_graphiques = tk.Button(
            self.frame_actions,
            text="📈 Graphiques",
            command=lambda: self.visualisation.afficher_graphiques(self.window),
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['bouton'],
            activebackground=COULEURS['bouton_hover'],
            activeforeground=COULEURS['fond']
        )
        self.bouton_graphiques.pack(side=tk.LEFT, padx=5)
        
        # Bouton Réinitialiser Stats avec icône
        self.bouton_reset_stats = tk.Button(
            self.frame_actions,
            text="🔄 Réinitialiser",
            command=self.confirmer_reinitialisation_stats,
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['warning'],
            activebackground='#C0392B',
            activeforeground=COULEURS['fond']
        )
        self.bouton_reset_stats.pack(side=tk.LEFT, padx=5)
        
        # Label pour le joueur actuel avec style amélioré
        self.label_joueur = tk.Label(
            self.frame_principal,
            text=f"Tour du Joueur {self.jeu.joueur_actuel}",
            **STYLE_SOUS_TITRE
        )
        self.label_joueur.pack(pady=(0, 10))
        
        # Création du canvas avec style amélioré
        self.canvas = tk.Canvas(
            self.frame_principal,
            width=COLONNES * TAILLE_CASE,
            height=LIGNES * TAILLE_CASE,
            **STYLE_CANVAS
        )
        self.canvas.pack()
        
        # Frame pour les boutons de contrôle
        self.frame_controles = tk.Frame(
            self.frame_principal,
            bg=COULEURS['fond'],
            padx=20,
            pady=20
        )
        self.frame_controles.pack(pady=20)
        
        # Bouton Nouvelle Partie avec icône
        self.bouton_nouvelle_partie = tk.Button(
            self.frame_controles,
            text="🆕 Nouvelle Partie",
            command=self.reinitialiser_jeu,
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['bouton'],
            activebackground=COULEURS['bouton_hover'],
            activeforeground=COULEURS['fond']
        )
        self.bouton_nouvelle_partie.pack(side=tk.LEFT, padx=10)
        
        # Bouton Mode IA avec icône
        self.bouton_mode_ia = tk.Button(
            self.frame_controles,
            text="🤖 Mode IA",
            command=self.changer_mode_ia,
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['bouton'],
            activebackground=COULEURS['bouton_hover'],
            activeforeground=COULEURS['fond']
        )
        self.bouton_mode_ia.pack(side=tk.LEFT, padx=10)
        
        # Bouton Quitter avec icône
        self.bouton_quitter = tk.Button(
            self.frame_controles,
            text="🚪 Quitter",
            command=self.window.quit,
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['warning'],
            activebackground='#C0392B',
            activeforeground=COULEURS['fond']
        )
        self.bouton_quitter.pack(side=tk.LEFT, padx=10)
        
        # Dessiner le plateau initial
        self.dessiner_plateau()
        
        # Bindings
        self.canvas.bind('<Button-1>', self.gerer_clic)
        self.canvas.bind('<Motion>', self.gerer_survol)
        
        # Centrer la fenêtre
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def dessiner_plateau(self):
        self.canvas.delete("all")
        
        # Dessiner le fond du plateau
        self.canvas.create_rectangle(
            0, 0,
            COLONNES * TAILLE_CASE, LIGNES * TAILLE_CASE,
            fill=COULEURS['plateau'],
            outline=COULEURS['bordure'],
            width=2
        )
        
        # Initialiser le tableau pour stocker les références des cases
        self.cases = []
        
        for ligne in range(LIGNES):
            ligne_cases = []
            for col in range(COLONNES):
                x1 = col * TAILLE_CASE
                y1 = ligne * TAILLE_CASE
                x2 = x1 + TAILLE_CASE
                y2 = y1 + TAILLE_CASE
                
                # Dessiner les cases avec ombre
                case = self.canvas.create_oval(
                    x1 + 5, y1 + 5,
                    x2 - 5, y2 - 5,
                    fill=COULEURS[self.jeu.plateau[ligne][col]],
                    outline=COULEURS['bordure'],
                    width=1
                )
                ligne_cases.append(case)
            self.cases.append(ligne_cases)

    def gerer_survol(self, event):
        colonne = event.x // TAILLE_CASE
        if 0 <= colonne < COLONNES:
            # Effacer le plateau
            self.dessiner_plateau()
            
            # Dessiner l'indicateur de survol
            x1 = colonne * TAILLE_CASE
            y1 = 0
            x2 = x1 + TAILLE_CASE
            y2 = TAILLE_CASE
            
            self.canvas.create_oval(
                x1 + 5, y1 + 5,
                x2 - 5, y2 - 5,
                fill=COULEURS['hover'],
                outline=COULEURS[self.jeu.joueur_actuel]
            )

    def gerer_clic(self, event):
        """Gère le clic sur le canvas"""
        # Si c'est le tour de l'IA, on ne permet pas au joueur de jouer
        if self.jeu.joueur_actuel == JOUEUR_O and self.jeu.mode_ia:
            return
            
        colonne = event.x // TAILLE_CASE
        
        # Always ensure temps_debut is set before potentially ending the game
        import time
        if not hasattr(self.jeu, 'temps_debut') or self.jeu.temps_debut is None:
            self.jeu.temps_debut = time.time()
            
        resultat = self.jeu.placer_jeton(colonne)
        
        if resultat == 'victoire':
            self.jeu.incrementer_score()
            self.mettre_a_jour_score()  # Mettre à jour le score
            self.dessiner_plateau()
            self.mettre_a_jour_interface()
            # On met à jour l'affichage immédiatement
            self.window.update()
            # Mettre en évidence les jetons gagnants avant d'afficher le message
            self.mettre_en_evidence_victoire()
            return
            
        elif resultat == 'nul':
            self.dessiner_plateau()
            self.mettre_a_jour_interface()
            # On met à jour l'affichage immédiatement
            self.window.update()
            
            # On attend un court instant avant d'afficher le message
            self.window.after(500, lambda: self.fin_partie_avec_message('N'))
            return
            
        elif resultat:
            self.jeu.changer_joueur()
            self.dessiner_plateau()
            self.mettre_a_jour_interface()
            
            # Tour de l'IA - on ajoute un délai de 1 seconde
            if self.jeu.joueur_actuel == JOUEUR_O and self.jeu.mode_ia:
                # Désactiver les événements pendant que l'IA réfléchit
                self.canvas.unbind('<Button-1>')
                # Mettre à jour le label pour montrer que l'IA réfléchit
                self.label_joueur.config(text="L'IA réfléchit... 🤔")
                # Appeler jouer_coup_ia après 1 seconde
                self.window.after(1000, self.jouer_coup_ia)

    def jouer_coup_ia(self):
        """Fait jouer l'IA"""
        try:
            # Always ensure temps_debut is set before the AI plays
            import time
            if not hasattr(self.jeu, 'temps_debut') or self.jeu.temps_debut is None:
                self.jeu.temps_debut = time.time()
                
            colonne = self.jeu.choisir_meilleur_coup()
            if colonne is not None:
                resultat = self.jeu.placer_jeton(colonne)
                
                if resultat == 'victoire':
                    self.jeu.incrementer_score()
                    self.mettre_a_jour_score()  # Mettre à jour le score
                    self.dessiner_plateau()
                    self.mettre_a_jour_interface()
                    # On met à jour l'affichage immédiatement
                    self.window.update()
                    # Mettre en évidence les jetons gagnants avant d'afficher le message
                    self.mettre_en_evidence_victoire()
                    return
                    
                elif resultat == 'nul':
                    self.dessiner_plateau()
                    self.mettre_a_jour_interface()
                    # On met à jour l'affichage immédiatement
                    self.window.update()
                    
                    # On attend un court instant avant d'afficher le message
                    self.window.after(500, lambda: self.fin_partie_avec_message('N'))
                    return
                    
                elif resultat:
                    self.jeu.changer_joueur()
                    self.dessiner_plateau()
                    self.mettre_a_jour_interface()
        finally:
            # Réactiver les événements après le coup de l'IA
            self.canvas.bind('<Button-1>', self.gerer_clic)
            # Remettre à jour le label du joueur
            self.label_joueur.config(text=f"Tour du Joueur {self.jeu.joueur_actuel}")

    def mettre_en_evidence_victoire(self):
        """Met en évidence les jetons gagnants"""
        jetons_gagnants = self.jeu.trouver_jetons_gagnants()
        couleur_originale = COULEURS[self.jeu.joueur_actuel]
        outline_original = COULEURS['bordure']
        
        def animation_clignotement(compteur=0):
            if compteur < 6:  # 3 clignotements (6 changements)
                # Alterner entre les couleurs
                fill_color = '#FFD700' if compteur % 2 == 0 else couleur_originale  # Or vif
                outline_color = '#FF4500' if compteur % 2 == 0 else outline_original  # Orange-rouge
                width = 3 if compteur % 2 == 0 else 1  # Épaisseur du contour
                
                for ligne, col in jetons_gagnants:
                    self.canvas.itemconfig(
                        self.cases[ligne][col],
                        fill=fill_color,
                        outline=outline_color,
                        width=width
                    )
                self.canvas.update()
                # Programmer le prochain changement dans 300ms
                self.window.after(200, lambda: animation_clignotement(compteur + 1))
            else:
                # Animation terminée, afficher le message de victoire
                self.window.after(100, lambda: self.fin_partie_avec_message(self.jeu.joueur_actuel))
        
        # Démarrer l'animation
        animation_clignotement()

    def fin_partie_avec_message(self, gagnant):
        """Gère la fin de partie avec message après un délai"""
        try:
            stats = self.jeu.fin_partie(gagnant)
            if gagnant == 'N':
                messagebox.showinfo("Fin de partie", "Match nul !")
            else:
                message = "L'IA a gagné !" if (self.jeu.mode_ia and gagnant == JOUEUR_O) else f"Le joueur {gagnant} a gagné !"
                messagebox.showinfo("Fin de partie", message)
        except Exception as e:
            print(f"Error in fin_partie: {e}")
            print(traceback.format_exc())
        finally:
            self.reinitialiser_jeu()

    def changer_mode_ia(self):
        self.jeu.mode_ia = not self.jeu.mode_ia
        self.bouton_mode_ia.config(
            text="Mode IA: Activé" if self.jeu.mode_ia else "Mode IA: Désactivé",
            bg='#2980B9' if self.jeu.mode_ia else COULEURS['bouton']
        )

    def mettre_a_jour_score(self):
        self.label_score_x.config(text=f"Joueur {JOUEUR_X}: {self.jeu.scores[JOUEUR_X]}")
        self.label_score_o.config(text=f"Joueur {JOUEUR_O}: {self.jeu.scores[JOUEUR_O]}")

    def reinitialiser_jeu(self):
        # Always make sure temps_debut is set to the current time before resetting
        import time
        self.jeu.temps_debut = time.time()
        
        # Now reset the game
        self.jeu.reinitialiser_jeu()
        
        # Verify temps_debut is still set after resetting
        if not hasattr(self.jeu, 'temps_debut') or self.jeu.temps_debut is None:
            self.jeu.temps_debut = time.time()
            
        self.label_joueur.config(text=f"Tour du Joueur {self.jeu.joueur_actuel}")
        self.dessiner_plateau()

    def confirmer_reinitialisation_stats(self):
        """Demande confirmation avant de réinitialiser les statistiques"""
        if messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir réinitialiser toutes les statistiques ?\nCette action est irréversible.",
            icon='warning'
        ):
            self.jeu.stats_manager.reinitialiser_stats()
            messagebox.showinfo("Succès", "Les statistiques ont été réinitialisées.")
            # Rafraîchir l'affichage si la fenêtre des stats est ouverte
            if hasattr(self, 'fenetre_stats') and self.fenetre_stats.winfo_exists():
                self.afficher_stats()

    def afficher_stats(self):
        """Affiche une fenêtre avec les statistiques"""
        stats = self.jeu.stats_manager.get_statistiques()
        historique = self.jeu.stats_manager.get_historique(10)
        
        # Créer une nouvelle fenêtre
        self.fenetre_stats = tk.Toplevel(self.window)
        self.fenetre_stats.title("Statistiques")
        self.fenetre_stats.configure(bg=COULEURS['fond'])
        
        # Frame pour les statistiques générales
        frame_stats = tk.Frame(self.fenetre_stats, bg=COULEURS['fond'], padx=20, pady=20)
        frame_stats.pack()
        
        # Afficher les statistiques
        tk.Label(
            frame_stats,
            text=f"Parties jouées: {stats['parties_jouées']}",
            font=('Arial', 12),
            bg=COULEURS['fond'],
            fg=COULEURS['texte']
        ).pack(anchor='w')
        
        tk.Label(
            frame_stats,
            text=f"Victoires Joueur: {stats['victoires_joueur']} ({stats['pourcentage_victoires_joueur']}%)",
            font=('Arial', 12),
            bg=COULEURS['fond'],
            fg=COULEURS[JOUEUR_X]
        ).pack(anchor='w')
        
        tk.Label(
            frame_stats,
            text=f"Victoires IA: {stats['victoires_ia']} ({stats['pourcentage_victoires_ia']}%)",
            font=('Arial', 12),
            bg=COULEURS['fond'],
            fg=COULEURS[JOUEUR_O]
        ).pack(anchor='w')
        
        tk.Label(
            frame_stats,
            text=f"Matchs nuls: {stats['matchs_nuls']} ({stats['pourcentage_matchs_nuls']}%)",
            font=('Arial', 12),
            bg=COULEURS['fond'],
            fg=COULEURS['texte']
        ).pack(anchor='w')
        
        # Frame pour l'historique
        frame_historique = tk.Frame(self.fenetre_stats, bg=COULEURS['fond'], padx=20, pady=20)
        frame_historique.pack()
        
        tk.Label(
            frame_historique,
            text="10 dernières parties:",
            font=('Arial', 12, 'bold'),
            bg=COULEURS['fond'],
            fg=COULEURS['texte']
        ).pack(anchor='w')
        
        # Afficher l'historique
        for partie in reversed(historique):
            gagnant = "Match nul" if partie['gagnant'] == "N" else f"Joueur {partie['gagnant']}"
            tk.Label(
                frame_historique,
                text=f"{partie['date']} - {gagnant} - Durée: {partie['durée']}s",
                font=('Arial', 10),
                bg=COULEURS['fond'],
                fg=COULEURS['texte']
            ).pack(anchor='w')

    def mettre_a_jour_interface(self):
        """Met à jour l'affichage du plateau de jeu"""
        for ligne in range(LIGNES):
            for colonne in range(COLONNES):
                couleur = COULEURS[VIDE]
                if self.jeu.plateau[ligne][colonne] == JOUEUR_X:
                    couleur = COULEURS[JOUEUR_X]
                elif self.jeu.plateau[ligne][colonne] == JOUEUR_O:
                    couleur = COULEURS[JOUEUR_O]
                    
                self.canvas.itemconfig(
                    self.cases[ligne][colonne],
                    fill=couleur
                )
        self.canvas.update()

    def lancer(self):
        self.window.mainloop()