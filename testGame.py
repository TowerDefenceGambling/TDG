import pygame
import random
import math
from button import Button

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
            target_x, target_y = self.path[self.path_index + 1]
            direction_x = target_x - self.x
            direction_y = target_y - self.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            direction_x /= distance
            direction_y /= distance

            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

            if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
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
        # Load and scale the bullet image
        self.image = pygame.transform.scale(Bullet_image, (20, 20))  # adjust size as needed
        self.radius = 10  # Adjust hit radius as needed

    def move(self):
        direction_x = self.target.x - self.x
        direction_y = self.target.y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
        direction_x /= distance
        direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def draw(self, screen):
        # Draw the bullet as an image instead of a black circle
        rotated_image = pygame.transform.rotate(self.image, 0)  # Rotate if needed
        screen.blit(rotated_image, (int(self.x - self.image.get_width() / 2), int(self.y - self.image.get_height() / 2)))

    def has_hit_target(self):
        return (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2 <= self.radius ** 2
        return (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2 <= self.radius ** 2

# Tower class (now with selectable cannon types)
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
        for bullet in self.bullets:
            bullet.move()
            if bullet.has_hit_target():
                bullet.target.health = 0
                self.bullets.remove(bullet)

    def update_rotation(self):
        if self.target:
            direction_x = self.target.x - self.x
            direction_y = self.target.y - self.y
            self.angle = math.degrees(math.atan2(-direction_y, direction_x)) - 90

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = current_time

        for enemy in self.enemies:
            enemy.move()
        for tower in self.towers:
            tower.shoot(self.enemies, current_time)
            tower.update_bullets()
            tower.update_rotation()

        # Check if any enemies have reached the end
        for enemy in self.enemies:
            if enemy.has_reached_end():
                self.lives -= 1
                self.enemies.remove(enemy)

        # Remove dead enemies
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

        # End game if lives reach 0
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


    def pause_menu(self):
        paused = True
        font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)

        resume_button = Button(None, (640, 250), "Resume", button_font, WHITE, RED)
        exit_button = Button(None, (640, 330), "Exit", button_font, WHITE, RED)
        volume_button = Button(None, (640, 410), "Toggle Sound", button_font, WHITE, RED)

        while paused:
            self.screen.fill((50, 50, 50))
            pause_text = font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, 150)))

            mouse_pos = pygame.mouse.get_pos()

            for button in [resume_button, exit_button, volume_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.checkForInput(mouse_pos):
                        paused = False
                    elif exit_button.checkForInput(mouse_pos):
                        self.running = False
                        return
                    elif volume_button.checkForInput(mouse_pos):
                        vol = pygame.mixer.music.get_volume()
                        pygame.mixer.music.set_volume(0.0 if vol > 0 else 1.0)

    def game_over_screen(self):
        font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)

        restart_button = Button(None, (640, 300), "Restart", button_font, WHITE, RED)
        exit_button = Button(None, (640, 380), "Exit", button_font, WHITE, RED)

        while True:
            self.screen.fill((0, 0, 0))
            game_over_text = font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150)))

            mouse_pos = pygame.mouse.get_pos()

            for button in [restart_button, exit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.checkForInput(mouse_pos):
                        self.__init__()  # Neustart
                        self.run()
                        return
                    elif exit_button.checkForInput(mouse_pos):
                        self.running = False
                        return



# Run the game
if __name__ == "__main__":
    game = TowerDefenseGame()
    game.run()
    game = TowerDefenseGame()
    game.run()
    pygame.quit()
