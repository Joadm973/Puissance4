# Game constants
ROWS = 6
COLUMNS = 7
CELL_SIZE = 80

# Players
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Colors
COLORS = {
    'background': '#1E1E1E',
    'text': '#EFEFEF',
    'board': '#2C2C2C',
    'border': '#3A3A3A',
    'stats_background': '#272727',
    'button': '#3498DB',
    'button_hover': '#2980B9',
    'warning': '#E74C3C',
    'hover': '#CCCCCC50',
    PLAYER_X: '#FF6347',  # Red
    PLAYER_O: '#5DADE2',  # Blue
    EMPTY: '#2C2C2C'      # Dark gray (same as board)
}

# Styles
BUTTON_STYLE = {
    'font': ('Arial', 12),
    'borderwidth': 0,
    'relief': 'flat',
    'padx': 10,
    'pady': 5
}

LABEL_STYLE = {
    'font': ('Arial', 12),
    'bg': COLORS['background'],
    'fg': COLORS['text'],
    'padx': 5,
    'pady': 5
}

TITLE_STYLE = {
    'font': ('Arial', 24, 'bold'),
    'bg': COLORS['background'],
    'fg': COLORS['text'],
    'padx': 10,
    'pady': 10
}

SUBTITLE_STYLE = {
    'font': ('Arial', 14, 'bold'),
    'bg': COLORS['background'],
    'fg': COLORS['text'],
    'padx': 5,
    'pady': 5
}

CANVAS_STYLE = {
    'bg': COLORS['board'],
    'highlightthickness': 0,
    'borderwidth': 2,
    'relief': 'ridge'
}