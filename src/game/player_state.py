import pygame


class PlayerState:
    def __init__(
        self,
        player_id,
        position=None,
        velocity=None,
        aim_world_position=None,
        health=100,
        alive=True,
        ammo=0,
        is_reloading=False,
        current_spread=0.0
    ):
        if position is None:
            position = pygame.Vector2(0, 0)

        if velocity is None:
            velocity = pygame.Vector2(0, 0)

        if aim_world_position is None:
            aim_world_position = pygame.Vector2(0, 0)

        self.player_id = player_id
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.aim_world_position = pygame.Vector2(
            aim_world_position
        )

        self.health = health
        self.alive = alive
        self.ammo = ammo
        self.is_reloading = is_reloading
        self.current_spread = current_spread

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "position_x": self.position.x,
            "position_y": self.position.y,
            "velocity_x": self.velocity.x,
            "velocity_y": self.velocity.y,
            "aim_x": self.aim_world_position.x,
            "aim_y": self.aim_world_position.y,
            "health": self.health,
            "alive": self.alive,
            "ammo": self.ammo,
            "is_reloading": self.is_reloading,
            "current_spread": self.current_spread
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            player_id=data["player_id"],
            position=pygame.Vector2(
                data.get("position_x", 0.0),
                data.get("position_y", 0.0)
            ),
            velocity=pygame.Vector2(
                data.get("velocity_x", 0.0),
                data.get("velocity_y", 0.0)
            ),
            aim_world_position=pygame.Vector2(
                data.get("aim_x", 0.0),
                data.get("aim_y", 0.0)
            ),
            health=data.get("health", 100),
            alive=data.get("alive", True),
            ammo=data.get("ammo", 0),
            is_reloading=data.get(
                "is_reloading",
                False
            ),
            current_spread=data.get(
                "current_spread",
                0.0
            )
        )

    @classmethod
    def from_player(cls, player):
        return cls(
            player_id=player.player_id,
            position=player.position,
            velocity=player.velocity,
            aim_world_position=(
                player.aim_world_position
            ),
            health=player.health,
            alive=player.alive,
            ammo=player.weapon.current_ammo,
            is_reloading=(
                player.weapon.is_reloading
            ),
            current_spread=(
                player.weapon.accuracy.current_spread
            )
        )