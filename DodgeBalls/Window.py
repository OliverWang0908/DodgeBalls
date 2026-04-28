# Window
import math

import pygame


class window:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dodge the Balls: Frost Rush")

        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("Arial", 28, bold=True)
        self.SMALL = pygame.font.SysFont("Arial", 18)
        self.TINY = pygame.font.SysFont("Arial", 14)
        self.BIG = pygame.font.SysFont("Arial", 58, bold=True)
        self.MID = pygame.font.SysFont("Arial", 34, bold=True)
        self.POWER = pygame.font.SysFont("Arial", 15, bold=True)
        self._background = self._make_background(WIDTH, HEIGHT)

    def _make_background(self, width, height):
        surface = pygame.Surface((width, height))
        top = (24, 30, 48)
        bottom = (98, 121, 154)
        for y in range(height):
            t = y / height
            color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (width, y))

        for i in range(9):
            x = i * 86 - 80
            pygame.draw.polygon(surface, (36, 56, 70), [(x, height), (x + 110, height - 210), (x + 220, height)])
            pygame.draw.polygon(surface, (50, 78, 92), [(x + 70, height), (x + 178, height - 260), (x + 300, height)])
            pygame.draw.polygon(surface, (223, 239, 246), [(x + 110, height - 210), (x + 84, height - 158), (x + 136, height - 158)])
            pygame.draw.polygon(surface, (230, 244, 249), [(x + 178, height - 260), (x + 148, height - 195), (x + 212, height - 195)])

        pygame.draw.rect(surface, (232, 242, 247), (0, height - 32, width, 32))
        return surface.convert()

    def draw_background(self, snowflakes, score):
        self.screen.blit(self._background, (0, 0))
        lane_alpha = 22 + int(8 * math.sin(score * 0.01))
        lane = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        for x in range(75, self.WIDTH, 150):
            pygame.draw.line(lane, (255, 255, 255, lane_alpha), (x, 90), (x, self.HEIGHT), 2)
        self.screen.blit(lane, (0, 0))
        for snow in snowflakes:
            snow.draw(self.screen)

    def draw_hud(self, player, score, survival, high_score, combo, slow_time, boost_time):
        hud = pygame.Surface((self.WIDTH, 82), pygame.SRCALPHA)
        pygame.draw.rect(hud, (12, 16, 28, 174), (0, 0, self.WIDTH, 82))
        pygame.draw.line(hud, (255, 255, 255, 46), (0, 81), (self.WIDTH, 81), 1)
        self.screen.blit(hud, (0, 0))

        score_text = self.FONT.render(f"{score:06d}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 14))
        time_text = self.SMALL.render(f"TIME {survival:05.1f}", True, (209, 227, 238))
        self.screen.blit(time_text, (22, 50))

        best_text = self.SMALL.render(f"BEST {high_score:06d}", True, (209, 227, 238))
        self.screen.blit(best_text, (self.WIDTH - best_text.get_width() - 20, 18))
        combo_text = self.SMALL.render(f"COMBO x{combo}", True, (255, 224, 114))
        self.screen.blit(combo_text, (self.WIDTH - combo_text.get_width() - 20, 48))

        for i in range(player.max_lives):
            x = self.WIDTH // 2 - 42 + i * 42
            color = (255, 105, 123) if i < player.lives else (85, 91, 108)
            pygame.draw.circle(self.screen, color, (x, 34), 13)
            pygame.draw.circle(self.screen, (255, 255, 255, 80), (x - 4, 30), 4)

        self._draw_status_bar("SHIELD", player.shield_time, 6, (86, 209, 255))
        self._draw_status_bar("SLOW", slow_time, 7, (132, 125, 255))
        self._draw_status_bar("BOOST", boost_time, 8, (255, 214, 91))

    def _draw_status_bar(self, label, value, max_value, color):
        if value <= 0:
            return
        x = 210
        y = 11 + {"SHIELD": 0, "SLOW": 21, "BOOST": 42}[label]
        width = 180
        pygame.draw.rect(self.screen, (255, 255, 255, 35), (x, y, width, 10), border_radius=5)
        pygame.draw.rect(self.screen, color, (x, y, width * min(1, value / max_value), 10), border_radius=5)
        text = self.TINY.render(label, True, (232, 242, 247))
        self.screen.blit(text, (x - text.get_width() - 8, y - 3))

    def draw_menu(self, high_score):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (4, 8, 16, 78), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))

        title = self.BIG.render("FROST RUSH", True, (255, 255, 255))
        subtitle = self.MID.render("DODGE THE BALLS", True, (255, 217, 92))
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 232)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(self.WIDTH // 2, 292)))

        best = self.FONT.render(f"BEST SCORE {high_score:06d}", True, (214, 231, 241))
        self.screen.blit(best, best.get_rect(center=(self.WIDTH // 2, 368)))
        self._button("PRESS ENTER", self.WIDTH // 2, 452, (255, 217, 92))
        self._button("DIRECTION", self.WIDTH // 2, 516, (142, 219, 255))

        hint = self.SMALL.render("WASD / ARROWS MOVE    SPACE DASH    P PAUSE", True, (230, 240, 246))
        self.screen.blit(hint, hint.get_rect(center=(self.WIDTH // 2, 592)))

    def direction_button_rect(self):
        return self._button_rect("DIRECTION", self.WIDTH // 2, 516)

    def directions_back_rect(self):
        return self._button_rect("BACK", self.WIDTH // 2, 636)

    def draw_directions(self):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (4, 7, 15, 190), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(58, 142, self.WIDTH - 116, 548)
        pygame.draw.rect(self.screen, (232, 242, 247), panel, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), panel, 3, border_radius=8)

        title = self.MID.render("HOW TO PLAY", True, (28, 30, 38))
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 188)))

        lines = [
            "Move with WASD or the arrow keys.",
            "Dodge every falling ball for as long as you can.",
            "Press Space while moving to dash out of danger.",
            "Collect power-ups for shields, healing, slow time,",
            "and score boosts.",
            "Avoid hits. You have three lives.",
            "Survive longer and chain dodges to raise your score.",
            "Press P to pause during the game.",
        ]
        y = 252
        for line in lines:
            text = self.SMALL.render(line, True, (45, 52, 66))
            self.screen.blit(text, text.get_rect(center=(self.WIDTH // 2, y)))
            y += 38

        close_hint = self.TINY.render("Press Enter or Esc to return", True, (82, 93, 112))
        self.screen.blit(close_hint, close_hint.get_rect(center=(self.WIDTH // 2, 584)))
        self._button("BACK", self.WIDTH // 2, 636, (255, 217, 92))

    def draw_pause(self):
        self._modal("PAUSED", "Press P to resume")

    def draw_game_over(self, score, high_score, survival):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (4, 7, 15, 166), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))

        title = self.BIG.render("GAME OVER", True, (255, 109, 109))
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 260)))
        line1 = self.FONT.render(f"SCORE {score:06d}   TIME {survival:05.1f}", True, (255, 255, 255))
        line2 = self.SMALL.render(f"BEST {high_score:06d}", True, (214, 231, 241))
        self.screen.blit(line1, line1.get_rect(center=(self.WIDTH // 2, 342)))
        self.screen.blit(line2, line2.get_rect(center=(self.WIDTH // 2, 386)))
        self._button("ENTER TO RETRY", self.WIDTH // 2, 466, (255, 217, 92))

    def _modal(self, title, body):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (4, 7, 15, 132), overlay.get_rect())
        self.screen.blit(overlay, (0, 0))
        title_text = self.BIG.render(title, True, (255, 255, 255))
        body_text = self.FONT.render(body, True, (226, 237, 244))
        self.screen.blit(title_text, title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 38)))
        self.screen.blit(body_text, body_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 34)))

    def _button(self, text, cx, cy, color):
        rect = self._button_rect(text, cx, cy)
        label = self.FONT.render(text, True, (28, 30, 38))
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255, 110), rect, 2, border_radius=8)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _button_rect(self, text, cx, cy):
        label = self.FONT.render(text, True, (28, 30, 38))
        rect = pygame.Rect(0, 0, label.get_width() + 58, 54)
        rect.center = (cx, cy)
        return rect
