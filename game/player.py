import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)

        # Task 3: leaning animation
        self.lean = 0.0
        self.target_lean = 0.0

    def set_momentum(self, momentum, side):
        """
        Set leaning based on rope pulling momentum.

        side = -1 for player on the left
        side = +1 for computer on the right
        """
        # Puller leans in the direction they are pulling.
        self.target_lean = momentum * 18.0 * side

        # Limit the maximum visual lean
        self.target_lean = max(-18.0, min(18.0, self.target_lean))

    def update_animation(self):
        # Smoothly move toward target lean
        self.lean += (self.target_lean - self.lean) * 0.2

    def render(self, surface):
        """Draw avatar with leaning animation."""

        self.update_animation()

        lean = int(self.lean)

        # Body becomes a slightly tilted polygon
        body_points = [
            (self.x - 20 + lean, self.y - 35),
            (self.x + 20 + lean, self.y - 35),
            (self.x + 16, self.y + 35),
            (self.x - 24, self.y + 35),
        ]

        pygame.draw.polygon(
            surface,
            self.color,
            body_points
        )

        # Round the body edges slightly with a center rectangle
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(
                self.x - 20 + lean // 2,
                self.y - 30,
                40,
                60
            ),
            border_radius=6
        )

        # Head follows the lean
        head_x = self.x + lean
        head_y = self.y - 50

        pygame.draw.circle(
            surface,
            (240, 210, 180),
            (head_x, head_y),
            16
        )

        # Name / control tag
        label_surf = self.font.render(
            self.label,
            True,
            (240, 240, 240)
        )

        surface.blit(
            label_surf,
            (
                self.x - label_surf.get_width() // 2,
                self.y + 45
            )
        )
