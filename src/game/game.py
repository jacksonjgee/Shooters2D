import math
import pygame

from settings import FPS, PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from src.game.bullet import Bullet
from src.game.camera import Camera
from src.game.map import GameMap
from src.game.player import Player
from src.game.ui import GameUI
from src.game.visibility import VisibilitySystem


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Shooters2D")

        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(
            player_id=1,
            position=(150, 150),
            team="attackers",
            name="Jackson"
        )

        self.enemies = [
            # Top-left room
            Player(
                player_id=2,
                position=(500, 500),
                team="defenders",
                name="Enemy 1"
            ),

            # Top-centre corridor
            Player(
                player_id=3,
                position=(1250, 400),
                team="defenders",
                name="Enemy 2"
            ),

            # Top-right room
            Player(
                player_id=4,
                position=(2200, 500),
                team="defenders",
                name="Enemy 3"
            ),

            # Centre structure
            Player(
                player_id=5,
                position=(1350, 1050),
                team="defenders",
                name="Enemy 4"
            ),

            # Right stepped corridor
            Player(
                player_id=6,
                position=(2350, 1100),
                team="defenders",
                name="Enemy 5"
            ),

            # Bottom-left room
            Player(
                player_id=7,
                position=(500, 1600),
                team="defenders",
                name="Enemy 6"
            ),

            # Bottom-centre passage
            Player(
                player_id=8,
                position=(1350, 1500),
                team="defenders",
                name="Enemy 7"
            ),

            # Bottom-right room
            Player(
                player_id=9,
                position=(2300, 1450),
                team="defenders",
                name="Enemy 8"
            ),
        ]

        self.players = [
            self.player,
            *self.enemies
        ]

        self.players = [
            self.player,
            *self.enemies
        ]

        self.game_map = GameMap()
        self.camera = Camera()
        self.ui = GameUI()
        self.bullets = []

        self.visibility = VisibilitySystem()

    def run(self) -> None:
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(delta_time)
            self.draw()

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.player.start_reload()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.player.is_reloading:
                        self.player.cancel_reload()

                    # Immediately attempts to fire on the click
                    self.fire_bullet()

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
            self.player.face_left()
        if keys[pygame.K_d]:
            dx += 1
            self.player.face_right()

        if dx != 0 and dy != 0:
            dx /= math.sqrt(2)
            dy /= math.sqrt(2)

        self.player.move(
            dx * PLAYER_SPEED,
            dy * PLAYER_SPEED,
            self.game_map.walls,
            self.players
        )

    def update(self, delta_time: float) -> None:
        # Update reload and fire-rate timers
        for player in self.players:
            player.update(delta_time)

        # Keep camera centred on the player
        self.camera.update(self.player.hitbox)

        # Hold left mouse button to continuously fire
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] and not self.player.is_reloading:
            self.fire_bullet()

        # Move bullets and check wall collisions
        for bullet in self.bullets:
            bullet.update(
                delta_time,
                self.game_map.walls,
                self.players
            )

        # Remove bullets that are no longer active
        self.bullets = [
            bullet
            for bullet in self.bullets
            if bullet.alive
        ]

    def draw(self) -> None:
        self.screen.fill("white")

        self.game_map.draw(
            self.screen,
            self.camera
        )

        for bullet in self.bullets:
            bullet.draw(
                self.screen,
                self.camera
            )

        for player in self.players:
            player.draw(
                self.screen,
                self.camera
            )

        self.visibility.draw(
            self.screen,
            self.player,
            self.camera,
            self.game_map.walls
        )

        self.game_map.draw(
            self.screen,
            self.camera
        )

        self.ui.draw(
            self.screen,
            self.player,
            self.camera,
            self.game_map.walls
        )

        pygame.display.flip()
    
    def fire_bullet(self) -> None:
        if not self.player.shoot():
            return

        mouse_screen_position = pygame.Vector2(
            pygame.mouse.get_pos()
        )

        mouse_world_position = (
            mouse_screen_position + self.camera.offset
        )

        bullet = Bullet(
            self.player.hitbox.center,
            mouse_world_position,
            owner_id=self.player.player_id,
            team=self.player.team
        )

        self.bullets.append(bullet)