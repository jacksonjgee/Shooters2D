import pygame

from settings import PLAYER_SPEED, PLAYER_SIZE


class Player:
    def __init__(self, player_id, position, team, name=None):
        self.player_id = player_id
        self.name = name
        self.team = team

        self.health = 100.0
        self.shield = 0.0
        self.alive = True

        self.speed = PLAYER_SPEED

        self.max_ammo = 30
        self.ammo = self.max_ammo

        self.reload_duration = 3.0
        self.reload_timer = 0.0
        self.is_reloading = False

        self.fire_rate = 8
        self.fire_cooldown = 0.0

        self.original_image = pygame.image.load(
            "assets/player0.webp"
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
            self.original_image,
            (PLAYER_SIZE, PLAYER_SIZE)
        )

        self.image_right = self.original_image

        self.image_left = pygame.transform.flip(
            self.original_image,
            True,
            False
        )

        self.image = self.image_right

        # Rectangle used to draw the full sprite
        self.rect = self.image.get_rect(center=position)

        # Smaller rectangle used for collisions
        self.hitbox_offset_y = -10
        self.hitbox = pygame.Rect(0, 0, 25, 60)

        self.hitbox.center = (
            self.rect.centerx,
            self.rect.centery + self.hitbox_offset_y
        )

    def move(self, dx, dy, walls):
        # Move horizontally
        self.hitbox.x += dx

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if dx > 0:
                    self.hitbox.right = wall.left
                elif dx < 0:
                    self.hitbox.left = wall.right

        # Move vertically
        self.hitbox.y += dy

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if dy > 0:
                    self.hitbox.bottom = wall.top
                elif dy < 0:
                    self.hitbox.top = wall.bottom

        # Keep the sprite aligned with the offset hitbox
        self.rect.center = (
            self.hitbox.centerx,
            self.hitbox.centery - self.hitbox_offset_y
        )

    def update(self, delta_time):
        # Update firing cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= delta_time
            self.fire_cooldown = max(0.0, self.fire_cooldown)

        # Update reload timer
        if self.is_reloading:
            self.reload_timer -= delta_time

            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.reload_timer = 0.0
                self.is_reloading = False

    def can_shoot(self):
        return (
            self.ammo > 0
            and self.fire_cooldown <= 0
            and self.alive
        )

    def shoot(self):
        if self.is_reloading:
            return False

        if not self.can_shoot():
            return False

        self.ammo -= 1
        self.fire_cooldown = 1 / self.fire_rate

        return True

    def start_reload(self):
        if self.is_reloading:
            return

        if self.ammo == self.max_ammo:
            return

        if not self.alive:
            return

        self.is_reloading = True
        self.reload_timer = self.reload_duration

    def cancel_reload(self):
        self.is_reloading = False
        self.reload_timer = 0.0

    def take_damage(self, amount):
        remaining_damage = amount

        if self.shield > 0:
            absorbed_damage = min(
                self.shield,
                remaining_damage
            )

            self.shield -= absorbed_damage
            remaining_damage -= absorbed_damage

        self.health -= remaining_damage
        self.health = max(0.0, self.health)

        if self.health <= 0:
            self.alive = False

    def get_health(self):
        return self.health

    def get_shield(self):
        return self.shield

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health_and_shield(self):
        return self.health + self.shield

    def get_xpos(self):
        return self.hitbox.centerx

    def get_ypos(self):
        return self.hitbox.centery

    def set_xpos(self, xpos):
        self.hitbox.centerx = xpos
        self.rect.centerx = self.hitbox.centerx

    def set_ypos(self, ypos):
        self.hitbox.centery = ypos

        self.rect.centery = (
            self.hitbox.centery - self.hitbox_offset_y
        )

    def change_shield(self, delta):
        self.shield += delta
        self.shield = max(0.0, self.shield)

    def change_health(self, delta):
        self.health += delta
        self.health = max(0.0, self.health)

        if self.health <= 0:
            self.alive = False

    def face_left(self):
        self.image = self.image_left

    def face_right(self):
        self.image = self.image_right

    def draw(self, screen, camera):
        if not self.alive:
            return

        screen.blit(
            self.image,
            camera.apply(self.rect)
        )

        # Temporary debug hitbox
        pygame.draw.rect(
            screen,
            "red",
            camera.apply(self.hitbox),
            2
        )