import pygame


class PlayerCommand:
    def __init__(
        self,
        movement_direction=None,
        walking=False,
        aim_world_position=None,
        shooting=False,
        reload_pressed=False
    ):
        if movement_direction is None:
            movement_direction = pygame.Vector2(0, 0)

        if aim_world_position is None:
            aim_world_position = pygame.Vector2(0, 0)

        self.movement_direction = pygame.Vector2(
            movement_direction
        )

        self.walking = walking

        self.aim_world_position = pygame.Vector2(
            aim_world_position
        )

        self.shooting = shooting
        self.reload_pressed = reload_pressed

    def to_dict(self):
        return {
            "movement_x": self.movement_direction.x,
            "movement_y": self.movement_direction.y,
            "walking": self.walking,
            "aim_x": self.aim_world_position.x,
            "aim_y": self.aim_world_position.y,
            "shooting": self.shooting,
            "reload_pressed": self.reload_pressed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            movement_direction=pygame.Vector2(
                data.get("movement_x", 0.0),
                data.get("movement_y", 0.0)
            ),
            walking=data.get("walking", False),
            aim_world_position=pygame.Vector2(
                data.get("aim_x", 0.0),
                data.get("aim_y", 0.0)
            ),
            shooting=data.get("shooting", False),
            reload_pressed=data.get(
                "reload_pressed",
                False
            )
        )