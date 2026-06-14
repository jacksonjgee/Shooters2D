import pygame
import math
from src.game.player import Player

class Game:
    def __init__(self) -> None:
        pygame.init() 
        self.screen = pygame.display.set_mode((1280, 1024))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
    
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        speed = 5
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

    def update(self):
        pass

    def draw(self):
        pygame.display.set_caption("Shooters2D")
        self.screen.fill("white")

        self.player.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)