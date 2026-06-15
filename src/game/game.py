import pygame
from src.game.player import Player
from src.game.map import GameMap
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS


class Game:
    def __init__(self):
        pygame.init()
        self.game_map = GameMap()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooters 2D")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create the player
        self.player = Player(
            player_id=1,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            team="attacker",
            name="Jackson"
        )

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt)

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.game_map.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()