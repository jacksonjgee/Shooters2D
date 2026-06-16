class EntityManager:
    def __init__(self):
        self.bullets = []
        self.players = []

    def draw(self, screen, camera):
        self.draw_bullets(screen, camera)
        self.draw_players(screen, camera)

    def add_bullet(self, bullet):
        if bullet is not None:
            self.bullets.append(bullet)

    def add_player(self, player):
        if player is not None:
            self.players.append(player)

    def update(self, dt):
        for player in self.players:
            player.update_respawn(dt)

        for bullet in self.bullets:
            bullet.update(dt)

        self.bullets = [
            bullet
            for bullet in self.bullets
            if bullet.alive
        ]

    def draw_players(self, screen, camera):
        for player in self.players:
            player.draw(screen, camera)

    def draw_bullets(self, screen, camera):
        for bullet in self.bullets:
            bullet.draw(screen, camera)