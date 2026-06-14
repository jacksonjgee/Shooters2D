import pygame

from settings import MAP_HEIGHT, MAP_WIDTH


class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        wall = 40

        self.walls = [
            # ==================================================
            # OUTER BORDER
            # ==================================================

            pygame.Rect(
                0,
                0,
                MAP_WIDTH,
                wall
            ),

            pygame.Rect(
                0,
                MAP_HEIGHT - wall,
                MAP_WIDTH,
                wall
            ),

            pygame.Rect(
                0,
                0,
                wall,
                MAP_HEIGHT
            ),

            pygame.Rect(
                MAP_WIDTH - wall,
                0,
                wall,
                MAP_HEIGHT
            ),

            # ==================================================
            # TOP-LEFT ROOM
            # ==================================================

            pygame.Rect(
                250,
                200,
                550,
                wall
            ),

            pygame.Rect(
                250,
                200,
                wall,
                450
            ),

            pygame.Rect(
                250,
                610,
                250,
                wall
            ),

            pygame.Rect(
                650,
                610,
                150,
                wall
            ),

            pygame.Rect(
                760,
                200,
                wall,
                250
            ),

            # Small cover inside room
            pygame.Rect(
                420,
                350,
                180,
                wall
            ),

            pygame.Rect(
                560,
                350,
                wall,
                130
            ),

            # ==================================================
            # TOP-CENTRE CORRIDOR
            # ==================================================

            pygame.Rect(
                950,
                180,
                650,
                wall
            ),

            pygame.Rect(
                950,
                180,
                wall,
                350
            ),

            pygame.Rect(
                1150,
                490,
                450,
                wall
            ),

            pygame.Rect(
                1560,
                180,
                wall,
                350
            ),

            # Corridor divider
            pygame.Rect(
                1220,
                300,
                220,
                wall
            ),

            # ==================================================
            # TOP-RIGHT ROOM
            # ==================================================

            pygame.Rect(
                1800,
                180,
                850,
                wall
            ),

            pygame.Rect(
                1800,
                180,
                wall,
                500
            ),

            pygame.Rect(
                1800,
                640,
                300,
                wall
            ),

            pygame.Rect(
                2250,
                640,
                400,
                wall
            ),

            pygame.Rect(
                2610,
                180,
                wall,
                500
            ),

            # Interior cover
            pygame.Rect(
                2050,
                360,
                300,
                wall
            ),

            pygame.Rect(
                2310,
                360,
                wall,
                160
            ),

            # ==================================================
            # CENTRE STRUCTURE
            # ==================================================

            pygame.Rect(
                950,
                750,
                850,
                wall
            ),

            pygame.Rect(
                950,
                750,
                wall,
                450
            ),

            pygame.Rect(
                950,
                1160,
                300,
                wall
            ),

            pygame.Rect(
                1450,
                1160,
                350,
                wall
            ),

            pygame.Rect(
                1760,
                750,
                wall,
                450
            ),

            # Central cover pieces
            pygame.Rect(
                1180,
                900,
                200,
                wall
            ),

            pygame.Rect(
                1380,
                900,
                wall,
                150
            ),

            pygame.Rect(
                1500,
                980,
                140,
                wall
            ),

            # ==================================================
            # STEPPED "ANGLED" WALL
            # ==================================================

            pygame.Rect(
                300,
                900,
                180,
                wall
            ),

            pygame.Rect(
                440,
                940,
                180,
                wall
            ),

            pygame.Rect(
                580,
                980,
                180,
                wall
            ),

            pygame.Rect(
                720,
                1020,
                180,
                wall
            ),

            # Another stepped angle
            pygame.Rect(
                2050,
                850,
                180,
                wall
            ),

            pygame.Rect(
                2190,
                890,
                180,
                wall
            ),

            pygame.Rect(
                2330,
                930,
                180,
                wall
            ),

            pygame.Rect(
                2470,
                970,
                180,
                wall
            ),

            # ==================================================
            # BOTTOM-LEFT AREA
            # ==================================================

            pygame.Rect(
                200,
                1350,
                700,
                wall
            ),

            pygame.Rect(
                200,
                1350,
                wall,
                400
            ),

            pygame.Rect(
                200,
                1710,
                260,
                wall
            ),

            pygame.Rect(
                600,
                1710,
                300,
                wall
            ),

            pygame.Rect(
                860,
                1350,
                wall,
                400
            ),

            # Cover
            pygame.Rect(
                400,
                1500,
                180,
                wall
            ),

            pygame.Rect(
                650,
                1570,
                wall,
                100
            ),

            # ==================================================
            # BOTTOM-CENTRE PASSAGE
            # ==================================================

            pygame.Rect(
                1050,
                1370,
                700,
                wall
            ),

            pygame.Rect(
                1050,
                1370,
                wall,
                350
            ),

            pygame.Rect(
                1050,
                1680,
                250,
                wall
            ),

            pygame.Rect(
                1450,
                1680,
                300,
                wall
            ),

            pygame.Rect(
                1710,
                1370,
                wall,
                350
            ),

            # ==================================================
            # BOTTOM-RIGHT AREA
            # ==================================================

            pygame.Rect(
                1950,
                1300,
                750,
                wall
            ),

            pygame.Rect(
                1950,
                1300,
                wall,
                450
            ),

            pygame.Rect(
                1950,
                1710,
                300,
                wall
            ),

            pygame.Rect(
                2400,
                1710,
                300,
                wall
            ),

            pygame.Rect(
                2660,
                1300,
                wall,
                450
            ),

            # Interior cover
            pygame.Rect(
                2150,
                1480,
                220,
                wall
            ),

            pygame.Rect(
                2450,
                1450,
                wall,
                150
            ),
        ]

    def draw(self, screen, camera):
        for wall in self.walls:
            pygame.draw.rect(
                screen,
                "darkgray",
                camera.apply(wall)
            )