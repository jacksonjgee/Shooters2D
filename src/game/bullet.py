import pygame

from settings import BULLET_SPEED, BULLET_HITBOX_SIZE


class Bullet:
    def __init__(self, position, direction):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.speed = BULLET_SPEED
        self.alive = True

        self.hitbox = pygame.Rect(
            0,
            0,
            BULLET_HITBOX_SIZE,
            BULLET_HITBOX_SIZE
        )
        self.hitbox.center = self.position

    def move(self, dt, walls):
        start_position = self.position.copy()
        movement = self.direction * self.speed * dt
        end_position = start_position + movement

        if self._collides_with_wall(
            start_position,
            end_position,
            walls
        ):
            self.alive = False
            return

        self.position = end_position
        self.hitbox.center = (
            round(self.position.x),
            round(self.position.y)
        )

    def _collides_with_wall(self, start_position, end_position, walls):
        start = (
            round(start_position.x),
            round(start_position.y)
        )

        end = (
            round(end_position.x),
            round(end_position.y)
        )

        for wall in walls:
            expanded_wall = wall.inflate(
                self.hitbox.width,
                self.hitbox.height
            )

            if expanded_wall.clipline(start, end):
                return True

        return False

    def update(self, dt, walls):
        self.move(dt, walls)

    def draw(self, screen, camera):
        if self.alive == True:
            pygame.draw.rect(
                screen,
                (255, 220, 50),
                camera.apply(self.hitbox)
            )