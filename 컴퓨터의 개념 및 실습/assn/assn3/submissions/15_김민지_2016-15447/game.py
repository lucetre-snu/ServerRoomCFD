import pygame
import random
from pygame.constants import KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT, K_RSHIFT, K_w, K_s, K_a, K_d, K_LSHIFT

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (203, 141, 226)
PINK = (255, 153, 204)
ORANGE = (254, 111, 97)
LIGHT_ORANGE = (246, 161, 152)
YELLOW = (254, 173, 81)
LIGHT_YELLOW = (252, 217, 157)
HIGHLIGHT = (198, 41, 158)

pygame.init()
game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("dccp58 Snake Game")
clock = pygame.time.Clock()

game_over = False


class Player:
    def __init__(self, display, up, down, left, right, boost_key, x_start, y_start):
        self.x = [0]
        self.y = [0]
        self.dx = 0
        self.dy = 0
        self.length = 2
        self.count = 0
        self.count_max = 2
        self.display = display
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.boost_key = boost_key
        self.x[0] = x_start
        self.y[0] = y_start

        for i in range(0, self.length):
            self.x.append(0)
            self.y.append(0)

    def handle_event(self, event, pressed):
        if event.type == KEYDOWN:
            if event.key == self.left:
                self.dx = -10
                self.dy = 0
            elif event.key == self.right:
                self.dx = 10
                self.dy = 0
            elif event.key == self.up:
                self.dx = 0
                self.dy = -10
            elif event.key == self.down:
                self.dx = 0
                self.dy = 10

    def tick(self):
        self.x[0] += self.dx
        self.y[0] += self.dy

        for i in range(self.length, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

    def draw(self, color, color2):
        pygame.draw.rect(self.display, color, [self.x[0], self.y[0], 10, 10])
        for i in range(2, self.length):
            pygame.draw.rect(self.display, color2, [self.x[i], self.y[i], 10, 10])

    def grow(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)


class Food:
    active = True

    def __init__(self):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10


player_one = Player(game_display, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, 0, 0)
player_two = Player(game_display, K_w, K_s, K_a, K_d, K_LSHIFT, 100, 100)
foods = [Food() for i in range(20)]

# 창 띄우기
while not game_over:
    for event in pygame.event.get():  # 사용자가 만들어주는 모든 입력 가져오기
        if event.type == QUIT:
            game_over = True
            break
        pressed = pygame.key.get_pressed()
        player_one.handle_event(event, pressed)
        player_two.handle_event(event, pressed)

    player_one.tick()
    player_two.tick()
    if pressed[K_RSHIFT]:
        player_one.tick()

    if pressed[K_LSHIFT]:
        player_two.tick()

    game_display.fill(PURPLE)  # 모든 공간 다 채우기
    player_one.draw(YELLOW, LIGHT_YELLOW)
    player_two.draw(ORANGE, LIGHT_ORANGE)

    for food in foods:
        index = foods.index(food)
        if food.active:
            pygame.draw.rect(game_display, WHITE, [food.x, food.y, 10, 10])

        if player_one.x[0] == food.x and player_one.y[0] == food.y:
            food.active = False
            new_food = Food()
            foods[index] = new_food
            pygame.draw.rect(game_display, WHITE, [new_food.x, new_food.y, 10, 10])
            player_one.grow()
        if player_two.x[0] == food.x and player_two.y[0] == food.y:
            food.active = False
            new_food = Food()
            foods[index] = new_food
            pygame.draw.rect(game_display, WHITE, [new_food.x, new_food.y, 10, 10])
            player_two.grow()

    pygame.display.update()

    # GAME OVER 조건들
    if player_one.x[0] > 800 or player_one.x[0] < 0:
        game_over = True
        break
    elif player_one.y[0] < 0 or player_one.y[0] > 600:
        game_over = True
        break
    if player_two.x[0] > 800 or player_two.x[0] < 0:
        game_over = True
        break
    elif player_two.y[0] < 0 or player_two.y[0] > 600:
        game_over = True
        break

    for i in range(2, player_one.length):
        if player_one.x[0] == player_one.x[i]:
            if player_one.y[0] == player_one.y[i]:
                game_over = True
                break
    if player_one.length == 3:
        if player_one.x[1] == player_one.x[3]:
            if player_one.y[1] == player_one.y[3]:
                game_over = True
                break
    if player_two.length == 3:
        if player_two.x[1] == player_two.x[3]:
            if player_two.y[1] == player_two.y[3]:
                game_over = True
                break



    for i in range(0, player_one.length):
        if player_two.x[0] == player_one.x[i]:
            if player_two.y[0] == player_one.y[i]:
                game_over = True
                break
    for i in range(2, player_two.length):
        if player_two.x[0] == player_two.x[i]:
            if player_two.y[0] == player_two.y[i]:
                game_over = True
                break
    for i in range(0, player_two.length):
        if player_one.x[0] == player_two.x[i]:
            if player_one.y[0] == player_two.y[i]:
                game_over = True
                break

    clock.tick(10)  # 1초에 10번 업데이트

