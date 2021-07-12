import pygame
from pygame.constants import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, QUIT, KEYUP,KMOD_SHIFT, K_a, K_w, K_s , K_d
import random


class Player():
    x = 400
    y = 300
    dx = 0
    dy = 0

    x_prev = 0
    y_prev = 0
    tick_used = False

    def __init__(self, display, head_color, body_color):
        self.display = display
        self.body_list = [Body(self.x, self.y)]
        self.head_color = head_color
        self.body_color = body_color
        #self.body_list = []

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.dx = -10
                self.dy = 0
            elif event.key == K_RIGHT:
                self.dx = 10
                self.dy = 0
            elif event.key == K_UP:
                self.dx = 0
                self.dy = -10
            elif event.key == K_DOWN:
                self.dx = 0
                self.dy = 10

    def refresh_body(self):
        # print(len(self.body_list))
        if len(self.body_list) == 1:
            if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                self.body_list[0].x, self.body_list[0].y = self.x, self.y
                self.tick_used = True
            else:
                self.body_list[0].x, self.body_list[0].y = self.x, self.y
                self.tick_used = False


        else:
            if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                for i in range(len(self.body_list)-1, 0, -1):
                    self.body_list[i].x, self.body_list[i].y = self.body_list[i-1].x, self.body_list[i-1].y
                self.tick_used = True

            else:
                #print(self.x, self.x_prev)
                for i in range(len(self.body_list)-1, 0, -1):
                    self.body_list[i].x, self.body_list[i].y = self.body_list[i-1].x, self.body_list[i-1].y
                self.tick_used = False




                # print("body", i-1, self.body_list[i-1].x, self.body_list[i-1].y)
                # print("body", i, self.body_list[i].x,self.body_list[i].y)
                # print()
        self.body_list[0].x, self.body_list[0].y = self.x, self.y
        # print(self.body_list[0].x, self.body_list[0].y)



    def tick(self):
        if len(self.body_list) == 1:
            if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                self.x += self.dx
                self.y += self.dy
            else:
                self.x += self.dx
                self.y += self.dy
        else:
            if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                self.x_prev = self.body_list[1].x
                self.y_prev = self.body_list[1].y
                self.x += self.dx
                self.y += self.dy
                # print("self.body_list[1].x", self.body_list[1].x)
            else:
                self.x_prev = self.body_list[1].x
                self.y_prev = self.body_list[1].y
                self.x += self.dx
                self.y += self.dy

    def draw(self):
        # print("head", self.x, self.y)
        for i in range(len(self.body_list)):
            pygame.draw.rect(self.display, self.body_color, [self.body_list[i].x, self.body_list[i].y, 10, 10])
            pygame.draw.rect(self.display, self.head_color, [self.body_list[0].x, self.body_list[0].y, 10, 10])

            # print(i, self.body_list[i].x, self.body_list[i].y)
        # print()


    def check_pos(self):
        x, y = pygame.display.get_window_size()
        # print(self.x, self.y)
        if not(-11 < self.x < x+1 and -11 < self.y < y+1):
            # self.body_list.pop()
            # for i in range(len(self.body_list)):
            #     pygame.draw.rect(self.display, WHITE, [self.body_list[i].x, self.body_list[i].y, 10, 10])
            return True
        return False

    def collision(self):
        # print(self.x_prev, self.y_prev)
        # print(self.x, self.y)
        # print()
        if len(self.body_list) == 2:
            if self.x_prev == self.x and self.y_prev == self.y:
                return True
        for i in range(1, len(self.body_list)):
            # print(self.body_list[i].x, self.body_list[0].x, self.body_list[i].y, self.body_list[0].y)
            if(self.body_list[i].x == self.body_list[0].x and self.body_list[i].y == self.body_list[0].y):
                return True
        return False

class Body():
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Food():
    active = True

    def __init__(self, display):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 79) * 10
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])

class Player2(Player):
    x = 200
    y = 100
    dx = 0
    dy = 0

    x_prev = 0
    y_prev = 0
    tick_used = False

    def __init__(self,display, head_color, body_color):
        super().__init__(display, head_color, body_color)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.dx = -10
                self.dy = 0
            elif event.key == K_d:
                self.dx = 10
                self.dy = 0
            elif event.key == K_w:
                self.dx = 0
                self.dy = -10
            elif event.key == K_s:
                self.dx = 0
                self.dy = 10
    def refresh_body(self):
        # print(len(self.body_list))
        if len(self.body_list) == 1:
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                self.body_list[0].x, self.body_list[0].y = self.x, self.y
                self.tick_used = True
            else:
                self.body_list[0].x, self.body_list[0].y = self.x, self.y
                self.tick_used = False

        else:
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                for i in range(len(self.body_list)-1, 0, -1):
                    self.body_list[i].x, self.body_list[i].y = self.body_list[i-1].x, self.body_list[i-1].y
                self.tick_used = True

            else:
                #print(self.x, self.x_prev)
                for i in range(len(self.body_list)-1, 0, -1):
                    self.body_list[i].x, self.body_list[i].y = self.body_list[i-1].x, self.body_list[i-1].y
                self.tick_used = False




                # print("body", i-1, self.body_list[i-1].x, self.body_list[i-1].y)
                # print("body", i, self.body_list[i].x,self.body_list[i].y)
                # print()
        self.body_list[0].x, self.body_list[0].y = self.x, self.y
        # print(self.body_list[0].x, self.body_list[0].y)



    def tick(self):
        if len(self.body_list) == 1:
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                self.x += self.dx
                self.y += self.dy
            else:
                self.x += self.dx
                self.y += self.dy
        else:
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                self.x_prev = self.body_list[1].x
                self.y_prev = self.body_list[1].y
                self.x += self.dx
                self.y += self.dy
                # print("self.body_list[1].x", self.body_list[1].x)
            else:
                self.x_prev = self.body_list[1].x
                self.y_prev = self.body_list[1].y
                self.x += self.dx
                self.y += self.dy


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

pygame.init()

game_display = pygame.display.set_mode((800, 800))
pygame.display.set_caption('DCCP Snake Game ')
clock = pygame.time.Clock()

game_over = False

player = Player(game_display, RED, WHITE)
player2 = Player2(game_display, BLUE, PURPLE)
foods = [Food(game_display) for _ in range(20)]

while not game_over:


    for event in pygame.event.get():
        # for quitting
        if event.type == QUIT:
            game_over = True
            break

        # send event to player
        player.handle_event(event)
        player2.handle_event(event)
    player2.tick()

    player.tick()
    game_display.fill(BLACK)



    player.draw()
    player2.draw()
    # print("1", player.x, player.y)
    for food in foods:
        if food.active:
            food.draw()
        for i in range(len(player.body_list)):
            if player.body_list[i].x == food.x and player.body_list[i].y == food.y:
                food.active = False
                player.body_list.append(Body(player.body_list[len(player.body_list)-1].x, player.body_list[len(player.body_list)-1].y))
        for i in range(len(player2.body_list)):
            if player2.body_list[i].x == food.x and player2.body_list[i].y == food.y:
                food.active = False
                player2.body_list.append(Body(player2.body_list[len(player2.body_list)-1].x, player2.body_list[len(player2.body_list)-1].y))

    player2.refresh_body()

    player.refresh_body()
    # print(player.x, player.y)

    if player.collision() or player2.collision():
        game_over = True

    pygame.display.update()



    food_remains = False
    for i, food in enumerate(foods):
        if food.active:
            food_remains = True
        if not food.active:  # remove eaten one and create new one
            foods.pop(i)
            foods.insert(i, Food(game_display))

    if player.check_pos() or player2.check_pos():
        game_over = True

    if not food_remains:
        game_over = True

    for i in range(len(player.body_list)):
        for j in range(len(player2.body_list)):
            if player.body_list[i].x == player2.body_list[j].x and player.body_list[i].y == player2.body_list[j].y:
                game_over = True
                break

    if not (player.tick_used or player2.tick_used) :
        clock.tick(10)
    else:
        clock.tick(20)


