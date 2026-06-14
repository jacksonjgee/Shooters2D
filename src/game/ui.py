import pygame


class GameUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

        self.aim_distance = 450
        self.aim_spread_degrees = 1.5

    def get_ray_end(
        self,
        start,
        direction,
        walls
    ):
        intended_end = (
            start + direction * self.aim_distance
        )

        closest_point = intended_end
        closest_distance = self.aim_distance

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

            collision_distance = start.distance_to(
                collision_point
            )

            if collision_distance < closest_distance:
                closest_distance = collision_distance
                closest_point = collision_point

        return closest_point

    def draw_aim_funnel(
        self,
        screen,
        player,
        camera,
        walls
    ):
        start_world = pygame.Vector2(
            player.hitbox.center
        )

        mouse_world = (
            pygame.Vector2(pygame.mouse.get_pos())
            + camera.offset
        )

        centre_direction = mouse_world - start_world

        if centre_direction.length_squared() == 0:
            return

        centre_direction = centre_direction.normalize()

        left_direction = centre_direction.rotate(
            -self.aim_spread_degrees
        )

        right_direction = centre_direction.rotate(
            self.aim_spread_degrees
        )

        left_end_world = self.get_ray_end(
            start_world,
            left_direction,
            walls
        )

        right_end_world = self.get_ray_end(
            start_world,
            right_direction,
            walls
        )

        start_screen = start_world - camera.offset
        left_end_screen = left_end_world - camera.offset
        right_end_screen = right_end_world - camera.offset

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        pygame.draw.polygon(
            overlay,
            (200, 200, 200, 60),
            [
                start_screen,
                left_end_screen,
                right_end_screen
            ]
        )

        pygame.draw.line(
            overlay,
            (200, 200, 200, 180),
            start_screen,
            left_end_screen,
            2
        )

        pygame.draw.line(
            overlay,
            (200, 200, 200, 180),
            start_screen,
            right_end_screen,
            2
        )

        screen.blit(overlay, (0, 0))

    def draw_hud(self, screen, player):
        health_text = self.font.render(
            f"Health: {int(player.health)}",
            True,
            "black"
        )

        ammo_text = self.font.render(
            f"Ammo: {player.ammo}/{player.max_ammo}",
            True,
            "black"
        )

        screen.blit(health_text, (20, 20))
        screen.blit(ammo_text, (20, 60))

        if player.is_reloading:
            reload_text = self.font.render(
                f"Reloading: {player.reload_timer:.1f}",
                True,
                "orange"
            )

            screen.blit(reload_text, (20, 100))

    def draw(
        self,
        screen,
        player,
        camera,
        walls
    ):
        self.draw_aim_funnel(
            screen,
            player,
            camera,
            walls
        )

        self.draw_hud(
            screen,
            player
        )

        self.draw_reticle(screen)
    
    def draw_reticle(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        color = (220, 220, 220)
        gap = 6
        line_length = 10
        thickness = 2
        radius = 2

        # Left line
        pygame.draw.line(
            screen,
            color,
            (mouse_x - gap - line_length, mouse_y),
            (mouse_x - gap, mouse_y),
            thickness
        )

        # Right line
        pygame.draw.line(
            screen,
            color,
            (mouse_x + gap, mouse_y),
            (mouse_x + gap + line_length, mouse_y),
            thickness
        )

        # Top line
        pygame.draw.line(
            screen,
            color,
            (mouse_x, mouse_y - gap - line_length),
            (mouse_x, mouse_y - gap),
            thickness
        )

        # Bottom line
        pygame.draw.line(
            screen,
            color,
            (mouse_x, mouse_y + gap),
            (mouse_x, mouse_y + gap + line_length),
            thickness
        )

        # Small centre dot
        pygame.draw.circle(
            screen,
            color,
            (mouse_x, mouse_y),
            radius
        )