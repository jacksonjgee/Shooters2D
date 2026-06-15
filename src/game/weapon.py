import pygame

from src.game.bullet import Bullet

from settings import WEAPON_FIRE_RATE


class Weapon:
    def __init__(self):
        self.fire_rate = WEAPON_FIRE_RATE
        self.fire_cooldown = 0.0

    def update(self, dt):
        self.fire_cooldown = max(
            0.0,
            self.fire_cooldown - dt
        )

    def shoot(self, position, direction, walls):
        if self.fire_cooldown > 0:
            return None

        if direction.length_squared() == 0:
            return None

        self.fire_cooldown = 1 / self.fire_rate

        return Bullet(
            position=position,
            direction=direction,
            walls=walls
        )