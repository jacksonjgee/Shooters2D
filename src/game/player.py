import pygame


class Player:
    def __init__(self, name=None):
        self.original_image = pygame.image.load(
            "assets/player0.webp"
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
            self.original_image,
            (100, 100)
        )

        self.image_right = self.original_image
        self.image_left = pygame.transform.flip(
            self.original_image,
            True,
            False
        )

        self.image = self.image_right
        self.rect = self.image.get_rect(center=(300, 300))

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
        return self.rect.centerx

    def get_ypos(self):
        return self.rect.centery

    def set_xpos(self, xpos):
        self.rect.centerx = xpos

    def set_ypos(self, ypos):
        self.rect.centery = ypos

    def change_xpos(self, delta):
        self.rect.x += delta

    def change_ypos(self, delta):
        self.rect.y += delta

    def change_shield(self, delta):
        self.shield += delta

    def change_health(self, delta):
        self.health += delta

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def face_left(self):
        self.image = self.image_left

    def face_right(self):
        self.image = self.image_right