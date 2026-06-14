import pygame
from settings import BULLET_SPEED

class Bullet:
    def __init__(self, start_position, target_position, owner_id, team):
        self.owner_id = owner_id
        self.team = team
        self.damage = 25

        self.position = pygame.Vector2(start_position)

        direction = (
            pygame.Vector2(target_position)
            - self.position
        )

        if direction.length_squared() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2()

        self.speed = BULLET_SPEED
        self.radius = 5
        self.alive = True

    def update(self, delta_time, walls):
        old_position = self.position.copy()

        movement = self.direction * self.speed * delta_time
        new_position = old_position + movement

        for wall in walls:
            collision_line = wall.inflate(
                self.radius * 2,
                self.radius * 2
            )

            if collision_line.clipline(
                old_position.x,
                old_position.y,
                new_position.x,
                new_position.y
            ):
                self.alive = False
                return

        self.position = new_position

    def draw(self, screen, camera):
        screen_position = self.position - camera.offset

        pygame.draw.circle(
            screen,
            "orange",
            (
                round(screen_position.x),
                round(screen_position.y)
            ),
            self.radius
        )