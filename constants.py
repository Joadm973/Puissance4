# Dimensions du plateau
LIGNES = 6
COLONNES = 7
TAILLE_CASE = 60

# Symboles des joueurs
JOUEUR_X = 'X'
JOUEUR_O = 'O'
VIDE = ' '

# Couleurs par défaut
COULEURS = {
    'X': '#E74C3C',  # Rouge vif
    'O': '#3498DB',  # Bleu clair
    ' ': '#34495E',  # Gris bleuté
    'hover': '#95A5A6',  # Gris clair
    'fond': '#2C3E50',  # Bleu foncé
    'plateau': '#34495E',  # Gris bleuté
    'bouton': '#2ECC71',  # Vert
    'bouton_hover': '#27AE60',  # Vert foncé
    'texte': '#ECF0F1',  # Blanc cassé
    'bordure': '#1A2530',  # Bleu très foncé
    'ombre': '#1A2530',  # Bleu très foncé
    'fond_stats': '#2C3E50',  # Bleu foncé
    'fond_graphiques': '#2C3E50',  # Bleu foncé
    'titre': '#ECF0F1',  # Blanc cassé
    'sous_titre': '#BDC3C7',  # Gris clair
    'warning': '#E74C3C',  # Rouge
    'success': '#2ECC71'  # Vert
}

# Style des boutons
STYLE_BOUTON = {
    'font': ('Arial', 10, 'bold'),
    'relief': 'flat',
    'padx': 15,
    'pady': 5,
    'borderwidth': 0,
    'highlightthickness': 0
}

# Style des labels
STYLE_LABEL = {
    'font': ('Arial', 12),
    'bg': COULEURS['fond'],
    'fg': COULEURS['texte'],
    'padx': 5,
    'pady': 2
}

# Style des titres
STYLE_TITRE = {
    'font': ('Arial', 16, 'bold'),
    'bg': COULEURS['fond'],
    'fg': COULEURS['titre'],
    'padx': 5,
    'pady': 5
}

# Style des sous-titres
STYLE_SOUS_TITRE = {
    'font': ('Arial', 14, 'bold'),
    'bg': COULEURS['fond'],
    'fg': COULEURS['sous_titre'],
    'padx': 5,
    'pady': 3
}

# Style des frames
STYLE_FRAME = {
    'bg': COULEURS['fond'],
    'padx': 20,
    'pady': 10
}

# Style du canvas
STYLE_CANVAS = {
    'bg': COULEURS['plateau'],
    'highlightthickness': 0,
    'borderwidth': 0
} 