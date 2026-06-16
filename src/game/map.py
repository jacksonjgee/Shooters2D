import pygame


class GameMap:
    def __init__(self):
        self.width = 2000
        self.height = 1400

        self.defender_spawn = pygame.Vector2(
            250,
            self.height // 2
        )

        self.attacker_spawn = pygame.Vector2(
            self.width - 250,
            self.height // 2
        )

        self.walls = self._create_walls()

    def _create_walls(self):
        walls = []

        wall_thickness = 40

        # =========================================================
        # OUTER BOUNDARIES
        # =========================================================

        walls.extend([
            pygame.Rect(
                0,
                0,
                self.width,
                wall_thickness
            ),

            pygame.Rect(
                0,
                self.height - wall_thickness,
                self.width,
                wall_thickness
            ),

            pygame.Rect(
                0,
                0,
                wall_thickness,
                self.height
            ),

            pygame.Rect(
                self.width - wall_thickness,
                0,
                wall_thickness,
                self.height
            )
        ])

        # =========================================================
        # DEFENDER-SIDE SPAWN COVER
        # =========================================================

        # Upper spawn nook
        walls.extend([
            pygame.Rect(
                180,
                190,
                260,
                40
            ),

            pygame.Rect(
                400,
                190,
                40,
                220
            ),

            pygame.Rect(
                280,
                370,
                160,
                40
            )
        ])

        # Lower spawn nook
        walls.extend([
            pygame.Rect(
                180,
                self.height - 230,
                260,
                40
            ),

            pygame.Rect(
                400,
                self.height - 410,
                40,
                220
            ),

            pygame.Rect(
                280,
                self.height - 410,
                160,
                40
            )
        ])

        # =========================================================
        # ATTACKER-SIDE SPAWN COVER
        # =========================================================

        # Upper spawn nook
        walls.extend([
            pygame.Rect(
                self.width - 440,
                190,
                260,
                40
            ),

            pygame.Rect(
                self.width - 440,
                190,
                40,
                220
            ),

            pygame.Rect(
                self.width - 440,
                370,
                160,
                40
            )
        ])

        # Lower spawn nook
        walls.extend([
            pygame.Rect(
                self.width - 440,
                self.height - 230,
                260,
                40
            ),

            pygame.Rect(
                self.width - 440,
                self.height - 410,
                40,
                220
            ),

            pygame.Rect(
                self.width - 440,
                self.height - 410,
                160,
                40
            )
        ])

        # =========================================================
        # TOP CORRIDOR
        # =========================================================

        # Long corridor walls
        walls.extend([
            pygame.Rect(
                520,
                150,
                360,
                40
            ),

            pygame.Rect(
                520,
                330,
                280,
                40
            ),

            pygame.Rect(
                1160,
                150,
                320,
                40
            ),

            pygame.Rect(
                1200,
                330,
                280,
                40
            )
        ])

        # Offset blocks create corners and partial angles
        walls.extend([
            pygame.Rect(
                760,
                190,
                40,
                100
            ),

            pygame.Rect(
                800,
                250,
                120,
                40
            ),

            pygame.Rect(
                1080,
                190,
                40,
                100
            ),

            pygame.Rect(
                1000,
                250,
                120,
                40
            )
        ])

        # =========================================================
        # BOTTOM CORRIDOR
        # =========================================================

        walls.extend([
            pygame.Rect(
                520,
                self.height - 190,
                360,
                40
            ),

            pygame.Rect(
                520,
                self.height - 370,
                280,
                40
            ),

            pygame.Rect(
                1160,
                self.height - 190,
                320,
                40
            ),

            pygame.Rect(
                1200,
                self.height - 370,
                280,
                40
            )
        ])

        walls.extend([
            pygame.Rect(
                760,
                self.height - 290,
                40,
                100
            ),

            pygame.Rect(
                800,
                self.height - 290,
                120,
                40
            ),

            pygame.Rect(
                1080,
                self.height - 290,
                40,
                100
            ),

            pygame.Rect(
                1000,
                self.height - 290,
                120,
                40
            )
        ])

        # =========================================================
        # LEFT-MIDDLE ZIG-ZAG PATH
        # =========================================================

        walls.extend([
            pygame.Rect(
                480,
                470,
                220,
                40
            ),

            pygame.Rect(
                660,
                470,
                40,
                150
            ),

            pygame.Rect(
                580,
                580,
                120,
                40
            ),

            pygame.Rect(
                580,
                580,
                40,
                150
            ),

            pygame.Rect(
                580,
                690,
                190,
                40
            ),

            pygame.Rect(
                730,
                690,
                40,
                150
            ),

            pygame.Rect(
                650,
                800,
                120,
                40
            )
        ])

        # =========================================================
        # RIGHT-MIDDLE ZIG-ZAG PATH
        # =========================================================

        walls.extend([
            pygame.Rect(
                self.width - 700,
                470,
                220,
                40
            ),

            pygame.Rect(
                self.width - 700,
                470,
                40,
                150
            ),

            pygame.Rect(
                self.width - 700,
                580,
                120,
                40
            ),

            pygame.Rect(
                self.width - 620,
                580,
                40,
                150
            ),

            pygame.Rect(
                self.width - 770,
                690,
                190,
                40
            ),

            pygame.Rect(
                self.width - 770,
                690,
                40,
                150
            ),

            pygame.Rect(
                self.width - 770,
                800,
                120,
                40
            )
        ])

        # =========================================================
        # CENTRAL COMBAT AREA
        # =========================================================

        # Central upper L-shape
        walls.extend([
            pygame.Rect(
                860,
                430,
                220,
                40
            ),

            pygame.Rect(
                1040,
                430,
                40,
                150
            )
        ])

        # Central lower reverse L-shape
        walls.extend([
            pygame.Rect(
                920,
                830,
                220,
                40
            ),

            pygame.Rect(
                920,
                720,
                40,
                150
            )
        ])

        # Centre pillars
        walls.extend([
            pygame.Rect(
                840,
                600,
                70,
                110
            ),

            pygame.Rect(
                1090,
                690,
                70,
                110
            )
        ])

        # Small centre cover blocks
        walls.extend([
            pygame.Rect(
                960,
                560,
                80,
                40
            ),

            pygame.Rect(
                960,
                800,
                80,
                40
            )
        ])

        # =========================================================
        # SMALL NOOKS AND PEEK CORNERS
        # =========================================================

        walls.extend([
            # Left-upper pocket
            pygame.Rect(
                470,
                390,
                40,
                90
            ),

            pygame.Rect(
                470,
                390,
                100,
                40
            ),

            # Left-lower pocket
            pygame.Rect(
                470,
                920,
                40,
                90
            ),

            pygame.Rect(
                470,
                970,
                100,
                40
            ),

            # Right-upper pocket
            pygame.Rect(
                self.width - 510,
                390,
                40,
                90
            ),

            pygame.Rect(
                self.width - 570,
                390,
                100,
                40
            ),

            # Right-lower pocket
            pygame.Rect(
                self.width - 510,
                920,
                40,
                90
            ),

            pygame.Rect(
                self.width - 570,
                970,
                100,
                40
            )
        ])

        return walls
    
    def draw(self, screen, camera):
        for wall in self.walls:
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                camera.apply(wall)
            )