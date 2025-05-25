# Configuration file for Tower Defense Game

# Game settings
INITIAL_LIVES = 50
START_COINS = 0
COIN_REWARD = 5

# Enemy settings
ENEMY_HEALTH = 100  # initial health of each enemy
ENEMY_SPEED = 2     # movement speed of enemies

# Tower settings (cost, range in pixels, cooldown in ms, damage per shot)
TOWER_CONFIG = {
    "double": {
        "cost": 20,
        "range": 150,
        "cooldown": 2000,
        "damage": 20,
    },
    "small": {
        "cost": 10,
        "range": 100,
        "cooldown": 1000,
        "damage": 10,
    },
}

# Grid and placement cells
GRID_SIZE = 80  # size of each grid cell in pixels
PLACEMENT_CELLS = [
    (7, 8), (9, 8),
    (6, 6), (10, 6),
    (8, 5), (10, 5), (8, 4), (10, 4),
    (5, 3), (7, 3),
    (5, 2), (7, 2), (5, 1), (7, 1),
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
