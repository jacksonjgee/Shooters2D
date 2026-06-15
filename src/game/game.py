import pygame
import asyncio

from src.game.player import Player
from src.game.map import GameMap
from src.game.camera import Camera
from src.game.input_handler import InputHandler
from src.game.entity_manager import EntityManager

from settings import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    FPS
    )


class Game:
    def __init__(self):
        pygame.init()
        self.game_map = GameMap()
        self.camera = Camera()
        self.input_handler = InputHandler()
        self.entity_manager = EntityManager()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooters 2D")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create the player
        self.player = Player(
            player_id=1,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            team="defender",
            name="Jackson"
        )

    async def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

            await asyncio.sleep(0)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        self.input_handler.update()

        self.player.update(
            dt,
            self.input_handler.movement_direction,
            self.input_handler.mouse_screen_position,
            self.camera,
            self.game_map.walls
        )

        self.camera.update(self.player)

        if self.input_handler.shoot_held:
            bullet = self.player.shoot(
                self.input_handler.mouse_screen_position,
                self.camera
            )

            self.entity_manager.add_bullet(bullet)

        self.entity_manager.update(dt, self.game_map.walls)

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.game_map.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        self.entity_manager.draw(self.screen, self.camera)
        pygame.display.flip()