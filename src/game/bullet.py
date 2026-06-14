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

    def update(self, delta_time, walls, players):
        old_position = self.position.copy()

        movement = self.direction * self.speed * delta_time
        new_position = old_position + movement

        closest_distance = movement.length()
        collision_target = None

        # Check walls
        for wall in walls:
            expanded_wall = wall.inflate(
                self.radius * 2,
                self.radius * 2
            )

            collision = expanded_wall.clipline(
                old_position.x,
                old_position.y,
                new_position.x,
                new_position.y
            )

            if collision:
                collision_point = pygame.Vector2(collision[0])
                distance = old_position.distance_to(collision_point)

                if distance < closest_distance:
                    closest_distance = distance
                    collision_target = "wall"

        # Check players
        for player in players:
            if not player.alive:
                continue

            # Do not hit the player who fired the bullet
            if player.player_id == self.owner_id:
                continue

            # Prevent friendly fire
            if player.team == self.team:
                continue

            expanded_hitbox = player.hitbox.inflate(
                self.radius * 2,
                self.radius * 2
            )

            collision = expanded_hitbox.clipline(
                old_position.x,
                old_position.y,
                new_position.x,
                new_position.y
            )

            if collision:
                collision_point = pygame.Vector2(collision[0])
                distance = old_position.distance_to(collision_point)

                if distance < closest_distance:
                    closest_distance = distance
                    collision_target = player

        if collision_target is not None:
            if collision_target != "wall":
                collision_target.take_damage(self.damage)

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