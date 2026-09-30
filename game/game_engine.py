import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rope = Rope(width, height)
        self.player = Puller(
            90,
            height // 2,
            (50, 120, 220),
            "PLAYER (A/D)"
        )
        self.computer = Puller(
            width - 90,
            height // 2,
            (220, 80, 50),
            "COMPUTER"
        )

        self.last_key = None
        self.is_pull_locked = False
        self.winner = None
        self.game_state = "PLAYING"

        # Task 2: Computer difficulty
        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()

        # Task 4: 45-second match timer
        self.match_duration = 45_000
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        # Task 1:
        # Allow A and D to alternate rapidly.
        # Ignore repeated KEYDOWN events for the same key.
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                if event.key != self.last_key:

                    # Task 4:
                    # Double player pull distance during Sudden Death.
                    pull_strength = 2.0 if self.sudden_death else 1.0

                    self.rope.pull_left(pull_strength)
                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Task 4: Check the 45-second timer.
        if not self.sudden_death:
            elapsed = now - self.match_start_time

            if elapsed >= self.match_duration:
                self.sudden_death = True
                self.game_state = "PLAYING"

        # Task 2 + Task 4:
        # Dynamic computer difficulty.
        distance_to_player_goal = (
            self.rope.marker_x - self.rope.left_win_x
        )

        if distance_to_player_goal <= 120:
            panic_cooldown = 90
            computer_variance = random.uniform(1.2, 1.6)
        else:
            panic_cooldown = self.computer_pull_cooldown
            computer_variance = random.uniform(0.7, 1.2)

        # Task 4:
        # Double computer pull distance during Sudden Death.
        if self.sudden_death:
            computer_variance *= 2.0

        if now - self.last_computer_pull >= panic_cooldown:
            self.rope.pull_right(computer_variance)
            self.last_computer_pull = now

        # Check whether either side has reached its boundary.
        result = self.rope.check_winner()

        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()

        self.last_key = None
        self.is_pull_locked = False
        self.winner = None

        self.game_state = "PLAYING"

        # Task 4: Reset timer and Sudden Death.
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(
            self.width // 2 - 120,
            self.height // 2 - 80,
            240,
            160
        )

        pygame.draw.rect(
            screen,
            (45, 38, 30),
            mud_rect,
            border_radius=12
        )

        self.rope.render(screen)
        self.player.render(screen)
        self.computer.render(screen)

        # Instructions
        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!",
            True,
            (210, 210, 210)
        )

        screen.blit(
            inst_surf,
            (
                self.width // 2 - inst_surf.get_width() // 2,
                40
            )
        )

        # Task 4: Display timer / Sudden Death state.
        if self.sudden_death:
            timer_text = "SUDDEN DEATH!"
            timer_color = (255, 80, 80)
        else:
            elapsed = pygame.time.get_ticks() - self.match_start_time
            remaining_ms = max(0, self.match_duration - elapsed)
            remaining_seconds = (remaining_ms + 999) // 1000

            timer_text = f"TIME: {remaining_seconds}s"
            timer_color = (240, 240, 240)

        timer_surf = self.font_small.render(
            timer_text,
            True,
            timer_color
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2 - timer_surf.get_width() // 2,
                75
            )
        )

        # Game Over overlay
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"

            color = (
                (80, 220, 80)
                if self.winner == "PLAYER"
                else (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2 - text_surf.get_width() // 2,
                    self.height // 2 - 50
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )
