import pygame
from random import choice

colors = {
    "border_default": (98, 137, 64),  # Dark green
    "game_over_screen": (0, 0, 0, 190)  # Transparent drak
}


class Level:
    """All amazing levels"""

    def __init__(self, win, case, start_x, start_y, width, height, level=None, border_style=colors["border_default"]):
        self.win = win
        self.case = case
        self.start_x, self.start_y = start_x, start_y
        self.width, self.height = width, height
        self.level_rect = pygame.Rect(start_x, start_y, width, height)
        self.border_style = border_style
        self.levels = [
            pygame.image.load("assets/img/bg/bg.png"),
        ]
        self.file = self.get_level(level)

    def get_level(self, level):
        if level is not None:
            return self.levels[level]
        else:
            return choice(self.levels)

    def draw_level(self, height_ban):
        pygame.draw.rect(self.win, self.border_style,
                         pygame.Rect(0, height_ban, self.width + self.case * 2, self.height + self.case))
        self.win.blit(self.file, (self.start_x, self.start_y))

    def waiting_screen(self, height_ban):
        rect = pygame.Rect(0, height_ban, self.width + self.case * 2, self.height + self.case)
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, colors["game_over_screen"], shape_surf.get_rect())
        self.win.blit(shape_surf, rect)

        pygame.display.update()
