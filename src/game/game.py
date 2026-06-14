import pygame
import math
from src.game.player import Player
from src.game.map import GameMap
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED
from src.game.camera import Camera

class Game:
    def __init__(self) -> None:
        pygame.init() 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.game_map = GameMap()
        self.camera = Camera()
    
    def run(self) -> None:
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(delta_time)
            self.draw()

        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        speed = PLAYER_SPEED
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= speed
        if keys[pygame.K_s]:
            dy += speed
        if keys[pygame.K_a]:
            dx -= speed
            self.player.face_left()
        if keys[pygame.K_d]:
            dx += speed
            self.player.face_right()

        # Prevent diagonal movement from being faster
        if dx != 0 and dy != 0:
            diagonal_speed = speed / math.sqrt(2)
            dx *= diagonal_speed
            dy *= diagonal_speed
        else:
            dx *= speed
            dy *= speed

        self.player.change_xpos(dx)
        self.player.change_ypos(dy)

    def update(self, delta_time):
        self.camera.update(self.player.rect)

    def draw(self):
        pygame.display.set_caption("Shooters2D")
        self.screen.fill("white")
        self.game_map.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        

        pygame.display.flip()
        self.clock.tick(60)