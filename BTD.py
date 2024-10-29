import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background1.png")

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Tower Defense Game Classes
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Get screen dimensions for fullscreen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Load and scale background image
BACKGROUND_IMAGE = pygame.image.load("assets/map.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the path as a list of (x, y) coordinates
PATH = [
    (660, SCREEN_HEIGHT), (660, 560), (790, 560), (790, 385), (520, 385), (520, 0)
]

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[self.path_index]
        self.speed = 2
        self.health = 100

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
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)

    def has_reached_end(self):
        return self.path_index >= len(self.path) - 1

class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.radius = 5

    def move(self):
        direction_x = self.target.x - self.x
        direction_y = self.target.y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
        direction_x /= distance
        direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

    def has_hit_target(self):
        return (self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2 <= self.radius ** 2

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 10
        self.cooldown = 5000  # 5 seconds cooldown
        self.last_shot = 0
        self.bullets = []

    def shoot(self, enemies, current_time):
        if current_time - self.last_shot >= self.cooldown:
            for enemy in enemies:
                if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                    self.bullets.append(Bullet(self.x, self.y, enemy))
                    self.last_shot = current_time
                    break

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.has_hit_target():
                bullet.target.health = 0  # Set health to 0 when hit
                self.bullets.remove(bullet)

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 15)
        for bullet in self.bullets:
            bullet.draw(screen)

class TowerDefenseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemies = []
        self.towers = []
        self.wave_number = 0
        self.spawn_timer = 0
        self.spawn_interval = 2000  # Spawn new enemies every 2 seconds
        self.lives = 50  # Player starts with 50 lives

    def spawn_wave(self):
        self.wave_number += 1
        for _ in range(self.wave_number * 5):
            self.enemies.append(Enemy(PATH))

    def spawn_enemy(self):
        self.enemies.append(Enemy(PATH))

    def run(self):
        self.spawn_wave()  # Start the game by spawning the first wave
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        # Once the game ends, return to the main menu
        main_menu()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.towers.append(Tower(x, y))

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
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for tower in self.towers:
            tower.draw(self.screen)

        # Draw lives
        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(lives_text, (10, 10))

        pygame.display.flip()

# Play button starts the game
def play():
    game = TowerDefenseGame()
    game.run()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("TD-Gambling", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Start the Tower Defense game when Play button is clicked
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
