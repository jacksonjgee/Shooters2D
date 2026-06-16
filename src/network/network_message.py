import json


class NetworkMessage:
    def __init__(
        self,
        message_type,
        player_id=None,
        data=None
    ):
        self.message_type = message_type
        self.player_id = player_id

        if data is None:
            data = {}

        self.data = data

    def to_dict(self):
        return {
            "type": self.message_type,
            "player_id": self.player_id,
            "data": self.data
        }

    def to_json(self):
        return json.dumps(
            self.to_dict()
        )

    @classmethod
    def from_dict(cls, message_data):
        return cls(
            message_type=message_data.get("type"),
            player_id=message_data.get("player_id"),
            data=message_data.get("data", {})
        )

    @classmethod
    def from_json(cls, message_json):
        message_data = json.loads(
            message_json
        )

        return cls.from_dict(
            message_data
        )