import pygame
import math


class HUD:
    def __init__(self):
        self.aim_funnel_colour = (180, 180, 180)
        self.aim_funnel_width = 1
        self.aim_funnel_length = 300

        self.reticle_colour = (255, 255, 255)
        self.reticle_radius = 8
        self.reticle_line_length = 5
        self.reticle_line_width = 2

        # Temporary movement debug display
        self.debug_font = pygame.font.Font(None, 28)

    def draw(
        self,
        screen,
        player,
        mouse_screen_position,
        camera
    ):
        self._draw_aim_funnel(
            screen,
            player,
            mouse_screen_position,
            camera
        )

        self._draw_reticle(
            screen,
            mouse_screen_position
        )

        self._draw_speed(
            screen,
            player
        )

        self._draw_ammo(
            screen,
            player
        )

    def _draw_aim_funnel(
        self,
        screen,
        player,
        mouse_screen_position,
        camera
    ):
        player_screen_position = (
            player.position - camera.offset
        )

        aim_direction = (
            mouse_screen_position - player_screen_position
        )

        if aim_direction.length_squared() == 0:
            return

        aim_direction = aim_direction.normalize()

        perpendicular_direction = pygame.Vector2(
            -aim_direction.y,
            aim_direction.x
        )

        spread_degrees = (
            player.weapon.accuracy.current_spread
        )

        spread_radians = math.radians(
            spread_degrees
        )

        funnel_half_width = (
            math.tan(spread_radians)
            * self.aim_funnel_length
        )

        funnel_centre_end = (
            player_screen_position
            + aim_direction * self.aim_funnel_length
        )

        funnel_left_end = (
            funnel_centre_end
            + perpendicular_direction * funnel_half_width
        )

        funnel_right_end = (
            funnel_centre_end
            - perpendicular_direction * funnel_half_width
        )

        pygame.draw.line(
            screen,
            self.aim_funnel_colour,
            player_screen_position,
            funnel_left_end,
            self.aim_funnel_width
        )

        pygame.draw.line(
            screen,
            self.aim_funnel_colour,
            player_screen_position,
            funnel_right_end,
            self.aim_funnel_width
        )

    def _draw_reticle(
        self,
        screen,
        mouse_screen_position
    ):
        mouse_x = round(mouse_screen_position.x)
        mouse_y = round(mouse_screen_position.y)

        pygame.draw.circle(
            screen,
            self.reticle_colour,
            (mouse_x, mouse_y),
            self.reticle_radius,
            self.reticle_line_width
        )

        pygame.draw.line(
            screen,
            self.reticle_colour,
            (
                mouse_x - self.reticle_radius
                - self.reticle_line_length,
                mouse_y
            ),
            (
                mouse_x - self.reticle_radius,
                mouse_y
            ),
            self.reticle_line_width
        )

        pygame.draw.line(
            screen,
            self.reticle_colour,
            (
                mouse_x + self.reticle_radius,
                mouse_y
            ),
            (
                mouse_x + self.reticle_radius
                + self.reticle_line_length,
                mouse_y
            ),
            self.reticle_line_width
        )

        pygame.draw.line(
            screen,
            self.reticle_colour,
            (
                mouse_x,
                mouse_y - self.reticle_radius
                - self.reticle_line_length
            ),
            (
                mouse_x,
                mouse_y - self.reticle_radius
            ),
            self.reticle_line_width
        )

        pygame.draw.line(
            screen,
            self.reticle_colour,
            (
                mouse_x,
                mouse_y + self.reticle_radius
            ),
            (
                mouse_x,
                mouse_y + self.reticle_radius
                + self.reticle_line_length
            ),
            self.reticle_line_width
        )
    
    def _draw_speed(self, screen, player):
        current_speed = player.velocity.length()

        speed_text = self.debug_font.render(
            f"Speed: {current_speed:.1f}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            speed_text,
            (20, 20)
        )
    
    def _draw_ammo(self, screen, player):
        weapon = player.weapon

        if weapon.is_reloading:
            ammo_display = "Reloading..."
        else:
            ammo_display = (
                f"Ammo: {weapon.current_ammo}"
                f" / {weapon.magazine_size}"
            )

        ammo_text = self.debug_font.render(
            ammo_display,
            True,
            (255, 255, 255)
        )

        screen.blit(
            ammo_text,
            (20, 50)
        )