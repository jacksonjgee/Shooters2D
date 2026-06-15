import pygame
from settings import MAP_HEIGHT, MAP_WIDTH


class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.walls = [
            pygame.Rect(0, 0, self.width, 40),
            pygame.Rect(0, self.height - 40, self.width, 40),
            pygame.Rect(0, 0, 40, self.height),
            pygame.Rect(self.width - 40, 0, 40, self.height),

            pygame.Rect(400, 300, 300, 40),
            pygame.Rect(900, 600, 40, 300),
        ]

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (100, 100, 100), wall)