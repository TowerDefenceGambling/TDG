# enemy.py
import pygame

RED = (255, 0, 0)

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