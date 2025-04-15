import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from constants import *

class VisualisationStats:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager

    def creer_figure(self):
        """Crée une figure matplotlib avec plusieurs graphiques"""
        fig = plt.Figure(figsize=(10, 8))
        fig.patch.set_facecolor(COULEURS['fond'])
        
        # Graphique 1: Répartition des résultats (camembert)
        ax1 = fig.add_subplot(221)
        stats = self.stats_manager.get_statistiques()
        labels = ['Victoires Joueur', 'Victoires IA', 'Matchs Nuls']
        sizes = [stats['victoires_joueur'], stats['victoires_ia'], stats['matchs_nuls']]
        colors = [COULEURS[JOUEUR_X], COULEURS[JOUEUR_O], COULEURS['texte']]
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Répartition des résultats')
        
        # Graphique 2: Évolution des victoires
        ax2 = fig.add_subplot(222)
        historique = self.stats_manager.get_historique(100)
        dates = [datetime.strptime(partie['date'], "%Y-%m-%d %H:%M:%S") for partie in historique]
        victoires_joueur = []
        victoires_ia = []
        matchs_nuls = []
        cumul_joueur = 0
        cumul_ia = 0
        cumul_nul = 0
        
        for partie in historique:
            if partie['gagnant'] == 'X':
                cumul_joueur += 1
            elif partie['gagnant'] == 'O':
                cumul_ia += 1
            else:
                cumul_nul += 1
            victoires_joueur.append(cumul_joueur)
            victoires_ia.append(cumul_ia)
            matchs_nuls.append(cumul_nul)
        
        ax2.plot(dates, victoires_joueur, label='Joueur', color=COULEURS[JOUEUR_X])
        ax2.plot(dates, victoires_ia, label='IA', color=COULEURS[JOUEUR_O])
        ax2.plot(dates, matchs_nuls, label='Matchs nuls', color=COULEURS['texte'])
        ax2.set_title('Évolution des victoires')
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Simplifier le format des heures
        ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Afficher une étiquette toutes les heures
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Graphique 3: Durée des parties
        ax3 = fig.add_subplot(223)
        durees = [partie['duree'] for partie in historique]
        ax3.hist(durees, bins=10, color=COULEURS['bouton'])
        ax3.set_title('Distribution des durées de parties')
        ax3.set_xlabel('Durée (secondes)')
        ax3.set_ylabel('Nombre de parties')
        
        # Graphique 4: Tendance des victoires
        ax4 = fig.add_subplot(224)
        fenetre = 10  # Nombre de parties pour la moyenne mobile
        tendance_joueur = []
        tendance_ia = []
        
        for i in range(len(historique)):
            debut = max(0, i - fenetre + 1)
            parties_fenetre = historique[debut:i+1]
            victoires_fenetre = sum(1 for p in parties_fenetre if p['gagnant'] == 'X')
            victoires_ia_fenetre = sum(1 for p in parties_fenetre if p['gagnant'] == 'O')
            tendance_joueur.append(victoires_fenetre / len(parties_fenetre) * 100)
            tendance_ia.append(victoires_ia_fenetre / len(parties_fenetre) * 100)
        
        ax4.plot(dates, tendance_joueur, label='Joueur', color=COULEURS[JOUEUR_X])
        ax4.plot(dates, tendance_ia, label='IA', color=COULEURS[JOUEUR_O])
        ax4.set_title(f'Tendance sur {fenetre} parties')
        ax4.set_ylabel('Pourcentage de victoires')
        ax4.legend()
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Simplifier le format des heures
        ax4.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Afficher une étiquette toutes les heures
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        return fig

    def afficher_graphiques(self, parent):
        """Affiche les graphiques dans une fenêtre Tkinter"""
        fenetre_graphiques = tk.Toplevel(parent)
        fenetre_graphiques.title("Visualisation des statistiques")
        fenetre_graphiques.configure(bg=COULEURS['fond'])
        
        # Créer la figure
        fig = self.creer_figure()
        
        # Intégrer la figure dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=fenetre_graphiques)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour rafraîchir les graphiques
        bouton_rafraichir = tk.Button(
            fenetre_graphiques,
            text="Rafraîchir",
            command=lambda: self.rafraichir_graphiques(canvas, fig),
            **STYLE_BOUTON,
            fg=COULEURS['fond'],
            bg=COULEURS['bouton'],
            activebackground=COULEURS['bouton_hover'],
            activeforeground=COULEURS['fond']
        )
        bouton_rafraichir.pack(pady=10)

    def rafraichir_graphiques(self, canvas, fig):
        """Rafraîchit les graphiques avec les dernières données"""
        fig.clear()
        fig = self.creer_figure()
        canvas.figure = fig
        canvas.draw()