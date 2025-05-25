import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Get screen dimensions for fullscreen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Grid and placement setup
GRID_SIZE = 80  # size of one grid cell
PLACEMENT_CELLS = [
    (7, 8), (9, 8),
    (6, 6), (10, 6),
    (8, 5), (10, 5), (8, 4), (10, 4),
    (5, 3), (7, 3),
    (5, 2), (7, 2), (5, 1), (7, 1),
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Icon, font, and shop sizes
ICON_SIZE = 70
ICON_PADDING = 10
HUD_FONT_SIZE = 40
SHOP_WIDTH = ICON_SIZE + ICON_PADDING * 2

# Load and scale background image
BACKGROUND_IMAGE = pygame.image.load("assets/images/level1/Tiles.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load cannon images
RAW_CANNON_DOUBLE = pygame.image.load("assets/images/tower/Cannon3.png")
RAW_CANNON_SMALL = pygame.image.load("assets/images/tower/Cannon2.png")
Bullet_image = pygame.image.load("assets/images/tower/Bullet_Cannon.png")

# Scale cannon images for towers and selection icons
CANNON_double = pygame.transform.scale(RAW_CANNON_DOUBLE, (ICON_SIZE, ICON_SIZE))
CANNON_small = pygame.transform.scale(RAW_CANNON_SMALL, (ICON_SIZE, ICON_SIZE))

# Define the path as a list of (x, y) coordinates in percentages
PATH_PERCENTAGES = [
    (0.51, 1.0), (0.51, 0.78), (0.62, 0.78), (0.62, 0.53), (0.405, 0.53), (0.405, 0.0)
]

# Convert path percentages to actual screen coordinates
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in PATH_PERCENTAGES]

# Enemy class
def draw_circle(screen, pos, color, radius):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[self.path_index]
        self.speed = 2
        self.health = 100

    def move(self):
        if self.path_index < len(self.path) - 1:
            tx, ty = self.path[self.path_index + 1]
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist:
                dx, dy = dx / dist, dy / dist
            self.x += dx * self.speed
            self.y += dy * self.speed
            if abs(self.x - tx) < self.speed and abs(self.y - ty) < self.speed:
                self.path_index += 1

    def draw(self, screen):
        draw_circle(screen, (self.x, self.y), RED, 10)

    def has_reached_end(self):
        return self.path_index >= len(self.path) - 1

# Bullet class
class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 10
        self.image = pygame.transform.scale(Bullet_image, (20, 20))
        self.radius = 10

    def move(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist:
            dx, dy = dx / dist, dy / dist
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, (int(self.x - 10), int(self.y - 10)))

    def has_hit_target(self):
        return (self.target.x - self.x)**2 + (self.target.y - self.y)**2 <= self.radius**2

# Tower class
class Tower:
    def __init__(self, x, y, cannon_type):
        self.x, self.y = x, y
        self.cannon_type = cannon_type
        self.range = 350 if cannon_type == "double" else 200
        self.cooldown = 2000 if cannon_type == "double" else 1000
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.angle = 0
        self.image = CANNON_double if cannon_type == "double" else CANNON_small

    def shoot(self, enemies, now):
        if now - self.last_shot >= self.cooldown:
            for e in enemies:
                if (e.x - self.x)**2 + (e.y - self.y)**2 <= self.range**2:
                    self.bullets.append(Bullet(self.x, self.y, e))
                    self.target, self.last_shot = e, now
                    break

    def update_bullets(self):
        for b in self.bullets[:]:
            b.move()
            if b.has_hit_target():
                b.target.health = 0
                self.bullets.remove(b)

    def update_rotation(self):
        if self.target:
            dx, dy = self.target.x - self.x, self.target.y - self.y
            self.angle = math.degrees(math.atan2(-dy, dx)) - 90

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        r = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, r.topleft)
        for b in self.bullets:
            b.draw(screen)

# Main game class
class TowerDefenseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemies, self.towers = [], []
        self.spawn_timer, self.spawn_interval = 0, 2000
        self.lives = 10
        # Münzsystem
        self.coins = 15
        self.coin_reward = 5
        self.tower_costs = {"double": 20, "small": 10}
        self.selected_cannon_type = "double"
        self.message, self.message_timer = "", 0

    def spawn_enemy(self):
        self.enemies.append(Enemy(PATH))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Calculate shop icon positions
                font = pygame.font.SysFont(None, HUD_FONT_SIZE)
                coins_h = font.render(f"Münzen: {self.coins}", True, BLACK).get_height()
                lives_h = font.render(f"Lives: {self.lives}", True, BLACK).get_height()
                y_start = ICON_PADDING*2 + coins_h + lives_h  # first icon y
                y_double = y_start
                y_small = y_double + ICON_SIZE + ICON_PADDING
                # Double tower icon click
                if ICON_PADDING <= x <= ICON_PADDING + ICON_SIZE and y_double <= y <= y_double + ICON_SIZE:
                    self.selected_cannon_type = "double"
                # Small tower icon click
                if ICON_PADDING <= x <= ICON_PADDING + ICON_SIZE and y_small <= y <= y_small + ICON_SIZE:
                    self.selected_cannon_type = "small"
                # Place tower
                if x > SHOP_WIDTH:  # ensure click is in game area
                    gx, gy = x//GRID_SIZE, y//GRID_SIZE
                    if (gx, gy) in PLACEMENT_CELLS:
                        cost = self.tower_costs[self.selected_cannon_type]
                        if self.coins >= cost:
                            self.coins -= cost
                            wx, wy = gx*GRID_SIZE + GRID_SIZE//2, gy*GRID_SIZE + GRID_SIZE//2
                            self.towers.append(Tower(wx, wy, self.selected_cannon_type))
                        else:
                            self.message, self.message_timer = f"Benötigt: {cost} Münzen", pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = now
        for e in self.enemies:
            e.move()
        for t in self.towers:
            t.shoot(self.enemies, now)
            t.update_bullets()
            t.update_rotation()
        for e in self.enemies[:]:
            if e.has_reached_end():
                self.lives -= 1
                self.enemies.remove(e)
            elif e.health <= 0:
                self.coins += self.coin_reward
                self.enemies.remove(e)
        if self.lives <= 0:
            self.running = False

    def draw(self):
        # Background and sidebar
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(self.screen, GRAY, (0, 0, SHOP_WIDTH, SCREEN_HEIGHT))
        # Coins and lives
        font = pygame.font.SysFont(None, HUD_FONT_SIZE)
        coins_surf = font.render(f"Münzen: {self.coins}", True, BLACK)
        lives_surf = font.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(coins_surf, (ICON_PADDING, ICON_PADDING))
        self.screen.blit(lives_surf, (ICON_PADDING, ICON_PADDING + coins_surf.get_height() + ICON_PADDING))
        # Shop icons
        y_start = ICON_PADDING*2 + coins_surf.get_height() + lives_surf.get_height()
        y_double = y_start
        y_small = y_double + ICON_SIZE + ICON_PADDING
        # Button backgrounds
        color_d = GREEN if self.coins >= self.tower_costs["double"] else RED
        pygame.draw.rect(self.screen, color_d, (ICON_PADDING, y_double, ICON_SIZE, ICON_SIZE))
        color_s = GREEN if self.coins >= self.tower_costs["small"] else RED
        pygame.draw.rect(self.screen, color_s, (ICON_PADDING, y_small, ICON_SIZE, ICON_SIZE))
        # Icons
        self.screen.blit(CANNON_double, (ICON_PADDING, y_double))
        self.screen.blit(CANNON_small, (ICON_PADDING, y_small))
        # Game area
        for e in self.enemies:
            e.draw(self.screen)
        for t in self.towers:
            t.draw(self.screen)
        # Grid debug
        for gx, gy in PLACEMENT_CELLS:
            pygame.draw.rect(self.screen, GREEN, (gx*GRID_SIZE, gy*GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)
        # Message
        if self.message and pygame.time.get_ticks() - self.message_timer < 2000:
            msg = font.render(self.message, True, RED)
            self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, ICON_PADDING))
        pygame.display.flip()

if __name__ == "__main__":
    TowerDefenseGame().run()
    pygame.quit()
