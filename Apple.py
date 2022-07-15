import pygame
from random import choice

# Food assets
apple = pygame.image.load("assets/img/food/apple.png")


class Apple:
    """Snakes favourite food"""

    def __init__(self, win):
        self.win = win
        self.pos = None

    def spawn_apple(self, available_cases):
        apple_pos = choice(available_cases)
        self.win.blit(apple, apple_pos)
        self.pos = apple_pos

    def stay(self):
        self.win.blit(apple, self.pos)
