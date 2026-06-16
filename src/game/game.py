import pygame
import asyncio

from src.game.map import GameMap
from src.game.camera import Camera
from src.game.input_handler import InputHandler
from src.game.entity_manager import EntityManager
from src.game.hud import HUD
from src.game.player_command import PlayerCommand

from settings import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    FPS
    )


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.game_map = GameMap()
        self.camera = Camera()
        self.input_handler = InputHandler()
        self.entity_manager = EntityManager()
        self.hud = HUD()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooters 2D")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create the player
        self.local_player = (
            self.entity_manager.create_player(
                player_id=1,
                position=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2
                ),
                team="defender",
                name="Jackson"
            )
        )

        self.enemy_player = (
            self.entity_manager.create_player(
                player_id=2,
                position=(
                    SCREEN_WIDTH // 2 + 100,
                    SCREEN_HEIGHT // 2 + 100
                ),
                team="attacker",
                name="Enemy"
            )
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
            self.input_handler.handle_event(event)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        self.input_handler.update()

        commands = self._create_player_commands()

        self.entity_manager.update(
            dt=dt,
            commands=commands,
            walls=self.game_map.walls
        )

        self.camera.update(
            self.local_player
        )

    def draw(self):
        self.screen.fill((40, 40, 40))

        self.game_map.draw(
            self.screen,
            self.camera
        )

        self.entity_manager.draw(
            self.screen,
            self.camera
        )

        self.hud.draw(
            screen=self.screen,
            player=self.local_player,
            mouse_screen_position=(
                self.input_handler.mouse_screen_position
            ),
            camera=self.camera
        )

        pygame.display.flip()

    def _create_player_commands(self):
        local_aim_world_position = (
            self.input_handler.mouse_screen_position
            + self.camera.offset
        )

        local_command = PlayerCommand(
            movement_direction=(
                self.input_handler.movement_direction
            ),
            walking=self.input_handler.walk_toggled,
            aim_world_position=(
                local_aim_world_position
            ),
            shooting=self.input_handler.shoot_held,
            reload_pressed=(
                self.input_handler.reload_pressed
            )
        )

        self.input_handler.reload_pressed = False

        enemy_command = PlayerCommand(
            aim_world_position=(
                self.enemy_player.position.copy()
            )
        )

        return {
            self.local_player.player_id: local_command,
            self.enemy_player.player_id: enemy_command
        }