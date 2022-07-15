import pygame

# Some colors :
# "black_snake": (0, 0, 0),
# "green_snake": (107, 161, 63),
# "light_green_snake": (177, 199, 51),
# "dark_green_snake": (69, 141, 62),
# "red_snake": (236, 25, 36),
# "light_green": (173, 221, 70),
# "dark_green": (152, 203, 64),

# Snake assets
snake_hori = pygame.image.load("assets/img/snake/snake_hori.png")
snake_verti = pygame.image.load("assets/img/snake/snake_verti.png")
snake_head_up = pygame.image.load("assets/img/snake/snake_head_up.png")
snake_head_left = pygame.image.load("assets/img/snake/snake_head_left.png")
snake_head_right = pygame.image.load("assets/img/snake/snake_head_right.png")
snake_head_down = pygame.image.load("assets/img/snake/snake_head_down.png")
snake_head_up_tongue = pygame.image.load("assets/img/snake/snake_head_up_tongue.png")
snake_head_left_tongue = pygame.image.load("assets/img/snake/snake_head_left_tongue.png")
snake_head_right_tongue = pygame.image.load("assets/img/snake/snake_head_right_tongue.png")
snake_head_down_tongue = pygame.image.load("assets/img/snake/snake_head_down_tongue.png")
snake_right_down = pygame.image.load("assets/img/snake/snake_right_down.png")
snake_right_up = pygame.image.load("assets/img/snake/snake_right_up.png")
snake_left_down = pygame.image.load("assets/img/snake/snake_left_down.png")
snake_left_up = pygame.image.load("assets/img/snake/snake_left_up.png")
snake_tail_down = pygame.image.load("assets/img/snake/snake_tail_down.png")
snake_tail_right = pygame.image.load("assets/img/snake/snake_tail_right.png")
snake_tail_left = pygame.image.load("assets/img/snake/snake_tail_left.png")
snake_tail_up = pygame.image.load("assets/img/snake/snake_tail_up.png")

heads = [snake_head_right, snake_head_down, snake_head_left, snake_head_up]
bodies = [snake_hori, snake_verti]
intersections = [snake_left_down, snake_left_up, snake_right_up, snake_right_down]
tails = [snake_tail_right, snake_tail_down, snake_tail_left, snake_tail_up]
tongues = {
    snake_head_right: snake_head_right_tongue,
    snake_head_down: snake_head_down_tongue,
    snake_head_left: snake_head_left_tongue,
    snake_head_up: snake_head_up_tongue
}


def createFirstSnake(lenght, case, x, y):
    yield [snake_head_right, [x, y]]
    space = case
    lenght -= 1
    while lenght > 1:
        yield [snake_hori, [x - space, y]]
        space += case
        lenght -= 1
    yield [snake_tail_right, [x - space, y]]


class Snake:
    """
    Snake to control
    Colors used for snake assets :
    Black : #000000
    Green : #6ba13f
    Light green : #b1c733
    Dark green : #458d3e
    Red : #ec1925
    """

    def __init__(self, win, case, lenght, x, y):
        """x, y : head position of the snake"""

        self.win = win
        self.case = case
        self.snake = []  # self.snake[0] --> head / self.snake[-1] --> tail
        for part in createFirstSnake(lenght, self.case, x, y):
            self.snake.append(part)
        self.length = len(self.snake)
        self.need_intersection = {0: {}, 1: {}}
        self.last_inter = []

    def show(self, tongue=False):
        head = self.snake[0][0]
        if tongue:
            self.snake[0][0] = tongues[head]
        self.win.blits(self.snake)
        self.snake[0][0] = head

    def getHeadPos(self):
        return self.snake[0][1][0], self.snake[0][1][1]  # x and y

    def getBodyPos(self):
        snake_pos = []
        for part in self.snake:
            snake_pos.append(part[1])
        del snake_pos[0]
        return snake_pos

    def getSnakePos(self):
        snake_pos = [list(self.getHeadPos())]
        for part in self.getBodyPos():
            snake_pos.append(part)
        return snake_pos

    def move(self, direction, step=None):
        """direction can be 'up'⬆️, 'down'⬇️, 'right'➡️ or 'left'⬅️"""

        if step is None:
            step = self.case

        last_pos = None
        last_index = None  # self.snake[last_index][0] == ... --> new part
        last_part = None   # last_part == ... --> last part
        first = True

        self.last_inter = self.snake[-2].copy()

        for part in self.snake:
            current_pos = [part[1][0], part[1][1]]
            current_index = self.snake.index(part)
            current_part = part[0]

            # Head
            if first:
                if direction == "up":
                    part[0] = snake_head_up
                    part[1][1] -= step

                elif direction == "down":
                    part[0] = snake_head_down
                    part[1][1] += step

                elif direction == "right":
                    part[0] = snake_head_right
                    part[1][0] += step

                elif direction == "left":
                    part[0] = snake_head_left
                    part[1][0] -= step

                last_pos = current_pos.copy()
                last_index = current_index
                last_part = current_part
                first = False
                continue

            part[1][0], part[1][1] = last_pos[0], last_pos[1]

            # Intersection
            if part == self.snake[1]:
                if self.snake[last_index][0] == snake_head_up:
                    if current_pos[0] + step == last_pos[0]:
                        part[0] = snake_left_up
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_left_up
                        }
                    elif current_pos[0] - step == last_pos[0]:
                        part[0] = snake_right_up
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_right_up
                        }
                    else:
                        part[0] = snake_verti

                elif self.snake[last_index][0] == snake_head_down:
                    if current_pos[0] + step == last_pos[0]:
                        part[0] = snake_left_down
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_left_down
                        }
                    elif current_pos[0] - step == last_pos[0]:
                        part[0] = snake_right_down
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_right_down
                        }
                    else:
                        part[0] = snake_verti

                elif self.snake[last_index][0] == snake_head_right:
                    if current_pos[1] + step == last_pos[1]:
                        part[0] = snake_right_up
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_right_up
                        }
                    elif current_pos[1] - step == last_pos[1]:
                        part[0] = snake_right_down
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_right_down
                        }
                    else:
                        part[0] = snake_hori

                elif self.snake[last_index][0] == snake_head_left:
                    if current_pos[1] + step == last_pos[1]:
                        part[0] = snake_left_up
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_left_up
                        }
                    elif current_pos[1] - step == last_pos[1]:
                        part[0] = snake_left_down
                        self.need_intersection[1] = self.need_intersection.pop(1) | {
                            current_index + 1: snake_left_down
                        }
                    else:
                        part[0] = snake_hori

            elif part[0] == snake_left_up and current_index not in self.need_intersection[0] or\
                part[0] == snake_right_up and current_index not in self.need_intersection[0] or\
                part[0] == snake_left_down and current_index not in self.need_intersection[0] or\
                    part[0] == snake_right_down and current_index not in self.need_intersection[0]:
                if current_pos[0] + step == last_pos[0] or\
                        current_pos[0] - step == last_pos[0]:
                    part[0] = snake_hori
                else:
                    part[0] = snake_verti

            elif current_index in self.need_intersection[0]:
                part[0] = self.need_intersection[0][current_index]
                if not part == self.snake[-2]:
                    self.need_intersection[1] = self.need_intersection.pop(1) | {
                        current_index + 1: self.need_intersection[0][current_index]
                    }
                del self.need_intersection[0][current_index]

            # Tail
            if part == self.snake[-1]:
                if self.snake[last_index][0] == snake_left_down:
                    if self.snake[last_index][1][1] + step == self.snake[last_index - 1][1][1]:
                        part[0] = snake_tail_right
                    else:
                        part[0] = snake_tail_up

                elif self.snake[last_index][0] == snake_left_up:
                    if self.snake[last_index][1][0] - step == self.snake[last_index - 1][1][0]:
                        part[0] = snake_tail_down
                    else:
                        part[0] = snake_tail_right

                elif self.snake[last_index][0] == snake_right_up:
                    if self.snake[last_index][1][1] - step == self.snake[last_index - 1][1][1]:
                        part[0] = snake_tail_left
                    else:
                        part[0] = snake_tail_down

                elif self.snake[last_index][0] == snake_right_down:
                    if self.snake[last_index][1][0] + step == self.snake[last_index - 1][1][0]:
                        part[0] = snake_tail_up
                    else:
                        part[0] = snake_tail_left

                elif self.snake[last_index][0] == snake_hori:
                    if last_part == snake_left_down or last_part == snake_left_up:
                        part[0] = snake_tail_left
                    elif last_part == snake_right_up or last_part == snake_right_down:
                        part[0] = snake_tail_right
                    elif current_pos[0] + step == last_pos[0]:
                        part[0] = snake_tail_right
                    else:
                        part[0] = snake_tail_left

                elif self.snake[last_index][0] == snake_verti:
                    if last_part == snake_left_down or last_part == snake_right_down:
                        part[0] = snake_tail_down
                    elif last_part == snake_left_up or last_part == snake_right_up:
                        part[0] = snake_tail_up
                    elif current_pos[1] + step == last_pos[1]:
                        part[0] = snake_tail_down
                    else:
                        part[0] = snake_tail_up

            last_pos = current_pos.copy()
            last_index = current_index
            last_part = current_part

        self.need_intersection[0] = self.need_intersection.pop(1)
        self.need_intersection[1] = {}

    def grow(self, step=None):
        if step is None:
            step = self.case

        if self.last_inter[0] in intersections:
            self.snake[-1][0] = self.last_inter[0]

        elif self.snake[-1][0] == snake_tail_right or self.snake[-1][0] == snake_tail_left:
            self.snake[-1][0] = snake_hori

        else:
            self.snake[-1][0] = snake_verti

        if self.snake[-2][0] in intersections:
            self.need_intersection[0] = self.need_intersection.pop(0) | {
                self.snake.index(self.snake[-1]): self.snake[-2][0]
            }

        if self.snake[-1][0] in intersections:
            if self.snake[-1][0] == snake_left_down:
                if self.snake[-1][1][0] - step == self.snake[-2][1][0]:
                    self.snake.append([snake_tail_up, [self.snake[-1][1][0], self.snake[-1][1][1] + step]])
                else:
                    self.snake.append([snake_tail_right, [self.snake[-1][1][0] - step, self.snake[-1][1][1]]])

            elif self.snake[-1][0] == snake_left_up:
                if self.snake[-1][1][0] - step == self.snake[-2][1][0]:
                    self.snake.append([snake_tail_down, [self.snake[-1][1][0], self.snake[-1][1][1] - step]])
                else:
                    self.snake.append([snake_tail_right, [self.snake[-1][1][0] - step, self.snake[-1][1][1]]])

            elif self.snake[-1][0] == snake_right_up:
                if self.snake[-1][1][0] + step == self.snake[-2][1][0]:
                    self.snake.append([snake_tail_down, [self.snake[-1][1][0], self.snake[-1][1][1] - step]])
                else:
                    self.snake.append([snake_tail_left, [self.snake[-1][1][0] + step, self.snake[-1][1][1]]])

            else:
                if self.snake[-1][1][0] + step == self.snake[-2][1][0]:
                    self.snake.append([snake_tail_up, [self.snake[-1][1][0], self.snake[-1][1][1] + step]])
                else:
                    self.snake.append([snake_tail_left, [self.snake[-1][1][0] + step, self.snake[-1][1][1]]])

        else:
            if self.snake[-1][1][0] + step == self.snake[-2][1][0]:
                self.snake.append([snake_tail_right, [self.snake[-1][1][0] - step, self.snake[-1][1][1]]])

            elif self.snake[-1][1][0] - step == self.snake[-2][1][0]:
                self.snake.append([snake_tail_left, [self.snake[-1][1][0] + step, self.snake[-1][1][1]]])

            elif self.snake[-1][1][1] + step == self.snake[-2][1][1]:
                self.snake.append([snake_tail_down, [self.snake[-1][1][0], self.snake[-1][1][1] - step]])

            else:
                self.snake.append([snake_tail_up, [self.snake[-1][1][0], self.snake[-1][1][1] + step]])
