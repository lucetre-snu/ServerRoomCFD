import pygame
import random
from pygame.constants import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RSHIFT, K_a, K_d, K_w, K_s, K_LSHIFT

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DCCP Snake Game")

class Body:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


    def tick(self):
        self.x += self.dx
        self.y += self.dy

class Player:
    def __init__(self, x, y, left, right, up, down):
        self.x = x
        self.dx = 0
        self.y = y
        self.dy = 0
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.body_list = []

    def handle_event(self, event):
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
        self.x+=self.dx
        self.y+=self.dy
        if len(self.body_list)!=0:
            for body in self.body_list:
                body.tick()
            for i in range(len(self.body_list)-1,0, -1):
                self.body_list[i].dx = self.body_list[i-1].dx
                self.body_list[i].dy = self.body_list[i - 1].dy
            self.body_list[0].dx = self.dx
            self.body_list[0].dy = self.dy


    def add_body(self):
        if len(self.body_list)==0:
            self.body_list.append(Body(self.x-self.dx, self.y-self.dy, self.dx, self.dy))
        else:
            self.body_list.append(Body(self.body_list[-1].x-self.body_list[-1].dx, self.body_list[-1].y-self.body_list[-1].dy, self.body_list[-1].dx, self.body_list[-1].dy))


class Food:
    def __init__(self):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10

game_over = False
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 192)
GREEN = (0,255,0)
RED = (255, 0, 0)
LIGHTRED = (192, 0, 0)


player1 = Player(450, 300, K_LEFT, K_RIGHT, K_UP, K_DOWN)
player2 = Player(350, 300, K_a, K_d, K_w, K_s)
foods = [Food() for _ in range(20)]

game_display.fill(BLACK)
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True
            break
        if event.type == KEYDOWN:
            player1.handle_event(event)
            player2.handle_event(event)
    if pygame.key.get_pressed()[K_RSHIFT]:
        player1.tick()
    if pygame.key.get_pressed()[K_LSHIFT]:
        player2.tick()

    player1.tick()
    player2.tick()
    game_display.fill(BLACK)
    if not (0<=player1.x<=790 and 0<=player1.y<=590 and 0<=player2.x<=790 and 0<=player2.y<=590):
        game_over=True
    for i, food in enumerate(foods):
        pygame.draw.rect(game_display, GREEN, [food.x, food.y, 10, 10])
        if player1.x == food.x and player1.y == food.y:
            foods[i]=Food()
            player1.add_body()
        elif player2.x == food.x and player2.y == food.y:
            foods[i]=Food()
            player2.add_body()
    pygame.draw.rect(game_display, RED, [player1.x, player1.y, 10, 10])
    pygame.draw.rect(game_display, BLUE, [player2.x, player2.y, 10, 10])
    for body in player1.body_list:
        pygame.draw.rect(game_display, LIGHTRED, [body.x, body.y, 10, 10])
        if player1.x == body.x and player1.y == body.y:
            game_over=True
        elif player2.x == body.x and player2.y == body.y:
            game_over=True

    for body in player2.body_list:
        pygame.draw.rect(game_display, LIGHTBLUE, [body.x, body.y, 10, 10])
        if player1.x == body.x and player1.y == body.y:
            game_over = True
        elif player2.x == body.x and player2.y == body.y:
            game_over = True
    pygame.display.update()

    clock.tick(10)

