# Window
import pygame

class window:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dodge the Balls")

        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("Arial", 28)
    
        