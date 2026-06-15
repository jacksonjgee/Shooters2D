import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def update(self, target):
        self.offset.x = target.position.x - self.screen_width / 2
        self.offset.y = target.position.y - self.screen_height / 2
    
    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)