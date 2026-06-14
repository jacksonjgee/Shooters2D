import math

import pygame


class VisibilitySystem:
    def __init__(self):
        self.view_distance = 1280
        self.ray_count = 720
        self.darkness_alpha = 254

    def cast_ray(self, start, direction, walls):
        intended_end = (
            start + direction * self.view_distance
        )

        closest_point = intended_end
        closest_distance = self.view_distance

        for wall in walls:
            collision = wall.clipline(
                start.x,
                start.y,
                intended_end.x,
                intended_end.y
            )

            if not collision:
                continue

            collision_point = pygame.Vector2(
                collision[0]
            )

            distance = start.distance_to(
                collision_point
            )

            if distance < closest_distance:
                closest_distance = distance
                closest_point = collision_point

        return closest_point

    def calculate_visible_points(self, player, walls):
        start = pygame.Vector2(
            player.hitbox.center
        )

        visible_points = []

        for ray_index in range(self.ray_count):
            angle = (
                ray_index / self.ray_count
            ) * 360

            angle_radians = math.radians(angle)

            direction = pygame.Vector2(
                math.cos(angle_radians),
                math.sin(angle_radians)
            )

            end_point = self.cast_ray(
                start,
                direction,
                walls
            )

            visible_points.append(end_point)

        return visible_points

    def draw(self, screen, player, camera, walls):
        visible_world_points = self.calculate_visible_points(
            player,
            walls
        )

        player_screen_position = (
            pygame.Vector2(player.hitbox.center)
            - camera.offset
        )

        visible_screen_points = [
            point - camera.offset
            for point in visible_world_points
        ]

        darkness = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        darkness.fill(
            (35, 35, 35, self.darkness_alpha)
        )

        if len(visible_screen_points) >= 3:
            pygame.draw.polygon(
                darkness,
                (0, 0, 0, 0),
                visible_screen_points
            )

        screen.blit(darkness, (0, 0))