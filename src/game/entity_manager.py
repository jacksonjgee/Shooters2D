class EntityManager:
    def __init__(self):
        self.bullets = []

    def add_bullet(self, bullet):
        if bullet is not None:
            self.bullets.append(bullet)

    def update(self, dt, walls):
        for bullet in self.bullets:
            bullet.update(dt, walls)

    def draw(self, screen, camera):
        for bullet in self.bullets:
            bullet.draw(screen, camera)