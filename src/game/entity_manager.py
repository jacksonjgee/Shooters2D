from src.game.player import Player

class EntityManager:
    def __init__(self):
        self.bullets = []
        self.players = []

        self.show_hitboxes = True

    def add_bullet(self, bullet):
        if bullet is not None:
            self.bullets.append(bullet)

    def add_player(self, player):
        if player is not None:
            self.players.append(player)

    def create_player(
        self,
        player_id,
        position,
        team,
        name
    ):
        player = Player(
            player_id=player_id,
            position=position,
            team=team,
            name=name
        )

        self.add_player(player)

        return player

    def get_player(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player

        return None

    def update(
        self,
        dt,
        commands,
        walls
    ):
        self._update_players(
            dt=dt,
            commands=commands,
            walls=walls
        )

        self._update_respawns(dt)
        self._update_bullets(dt)

    def draw(self, screen, camera):
        self._draw_players(
            screen,
            camera
        )

        self._draw_bullets(
            screen,
            camera
        )

        if self.show_hitboxes:
            self._draw_hitboxes(
                screen,
                camera
            )

    def _draw_players(self, screen, camera):
        for player in self.players:
            player.draw(
                screen,
                camera
            )

    def _draw_bullets(self, screen, camera):
        for bullet in self.bullets:
            bullet.draw(
                screen,
                camera
            )

    def _draw_hitboxes(self, screen, camera):
        for player in self.players:
            player.draw_hitbox(
                screen,
                camera
            )
    
    def _update_players(
        self,
        dt,
        commands,
        walls
    ):
        for player in self.players:
            command = commands.get(
                player.player_id
            )

            if command is None:
                continue

            player.update(
                dt=dt,
                command=command,
                walls=walls,
                players=self.players
            )

            bullet = player.process_actions(
                command=command,
                walls=walls,
                players=self.players
            )

            self.add_bullet(bullet)

    def _update_respawns(self, dt):
        for player in self.players:
            player.update_respawn(dt)

    def _update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

        self.bullets = [
            bullet
            for bullet in self.bullets
            if bullet.alive
        ]