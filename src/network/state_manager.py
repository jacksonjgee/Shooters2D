from src.game.bullet import Bullet
from src.game.player_state import PlayerState
from src.network.network_message import NetworkMessage


class StateManager:
    def __init__(self, connection):
        self.connection = connection

    def update(
        self,
        players,
        entity_manager
    ):
        if not self.connection.is_connected():
            return

        role = self.connection.get_role()

        if role == "host":
            self._send_player_states(
                players
            )

            self._send_new_bullets(
                entity_manager
            )

        elif role == "client":
            self._receive_and_apply_messages(
                players=players,
                entity_manager=entity_manager
            )

    def _send_player_states(
        self,
        players
    ):
        for player in players:
            state = PlayerState.from_player(
                player
            )

            message = NetworkMessage(
                message_type="player_state",
                player_id=player.player_id,
                data=state.to_dict()
            )

            self.connection.send(
                message.to_json()
            )

    def _send_new_bullets(
        self,
        entity_manager
    ):
        new_bullets = (
            entity_manager.take_new_bullets()
        )

        for bullet in new_bullets:
            message = NetworkMessage(
                message_type="bullet_fired",
                data={
                    "start_x":
                        bullet.start_position.x,

                    "start_y":
                        bullet.start_position.y,

                    "end_x":
                        bullet.end_position.x,

                    "end_y":
                        bullet.end_position.y,

                    "remaining_time":
                        bullet.remaining_time
                }
            )

            self.connection.send(
                message.to_json()
            )

    def _receive_and_apply_messages(
        self,
        players,
        entity_manager
    ):
        messages = (
            self.connection.receive_all()
        )

        for message_json in messages:
            message = NetworkMessage.from_json(
                message_json
            )

            if message.message_type == "player_state":
                self._apply_player_state(
                    message=message,
                    players=players
                )

            elif message.message_type == "bullet_fired":
                self._create_client_tracer(
                    message=message,
                    entity_manager=entity_manager
                )

    def _apply_player_state(
        self,
        message,
        players
    ):
        state = PlayerState.from_dict(
            message.data
        )

        player = self._find_player(
            players=players,
            player_id=state.player_id
        )

        if player is None:
            return

        player.apply_state(
            state
        )

    def _create_client_tracer(
        self,
        message,
        entity_manager
    ):
        data = message.data

        tracer = Bullet.create_visual_tracer(
            start_position=(
                data.get("start_x", 0.0),
                data.get("start_y", 0.0)
            ),
            end_position=(
                data.get("end_x", 0.0),
                data.get("end_y", 0.0)
            ),
            remaining_time=data.get(
                "remaining_time",
                0.0
            )
        )

        entity_manager.add_bullet(
            tracer,
            record_as_new=False
        )

    def _find_player(
        self,
        players,
        player_id
    ):
        for player in players:
            if player.player_id == player_id:
                return player

        return None