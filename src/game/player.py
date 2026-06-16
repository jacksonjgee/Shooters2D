import pygame
from src.game.weapon import Weapon

from settings import (
    PLAYER_SIZE,
    PLAYER_RUN_SPEED,
    PLAYER_WALK_SPEED,
    PLAYER_HITBOX_SIZE,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION
)

class Player:
    def __init__(self, player_id, position, team, name):
        self.weapon = Weapon()

        self.player_id = player_id
        self.team = team
        self.name = name

        self.position = pygame.Vector2(position)

        # Movement state
        self.velocity = pygame.Vector2(0, 0)

        self.run_speed = PLAYER_RUN_SPEED
        self.walk_speed = PLAYER_WALK_SPEED
        self.max_speed = self.run_speed

        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION

        self.image_offset = pygame.Vector2(0, -7)

        self.original_image = pygame.image.load(
            f"assets/{team}.png"
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
            self.original_image,
            (PLAYER_SIZE, PLAYER_SIZE)
        )

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=position)

        self.hitbox = pygame.Rect(
            0,
            0,
            PLAYER_HITBOX_SIZE,
            PLAYER_HITBOX_SIZE
        )
        self.hitbox.center = position

        self.debug_font = pygame.font.Font(None, 28) # temporary

    def move(
        self,
        dt,
        movement_direction,
        walking,
        walls
    ):
        if walking:
            self.max_speed = self.walk_speed
        else:
            self.max_speed = self.run_speed

        if movement_direction.length_squared() > 0:
            target_velocity = (
                movement_direction * self.max_speed
            )

            velocity_difference = (
                target_velocity - self.velocity
            )

            maximum_velocity_change = (
                self.acceleration * dt
            )

            if (
                velocity_difference.length_squared()
                > maximum_velocity_change ** 2
            ):
                velocity_difference.scale_to_length(
                    maximum_velocity_change
                )

            self.velocity += velocity_difference

        else:
            current_speed = self.velocity.length()
            friction_amount = self.friction * dt

            if current_speed <= friction_amount:
                self.velocity.update(0, 0)
            else:
                self.velocity.scale_to_length(
                    current_speed - friction_amount
                )

        movement = self.velocity * dt

        # Horizontal movement
        self.position.x += movement.x
        self.hitbox.centerx = round(self.position.x)
        self._check_collisions(
            walls,
            "x",
            movement.x
        )

        # Vertical movement
        self.position.y += movement.y
        self.hitbox.centery = round(self.position.y)
        self._check_collisions(
            walls,
            "y",
            movement.y
        )

        self.rect.center = self.hitbox.center
    
    def _check_collisions(self, walls, axis, movement):
        for wall in walls:
            if not self.hitbox.colliderect(wall):
                continue

            if axis == "x":
                if movement > 0:
                    self.hitbox.right = wall.left
                elif movement < 0:
                    self.hitbox.left = wall.right

                self.position.x = self.hitbox.centerx
                self.velocity.x = 0

            elif axis == "y":
                if movement > 0:
                    self.hitbox.bottom = wall.top
                elif movement < 0:
                    self.hitbox.top = wall.bottom

                self.position.y = self.hitbox.centery
                self.velocity.y = 0
    
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
        walking,
        mouse_screen_position,
        camera,
        walls
    ):
        self.move(
            dt=dt,
            movement_direction=movement_direction,
            walking=walking,
            walls=walls
        )

        self.rotate(
            mouse_screen_position,
            camera
        )

        self.weapon.update(
            dt=dt,
            movement_speed=self.velocity.length(),
            maximum_movement_speed=self.run_speed
        )

    def draw(self, screen, camera):
        screen.blit(
            self.image,
            camera.apply(self.rect)
        )

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            camera.apply(self.hitbox),
            2
        )

        current_speed = self.velocity.length()

        speed_text = self.debug_font.render(
            f"Speed: {current_speed:.1f}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            speed_text,
            (20, 20)
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
        
        
    
    