import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Get screen dimensions for fullscreen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Load and scale background image
BACKGROUND_IMAGE = pygame.image.load("assets/images/level1/Tiles.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load cannon images
CANNON_double = pygame.image.load("assets/images/tower/Cannon3.png")
CANNON_small = pygame.image.load("assets/images/tower/Cannon2.png")
Bullet_image = pygame.image.load("assets/images/tower/Bullet_Cannon.png")

# Scale cannon images
CANNON_double = pygame.transform.scale(CANNON_double, (45, 45))
CANNON_small = pygame.transform.scale(CANNON_small, (45, 45))

# Define the path as a list of (x, y) coordinates in percentages
PATH_PERCENTAGES = [
    (0.51, 1.0), (0.51, 0.78), (0.62, 0.78), (0.62, 0.53), (0.405, 0.53), (0.405, 0.0)
]

# Convert path percentages to actual screen coordinates
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in PATH_PERCENTAGES]

# Enemy class
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

# Bullet class
class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
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

# Tower class (now with selectable cannon types)
class Tower:
    def __init__(self, x, y, cannon_type):
        self.x = x
        self.y = y
        self.cannon_type = cannon_type
        self.range = 150 if cannon_type == "double" else 100
        self.damage = 20 if cannon_type == "double" else 10
        self.cooldown = 2000 if cannon_type == "double" else 1000  # different cooldowns for cannon types
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.angle = 0
        self.image = CANNON_double if cannon_type == "double" else CANNON_small

    def shoot(self, enemies, current_time):
        if current_time - self.last_shot >= self.cooldown:
            for enemy in enemies:
                if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                    self.bullets.append(Bullet(self.x, self.y, enemy))
                    self.target = enemy
                    self.last_shot = current_time
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
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)

# Main game class
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
        self.spawn_interval = 2000
        self.lives = 50
        self.selected_cannon_type = "double"  # Default selected cannon type

    def spawn_enemy(self):
        self.enemies.append(Enemy(PATH))

    def run(self):
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
                # Check if user clicked on cannon selection buttons
                if 10 <= x <= 60 and 10 <= y <= 60:
                    self.selected_cannon_type = "double"
                elif 10 <= x <= 60 and 70 <= y <= 120:
                    self.selected_cannon_type = "small"
                else:
                    # Place tower with the selected cannon type
                    self.towers.append(Tower(x, y, self.selected_cannon_type))

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
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for tower in self.towers:
            tower.draw(self.screen)

        # Draw lives
        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(lives_text, (10, 10))

        # Draw cannon selection icons
        pygame.draw.rect(self.screen, GRAY, (10, 10, 50, 50))  # Button for double cannon
        pygame.draw.rect(self.screen, GRAY, (10, 70, 50, 50))  # Button for small cannon
        self.screen.blit(CANNON_double, (10, 10))
        self.screen.blit(CANNON_small, (10, 70))

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = TowerDefenseGame()
    game.run()
    pygame.quit()
