# Configuration file for Tower Defense Game

# Game settings
INITIAL_LIVES = 15  # Number of lives at game start
START_COINS   = 1125  # Starting coins
COIN_REWARD   = 7   # Coins earned per enemy kill

# Enemy settings
ENEMY_HEALTH = 120   # Initial health of each enemy
ENEMY_SPEED  = 1.5   # Movement speed of enemies

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
SHOP_WIDTH     = ICON_SIZE + ICON_PADDING * 4  # Width of the sidebar

# Colors (RGB)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
GREEN = (0,   255, 0)
BLUE  = (0,   0, 255)
GRAY  = (169, 169, 169)

# Enemy path defined as relative percentages of screen size
PATH_PERCENTAGES_LEVEL_1 = [
    (0.4641, 1.00),
    (0.4641, 0.7056),
    (0.582, 0.6861),
    (0.59, 0.47),
    (0.36, 0.45),
    (0.36, 0.00),
]
PATH_PERCENTAGES_LEVEL_2 = [
    (0.5547, 0.9986),
    (0.5563, 0.9583),
    (0.5648, 0.9097),
    (0.5727, 0.8375),
    (0.5445, 0.8306),
    (0.5078, 0.8167),
    (0.4859, 0.8042),
    (0.4633, 0.7764),
    (0.4383, 0.7417),
    (0.4242, 0.7014),
    (0.4242, 0.6417),
    (0.4172, 0.5972),
    (0.4, 0.5597),
    (0.3773, 0.5264),
    (0.3516, 0.5181),
    (0.3344, 0.4986),
    (0.3195, 0.4736),
    (0.307, 0.4347),
    (0.3, 0.3958),
    (0.2961, 0.3542),
    (0.3008, 0.3111),
    (0.3141, 0.2597),
    (0.3406, 0.2125),
    (0.3609, 0.1722),
    (0.3695, 0.1153),
    (0.3695, 0.0847),
    (0.3695, 0.0375),
    (0.3672, 0.0),
]

PATH_PERCENTAGES_LEVEL_3 = [
    (0.2086, 0.9986),
    (0.207, 0.8278),
    (0.2383, 0.8056),
    (0.2859, 0.7931),
    (0.3445, 0.7847),
    (0.3461, 0.6333),
    (0.3883, 0.6153),
    (0.4633, 0.6056),
    (0.5258, 0.5944),
    (0.5219, 0.4389),
    (0.4727, 0.4222),
    (0.4211, 0.4208),
    (0.3539, 0.4236),
    (0.3133, 0.3889),
    (0.3047, 0.2181),
    (0.3086, 0.0),
]