import pygame

from settings import SHOT_RANGE, TRACER_DURATION, TRACER_WIDTH


class Bullet:
    def __init__(self, position, direction, walls):
        self.start_position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.end_position = self._find_end_position(walls)

        self.remaining_time = TRACER_DURATION
        self.alive = True

    def _find_end_position(self, walls):
        maximum_end_position = (
            self.start_position
            + self.direction * SHOT_RANGE
        )

        closest_point = maximum_end_position
        closest_distance_squared = SHOT_RANGE ** 2

        start = (
            round(self.start_position.x),
            round(self.start_position.y)
        )

        end = (
            round(maximum_end_position.x),
            round(maximum_end_position.y)
        )

        for wall in walls:
            intersection = wall.clipline(start, end)

            if not intersection:
                continue

            wall_entry_point = pygame.Vector2(intersection[0])

            distance_squared = (
                wall_entry_point - self.start_position
            ).length_squared()

            if distance_squared < closest_distance_squared:
                closest_distance_squared = distance_squared
                closest_point = wall_entry_point

        return closest_point

    def update(self, dt):
        self.remaining_time -= dt

        if self.remaining_time <= 0:
            self.alive = False

    def draw(self, screen, camera):
        start_screen_position = (
            self.start_position - camera.offset
        )

        end_screen_position = (
            self.end_position - camera.offset
        )

        pygame.draw.line(
            screen,
            (255, 220, 50),
            start_screen_position,
            end_screen_position,
            TRACER_WIDTH
        )