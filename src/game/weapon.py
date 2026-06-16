import pygame
import random

from src.game.bullet import Bullet
from src.game.accuracy import Accuracy
from settings import WEAPON_FIRE_RATE


class Weapon:
    def __init__(self):
        self.fire_rate = WEAPON_FIRE_RATE
        self.fire_cooldown = 0.0

        self.accuracy = Accuracy()

    def update(
        self,
        dt,
        movement_speed,
        maximum_movement_speed
    ):
        self.fire_cooldown = max(
            0.0,
            self.fire_cooldown - dt
        )

        self.accuracy.update(
            dt=dt,
            movement_speed=movement_speed,
            maximum_movement_speed=maximum_movement_speed
        )

    def shoot(self, position, direction, walls):
        if self.fire_cooldown > 0:
            return None

        if direction.length_squared() == 0:
            return None

        self.fire_cooldown = 1 / self.fire_rate

        aim_direction = direction.normalize()

        current_spread = (
            self.accuracy.current_spread
        )

        random_angle = random.uniform(
            -current_spread,
            current_spread
        )

        inaccurate_direction = (
            aim_direction.rotate(random_angle)
        )

        bullet = Bullet(
            position=position,
            direction=inaccurate_direction,
            walls=walls
        )

        self.accuracy.register_shot()

        return bullet