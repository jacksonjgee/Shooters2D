import pygame

class InputHandler:
    def __init__(self):
        self.movement_direction = pygame.Vector2(0, 0)
        self.mouse_screen_position = pygame.Vector2(0, 0)

        self.shoot_held = False
        self.walk_toggled = False
        self.reload_pressed = False

    def update(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        self._update_movement_direction(keys)
        self._update_mouse_position()
        self._update_shooting_input(mouse_buttons)

    def _update_movement_direction(self, keys):
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

    def _update_shooting_input(self, mouse_buttons):
        self.shoot_held = mouse_buttons[0]
    
    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return

        if event.key in (
            pygame.K_LSHIFT,
            pygame.K_RSHIFT
        ):
            self.walk_toggled = not self.walk_toggled

        elif event.key == pygame.K_r:
            self.reload_pressed = True
