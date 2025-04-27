import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from constants import *

class StatsVisualization:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager

    def create_figure(self):
        """Creates a matplotlib figure with multiple charts"""
        fig = plt.Figure(figsize=(10, 8))
        fig.patch.set_facecolor(COLORS['background'])
        
        # Chart 1: Results distribution (pie chart)
        ax1 = fig.add_subplot(221)
        stats = self.stats_manager.get_statistiques()
        labels = ['Player Wins', 'AI Wins', 'Draws']
        sizes = [stats['victoires_joueur'], stats['victoires_ia'], stats['matchs_nuls']]
        colors = [COLORS[PLAYER_X], COLORS[PLAYER_O], COLORS['text']]
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Results Distribution')
        
        # Chart 2: Evolution of wins
        ax2 = fig.add_subplot(222)
        history = self.stats_manager.get_historique(100)
        dates = [datetime.strptime(game['date'], "%Y-%m-%d %H:%M:%S") for game in history]
        player_wins = []
        ai_wins = []
        draws = []
        cumul_player = 0
        cumul_ai = 0
        cumul_draw = 0
        
        for game in history:
            if game['gagnant'] == 'X':
                cumul_player += 1
            elif game['gagnant'] == 'O':
                cumul_ai += 1
            else:
                cumul_draw += 1
            player_wins.append(cumul_player)
            ai_wins.append(cumul_ai)
            draws.append(cumul_draw)
        
        ax2.plot(dates, player_wins, label='Player', color=COLORS[PLAYER_X])
        ax2.plot(dates, ai_wins, label='AI', color=COLORS[PLAYER_O])
        ax2.plot(dates, draws, label='Draws', color=COLORS['text'])
        ax2.set_title('Wins Evolution')
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Simplify hours format
        ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Show a label every hour
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Chart 3: Game duration
        ax3 = fig.add_subplot(223)
        durations = [game['duree'] for game in history]
        ax3.hist(durations, bins=10, color=COLORS['button'])
        ax3.set_title('Game Duration Distribution')
        ax3.set_xlabel('Duration (seconds)')
        ax3.set_ylabel('Number of games')
        
        # Chart 4: Win trends
        ax4 = fig.add_subplot(224)
        window = 10  # Number of games for moving average
        player_trend = []
        ai_trend = []
        
        for i in range(len(history)):
            start = max(0, i - window + 1)
            window_games = history[start:i+1]
            window_wins = sum(1 for g in window_games if g['gagnant'] == 'X')
            window_ai_wins = sum(1 for g in window_games if g['gagnant'] == 'O')
            player_trend.append(window_wins / len(window_games) * 100)
            ai_trend.append(window_ai_wins / len(window_games) * 100)
        
        ax4.plot(dates, player_trend, label='Player', color=COLORS[PLAYER_X])
        ax4.plot(dates, ai_trend, label='AI', color=COLORS[PLAYER_O])
        ax4.set_title(f'Trend over {window} games')
        ax4.set_ylabel('Win percentage')
        ax4.legend()
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Simplify hours format
        ax4.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Show a label every hour
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        return fig

    def show_graphs(self, parent):
        """Displays the charts in a Tkinter window"""
        graph_window = tk.Toplevel(parent)
        graph_window.title("Stats Visualization")
        graph_window.configure(bg=COLORS['background'])
        
        # Create the figure
        fig = self.create_figure()
        
        # Embed figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        refresh_button = tk.Button(
            graph_window,
            text="Refresh",
            command=lambda: self.refresh_graphs(canvas, fig),
            **BUTTON_STYLE,
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        refresh_button.pack(pady=10)

    def refresh_graphs(self, canvas, fig):
        """Refreshes graphs with latest data"""
        fig.clear()
        fig = self.create_figure()
        canvas.figure = fig
        canvas.draw()