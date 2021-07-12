import random

import pygame
from pygame.math import Vector2


class BodyPart(pygame.sprite.Rect):

    def __init__(self, block_size, x_i, y_i, display):
        super().__init__(block_size * x_i, block_size * y_i, block_size, block_size)

    def draw(self, display, color):
        pygame.draw.rect(display, color, self)

    def change_color(self, display, color):
        pygame.draw.rect(display, color, self)


class Food(pygame.sprite.Rect):

    def __init__(self, block_size, x_i, y_i, display):
        super().__init__(block_size * x_i, block_size * y_i, block_size, block_size)
        pygame.draw.rect(display, pygame.Color("green"), self)

    def draw(self, display):
        pygame.draw.rect(display, pygame.Color("green"), self)


class Snake(object):

    def __init__(self, block_size, x_position_i, y_position_i, display, head_color, body_color):
        self.__body = [BodyPart(block_size, x_position_i, y_position_i, display)]
        self.__velocity = Vector2((0, 0))
        self.__block_size = block_size
        self.__minimum_speed = round(5 * 10 * self.__block_size / 50)
        self.__maximum_speed = round(10 * 10 * self.__block_size / 50)
        self.__head_color = pygame.Color(head_color)
        self.__body_color = pygame.Color(body_color)
        self.__body[0].change_color(display, self.__head_color)
        self.__tail_trace = set()
        self.__head_trace = list()
        self.__display = display

    def eat(self, food_dict):
        for position in self.__tail_trace:
            if position in food_dict.keys():
                self.__body.append(BodyPart(self.__block_size, position[0] / self.__block_size, position[1] / self.__block_size, self.__display))
                del food_dict[position]

    def draw(self, display):
        for body in self.__body:
            body.draw(display, self.__body_color)
        self.__body[0].change_color(display, self.__head_color)

    def move(self):
        self.__tail_trace.clear()
        self.__head_trace.clear()

        tmp_speed_i = abs(self.__velocity[0] + self.__velocity[1]) / self.__block_size

        if len(self.__body) > 1:
            for i in range(1, int(tmp_speed_i) + 1):
                self.__tail_trace.add(tuple(x for x in self.__body[-1 * i].topleft))
            for i in range(int(tmp_speed_i)):
                self.__head_trace.append(tuple(x * i / abs(self.__velocity[0] + self.__velocity[1]) for x in self.__velocity))

        else:
            if tmp_speed_i == 1:
                self.__tail_trace.add(tuple(x for x in self.__body[0].topleft))
            else:
                self.__tail_trace.add(tuple(self.__body[0].topleft))

        if len(self.__body) > 1:
            for tmp_vector in self.__head_trace:
                tmp_position = self.__body[0].move(*tmp_vector).topleft
                self.__body.insert(1, BodyPart(self.__block_size, tmp_position[0] / self.__block_size, tmp_position[1] / self.__block_size, self.__display))
                self.__body.pop(-1)

        self.__body[0] = self.__body[0].move(self.__velocity)

    def set_upside(self):
        if self.__velocity[1] > 0:
            self.__velocity = Vector2(0, self.__minimum_speed)
        else:
            self.__velocity = Vector2(0, -1 * self.__minimum_speed)

    def set_downside(self):
        if self.__velocity[1] < 0:
            self.__velocity = Vector2(0, -1 * self.__minimum_speed)
        else:
            self.__velocity = Vector2(0, self.__minimum_speed)

    def set_rightside(self):
        if self.__velocity[0] < 0:
            self.__velocity = Vector2(-1 * self.__minimum_speed, 0)
        else:
            self.__velocity = Vector2(self.__minimum_speed, 0)

    def set_leftside(self):
        if self.__velocity[0] > 0:
            self.__velocity = Vector2(self.__minimum_speed, 0)
        else:
            self.__velocity = Vector2(-1 * self.__minimum_speed, 0)

    def boost(self):
        self.__velocity = Vector2(self.__velocity[0] * 2, self.__velocity[1] * 2)
        if abs(self.__velocity[0] + self.__velocity[1]) > self.__maximum_speed:
            if self.__velocity[0] != 0 and self.__velocity[0] > 0:
                self.__velocity = Vector2(self.__maximum_speed, 0)
            else:
                if self.__velocity[0] != 0:
                    self.__velocity = Vector2(-1 * self.__maximum_speed, 0)
            if self.__velocity[1] != 0 and self.__velocity[1] > 0:
                self.__velocity = Vector2(0, self.__maximum_speed)
            else:
                if self.__velocity[1] != 0:
                    self.__velocity = Vector2(0, -1 * self.__maximum_speed)

    @property
    def velocity(self):
        return self.__velocity

    @property
    def head(self):
        return self.__body[0]

    @property
    def body(self):
        return self.__body


class Manager(object):

    def __init__(self, block_size, n_food, n_cols, n_rows):

        pygame.init()
        self.__num_food = n_food
        self.__block_size = block_size
        self.__n_rows = n_rows
        self.__n_cols = n_cols
        self.__screen = pygame.display.set_mode((n_cols * self.__block_size, n_rows * self.__block_size))
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.__screen_rect = self.__screen.get_rect()
        self.__food_dict = dict()

        self.__snakes = list()
        self.__snakes.append(
            Snake(self.__block_size, random.randint(0, n_cols), random.randint(0, n_rows), self.__screen, "red",
                  "pink"))
        self.__snakes.append(
            Snake(self.__block_size, random.randint(0, n_cols), random.randint(0, n_rows), self.__screen, "blue",
                  "skyblue"))

        # 빈공간의 좌표를 담는 셋
        self.__empty_space_set = set()
        for i in range(self.__n_cols):
            for j in range(self.__n_rows):
                self.__empty_space_set.add((i * self.__block_size, j * self.__block_size))
        # food을 배분
        self.__prepare_food()

        pygame.display.set_caption('Snake Game')

        self.__draw_all_object()

    def __draw_food(self):
        for food in self.__food_dict.values():
            food.draw(self.__screen)

    def __prepare_food(self):
        tmp_set = self.__empty_space_set - set(self.__food_dict.keys())
        tmp_set = tmp_set - set(tmp_body.topleft for tmp_body in self.__snakes[0].body)
        tmp_set = tmp_set - set(tmp_body.topleft for tmp_body in self.__snakes[1].body)
        for _ in range(self.__num_food - len(self.__food_dict.keys())):
            tmp_position = random.choice(list(tmp_set))
            self.__food_dict[tmp_position] = Food(self.__block_size, tmp_position[0] / self.__block_size, tmp_position[1] / self.__block_size, self.__screen)
            self.__empty_space_set.remove(tmp_position)

    def __update_snakes_state(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or not self.__screen_rect.contains(self.__snakes[0].head) \
                    or not self.__screen_rect.contains((self.__snakes[1].head)):
                self.game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.__snakes[0].set_upside()
        elif pressed[pygame.K_RIGHT]:
            self.__snakes[0].set_rightside()
        elif pressed[pygame.K_DOWN]:
            self.__snakes[0].set_downside()
        elif pressed[pygame.K_LEFT]:
            self.__snakes[0].set_leftside()

        if pressed[pygame.K_RSHIFT]:
            self.__snakes[0].boost()

        if pressed[pygame.K_w]:
            self.__snakes[1].set_upside()
        elif pressed[pygame.K_d]:
            self.__snakes[1].set_rightside()
        elif pressed[pygame.K_s]:
            self.__snakes[1].set_downside()
        elif pressed[pygame.K_a]:
            self.__snakes[1].set_leftside()

        if pressed[pygame.K_LSHIFT]:
            self.__snakes[1].boost()

    def __check_overlap(self):
        if set(tmp_body.topleft for tmp_body in self.__snakes[0].body).intersection(set(tmp_body.topleft for tmp_body in self.__snakes[1].body)):
            self.game_over = True
        if len(list(tmp_body.topleft for tmp_body in self.__snakes[0].body)) != len(set(tmp_body.topleft for tmp_body in self.__snakes[0].body)) or len(list(tmp_body.topleft for tmp_body in self.__snakes[1].body)) != len( set(tmp_body.topleft for tmp_body in self.__snakes[1].body)):
            self.game_over = True

    def run_game(self):
        while not self.game_over:
            self.__update_snakes_state()
            self.__prepare_food()
            for snake in self.__snakes:
                snake.move()
                snake.eat(self.__food_dict)

            self.__check_overlap()
            self.__draw_all_object()
            self.clock.tick_busy_loop(50)

    def __draw_all_object(self):
        self.__screen.fill(pygame.Color("black"))
        for food in self.__food_dict.values():
            food.draw(self.__screen)
        for snake in self.__snakes:
            snake.draw(self.__screen)
        pygame.display.update()


if __name__ == "__main__":
    tmp_manager = Manager(10, 20, 180, 80)
    tmp_manager.run_game()

