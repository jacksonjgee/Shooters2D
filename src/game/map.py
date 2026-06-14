import pygame
from settings import MAP_HEIGHT, MAP_WIDTH


class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        wall_thickness = 50

        self.walls = [
            # Outer borders
            pygame.Rect(0, 0, MAP_WIDTH, wall_thickness),
            pygame.Rect(
                0,
                MAP_HEIGHT - wall_thickness,
                MAP_WIDTH,
                wall_thickness
            ),
            pygame.Rect(0, 0, wall_thickness, MAP_HEIGHT),
            pygame.Rect(
                MAP_WIDTH - wall_thickness,
                0,
                wall_thickness,
                MAP_HEIGHT
            ),

            # Interior walls
            pygame.Rect(
                MAP_WIDTH * 0.20,
                MAP_HEIGHT * 0.20,
                MAP_WIDTH * 0.25,
                wall_thickness
            ),

            pygame.Rect(
                MAP_WIDTH * 0.55,
                MAP_HEIGHT * 0.25,
                wall_thickness,
                MAP_HEIGHT * 0.30
            ),

            pygame.Rect(
                MAP_WIDTH * 0.35,
                MAP_HEIGHT * 0.65,
                MAP_WIDTH * 0.30,
                wall_thickness
            ),

            pygame.Rect(
                MAP_WIDTH * 0.75,
                MAP_HEIGHT * 0.60,
                wall_thickness,
                MAP_HEIGHT * 0.20
            ),
        ]

    def draw(self, screen, camera):
        for wall in self.walls:
            pygame.draw.rect(
                screen,
                "darkgray",
                camera.apply(wall)
            )