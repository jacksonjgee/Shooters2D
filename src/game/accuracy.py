from settings import (
    MOVEMENT_SPREAD_MAX_DEGREES,
    MOVEMENT_FULL_ACCURACY_SPEED,
    FIRING_SPREAD_PER_SHOT,
    FIRING_SPREAD_MAX_DEGREES,
    FIRING_SPREAD_RECOVERY_PER_SECOND,
    FIRING_SPREAD_RECOVERY_DELAY
)


class Accuracy:
    def __init__(self):
        self.movement_spread = 0.0
        self.firing_spread = 0.0
        self.current_spread = 0.0

        self.recovery_delay_timer = 0.0

    def update(
        self,
        dt,
        movement_speed,
        maximum_movement_speed
    ):
        self._update_movement_spread(
            movement_speed,
            maximum_movement_speed
        )

        self._update_firing_spread_recovery(dt)

        self.current_spread = (
            self.movement_spread
            + self.firing_spread
        )

    def _update_movement_spread(
        self,
        movement_speed,
        maximum_movement_speed
    ):
        if movement_speed <= MOVEMENT_FULL_ACCURACY_SPEED:
            self.movement_spread = 0.0
            return

        usable_speed_range = (
            maximum_movement_speed
            - MOVEMENT_FULL_ACCURACY_SPEED
        )

        if usable_speed_range <= 0:
            speed_ratio = 0.0
        else:
            speed_above_threshold = (
                movement_speed
                - MOVEMENT_FULL_ACCURACY_SPEED
            )

            speed_ratio = (
                speed_above_threshold
                / usable_speed_range
            )

        speed_ratio = max(
            0.0,
            min(speed_ratio, 1.0)
        )

        self.movement_spread = (
            speed_ratio
            * MOVEMENT_SPREAD_MAX_DEGREES
        )

    def _update_firing_spread_recovery(self, dt):
        if self.recovery_delay_timer > 0:
            self.recovery_delay_timer = max(
                0.0,
                self.recovery_delay_timer - dt
            )
            return

        self.firing_spread = max(
            0.0,
            self.firing_spread
            - FIRING_SPREAD_RECOVERY_PER_SECOND * dt
        )

    def register_shot(self):
        self.firing_spread = min(
            FIRING_SPREAD_MAX_DEGREES,
            self.firing_spread
            + FIRING_SPREAD_PER_SHOT
        )

        self.recovery_delay_timer = (
            FIRING_SPREAD_RECOVERY_DELAY
        )

        self.current_spread = (
            self.movement_spread
            + self.firing_spread
        )