import math
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

        # Task 3: rope tension and momentum
        self.tension = 0.0
        self.pull_direction = 0

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)

        # Increase tension and remember pulling direction
        self.tension = min(1.0, self.tension + 0.25 * strength)
        self.pull_direction = -1

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)

        # Increase tension and remember pulling direction
        self.tension = min(1.0, self.tension + 0.25 * strength)
        self.pull_direction = 1

    def get_momentum(self):
        return self.pull_direction * self.tension

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.tension = 0.0
        self.pull_direction = 0

    def render(self, surface):
        # Task 3: animated rope tension/sag
        time = pygame.time.get_ticks() / 1000.0

        # Tension naturally fades when nobody is pulling
        self.tension = max(0.0, self.tension - 0.01)

        start_x = 60
        end_x = self.screen_width - 60

        # Higher tension -> stronger vibration
        amplitude = 2.0 + (self.tension * 8.0)

        points = []

        segments = 40
        for i in range(segments + 1):
            ratio = i / segments
            x = start_x + (end_x - start_x) * ratio

            # Smooth wave which becomes more visible under tension
            wave = math.sin(time * 12.0 + ratio * math.pi * 8.0)
            y = self.center_y + wave * amplitude * self.tension

            points.append((int(x), int(y)))

        pygame.draw.lines(
            surface,
            (180, 140, 90),
            False,
            points,
            10
        )

        # Goal markers
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )

        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center boundary
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Center flag
        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )
