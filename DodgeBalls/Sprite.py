# Sprite
import math
import random

import pygame


class Player:
    def __init__(self, WIDTH, HEIGHT, speed, img_path):
        self.w = 50
        self.h = 72
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 112
        self.speed = speed
        self.base_speed = speed
        self.max_lives = 3
        self.lives = self.max_lives
        self.shield_time = 0
        self.invincible_time = 0
        self.dash_cooldown = 0
        self.dash_flash = 0

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def reset(self, WIDTH, HEIGHT):
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 112
        self.rect.topleft = (self.x, self.y)
        self.lives = self.max_lives
        self.shield_time = 0
        self.invincible_time = 0
        self.dash_cooldown = 0
        self.dash_flash = 0

    def move(self, keys, WIDTH, HEIGHT, dt):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        length = math.hypot(dx, dy)
        if length:
            dx /= length
            dy /= length

        multiplier = 1
        if keys[pygame.K_SPACE] and self.dash_cooldown <= 0 and length:
            multiplier = 3.2
            self.dash_cooldown = 0.8
            self.dash_flash = 0.18

        self.x += dx * self.speed * multiplier * dt * 60
        self.y += dy * self.speed * multiplier * dt * 60
        self.x = max(8, min(WIDTH - self.w - 8, self.x))
        self.y = max(96, min(HEIGHT - self.h - 28, self.y))
        self.rect.topleft = (round(self.x), round(self.y))

    def update(self, dt):
        self.shield_time = max(0, self.shield_time - dt)
        self.invincible_time = max(0, self.invincible_time - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.dash_flash = max(0, self.dash_flash - dt)

    def take_hit(self):
        if self.invincible_time > 0:
            return False
        if self.shield_time > 0:
            self.shield_time = 0
            self.invincible_time = 1.0
            return False

        self.lives -= 1
        self.invincible_time = 1.2
        return self.lives <= 0

    def draw(self, screen):
        if self.invincible_time > 0 and int(self.invincible_time * 14) % 2 == 0:
            return

        shadow = pygame.Surface((self.w + 18, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
        screen.blit(shadow, (self.rect.centerx - shadow.get_width() // 2, self.rect.bottom - 4))

        if self.shield_time > 0:
            shield = pygame.Surface((self.w + 28, self.h + 28), pygame.SRCALPHA)
            color = (74, 207, 255, 82 + int(30 * math.sin(pygame.time.get_ticks() * 0.012)))
            pygame.draw.ellipse(shield, color, shield.get_rect(), 4)
            screen.blit(shield, (self.rect.x - 14, self.rect.y - 14))

        if self.dash_flash > 0:
            streak = pygame.Surface((self.w + 20, self.h), pygame.SRCALPHA)
            pygame.draw.ellipse(streak, (255, 255, 255, 90), streak.get_rect())
            screen.blit(streak, (self.rect.x - 10, self.rect.y))

        screen.blit(self.image, self.rect.topleft)


class Ball:
    TYPES = {
        "fast": {"radius": 13, "color": (255, 91, 91), "speed": 1.35, "value": 18},
        "heavy": {"radius": 24, "color": (255, 171, 69), "speed": 0.72, "value": 26},
        "curve": {"radius": 17, "color": (214, 91, 255), "speed": 1.05, "value": 32},
        "normal": {"radius": 16, "color": (255, 107, 107), "speed": 1.0, "value": 14},
    }

    def __init__(self, speed, WIDTH, kind=None):
        self.kind = kind or random.choices(
            ["normal", "fast", "heavy", "curve"],
            weights=[54, 20, 16, 10],
            k=1,
        )[0]
        config = self.TYPES[self.kind]
        self.r = config["radius"]
        self.x = random.randint(self.r + 10, WIDTH - self.r - 10)
        self.y = -self.r - random.randint(0, 80)
        self.speed = speed * config["speed"]
        self.value = config["value"]
        self.color = config["color"]
        self.vx = random.uniform(-1.1, 1.1) if self.kind in ("curve", "fast") else 0
        self.phase = random.uniform(0, math.tau)
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def update(self, dt, slow_factor=1.0):
        self.phase += dt * 5
        drift = math.sin(self.phase) * 1.8 if self.kind == "curve" else self.vx
        self.x += drift * dt * 60
        self.y += self.speed * slow_factor * dt * 60
        self.rect.center = (round(self.x), round(self.y))

    def off_screen(self, HEIGHT):
        return self.y - self.r > HEIGHT

    def collides_with(self, rect):
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top, min(self.y, rect.bottom))
        return (self.x - cx) ** 2 + (self.y - cy) ** 2 <= self.r ** 2

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0, 60), (round(self.x + 4), round(self.y + 6)), self.r)
        pygame.draw.circle(screen, self.color, (round(self.x), round(self.y)), self.r)
        pygame.draw.circle(screen, (255, 255, 255, 95), (round(self.x - self.r * 0.32), round(self.y - self.r * 0.35)), max(3, self.r // 4))
        pygame.draw.circle(screen, (80, 24, 28), (round(self.x), round(self.y)), self.r, 2)


class PowerUp:
    TYPES = {
        "shield": {"color": (86, 209, 255), "label": "S"},
        "heal": {"color": (99, 222, 130), "label": "+"},
        "slow": {"color": (132, 125, 255), "label": "T"},
        "boost": {"color": (255, 214, 91), "label": "x2"},
    }

    def __init__(self, WIDTH):
        self.kind = random.choices(["shield", "heal", "slow", "boost"], [38, 18, 24, 20], k=1)[0]
        self.x = random.randint(40, WIDTH - 40)
        self.y = -40
        self.r = 18
        self.speed = random.uniform(2.4, 3.4)
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
        self.pulse = random.uniform(0, math.tau)

    def update(self, dt):
        self.pulse += dt * 5
        self.y += self.speed * dt * 60
        self.rect.center = (round(self.x), round(self.y))

    def off_screen(self, HEIGHT):
        return self.y - self.r > HEIGHT

    def draw(self, screen, font):
        config = self.TYPES[self.kind]
        glow_radius = self.r + 8 + int(math.sin(self.pulse) * 2)
        glow = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*config["color"], 56), (glow_radius, glow_radius), glow_radius)
        screen.blit(glow, (self.x - glow_radius, self.y - glow_radius))
        pygame.draw.circle(screen, config["color"], (round(self.x), round(self.y)), self.r)
        pygame.draw.circle(screen, (255, 255, 255), (round(self.x), round(self.y)), self.r, 2)
        label = font.render(config["label"], True, (24, 27, 36))
        screen.blit(label, label.get_rect(center=(self.x, self.y)))


class SnowFlake:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-screen_height, 0)
        self.radius = random.randint(1, 4)
        self.speed = random.uniform(0.6, 2.2)
        self.sway = random.uniform(0.4, 1.4)
        self.phase = random.uniform(0, math.tau)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        self.phase += dt * self.sway
        self.y += self.speed * dt * 60
        self.x += math.sin(self.phase) * 0.35

    def off_screen(self):
        return self.y > self.screen_height + 12

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 180), (int(self.x), int(self.y)), self.radius)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.35, 0.8)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.08 * dt * 60

    def alive(self):
        return self.life > 0

    def draw(self, screen):
        alpha = max(0, min(255, int(255 * self.life / self.max_life)))
        dot = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(dot, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(dot, (self.x - self.size, self.y - self.size))
