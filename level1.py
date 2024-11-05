import pygame, sys
import random
import enemy as enmy
import tower as twr

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Get screen dimensions for fullscreen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Load and scale background image
BACKGROUND_IMAGE = pygame.image.load("assets/level1/map/map.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the path as a list of (x, y) coordinates
PATH = [
    (660, SCREEN_HEIGHT), (660, 560), (790, 560), (790, 385), (520, 385), (520, 0)
]

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
            self.enemies.append(enmy.Enemy(PATH))

    def spawn_enemy(self):
        self.enemies.append(enmy.Enemy(PATH))

    def run(self):
        self.spawn_wave()  # Start the game by spawning the first wave
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.towers.append(twr.Tower(x, y))

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

# Start the game directly
game = TowerDefenseGame()
game.run()