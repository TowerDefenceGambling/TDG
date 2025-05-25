import pygame
import random
import math
import config

# Initialize Pygame
pygame.init()

# Get screen dimensions for fullscreen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Load and scale background image
BACKGROUND_IMAGE = pygame.image.load("assets/images/level1/Tiles.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Scale icons from config sizes
RAW_CANNON_DOUBLE = pygame.image.load("assets/images/tower/Cannon3.png")
RAW_CANNON_SMALL = pygame.image.load("assets/images/tower/Cannon2.png")
RAW_COIN_ICON = pygame.image.load("assets/images/level1/coin.png")
Bullet_image = pygame.image.load("assets/images/tower/Bullet_Cannon.png")

CANNON_double = pygame.transform.scale(RAW_CANNON_DOUBLE, (config.ICON_SIZE, config.ICON_SIZE))
CANNON_small = pygame.transform.scale(RAW_CANNON_SMALL, (config.ICON_SIZE, config.ICON_SIZE))
COIN_ICON = pygame.transform.scale(RAW_COIN_ICON, (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))

# Convert path percentages to actual screen coordinates
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in config.PATH_PERCENTAGES]

# Draw helper
def draw_circle(screen, pos, color, radius):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

# Enemy class
class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.speed = config.ENEMY_SPEED
        self.health = config.ENEMY_HEALTH

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
        draw_circle(screen, (self.x, self.y), config.RED, 10)

    def has_reached_end(self):
        return self.path_index >= len(self.path) - 1

# Bullet class
class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y, self.target = x, y, target
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
        return (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2 <= self.radius ** 2

# Tower class
class Tower:
    def __init__(self, x, y, type_):
        self.x, self.y = x, y
        cfg = config.TOWER_CONFIG[type_]
        self.cost = cfg["cost"]
        self.range = cfg["range"]
        self.cooldown = cfg["cooldown"]
        self.damage = cfg["damage"]
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.angle = 0
        self.image = CANNON_double if type_ == "double" else CANNON_small

    def shoot(self, enemies, now):
        if now - self.last_shot >= self.cooldown:
            for e in enemies:
                if (e.x - self.x) ** 2 + (e.y - self.y) ** 2 <= self.range ** 2:
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
        rot = pygame.transform.rotate(self.image, self.angle)
        rect = rot.get_rect(center=(self.x, self.y))
        screen.blit(rot, rect.topleft)
        for b in self.bullets:
            b.draw(screen)

# Main game
class TowerDefenseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemies = []
        self.towers = []
        self.spawn_timer = 0
        self.spawn_interval = config.spawn_interval if hasattr(config, 'spawn_interval') else 2000
        self.lives = config.INITIAL_LIVES
        self.coins = config.START_COINS
        self.coin_reward = config.COIN_REWARD
        self.tower_costs = {t: cfg["cost"] for t, cfg in config.TOWER_CONFIG.items()}
        self.selected = "double"
        self.message = ""
        self.msg_time = 0

    def spawn_enemy(self):
        self.enemies.append(Enemy(PATH))

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # calculate icon positions
                y0 = config.ICON_PADDING * 2 + COIN_ICON.get_height() + pygame.font.SysFont(None, config.HUD_FONT_SIZE).render(str(self.lives), True, config.BLACK).get_height()
                if config.ICON_PADDING <= x <= config.ICON_PADDING + config.ICON_SIZE and y0 <= y <= y0 + config.ICON_SIZE:
                    self.selected = "double"
                y1 = y0 + config.ICON_SIZE + config.ICON_PADDING
                if config.ICON_PADDING <= x <= config.ICON_PADDING + config.ICON_SIZE and y1 <= y <= y1 + config.ICON_SIZE:
                    self.selected = "small"
                if x > config.SHOP_WIDTH:
                    gx, gy = x // config.GRID_SIZE, y // config.GRID_SIZE
                    if (gx, gy) in config.PLACEMENT_CELLS:
                        cost = self.tower_costs[self.selected]
                        if self.coins >= cost:
                            self.coins -= cost
                            wx = gx * config.GRID_SIZE + config.GRID_SIZE // 2
                            wy = gy * config.GRID_SIZE + config.GRID_SIZE // 2
                            self.towers.append(Tower(wx, wy, self.selected))
                        else:
                            self.message = f"Benötigt: {cost} Münzen"
                            self.msg_time = pygame.time.get_ticks()

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
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(self.screen, config.GRAY, (0, 0, config.SHOP_WIDTH, SCREEN_HEIGHT))
        # coin icon + amount
        font = pygame.font.SysFont(None, config.HUD_FONT_SIZE)
        self.screen.blit(COIN_ICON, (config.ICON_PADDING, config.ICON_PADDING))
        amt = font.render(str(self.coins), True, config.BLACK)
        self.screen.blit(amt, (config.ICON_PADDING + COIN_ICON.get_width() + 5, config.ICON_PADDING + (COIN_ICON.get_height() - amt.get_height()) // 2))
        # lives
        lives_s = font.render(str(self.lives), True, config.BLACK)
        self.screen.blit(lives_s, (config.ICON_PADDING, config.ICON_PADDING + COIN_ICON.get_height() + config.ICON_PADDING))
        # shop icons
        y0 = config.ICON_PADDING * 2 + COIN_ICON.get_height() + lives_s.get_height()
        # double
        cd = config.GREEN if self.coins >= self.tower_costs["double"] else config.RED
        pygame.draw.rect(self.screen, cd, (config.ICON_PADDING, y0, config.ICON_SIZE, config.ICON_SIZE))
        self.screen.blit(CANNON_double, (config.ICON_PADDING, y0))
        # small
        y1 = y0 + config.ICON_SIZE + config.ICON_PADDING
        cs = config.GREEN if self.coins >= self.tower_costs["small"] else config.RED
        pygame.draw.rect(self.screen, cs, (config.ICON_PADDING, y1, config.ICON_SIZE, config.ICON_SIZE))
        self.screen.blit(CANNON_small, (config.ICON_PADDING, y1))
        # game area entities
        for e in self.enemies:
            e.draw(self.screen)
        for t in self.towers:
            t.draw(self.screen)
        # debug grid
        for gx, gy in config.PLACEMENT_CELLS:
            pygame.draw.rect(self.screen, config.GREEN, (gx * config.GRID_SIZE, gy * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 2)
        # message
        if self.message and pygame.time.get_ticks() - self.msg_time < 2000:
            msg = font.render(self.message, True, config.RED)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, config.ICON_PADDING))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = TowerDefenseGame()
    game.run()
    pygame.quit()
