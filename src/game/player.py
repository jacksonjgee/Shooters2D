import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED

class Player:
    def __init__(self, player_id, position, team, name):
        self.player_id = player_id
        self.team = team
        self.name = name

        self.position = pygame.Vector2(position)
        self.speed = PLAYER_SPEED

        self.original_image = pygame.image.load(f"assets/{team}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image,(PLAYER_SIZE, PLAYER_SIZE))

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=position)

    def move(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        
        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed * dt
        self.rect.center = self.position
    
    def rotate(self, camera):
        mouse_screen_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_world_pos = mouse_screen_pos + camera.offset
        direction = mouse_world_pos - self.position

        if direction.length_squared() == 0:
            return

        angle = direction.angle_to(pygame.Vector2(1, 0)) - 90

        self.image = pygame.transform.rotate(
            self.original_image,
            angle
        )

        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, camera):
        self.move(dt)
        self.rotate(camera)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))