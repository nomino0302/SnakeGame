import pygame
import json
import os.path
import copy

pygame.init()

colors = {
    "ban_default": (84, 116, 54),  # Darker green
    "input_passive": (38, 36, 36),  # Light black
    "input_active": (69, 64, 64),  # Black
}

icon_size = 40
input_size = 75
stick_width, stick_height = 10, 36
font_size = 34

# Icons
apple_ban = pygame.image.load("assets/img/ban/apple_ban.png")
trophy_ban = pygame.image.load("assets/img/ban/trophy_ban.png")

# Buttons
play = pygame.image.load("assets/img/ban/play.png")
pause = pygame.image.load("assets/img/ban/pause.png")
reset = pygame.image.load("assets/img/ban/redo.png")

# Sticks
no_stick = pygame.image.load("assets/img/ban/no_stick.png")
stick1 = pygame.image.load("assets/img/ban/stick1.png")
stick2 = pygame.image.load("assets/img/ban/stick2.png")
stick3 = pygame.image.load("assets/img/ban/stick3.png")
stick4 = pygame.image.load("assets/img/ban/stick4.png")
stick5 = pygame.image.load("assets/img/ban/stick5.png")
stick6 = pygame.image.load("assets/img/ban/stick6.png")

# Fonts
font = pygame.font.Font("assets/font/Mario-Kart-DS.ttf", font_size)
font_input = pygame.font.Font("assets/font/Crashnumberinggothic-MAjp.ttf", font_size)

space_icon = icon_size + 5
space_input = input_size + 5
space_stick = 1


class Banner:
    """Banner to control the game"""

    def __init__(self, win, case, width_ban, height_ban, ban_style=colors["ban_default"]):
        self.win = win
        self.case = case
        self.width_ban, self.height_ban = width_ban, height_ban
        self.ban_style = ban_style
        self.ban = pygame.draw.rect(self.win, self.ban_style,
                                    pygame.Rect(0, 0, self.width_ban, self.height_ban))

        self.best_scores, self.last_config = self.get_best_scores()
        self.pts = 0
        self.best = 0

        # Buttons
        self.play_button = None
        self.pause_button = None
        self.reset_button = None

        self.play_pressed = True
        self.pause_pressed = False

        # Inputs
        self.user_text_lenght = None
        self.lenght_input = None
        self.lenght_input_pressed = False

        self.speed_input = None
        self.speed = 0

        self.sticks = {
            "stick1": [None, no_stick, stick1],
            "stick2": [None, no_stick, stick2],
            "stick3": [None, no_stick, stick3],
            "stick4": [None, no_stick, stick4],
            "stick5": [None, no_stick, stick5],
            "stick6": [None, no_stick, stick6],
        }
        self.current_stick = 0

    def render(self):
        # Adding things to the banner on left
        x, y = self.ban.x + self.case, self.ban.y + 5  # 35, 5

        # Points
        self.win.blit(apple_ban, (x, y))
        x += space_icon

        pts_text = font.render(str(self.pts), True, (255, 255, 255))
        self.win.blit(pts_text, (x, y))
        x += space_icon

        # Best score
        self.win.blit(trophy_ban, (x, y))
        x += space_icon

        best_text = font.render(str(self.best), True, (255, 255, 255))
        self.win.blit(best_text, (x, y))

        # On right
        x = self.ban.w - self.case - space_icon

        # Redo button
        self.reset_button = self.win.blit(reset, (x, y))
        x -= space_icon

        # Pause & play button
        if self.pause_pressed:
            self.play_button = self.win.blit(play, (x, y))
            self.pause_button = None

        elif self.play_pressed:
            self.pause_button = self.win.blit(pause, (x, y))
            self.play_button = None

        x -= space_input
        x_stick, y_stick = x + 4, y + 2

        # Speed and lenght inputs
        # Speed
        self.speed_input = pygame.Rect(x, y, input_size, 40)
        pygame.draw.rect(self.win, colors["input_passive"], self.speed_input)

        for values in self.sticks.values():
            x_stick += space_stick
            values[0] = self.win.blit(values[1], (x_stick, y_stick))
            x_stick += stick_width

        x -= space_input

        # Lenght
        self.lenght_input = pygame.Rect(x, y, input_size, 40)
        if self.lenght_input_pressed:
            pygame.draw.rect(self.win, colors["input_active"], self.lenght_input)
        else:
            pygame.draw.rect(self.win, colors["input_passive"], self.lenght_input)

        lenght_text = font_input.render(self.user_text_lenght, True, (255, 255, 255))
        self.win.blit(lenght_text, (self.lenght_input.x + 2, self.lenght_input.y + 2))

        x -= space_input

    def update(self):
        self.ban = pygame.draw.rect(self.win, self.ban_style,
                                    pygame.Rect(0, 0, self.width_ban, self.height_ban))

        if self.pts > self.best:
            self.best = self.pts

        for stick in self.sticks.keys():
            if (last_index := int(stick[-1])) == self.current_stick:
                for replace_stick, values in self.sticks.items():
                    if int(replace_stick[-1]) <= last_index:
                        values[1] = values[2]
                    else:
                        values[1] = no_stick
                break

        self.render()

    @staticmethod
    def get_best_scores():
        if os.path.exists("scores.json"):
            with open("scores.json") as f:
                try:
                    json_file = json.load(f)
                except json.JSONDecodeError:
                    print("Failed to load scores.json... Creating a new dict...")
                    return {}, None
                best_scores, last_config = json_file[0], json_file[1]
                json_file = copy.deepcopy(best_scores)

                for param in list(json_file.keys()):
                    param = param.replace("(", "").replace(")", "")
                    key = list(map(float, param.split(", ")))
                    key[0] = int(key[0])
                    key = tuple(key)
                    best_scores[key] = json_file.pop(f"({param})")

                return best_scores, last_config
        else:
            return {}, None

    def get_best(self, lenght, frame):
        if (lenght, frame) in self.best_scores:
            return self.best_scores[(lenght, frame)]
        else:
            return 0

    def save_best(self, lenght, frame):
        if (lenght, frame) in self.best_scores:
            if self.best_scores[(lenght, frame)] < self.pts:
                self.best_scores[(lenght, frame)] = self.pts
        else:
            self.best_scores[(lenght, frame)] = self.pts

        with open("scores.json", "w") as f:
            json_file = copy.deepcopy(self.best_scores)
            for param in list(json_file.keys()):
                json_file[str(param)] = json_file.pop(param)
            json.dump([json_file, {"lenght": lenght, "speed": frame}], f, indent=4, sort_keys=True)
