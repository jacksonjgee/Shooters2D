import pygame

from settings import (
    SHOT_RANGE,
    TRACER_DURATION,
    TRACER_WIDTH
)


class Bullet:
    def __init__(
        self,
        position,
        direction,
        walls,
        players,
        shooter,
        damage
    ):
        self.start_position = pygame.Vector2(
            position
        )

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(
                direction
            ).normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.damage = damage
        self.hit_player = None

        self.end_position = (
            self._find_end_position(
                walls=walls,
                players=players,
                shooter=shooter
            )
        )

        if self.hit_player is not None:
            self.hit_player.take_damage(
                self.damage
            )

        self.remaining_time = TRACER_DURATION
        self.alive = True

    @classmethod
    def create_visual_tracer(
        cls,
        start_position,
        end_position,
        remaining_time
    ):
        bullet = cls.__new__(cls)

        bullet.start_position = pygame.Vector2(
            start_position
        )

        bullet.end_position = pygame.Vector2(
            end_position
        )

        direction = (
            bullet.end_position
            - bullet.start_position
        )

        if direction.length_squared() > 0:
            bullet.direction = direction.normalize()
        else:
            bullet.direction = pygame.Vector2(0, 0)

        bullet.damage = 0
        bullet.hit_player = None

        bullet.remaining_time = remaining_time
        bullet.alive = True

        return bullet

    def _find_end_position(
        self,
        walls,
        players,
        shooter
    ):
        maximum_end_position = (
            self.start_position
            + self.direction * SHOT_RANGE
        )

        closest_point = maximum_end_position
        closest_distance_squared = (
            SHOT_RANGE ** 2
        )

        start = (
            round(self.start_position.x),
            round(self.start_position.y)
        )

        end = (
            round(maximum_end_position.x),
            round(maximum_end_position.y)
        )

        # Check walls first.
        for wall in walls:
            intersection = wall.clipline(
                start,
                end
            )

            if not intersection:
                continue

            wall_entry_point = pygame.Vector2(
                intersection[0]
            )

            distance_squared = (
                wall_entry_point
                - self.start_position
            ).length_squared()

            if (
                distance_squared
                < closest_distance_squared
            ):
                closest_distance_squared = (
                    distance_squared
                )
                closest_point = wall_entry_point
                self.hit_player = None

        # Check all other living players.
        for player in players:
            if player is shooter:
                continue

            if not player.alive:
                continue

            intersection = player.hitbox.clipline(
                start,
                end
            )

            if not intersection:
                continue

            player_entry_point = pygame.Vector2(
                intersection[0]
            )

            distance_squared = (
                player_entry_point
                - self.start_position
            ).length_squared()

            if (
                distance_squared
                < closest_distance_squared
            ):
                closest_distance_squared = (
                    distance_squared
                )
                closest_point = player_entry_point
                self.hit_player = player

        return closest_point

    def update(self, dt):
        self.remaining_time -= dt

        if self.remaining_time <= 0:
            self.alive = False

    def draw(self, screen, camera):
        start_screen_position = (
            self.start_position
            - camera.offset
        )

        end_screen_position = (
            self.end_position
            - camera.offset
        )

        pygame.draw.line(
            screen,
            (255, 220, 50),
            start_screen_position,
            end_screen_position,
            TRACER_WIDTH
        )