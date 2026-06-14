import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, player_rect):
        self.offset.x = player_rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player_rect.centery - SCREEN_HEIGHT / 2

    def apply(self, rect):
        return rect.move(
            -round(self.offset.x),
            -round(self.offset.y)
        )