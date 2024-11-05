# tower_and_bullet.py
import pygame

BLACK = (0, 0, 0)

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