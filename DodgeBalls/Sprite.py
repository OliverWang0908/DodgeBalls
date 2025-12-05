# Sprite
import pygame
import random
import sys
import time

"""
class Player:
    def __init__(self, WIDTH, HEIGHT, speed):
        self.w = 60
        self.h = 20
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 80
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, keys, WIDTH):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 144, 255), self.rect)

"""

class Ball:
    def __init__(self, speed, WIDTH):
        self.r = 15
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = -self.r
        self.speed = speed
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 80, 80), (self.x, self.y), self.r)

class SnowFlake:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-screen_height, 0)
        self.radius = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.y += self.speed
        self.x += random.uniform(-0.3, 0.3)

    def off_screen(self):
        return self.y > self.screen_height

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)



class Player:
    def __init__(self, WIDTH, HEIGHT, speed, img_path):
        self.w = 60
        self.h = 60
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 80
        self.speed = speed

        
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

       
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, keys, WIDTH):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        
        self.x, self.y = self.rect.x, self.rect.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))



'''
class ChristmasTree:
    def __init__(self, screen_width, screen_height, tree_height=600, alpha=180):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tree_height = tree_height
        self.alpha = alpha

        
        self.image = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self._draw_tree()

    def _draw_tree(self):
        x_center = self.screen_width // 2
        y_bottom = self.screen_height - 30
        trunk_h = self.tree_height * 0.15
        trunk_w = self.tree_height * 0.1

        # trunk
        trunk_color = (210, 180, 140, self.alpha)
        pygame.draw.rect(self.image, trunk_color,
                         (x_center - trunk_w/2, y_bottom - trunk_h, trunk_w, trunk_h))

        # leaves
        leaf_color = (0, 128, 0, self.alpha)
        num_layers = 6
        for i in range(num_layers):
            layer_h = self.tree_height * 0.7 / num_layers
            layer_w = self.tree_height * 0.5 * (1 - i / (num_layers * 1.2))
            top_y = y_bottom - trunk_h - layer_h * (i+1)
            pygame.draw.polygon(self.image, leaf_color, [
                (x_center, top_y - layer_h),
                (x_center - layer_w/2, top_y),
                (x_center + layer_w/2, top_y)
            ])

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
'''


