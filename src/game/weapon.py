import random

from src.game.bullet import Bullet
from src.game.accuracy import Accuracy

from settings import (
    WEAPON_FIRE_RATE,
    WEAPON_MAGAZINE_SIZE,
    WEAPON_RELOAD_DURATION,
    WEAPON_DAMAGE
)


class Weapon:
    def __init__(self):
        self.fire_rate = WEAPON_FIRE_RATE
        self.fire_cooldown = 0.0

        self.magazine_size = WEAPON_MAGAZINE_SIZE
        self.current_ammo = self.magazine_size

        self.reload_duration = WEAPON_RELOAD_DURATION
        self.reload_timer = 0.0
        self.is_reloading = False
        self.damage = WEAPON_DAMAGE

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

        if self.is_reloading:
            self.reload_timer = max(
                0.0,
                self.reload_timer - dt
            )

            if self.reload_timer <= 0:
                self.current_ammo = self.magazine_size
                self.is_reloading = False

        self.accuracy.update(
            dt=dt,
            movement_speed=movement_speed,
            maximum_movement_speed=maximum_movement_speed
        )

    def start_reload(self):
        if self.is_reloading:
            return

        if self.current_ammo >= self.magazine_size:
            return

        self.is_reloading = True
        self.reload_timer = self.reload_duration

    def cancel_reload(self):
        if not self.is_reloading:
            return

        self.is_reloading = False
        self.reload_timer = 0.0

    def shoot(
        self,
        position,
        direction,
        walls,
        players,
        shooter
    ):
        if self.is_reloading:
            if self.current_ammo > 0:
                self.cancel_reload()
            else:
                return None

        if self.current_ammo <= 0:
            self.start_reload()
            return None

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
            walls=walls,
            players=players,
            shooter=shooter,
            damage=self.damage
        )

        self.current_ammo -= 1
        self.accuracy.register_shot()

        return bullet
    
    