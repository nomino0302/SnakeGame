# Author : nono0302
# Date : 30/07/2021
# Language : Python & 🇫🇷/🇺🇸
# OS : MacOS Big Sur / Macbook Air 2020 M1

"""SnakeGame🐍 : just a simple snake game made with pygame"""

import pygame
import sys
from Snake import Snake
from Banner import Banner
from Level import Level
from Apple import Apple
from random import choices

pygame.init()

# Dimensions
width_win, height_win = 630, 645
width_ban, height_ban = 630, 50
width_border_left, width_border_down, width_border_right = 35, 630, 35
height_border_left, height_border_down, height_border_right = 645, 35, 645
width, height = width_win - (width_border_left + width_border_right), height_win - (height_ban + height_border_down)
# width = 560/ height = 560
start_x, start_y = width_win - (width + width_border_right), height_win - (height + height_border_down)
# x = 35/ y = 50

# Game assets
icon = pygame.image.load("assets/img/icon/icon.png")
font_size = 34
font = pygame.font.Font("assets/font/Mario-Kart-DS.ttf", font_size)
eating = pygame.mixer.Sound("assets/sound/eat.mp3")

# Paramètres fenêtre
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)
win = pygame.display.set_mode((width_win, height_win))

# Game data
fps = 60  # Images par seconde
case = 35
nb_cases_width, nb_cases_height = width / case, height / case  # 16 / 16
nb_cases = int(nb_cases_width * nb_cases_height)  # 256
space_pause = False
escape_reset = False

# STATES
RUNNING = "RUNNING"
PAUSED = "PAUSED"
RESET = "RESET"
FORCED_EXIT = "FORCED_EXIT"
GAME_OVER = "GAME_OVER"
WIN = "WIN"

opposites = {
    "left": "right", "right": "left",
    "up": "down", "down": "up"
}

sticks_values = {
    "stick1": 0.25,
    "stick2": 0.2,
    "stick3": 0.15,
    "stick4": 0.12,
    "stick5": 0.08,
    "stick6": 0.05
}

key_mapping = {
    (pygame.K_RIGHT, pygame.K_d): "right",
    (pygame.K_DOWN, pygame.K_s): "down",
    (pygame.K_LEFT, pygame.K_q): "left",
    (pygame.K_UP, pygame.K_z): "up"
}

# Patterns
win_pattern = ["right"] * 12 + ["down"] + ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] +\
        ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] + ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] +\
        ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] + ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] +\
        ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] + ["left"] * 14 + ["down"] + ["right"] * 14 + ["down"] +\
        ["left"] * 15 + ["up"] * 15 + ["right"] * 3


def getPos(x=None, y=None):
    if x is None:
        return start_y + case * (y - 1)
    elif y is None:
        return start_x + case * (x - 1)
    else:
        return start_x + case * (x - 1), start_y + case * (y - 1)


def secondToFrame(second, frame_per_second):
    return second * frame_per_second


def getAvailableCases(total_cases, snake_pos):
    available_cases = []
    for available_case in total_cases:
        if available_case not in snake_pos:
            available_cases.append(available_case)
    return available_cases


def createSnake(lenght, pos_x, pos_y):
    # Snake creation
    pos_x, pos_y = getPos(pos_x, pos_y)
    return Snake(win, case, lenght, pos_x, pos_y)


def refresh(ban=None, level=None, snake=None, apple=None, tongue=False):
    if ban:
        ban.update()

    if level:
        level.draw_level(ban.height_ban)

    if snake:
        snake.show(tongue)

    if apple:
        apple.stay()

    pygame.display.update()


# Main game
def game(ban, level, snake, lenght=None, frame_quota=None, exit_output=None, test=False):
    global space_pause
    global escape_reset

    state = RUNNING

    if exit_output == RESET:
        if ban.play_button:  # If the game was reset while the game was paused
            ban.pause_pressed = False
            ban.play_pressed = True

    index = 0

    total_cases = []
    case_x, case_y = start_x, start_y
    while case_y < getPos(y=nb_cases_height + 1):
        while case_x < getPos(x=nb_cases_width + 1):
            total_cases.append([case_x, case_y])
            case_x += case
        case_x = start_x
        case_y += case

    apple = Apple(win)

    snake_pos = snake.getSnakePos()
    available_cases = getAvailableCases(total_cases, snake_pos)

    apple.spawn_apple(available_cases)

    clock = pygame.time.Clock()

    tongue = False
    tongue_counter = 0

    default_key = "right"
    key_pressed = default_key
    current_key = default_key

    last_lenght = str(lenght)

    refresh(ban, level, snake, apple, tongue)

    frame_counter = 0

    while True:
        clock.tick(fps)  # Limit the loop (while run) at 60 loops per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # --> Red cross
                return FORCED_EXIT

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or space_pause or escape_reset:
                pos = pygame.mouse.get_pos()
                if space_pause or escape_reset:
                    pos = (0, 0)

                ban.lenght_input_pressed = False

                if ban.lenght_input.collidepoint(pos):
                    ban.lenght_input_pressed = True

                for stick, values in ban.sticks.items():
                    if values[0].collidepoint(pos):
                        ban.current_stick = int(stick[-1])
                        ban.speed = sticks_values[stick]

                if ban.pause_button:  # If the game is running
                    if ban.pause_button.collidepoint(pos) or space_pause:
                        state = PAUSED
                        space_pause = False
                        ban.play_pressed = False
                        ban.pause_pressed = True

                if ban.play_button:  # If the game is not running
                    if ban.play_button.collidepoint(pos) or space_pause:
                        state = RUNNING
                        space_pause = False
                        ban.pause_pressed = False
                        ban.play_pressed = True

                if ban.reset_button:
                    if ban.reset_button.collidepoint(pos) or escape_reset:
                        return RESET

                if not ban.lenght_input_pressed:
                    if ban.user_text_lenght == "" or int(ban.user_text_lenght) < 3 or\
                            int(ban.user_text_lenght) > nb_cases:
                        ban.user_text_lenght = last_lenght
                    else:
                        ban.user_text_lenght = str(int(ban.user_text_lenght))
                        last_lenght = ban.user_text_lenght

                refresh(ban)

            if event.type == pygame.KEYDOWN:
                key = event.key  # TODO: Error?

                if ban.lenght_input_pressed:
                    if key == pygame.K_BACKSPACE:
                        ban.user_text_lenght = ban.user_text_lenght[:-1]
                    else:
                        if event.unicode.isdigit():
                            if len(ban.user_text_lenght) < 3:
                                ban.user_text_lenght += event.unicode
                    refresh(ban)

                if key == pygame.K_SPACE:
                    space_pause = True

                if key == pygame.K_ESCAPE:
                    escape_reset = True

                if state == RUNNING:
                    for keys in key_mapping:
                        if key in keys:
                            key_pressed = key_mapping[keys]

        if state == RUNNING:

            if frame_counter >= frame_quota:
                if not test:
                    if not opposites[key_pressed] == current_key:
                        current_key = key_pressed

                    snake.move(current_key)

                else:
                    snake.move(win_pattern[index])
                    index += 1
                    if index == len(win_pattern):
                        index = 0

                x, y = snake.getHeadPos()
                snake_body_pos = snake.getBodyPos()

                if x > getPos(x=nb_cases_width) or x < getPos(x=1) or y > getPos(y=nb_cases_height) or \
                        y < start_y or [x, y] in snake_body_pos:
                    return GAME_OVER  # Game Over

                if [x, y] == apple.pos:
                    snake.grow()
                    eating.play()
                    ban.pts += 1

                    snake_pos = snake.getSnakePos()
                    available_cases = getAvailableCases(total_cases, snake_pos)

                    if available_cases:
                        apple.spawn_apple(available_cases)

                    else:
                        refresh(ban, level, snake, tongue=True)
                        pygame.time.wait(3000)
                        return WIN

                result_tongue = choices([False, True], weights=[90, 5], k=1)[0]
                if result_tongue:
                    tongue = True
                    tongue_counter = 5

                if tongue_counter:
                    tongue_counter -= 1
                else:
                    tongue = False

                refresh(ban, level, snake, apple, tongue)

                frame_counter = 0

            frame_counter += 1


# Main loop
def main(test=False):
    global space_pause
    global escape_reset

    run = True
    reset = False
    exit_output = None

    ban = Banner(win, case, width_ban, height_ban)
    ban.render()

    case_x, case_y = 4, 8
    if ban.last_config:
        lenght = ban.last_config["lenght"]
        second_frame_quota = ban.last_config["speed"]
        for stick, values in sticks_values.items():
            if values == second_frame_quota:
                ban.current_stick = int(stick[-1])
    else:
        lenght = 3
        second_frame_quota = sticks_values["stick2"]
        ban.current_stick = 2

    ban.user_text_lenght, ban.speed = str(lenght), second_frame_quota
    last_lenght = str(lenght)

    level = Level(win, case, start_x, start_y, width, height, level=0)

    if test:
        case_x, case_y = 4, 1
    pos_x, pos_y = getPos(case_x, case_y)

    while run:
        snake = Snake(win, case, lenght, pos_x, pos_y)
        ban.best = ban.get_best(lenght, ban.speed)
        refresh(ban, level, snake)

        level.waiting_screen(height_ban)
        welcome_text = "Snake Game!!\nPress any key to play!"
        height_text = 0
        for text in welcome_text.split("\n"):
            text_surface = font.render(text, True, (255, 255, 255))
            win.blit(text_surface, (width / 2 - text_surface.get_width() / 2 + case, height / 2 + height_text))
            height_text += font_size + 10
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # --> Red cross
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or space_pause or escape_reset:
                    pos = pygame.mouse.get_pos()
                    if space_pause or escape_reset:
                        pos = (0, 0)

                    ban.lenght_input_pressed = False

                    if ban.lenght_input.collidepoint(pos):
                        ban.lenght_input_pressed = True

                    for stick, values in ban.sticks.items():
                        if values[0].collidepoint(pos):
                            ban.current_stick = int(stick[-1])
                            ban.speed = sticks_values[stick]

                    if not ban.lenght_input_pressed:
                        if ban.user_text_lenght == "" or int(ban.user_text_lenght) < 3 or \
                                int(ban.user_text_lenght) > nb_cases:
                            ban.user_text_lenght = last_lenght
                        else:
                            ban.user_text_lenght = str(int(ban.user_text_lenght))
                            last_lenght = ban.user_text_lenght

                    refresh(ban)

                if event.type == pygame.KEYDOWN or reset:
                    if ban.lenght_input_pressed:
                        key = event.key
                        if key == pygame.K_BACKSPACE:
                            ban.user_text_lenght = ban.user_text_lenght[:-1]
                        else:
                            if event.unicode.isdigit():
                                if len(ban.user_text_lenght) < 3:
                                    ban.user_text_lenght += event.unicode
                        refresh(ban)
                    else:
                        reset = False
                        lenght = int(ban.user_text_lenght)
                        frame_quota = secondToFrame(ban.speed, fps)

                        snake = Snake(win, case, lenght, pos_x, pos_y)
                        ban.pts = 0
                        ban.best = ban.get_best(lenght, ban.speed)
                        exit_output = game(ban, level, snake, lenght, frame_quota, exit_output, test)
                        lenght = int(ban.user_text_lenght)

                        if exit_output == FORCED_EXIT:
                            return

                        elif exit_output == RESET:
                            escape_reset = False
                            reset = True
                            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=1073741904))

                        elif exit_output == GAME_OVER or exit_output == WIN:
                            ban.save_best(lenght, ban.speed)

                            level.waiting_screen(height_ban)
                            if exit_output == GAME_OVER:
                                game_over_text = "Game Over!\nPress any key to replay..."
                            else:
                                game_over_text = "You win!\nPress any key to replay..."
                            height_text = 0
                            for text in game_over_text.split("\n"):
                                text_surface = font.render(text, True, (255, 255, 255))
                                win.blit(text_surface,
                                         (width / 2 - text_surface.get_width() / 2 + case, height / 2 + height_text))
                                height_text += font_size + 10
                            pygame.display.update()
                            pygame.time.delay(400)


if __name__ == "__main__":
    main(test=False)
    pygame.quit()
    sys.exit()
