import pygame
import asyncio

from src.game.map import GameMap
from src.game.camera import Camera
from src.game.input_handler import InputHandler
from src.game.entity_manager import EntityManager
from src.game.hud import HUD
from src.network.command_manager import CommandManager
from src.network.state_manager import StateManager
from src.network.webrtc_connection import WebRTCConnection
from src.network.network_session import NetworkSession
from src.game.lobby import Lobby

from settings import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    FPS
    )


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        self.game_map = GameMap()
        self.camera = Camera()
        self.input_handler = InputHandler()
        self.entity_manager = EntityManager()
        self.hud = HUD()
        self.lobby = Lobby()
        self.game_mode = "lobby"
        pygame.key.start_text_input()

        self.webrtc_connection = WebRTCConnection()

        self.network_session = NetworkSession(
            connection=self.webrtc_connection
        )

        self.command_manager = CommandManager(
            connection=self.webrtc_connection
        )

        self.state_manager = StateManager(
            connection=self.webrtc_connection
        )

        print(
            "WebRTC supported:",
            self.webrtc_connection.is_supported
        )

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooters 2D")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create the player
        # Create the players at the map spawn points.
        self.local_player = (
            self.entity_manager.create_player(
                player_id=1,
                position=self.game_map.defender_spawn,
                team="defender",
                name="Jackson"
            )
        )

        self.enemy_player = (
            self.entity_manager.create_player(
                player_id=2,
                position=self.game_map.attacker_spawn,
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
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    continue

            if self.game_mode == "lobby":
                self.lobby.handle_event(
                    event=event,
                    network_session=(
                        self.network_session
                    )
                )

            elif self.game_mode == "playing":
                self.input_handler.handle_event(
                    event
                )

    def update(self, dt):
        self.network_session.update()

        if self.game_mode == "lobby":
            next_mode = self.lobby.update(
                self.network_session
            )

            if next_mode == "playing":
                self.game_mode = "playing"

                pygame.key.stop_text_input()
                pygame.mouse.set_visible(False)

            return

        self.input_handler.update()

        commands = self._create_player_commands()

        role = self.webrtc_connection.get_role()

        connected = (
            self.webrtc_connection.is_connected()
        )

        if role != "client" or not connected:
            self.entity_manager.update(
                dt=dt,
                commands=commands,
                walls=self.game_map.walls
            )
        else:
            self.entity_manager.update_bullets_only(
                dt
            )

        self.state_manager.update(
            players=self.entity_manager.players,
            entity_manager=self.entity_manager
        )

        controlled_player = (
            self._get_controlled_player()
        )

        self.camera.update(
            controlled_player
        )

    def draw(self):
        if self.game_mode == "lobby":
            self.lobby.draw(
                screen=self.screen,
                network_session=(
                    self.network_session
                )
            )

            pygame.display.flip()
            return

        self.screen.fill(
            (40, 40, 40)
        )

        controlled_player = (
            self._get_controlled_player()
        )

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
            player=controlled_player,
            mouse_screen_position=(
                self.input_handler
                    .mouse_screen_position
            ),
            camera=self.camera
        )

        pygame.display.flip()

    def _create_player_commands(self):
        remote_players = [
            player
            for player in self.entity_manager.players
            if player is not self.local_player
        ]

        return self.command_manager.create_commands(
            input_handler=self.input_handler,
            camera=self.camera,
            local_player=self.local_player,
            remote_players=remote_players
        )

    def _get_controlled_player(self):
        if (
            self.webrtc_connection.is_connected()
            and self.webrtc_connection.get_role()
            == "client"
        ):
            return self.enemy_player

        return self.local_player