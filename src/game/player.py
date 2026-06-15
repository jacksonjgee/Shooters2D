import pygame
from src.game.weapon import Weapon
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_HITBOX_SIZE

class Player:
    def __init__(self, player_id, position, team, name):
        self.weapon = Weapon()

        self.player_id = player_id
        self.team = team
        self.name = name

        self.position = pygame.Vector2(position)
        self.speed = PLAYER_SPEED

        self.image_offset = pygame.Vector2(0, -7)
        self.original_image = pygame.image.load(f"assets/{team}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image,(PLAYER_SIZE, PLAYER_SIZE))

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=position)

        self.hitbox = pygame.Rect(0, 0, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_SIZE)
        self.hitbox.center = position

    def move(self, dt, movement_direction, walls):
        movement = movement_direction * self.speed * dt

        # Horizontal movement
        self.position.x += movement.x
        self.hitbox.centerx = round(self.position.x)
        self._check_collisions(walls, "x", movement.x)

        # Vertical movement
        self.position.y += movement.y
        self.hitbox.centery = round(self.position.y)
        self._check_collisions(walls, "y", movement.y)

        # Keep the image centred on the player's final position
        self.rect.center = self.hitbox.center
    
    def _check_collisions(self, walls, axis, movement):
        for wall in walls:
            if self.hitbox.colliderect(wall):

                if axis == "x":
                    if movement > 0:
                        self.hitbox.right = wall.left
                    elif movement < 0:
                        self.hitbox.left = wall.right

                    self.position.x = self.hitbox.centerx

                elif axis == "y":
                    if movement > 0:
                        self.hitbox.bottom = wall.top
                    elif movement < 0:
                        self.hitbox.top = wall.bottom

                    self.position.y = self.hitbox.centery
    
    def rotate(self, mouse_screen_position, camera):
        mouse_world_position = mouse_screen_position + camera.offset

        direction = mouse_world_position - self.position

        if direction.length_squared() == 0:
            return

        angle = direction.angle_to(pygame.Vector2(1, 0)) - 90

        self.image = pygame.transform.rotate(
            self.original_image,
            angle
        )

        rotated_offset = self.image_offset.rotate(-angle)
        image_center = self.position + rotated_offset

        self.rect = self.image.get_rect(center=image_center)

    def update(
        self,
        dt,
        movement_direction,
        mouse_screen_position,
        camera,
        walls
    ):
        self.move(dt, movement_direction, walls)
        self.rotate(mouse_screen_position, camera)
        self.weapon.update(dt)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            camera.apply(self.hitbox),
            2
        )

    def shoot(self, mouse_screen_position, camera, walls):
        mouse_world_position = (
            mouse_screen_position + camera.offset
        )

        direction = mouse_world_position - self.position

        return self.weapon.shoot(
            position=self.position.copy(),
            direction=direction,
            walls=walls
        )
        
        
    
    