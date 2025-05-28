# Configuration file for Tower Defense Game

# Game settings
INITIAL_LIVES = 15  # Number of lives at game start
START_COINS   = 25  # Starting coins
COIN_REWARD   = 7   # Coins earned per enemy kill

# Enemy settings
ENEMY_HEALTH = 120   # Initial health of each enemy
ENEMY_SPEED  = 1.2   # Movement speed of enemies

# Tower settings (cost in coins, range in pixels, cooldown in ms, damage per shot)
TOWER_CONFIG = {
    "double": {
        "cost":     12,
        "range":    180,
        "cooldown":  900,
        "damage":   15,
    },
    "small": {
        "cost":     25,
        "range":    300,
        "cooldown": 1800,
        "damage":   40,
    },
}

# Level-based upgrades: values & cost per level
# Level 1: +10 damage, +15 range, -200ms reload, cost 60 coins
# Level 2: +15 damage, +20 range, -250ms reload, cost 90 coins
# Level 3: +20 damage, +25 range, -300ms reload, cost 120 coins
TOWER_UPGRADES = {
    1: {'Damage': 5,  'Range': 10, 'Reload': 100, 'cost': 40},  # +30% DPS on Level 1
    2: {'Damage': 10, 'Range': 15, 'Reload': 150, 'cost': 80},  # +60% DPS total on Level 2
    3: {'Damage': 20, 'Range': 20, 'Reload': 200, 'cost': 120}, # +100% DPS total on Level 3
}
# Grid and placement cells
GRID_SIZE = 70  # Size of each grid cell in pixels
# Define your valid placement cell coordinates here
PLACEMENT_CELLS = [
    (8, 0),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
    (8, 5),
    (8, 6),
    (8, 7),
    (8, 8),
    (8, 9),
    (8, 10),
    (9, 0),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
    (9, 6),
    (9, 7),
    (9, 8),
    (9, 9),
    (9, 10),
    (10, 10),
    (10, 11),
    (11, 10),
    (11, 11),
    (11, 12),
    (11, 13),
    (11, 14),
    (11, 15),
    (11, 16),
    (12, 0),
    (12, 1),
    (12, 2),
    (12, 3),
    (12, 4),
    (12, 5),
    (12, 6),
    (12, 7),
    (12, 10),
    (12, 11),
    (12, 12),
    (12, 13),
    (12, 14),
    (12, 15),
    (12, 16),
    (13, 0),
    (13, 1),
    (13, 2),
    (13, 3),
    (13, 4),
    (13, 5),
    (13, 6),
    (13, 7),
    (13, 10),
    (13, 11),
    (14, 6),
    (14, 7),
    (14, 10),
    (14, 11),
    (15, 10),
    (15, 11),
    (15, 14),
    (15, 15),
    (15, 16),
    (15, 17),
    (16, 14),
    (16, 15),
    (16, 16),
    (16, 17),
    (17, 14),
    (17, 15),
    (18, 8),
    (18, 9),
    (18, 10),
    (18, 11),
    (18, 12),
    (18, 13),
    (18, 14),
    (19, 9),
    (19, 10),
    (19, 11),
    (19, 12),
    (19, 13),
]

# HUD and UI settings
ICON_SIZE      = 70   # Icon size for towers and upgrades
ICON_PADDING   = 10   # Padding around icons
HUD_FONT_SIZE  = 40   # Font size for HUD text
SHOP_WIDTH     = ICON_SIZE + ICON_PADDING * 2  # Width of the sidebar

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
GREEN = (0,   255, 0)
BLUE  = (0,   0, 255)
GRAY  = (169, 169, 169)

# Enemy path defined as relative percentages of screen size
PATH_PERCENTAGES = [
    (0.51, 1.00),
    (0.51, 0.78),
    (0.62, 0.78),
    (0.62, 0.53),
    (0.405, 0.53),
    (0.405, 0.00),
]
