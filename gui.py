import tkinter as tk
from tkinter import messagebox, ttk
import random
import traceback
from constants import *
from game import Connect4
from visualisation import StatsVisualization

class Connect4GUI:
    def __init__(self):
        # Check and fix potential issues in initialization
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.configure(bg=COLORS['background'])
        
        # Set minimum window size to ensure all elements are visible
        self.root.minsize(COLUMNS * CELL_SIZE + 100, ROWS * CELL_SIZE + 400)  # Increased minimum height
        
        # Global style
        style = ttk.Style()
        style.configure('TButton', **BUTTON_STYLE)
        style.configure('TLabel', **LABEL_STYLE)
        
        try:
            self.game = Connect4()
        except Exception as e:
            print(f"Error initializing game: {e}")
            # Create a fallback game object or initialize with None
            self.game = None
            
        # Only proceed with visualization if game was initialized successfully
        if self.game is not None:
            self.visualization = StatsVisualization(self.game.stats_manager)
        else:
            # Create a fallback visualization or skip it
            self.visualization = None
        
        # Main frame with shadow
        self.main_frame = tk.Frame(self.root, bg=COLORS['background'], padx=30, pady=30)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Game title
        self.title_label = tk.Label(
            self.main_frame,
            text="CONNECT 4",
            **TITLE_STYLE
        )
        self.title_label.pack(pady=(0, 20))
        
        # Frame for score and stats with slightly lighter background
        self.score_frame = tk.Frame(
            self.main_frame,
            bg=COLORS['stats_background'],
            padx=20,
            pady=15,
            relief='flat',
            borderwidth=1
        )
        self.score_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Labels for score with improved style
        score_x_style = LABEL_STYLE.copy()
        score_x_style['fg'] = COLORS[PLAYER_X]
        self.score_x_label = tk.Label(
            self.score_frame,
            text=f"Player {PLAYER_X}: 0",
            **score_x_style
        )
        self.score_x_label.pack(side=tk.LEFT, padx=20)
        
        score_o_style = LABEL_STYLE.copy()
        score_o_style['fg'] = COLORS[PLAYER_O]
        self.score_o_label = tk.Label(
            self.score_frame,
            text=f"Player {PLAYER_O}: 0",
            **score_o_style
        )
        self.score_o_label.pack(side=tk.LEFT, padx=20)

        # Frame for action buttons
        self.actions_frame = tk.Frame(self.score_frame, bg=COLORS['stats_background'])
        self.actions_frame.pack(side=tk.RIGHT, padx=20)

        # Statistics button with icon
        self.stats_button = tk.Button(
            self.actions_frame,
            text="📊 Statistics",
            command=self.show_stats,
            **BUTTON_STYLE,
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.stats_button.pack(side=tk.LEFT, padx=5)
        
        # Graphics button with icon
        self.graphs_button = tk.Button(
            self.actions_frame,
            text="📈 Graphs",
            command=lambda: self.visualization.show_graphs(self.root),
            **BUTTON_STYLE,
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.graphs_button.pack(side=tk.LEFT, padx=5)
        
        # Reset Stats button with icon
        self.reset_stats_button = tk.Button(
            self.actions_frame,
            text="🔄 Reset",
            command=self.confirm_stats_reset,
            **BUTTON_STYLE,
            fg=COLORS['background'],
            bg=COLORS['warning'],
            activebackground='#C0392B',
            activeforeground=COLORS['background']
        )
        self.reset_stats_button.pack(side=tk.LEFT, padx=5)
        
        # Label for current player with improved style
        self.player_label = tk.Label(
            self.main_frame,
            text=f"Player {self.game.current_player}'s turn",
            **SUBTITLE_STYLE
        )
        self.player_label.pack(pady=(0, 10))
        
        # Creation of canvas with improved style
        self.canvas = tk.Canvas(
            self.main_frame,
            width=COLUMNS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            **CANVAS_STYLE
        )
        self.canvas.pack(pady=(0, 30))  # Added bottom padding
        
        # Create separate frames for each row of buttons
        # First row of controls
        self.controls_frame1 = tk.Frame(
            self.main_frame,
            bg=COLORS['background'],
            padx=20,
            pady=10  # Reduced padding
        )
        self.controls_frame1.pack(fill=tk.X)
        
        # Second row of controls
        self.controls_frame2 = tk.Frame(
            self.main_frame,
            bg=COLORS['background'],
            padx=20,
            pady=10  # Reduced padding
        )
        self.controls_frame2.pack(fill=tk.X)
        
        # New Game button with icon - First row
        self.new_game_button = tk.Button(
            self.controls_frame1,
            text="🆕 New Game",
            command=self.reset_game,
            height=1,  # Fixed height
            width=12,  # Fixed width
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # AI Mode button with icon - First row
        self.ai_mode_button = tk.Button(
            self.controls_frame1,
            text="🤖 AI Mode",
            command=self.toggle_ai_mode,
            height=1,  # Fixed height
            width=12,  # Fixed width
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.ai_mode_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Button to view AI learned patterns - First row
        self.patterns_button = tk.Button(
            self.controls_frame1,
            text="🧠 AI Patterns",
            command=self.show_ai_patterns,
            height=1,  # Fixed height
            width=12,  # Fixed width
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.patterns_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Button for AI vs AI mode - Second row
        self.ai_vs_ai_button = tk.Button(
            self.controls_frame2,
            text="🤖 vs 🤖",
            command=self.toggle_ai_vs_ai_mode,
            height=1,  # Fixed height
            width=12,  # Fixed width
            fg=COLORS['background'],
            bg=COLORS['button'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['background']
        )
        self.ai_vs_ai_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Quit button with icon - Second row
        self.quit_button = tk.Button(
            self.controls_frame2,
            text="🚪 Quit",
            command=self.root.quit,
            height=1,  # Fixed height
            width=12,  # Fixed width
            fg=COLORS['background'],
            bg=COLORS['warning'],
            activebackground='#C0392B',
            activeforeground=COLORS['background']
        )
        self.quit_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Draw initial board
        self.draw_board()
        
        # Bindings
        self.canvas.bind('<Button-1>', self.handle_click)
        self.canvas.bind('<Motion>', self.handle_hover)
        
        # Center the window and set its size
        self.root.update_idletasks()
        width = max(self.root.winfo_reqwidth(), COLUMNS * CELL_SIZE + 100)
        height = max(self.root.winfo_reqheight(), ROWS * CELL_SIZE + 400)
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw board background
        self.canvas.create_rectangle(
            0, 0,
            COLUMNS * CELL_SIZE, ROWS * CELL_SIZE,
            fill=COLORS['board'],
            outline=COLORS['border'],
            width=2
        )
        
        # Initialize array to store cell references
        self.cells = []
        
        for row in range(ROWS):
            row_cells = []
            for col in range(COLUMNS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # Draw cells with shadow
                cell = self.canvas.create_oval(
                    x1 + 5, y1 + 5,
                    x2 - 5, y2 - 5,
                    fill=COLORS[self.game.board[row][col]],
                    outline=COLORS['border'],
                    width=1
                )
                row_cells.append(cell)
            self.cells.append(row_cells)

    def handle_hover(self, event):
        column = event.x // CELL_SIZE
        if 0 <= column < COLUMNS:
            # Clear the board
            self.draw_board()
            
            # Draw hover indicator
            x1 = column * CELL_SIZE
            y1 = 0
            x2 = x1 + CELL_SIZE
            y2 = CELL_SIZE
            
            self.canvas.create_oval(
                x1 + 5, y1 + 5,
                x2 - 5, y2 - 5,
                fill=COLORS['hover'],
                outline=COLORS[self.game.current_player]
            )

    def handle_click(self, event):
        """Handle click on canvas"""
        # If it's AI's turn, don't allow player to play
        if self.game.current_player == PLAYER_O and self.game.ai_mode:
            return
            
        column = event.x // CELL_SIZE
        
        # Always ensure start_time is set before potentially ending the game
        import time
        if not hasattr(self.game, 'start_time') or self.game.start_time is None:
            self.game.start_time = time.time()
            
        result = self.game.place_token(column)
        
        if result == 'victory':
            self.game.increment_score()
            self.update_score()  # Update score
            self.draw_board()
            self.update_interface()
            # Update display immediately
            self.root.update()
            # Highlight winning tokens before displaying message
            self.highlight_victory()
            return
            
        elif result == 'draw':
            self.draw_board()
            self.update_interface()
            # Update display immediately
            self.root.update()
            
            # Wait a short moment before displaying message
            self.root.after(500, lambda: self.end_game_with_message('N'))
            return
            
        elif result:
            self.game.change_player()
            self.draw_board()
            self.update_interface()
            
            # AI's turn - add a 1 second delay
            if self.game.current_player == PLAYER_O and self.game.ai_mode:
                # Disable events while AI is thinking
                self.canvas.unbind('<Button-1>')
                # Update label to show AI is thinking
                self.player_label.config(text="AI is thinking... 🤔")
                # Call play_ai_move after 1 second
                self.root.after(1000, self.play_ai_move)

    def play_ai_move(self):
        """Make the AI play"""
        try:
            # Always ensure start_time is set before AI plays
            import time
            if not hasattr(self.game, 'start_time') or self.game.start_time is None:
                self.game.start_time = time.time()
                
            column = self.game.choose_best_move()
            if column is not None:
                result = self.game.place_token(column)
                
                if result == 'victory':
                    self.game.increment_score()
                    self.update_score()  # Update score
                    self.draw_board()
                    self.update_interface()
                    # Update display immediately
                    self.root.update()
                    # Highlight winning tokens before displaying message
                    self.highlight_victory()
                    return
                    
                elif result == 'draw':
                    self.draw_board()
                    self.update_interface()
                    # Update display immediately
                    self.root.update()
                    
                    # Wait a short moment before displaying message
                    self.root.after(500, lambda: self.end_game_with_message('N'))
                    return
                    
                elif result:
                    self.game.change_player()
                    self.draw_board()
                    self.update_interface()
        finally:
            # Re-enable events after AI move
            self.canvas.bind('<Button-1>', self.handle_click)
            # Update player label
            self.player_label.config(text=f"Player {self.game.current_player}'s turn")

    def play_ai_vs_ai_move(self):
        """Make AI play against AI in automatic mode"""
        if not self.game.ai_vs_ai_mode:
            # If mode was disabled in the meantime, stop
            return
            
        # Update label to show which AI is thinking
        current_player_name = "AI 1 (X)" if self.game.current_player == PLAYER_X else "AI 2 (O)"
        self.player_label.config(text=f"{current_player_name} is thinking... 🤔")
        self.root.update()
        
        # Choose and play move
        column = self.game.choose_best_move()
        if column is not None:
            # Add delay to visualize moves
            self.root.after(500, lambda col=column: self.execute_ai_vs_ai_move(col))
        else:
            # If no valid move, consider it a draw
            self.end_game_with_message('N')
            
    def execute_ai_vs_ai_move(self, column):
        """Execute a move in AI vs AI mode after a delay"""
        if not self.game.ai_vs_ai_mode:
            return
            
        result = self.game.place_token(column)
        
        if result == 'victory':
            self.game.increment_score()
            self.update_score()
            self.draw_board()
            self.update_interface()
            self.root.update()
            
            # Animate winning tokens and end game
            self.highlight_victory_ai_vs_ai()
            return
            
        elif result == 'draw':
            self.draw_board()
            self.update_interface()
            self.root.update()
            self.end_game_with_message('N')
            return
            
        elif result:
            self.game.change_player()
            self.draw_board()
            self.update_interface()
            
            # Schedule next move with delay
            self.root.after(800, self.play_ai_vs_ai_move)
            
    def highlight_victory_ai_vs_ai(self):
        """Special version of highlighting for AI vs AI mode"""
        winning_tokens = self.game.find_winning_tokens()
        original_color = COLORS[self.game.current_player]
        original_outline = COLORS['border']
        
        def blink_animation(counter=0):
            if counter < 6:  # 3 blinks (6 changes)
                # Alternate between colors
                fill_color = '#FFD700' if counter % 2 == 0 else original_color
                outline_color = '#FF4500' if counter % 2 == 0 else original_outline
                width = 3 if counter % 2 == 0 else 1
                
                for row, col in winning_tokens:
                    self.canvas.itemconfig(
                        self.cells[row][col],
                        fill=fill_color,
                        outline=outline_color,
                        width=width
                    )
                self.canvas.update()
                self.root.after(200, lambda: blink_animation(counter + 1))
            else:
                # Animation finished
                winning_player = "AI 1 (X)" if self.game.current_player == PLAYER_X else "AI 2 (O)"
                message = f"{winning_player} has won!"
                try:
                    stats = self.game.end_game(self.game.current_player)
                    messagebox.showinfo("Game Over", message)
                except Exception as e:
                    print(f"Error in end_game: {e}")
                    print(traceback.format_exc())
                finally:
                    self.reset_game()
                    # If AI vs AI mode is still active, start a new game
                    if self.game.ai_vs_ai_mode:
                        self.root.after(1000, self.play_ai_vs_ai_move)
        
        # Start animation
        blink_animation()

    def highlight_victory(self):
        """Highlight winning tokens"""
        winning_tokens = self.game.find_winning_tokens()
        original_color = COLORS[self.game.current_player]
        original_outline = COLORS['border']
        
        def blink_animation(counter=0):
            if counter < 6:  # 3 blinks (6 changes)
                # Alternate between colors
                fill_color = '#FFD700' if counter % 2 == 0 else original_color  # Gold
                outline_color = '#FF4500' if counter % 2 == 0 else original_outline  # Orange-red
                width = 3 if counter % 2 == 0 else 1  # Outline thickness
                
                for row, col in winning_tokens:
                    self.canvas.itemconfig(
                        self.cells[row][col],
                        fill=fill_color,
                        outline=outline_color,
                        width=width
                    )
                self.canvas.update()
                # Schedule next change in 200ms
                self.root.after(200, lambda: blink_animation(counter + 1))
            else:
                # Animation finished, display victory message
                self.root.after(100, lambda: self.end_game_with_message(self.game.current_player))
        
        # Start animation
        blink_animation()

    def end_game_with_message(self, winner):
        """Handle end of game with message after a delay"""
        try:
            stats = self.game.end_game(winner)
            if winner == 'N':
                messagebox.showinfo("Game Over", "Draw!")
            else:
                message = "AI has won!" if (self.game.ai_mode and winner == PLAYER_O) else f"Player {winner} has won!"
                messagebox.showinfo("Game Over", message)
        except Exception as e:
            print(f"Error in end_game: {e}")
            print(traceback.format_exc())
        finally:
            self.reset_game()

    def toggle_ai_mode(self):
        """Toggle AI mode and show level selection dialog if enabled"""
        if not self.game.ai_mode:
            # AI mode is being enabled
            self.game.ai_mode = True
            self.show_ai_level_selector()
        else:
            # AI mode is being disabled
            self.game.ai_mode = False
            self.ai_mode_button.config(
                text="AI Mode: Off",
                bg=COLORS['button']
            )
    
    def show_ai_level_selector(self):
        """Show a dialog to select AI level"""
        # Create a new window
        level_window = tk.Toplevel(self.root)
        level_window.title("Select AI Level")
        level_window.configure(bg=COLORS['background'])
        level_window.geometry("300x200")
        level_window.transient(self.root)  # Set as transient to main window
        level_window.grab_set()  # Modal window
        level_window.resizable(False, False)
        
        # Center the window
        level_window.update_idletasks()
        x = (level_window.winfo_screenwidth() // 2) - (level_window.winfo_width() // 2)
        y = (level_window.winfo_screenheight() // 2) - (level_window.winfo_height() // 2)
        level_window.geometry(f"+{x}+{y}")
        
        # Title
        tk.Label(
            level_window,
            text="Select AI Level",
            font=('Arial', 14, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(pady=(20, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(level_window, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Moderate AI button
        def select_moderate():
            self.game.ai_level = 1
            self.ai_mode_button.config(
                text="AI: Moderate",
                bg='#2980B9'
            )
            level_window.destroy()
        
        # Fixed moderate button - text is included directly in the button
        moderate_button = tk.Button(
            buttons_frame,
            text="Moderate AI\nUses basic game logic",
            command=select_moderate,
            height=2,
            width=15,
            fg=COLORS['background'],
            bg='#3498DB',
            activebackground='#2980B9',
            activeforeground=COLORS['background']
        )
        moderate_button.pack(side=tk.LEFT, padx=10)
        
        # Advanced AI button
        def select_advanced():
            self.game.ai_level = 2
            self.ai_mode_button.config(
                text="AI: Advanced",
                bg='#8E44AD'
            )
            level_window.destroy()
        
        # Fixed advanced button - text is included directly in the button
        advanced_button = tk.Button(
            buttons_frame,
            text="Advanced AI\nUses pattern learning",
            command=select_advanced,
            height=2,
            width=15,
            fg=COLORS['background'],
            bg='#9B59B6',
            activebackground='#8E44AD',
            activeforeground=COLORS['background']
        )
        advanced_button.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        def cancel_selection():
            self.game.ai_mode = False
            level_window.destroy()
        
        cancel_button = tk.Button(
            level_window,
            text="Cancel",
            command=cancel_selection,
            fg=COLORS['text'],
            bg=COLORS['background'],
            activebackground=COLORS['background'],
            activeforeground=COLORS['text'],
            bd=0
        )
        cancel_button.pack(pady=20)

    def toggle_ai_vs_ai_mode(self):
        """Enable or disable AI vs AI mode"""
        # Disable player vs AI mode if activating AI vs AI mode
        if not self.game.ai_vs_ai_mode:
            self.game.ai_mode = False
            self.ai_mode_button.config(
                text="AI Mode: Off",
                bg=COLORS['button']
            )
            
        self.game.ai_vs_ai_mode = not self.game.ai_vs_ai_mode
        
        # Update button appearance
        self.ai_vs_ai_button.config(
            text="AI vs AI: On" if self.game.ai_vs_ai_mode else "🤖 vs 🤖",
            bg='#9B59B6' if self.game.ai_vs_ai_mode else COLORS['button']
        )
        
        # If activating this mode, automatically start a game
        if self.game.ai_vs_ai_mode:
            self.reset_game()
            # Let the interface refresh before starting
            self.root.update()
            self.root.after(500, self.play_ai_vs_ai_move)

    def update_score(self):
        self.score_x_label.config(text=f"Player {PLAYER_X}: {self.game.scores[PLAYER_X]}")
        self.score_o_label.config(text=f"Player {PLAYER_O}: {self.game.scores[PLAYER_O]}")

    def reset_game(self):
        # Always make sure start_time is set to the current time before resetting
        import time
        self.game.start_time = time.time()
        
        # Now reset the game
        self.game.reset_game()
        
        # Verify start_time is still set after resetting
        if not hasattr(self.game, 'start_time') or self.game.start_time is None:
            self.game.start_time = time.time()
            
        self.player_label.config(text=f"Player {self.game.current_player}'s turn")
        self.draw_board()

    def confirm_stats_reset(self):
        """Ask for confirmation before resetting statistics"""
        if messagebox.askyesno(
            "Confirmation",
            "Are you sure you want to reset all statistics?\nThis action is irreversible.",
            icon='warning'
        ):
            self.game.stats_manager.reinitialiser_stats()
            messagebox.showinfo("Success", "Statistics have been reset.")
            # Refresh display if stats window is open
            if hasattr(self, 'stats_window') and self.stats_window.winfo_exists():
                self.show_stats()

    def show_stats(self):
        """Display a window with statistics"""
        stats = self.game.stats_manager.get_statistiques()
        history = self.game.stats_manager.get_historique(10)
        
        # Create a new window
        self.stats_window = tk.Toplevel(self.root)
        self.stats_window.title("Statistics")
        self.stats_window.configure(bg=COLORS['background'])
        
        # Frame for general statistics
        stats_frame = tk.Frame(self.stats_window, bg=COLORS['background'], padx=20, pady=20)
        stats_frame.pack()
        
        # Display statistics
        tk.Label(
            stats_frame,
            text=f"Games played: {stats['parties_jouées']}",
            font=('Arial', 12),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(anchor='w')
        
        tk.Label(
            stats_frame,
            text=f"Player Wins: {stats['victoires_joueur']} ({stats['pourcentage_victoires_joueur']}%)",
            font=('Arial', 12),
            bg=COLORS['background'],
            fg=COLORS[PLAYER_X]
        ).pack(anchor='w')
        
        tk.Label(
            stats_frame,
            text=f"AI Wins: {stats['victoires_ia']} ({stats['pourcentage_victoires_ia']}%)",
            font=('Arial', 12),
            bg=COLORS['background'],
            fg=COLORS[PLAYER_O]
        ).pack(anchor='w')
        
        tk.Label(
            stats_frame,
            text=f"Draws: {stats['matchs_nuls']} ({stats['pourcentage_matchs_nuls']}%)",
            font=('Arial', 12),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(anchor='w')
        
        # Frame for history
        history_frame = tk.Frame(self.stats_window, bg=COLORS['background'], padx=20, pady=20)
        history_frame.pack()
        
        tk.Label(
            history_frame,
            text="Last 10 games:",
            font=('Arial', 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(anchor='w')
        
        # Display history
        for game in reversed(history):
            winner = "Draw" if game['gagnant'] == "N" else f"Player {game['gagnant']}"
            tk.Label(
                history_frame,
                text=f"{game['date']} - {winner} - Duration: {game['duree']}s",
                font=('Arial', 10),
                bg=COLORS['background'],
                fg=COLORS['text']
            ).pack(anchor='w')

    def show_ai_patterns(self):
        """Display AI learning patterns in a window"""
        # Create a new window
        patterns_window = tk.Toplevel(self.root)
        patterns_window.title("AI Learned Patterns")
        patterns_window.configure(bg=COLORS['background'])
        patterns_window.geometry("600x400")
        
        # Main frame
        main_frame = tk.Frame(patterns_window, bg=COLORS['background'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            main_frame,
            text="AI Learning Patterns",
            font=('Arial', 14, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(pady=(0, 20))
        
        # Check if patterns are available
        if not self.game.learned_patterns or not (
            'X' in self.game.learned_patterns and 
            'O' in self.game.learned_patterns and
            (self.game.learned_patterns['X']['frequence'] or 
             self.game.learned_patterns['O']['frequence'])
        ):
            tk.Label(
                main_frame,
                text="No learning patterns available.\nPlay some games for the AI to learn.",
                font=('Arial', 12),
                bg=COLORS['background'],
                fg=COLORS['text']
            ).pack(pady=20)
            return
            
        # Frame for player patterns
        player_frame = tk.LabelFrame(
            main_frame,
            text="Player X Patterns",
            font=('Arial', 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS[PLAYER_X]
        )
        player_frame.pack(fill=tk.X, pady=10)
        
        # Total number of recorded moves for player
        player_moves_count = len(self.game.learned_patterns['X']['coups']) if 'X' in self.game.learned_patterns else 0
        tk.Label(
            player_frame,
            text=f"Number of recorded moves: {player_moves_count}",
            font=('Arial', 10),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(anchor='w', padx=10, pady=5)
        
        # Frequent positions for player (top 5)
        if 'X' in self.game.learned_patterns and self.game.learned_patterns['X']['frequence']:
            player_positions = sorted(
                self.game.learned_patterns['X']['frequence'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            tk.Label(
                player_frame,
                text="Frequent positions:",
                font=('Arial', 10, 'bold'),
                bg=COLORS['background'],
                fg=COLORS['text']
            ).pack(anchor='w', padx=10, pady=5)
            
            for pos, freq in player_positions:
                tk.Label(
                    player_frame,
                    text=f"Position {pos}: used {freq} times",
                    font=('Arial', 10),
                    bg=COLORS['background'],
                    fg=COLORS['text']
                ).pack(anchor='w', padx=30, pady=2)
        
        # Frame for AI patterns
        ai_frame = tk.LabelFrame(
            main_frame,
            text="AI (O) Patterns",
            font=('Arial', 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS[PLAYER_O]
        )
        ai_frame.pack(fill=tk.X, pady=10)
        
        # Total number of recorded moves for AI
        ai_moves_count = len(self.game.learned_patterns['O']['coups']) if 'O' in self.game.learned_patterns else 0
        tk.Label(
            ai_frame,
            text=f"Number of recorded moves: {ai_moves_count}",
            font=('Arial', 10),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(anchor='w', padx=10, pady=5)
        
        # Frequent positions for AI (top 5)
        if 'O' in self.game.learned_patterns and self.game.learned_patterns['O']['frequence']:
            ai_positions = sorted(
                self.game.learned_patterns['O']['frequence'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            tk.Label(
                ai_frame,
                text="Frequent positions:",
                font=('Arial', 10, 'bold'),
                bg=COLORS['background'],
                fg=COLORS['text']
            ).pack(anchor='w', padx=10, pady=5)
            
            for pos, freq in ai_positions:
                tk.Label(
                    ai_frame,
                    text=f"Position {pos}: used {freq} times",
                    font=('Arial', 10),
                    bg=COLORS['background'],
                    fg=COLORS['text']
                ).pack(anchor='w', padx=30, pady=2)
                
        # Explanation of how learning works
        explanation_frame = tk.LabelFrame(
            main_frame,
            text="How Learning Works",
            font=('Arial', 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        explanation_frame.pack(fill=tk.X, pady=10)
        
        explanation_text = """
        The AI learns from previous games by:
        - Memorizing all moves played in winning games
        - Identifying positions that frequently lead to victory
        - Adapting its strategy to favor these positions
        - Avoiding positions that have often led to opponent's victory
        
        The more you play, the smarter the AI becomes!
        """
        
        tk.Label(
            explanation_frame,
            text=explanation_text,
            font=('Arial', 9),
            bg=COLORS['background'],
            fg=COLORS['text'],
            justify=tk.LEFT
        ).pack(anchor='w', padx=10, pady=5)

    def update_interface(self):
        """Update the game board display"""
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = COLORS[EMPTY]
                if self.game.board[row][column] == PLAYER_X:
                    color = COLORS[PLAYER_X]
                elif self.game.board[row][column] == PLAYER_O:
                    color = COLORS[PLAYER_O]
                    
                self.canvas.itemconfig(
                    self.cells[row][column],
                    fill=color
                )
        self.canvas.update()

    def start(self):
        self.root.mainloop()