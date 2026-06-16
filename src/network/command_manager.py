from src.game.player_command import PlayerCommand
from src.network.network_message import NetworkMessage


class CommandManager:
    def __init__(self, connection):
        self.connection = connection
        self.remote_commands = {}

    def create_commands(
        self,
        input_handler,
        camera,
        local_player,
        remote_players
    ):
        local_command = self._create_local_command(
            input_handler=input_handler,
            camera=camera
        )

        commands = {
            local_player.player_id: local_command
        }

        if not self.connection.is_connected():
            self._add_idle_remote_commands(
                commands=commands,
                remote_players=remote_players
            )

            return commands

        role = self.connection.get_role()

        if role == "client":
            self._send_client_command(
                command=local_command,
                remote_players=remote_players
            )

        elif role == "host":
            self._receive_remote_commands()

        self._add_received_remote_commands(
            commands=commands,
            remote_players=remote_players
        )

        return commands

    def _create_local_command(
        self,
        input_handler,
        camera
    ):
        aim_world_position = (
            input_handler.mouse_screen_position
            + camera.offset
        )

        command = PlayerCommand(
            movement_direction=(
                input_handler.movement_direction
            ),
            walking=input_handler.walk_toggled,
            aim_world_position=aim_world_position,
            shooting=input_handler.shoot_held,
            reload_pressed=(
                input_handler.reload_pressed
            )
        )

        input_handler.reload_pressed = False

        return command

    def _send_client_command(
        self,
        command,
        remote_players
    ):
        if not remote_players:
            return

        remote_player = remote_players[0]

        message = NetworkMessage(
            message_type="player_command",
            player_id=remote_player.player_id,
            data=command.to_dict()
        )

        self.connection.send(
            message.to_json()
        )

    def _receive_remote_commands(self):
        message_json_list = (
            self.connection.receive_all()
        )

        for message_json in message_json_list:
            message = NetworkMessage.from_json(
                message_json
            )

            if message.message_type != "player_command":
                continue

            if message.player_id is None:
                continue

            self.remote_commands[
                message.player_id
            ] = PlayerCommand.from_dict(
                message.data
            )

    def _add_received_remote_commands(
        self,
        commands,
        remote_players
    ):
        for remote_player in remote_players:
            command = self.remote_commands.get(
                remote_player.player_id
            )

            if command is None:
                command = self._create_idle_command(
                    remote_player
                )

            commands[
                remote_player.player_id
            ] = command

    def _add_idle_remote_commands(
        self,
        commands,
        remote_players
    ):
        for remote_player in remote_players:
            commands[
                remote_player.player_id
            ] = self._create_idle_command(
                remote_player
            )

    def _create_idle_command(
        self,
        player
    ):
        return PlayerCommand(
            aim_world_position=(
                player.position.copy()
            )
        )