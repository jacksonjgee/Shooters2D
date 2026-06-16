import pygame
from src.game.weapon import Weapon

from settings import (
    PLAYER_SIZE,
    PLAYER_RUN_SPEED,
    PLAYER_WALK_SPEED,
    PLAYER_HITBOX_SIZE,
    PLAYER_MAX_HEALTH,
    PLAYER_RESPAWN_DELAY,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION
)

class Player:
    def __init__(self, player_id, position, team, name):
        self.weapon = Weapon()

        self.player_id = player_id
        self.team = team
        self.name = name

        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.alive = True

        self.position = pygame.Vector2(position)
        self.aim_world_position = self.position.copy()

        # Movement state
        self.velocity = pygame.Vector2(0, 0)

        self.spawn_position = pygame.Vector2(position)

        self.respawn_delay = PLAYER_RESPAWN_DELAY
        self.respawn_timer = 0.0

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

    def move(
        self,
        dt,
        movement_direction,
        walking,
        walls,
        players
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
            walls=walls,
            players=players,
            axis="x",
            movement=movement.x
        )

        # Vertical movement
        self.position.y += movement.y
        self.hitbox.centery = round(self.position.y)

        self._check_collisions(
            walls=walls,
            players=players,
            axis="y",
            movement=movement.y
        )

        self.rect.center = self.hitbox.center
    
    def _check_collisions(
        self,
        walls,
        players,
        axis,
        movement
    ):
        for wall in walls:
            if self.hitbox.colliderect(wall):
                self._resolve_collision(
                    obstacle=wall,
                    axis=axis,
                    movement=movement
                )

        for player in players:
            if player is self:
                continue

            if not player.alive:
                continue

            if self.hitbox.colliderect(player.hitbox):
                self._resolve_collision(
                    obstacle=player.hitbox,
                    axis=axis,
                    movement=movement
                )
    
    def rotate(self, aim_world_position):
        direction = (
            aim_world_position - self.position
        )

        if direction.length_squared() == 0:
            return

        angle = (
            direction.angle_to(
                pygame.Vector2(1, 0)
            )
            - 90
        )

        self.image = pygame.transform.rotate(
            self.original_image,
            angle
        )

        rotated_offset = self.image_offset.rotate(
            -angle
        )

        image_center = (
            self.position + rotated_offset
        )

        self.rect = self.image.get_rect(
            center=image_center
        )

    def update(
        self,
        dt,
        command,
        walls,
        players
    ):
        if not self.alive:
            return

        self.move(
            dt=dt,
            movement_direction=command.movement_direction,
            walking=command.walking,
            walls=walls,
            players=players
        )

        self.aim_world_position.update(
            command.aim_world_position
        )

        self.rotate(
            command.aim_world_position
        )

        self.weapon.update(
            dt=dt,
            movement_speed=self.velocity.length(),
            maximum_movement_speed=self.run_speed
        )

    def draw(self, screen, camera):
        if not self.alive:
            return

        self._draw_sprite(
            screen,
            camera
        )

    def shoot(
        self,
        aim_world_position,
        walls,
        players
    ):
        if not self.alive:
            return None

        direction = (
            aim_world_position - self.position
        )

        return self.weapon.shoot(
            position=self.position.copy(),
            direction=direction,
            walls=walls,
            players=players,
            shooter=self
        )

    def _resolve_collision(
        self,
        obstacle,
        axis,
        movement
    ):
        if axis == "x":
            if movement > 0:
                self.hitbox.right = obstacle.left
            elif movement < 0:
                self.hitbox.left = obstacle.right

            self.position.x = self.hitbox.centerx
            self.velocity.x = 0

        elif axis == "y":
            if movement > 0:
                self.hitbox.bottom = obstacle.top
            elif movement < 0:
                self.hitbox.top = obstacle.bottom

            self.position.y = self.hitbox.centery
            self.velocity.y = 0

    def take_damage(self, amount):
        if not self.alive:
            return

        self.health = max(
            0,
            self.health - amount
        )

        if self.health <= 0:
            self.alive = False
            self.velocity.update(0, 0)
            self.respawn_timer = self.respawn_delay
    
    def update_respawn(self, dt):
        if self.alive:
            return

        self.respawn_timer = max(
            0.0,
            self.respawn_timer - dt
        )

        if self.respawn_timer > 0:
            return

        self.health = self.max_health
        self.alive = True

        self.position.update(
            self.spawn_position
        )

        self.velocity.update(0, 0)

        self.hitbox.center = (
            round(self.position.x),
            round(self.position.y)
        )

        self.rect.center = self.hitbox.center

        # Give the respawned player a fresh weapon.
        self.weapon = Weapon()

    def _draw_sprite(self, screen, camera):
        screen.blit(
            self.image,
            camera.apply(self.rect)
        )

    def _draw_health(self, screen, camera):
        font = pygame.font.Font(None, 24)

        health_text = font.render(
            f"{self.health}",
            True,
            (255, 255, 255)
        )

        health_position = (
            self.hitbox.centerx
            - camera.offset.x
            - health_text.get_width() / 2,
            self.hitbox.top
            - camera.offset.y
            - 22
        )

        screen.blit(
            health_text,
            health_position
        )

    def draw_hitbox(self, screen, camera):
        if not self.alive:
            return

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            camera.apply(self.hitbox),
            2
        )
    
    def process_actions(
        self,
        command,
        walls,
        players
    ):
        if not self.alive:
            return None

        if command.reload_pressed:
            self.weapon.start_reload()

        if command.shooting:
            return self.shoot(
                aim_world_position=(
                    command.aim_world_position
                ),
                walls=walls,
                players=players
            )

        return None
    
    def apply_state(self, state):
        if state.player_id != self.player_id:
            return

        self.position.update(
            state.position
        )

        self.velocity.update(
            state.velocity
        )

        self.aim_world_position.update(
            state.aim_world_position
        )

        self.health = state.health
        self.alive = state.alive

        self.weapon.current_ammo = state.ammo
        self.weapon.is_reloading = (
            state.is_reloading
        )
        self.weapon.accuracy.current_spread = (
            state.current_spread
        )

        self.hitbox.center = (
            round(self.position.x),
            round(self.position.y)
        )

        self.rotate(
            self.aim_world_position
        )