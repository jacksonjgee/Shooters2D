import pygame

class InputHandler:
    def __init__(self):
        self.movement_direction = pygame.Vector2(0, 0)
        self.mouse_screen_position = pygame.Vector2(0, 0)

    def update(self):
        self._update_movement_direction()
        self._update_mouse_position()

    def _update_movement_direction(self):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            direction.y -= 1

        if keys[pygame.K_s]:
            direction.y += 1

        if keys[pygame.K_a]:
            direction.x -= 1

        if keys[pygame.K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.movement_direction = direction

    def _update_mouse_position(self):
        self.mouse_screen_position = pygame.Vector2(
            pygame.mouse.get_pos()
        )