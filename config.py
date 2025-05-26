# Configuration file for Tower Defense Game

# Game settings
INITIAL_LIVES = 10
START_COINS = 20
COIN_REWARD = 5

# Enemy settings
ENEMY_HEALTH = 100  # initial health of each enemy
ENEMY_SPEED = 2     # movement speed of enemies

# Tower settings (cost, range in pixels, cooldown in ms, damage per shot)
TOWER_CONFIG = {
    "double": {
        "cost": 20,
        "range": 200,
        "cooldown": 2000,
        "damage": 35,
    },
    "small": {
        "cost": 10,
        "range": 350,
        "cooldown": 1000,
        "damage": 20,
    },
}

# Grid and placement cells
GRID_SIZE = 80  # size of each grid cell in pixels
PLACEMENT_CELLS = [
    (10, 6),
    (10, 3), (10, 8),
    (10, 5), (10, 4),
    (11, 8), (12, 8), (10, 2), (10, 1),(10, 0), (8, 0),
    (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
    (9, 8), (13, 8),(13, 9), (12, 9), (11, 9), (11, 10), (11, 11), (11 ,12),
    (13, 11), (13, 12), (14, 11), (15, 11), (16, 10), (16, 9), (16, 8), (16, 7),
    (14, 6), (13, 6), (12, 6), (11, 6)
]

# HUD and UI settings
ICON_SIZE = 70        # size for tower and coin icons in pixels
ICON_PADDING = 10     # padding around icons in pixels
HUD_FONT_SIZE = 40    # font size for HUD text
SHOP_WIDTH = ICON_SIZE + ICON_PADDING * 2  # width of the shop sidebar

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Enemy path percentages (x, y) relative positions on screen
PATH_PERCENTAGES = [
    (0.51, 1.0),
    (0.51, 0.78),
    (0.62, 0.78),
    (0.62, 0.53),
    (0.405, 0.53),
    (0.405, 0.0),
]

# Upgrade-Definitionen: Kosten und Effekt-Increment
TOWER_UPGRADES = {
    'Damage': {'cost': 20, 'increment': 5},
    'Range':  {'cost': 20, 'increment': 20},
    'Reload': {'cost': 20, 'decrement': 200},
}
