import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 221)
YELLOW = (255, 228, 0)

# set values
game_name = 'DCCP Snake Game 2016-10621 김무승'
row_num = 80
col_num = 60
food_num = 20
block_size = 10
tick_val = 10
speed_var = 10
player1_initial_point = (60, 30)
player2_initial_point = (20, 30)
background_color = BLACK
player1_headcolor = RED
player1_bodycolor = BLUE
player2_headcolor = PINK
player2_bodycolor = YELLOW
food_color = GREEN

pygame.init()

count1 = 0
count2 = 0
display_size = (row_num * block_size , col_num * block_size)
game_display = pygame.display.set_mode(display_size)
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()
x_pos_his = []
y_pos_his = []
x2_pos_his = []
y2_pos_his = []

game_over = False


class Player:
    dx = 0
    dy = 0

    def __init__(self, display, x, y):
        self.x = x
        self.y = y
        self.display = display

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.dx != speed_var:
                    self.dx = -speed_var
                    self.dy = 0
            elif event.key == pygame.K_RIGHT:
                if self.dx != -speed_var:
                    self.dx = speed_var
                    self.dy = 0
            elif event.key == pygame.K_UP:
                if self.dy != speed_var:
                    self.dx = 0
                    self.dy = -speed_var
            elif event.key == pygame.K_DOWN:
                if self.dy != -speed_var:
                    self.dx = 0
                    self.dy = speed_var

    def tick(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                self.x += 2*self.dx
                self.y += 2*self.dy
            else:
                self.x += self.dx
                self.y += self.dy
        else:
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        pygame.draw.rect(self.display, player1_headcolor, [self.x, self.y, block_size, block_size])
    
    def drawbody(self):
        pygame.draw.rect(self.display, player1_bodycolor, [x_pos_his[-(i+2)], y_pos_his[-(i+2)], block_size, block_size])

    def handle_event2(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.dx != speed_var:
                    self.dx = -speed_var
                    self.dy = 0
            elif event.key == pygame.K_d:
                if self.dx != -speed_var:
                    self.dx = speed_var
                    self.dy = 0
            elif event.key == pygame.K_w:
                if self.dy != speed_var:
                    self.dx = 0
                    self.dy = -speed_var
            elif event.key == pygame.K_s:
                if self.dy != -speed_var:
                    self.dx = 0
                    self.dy = speed_var

    def tick2(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.x += 2*self.dx
                self.y += 2*self.dy
            else:
                self.x += self.dx
                self.y += self.dy
        else:
            self.x += self.dx
            self.y += self.dy

    def draw2(self):
        pygame.draw.rect(self.display, player2_headcolor, [self.x, self.y, block_size, block_size])
    
    def drawbody2(self):
        pygame.draw.rect(self.display, player2_bodycolor, [x2_pos_his[-(i+2)], y2_pos_his[-(i+2)], block_size, block_size])


class Food:
    active = True
    def __init__(self, display):
        self.display = display
        self.x = random.randint(0,(display_size[0]/10)-1) * block_size
        self.y = random.randint(0,(display_size[1]/10)-1) * block_size

    def draw(self):
        pygame.draw.rect(self.display, food_color, [self.x, self.y, block_size, block_size])

player = Player(game_display, player1_initial_point[0] * block_size, player1_initial_point[1] * block_size)
player2 = Player(game_display, player2_initial_point[0] * block_size, player2_initial_point[1] * block_size)
foods = [Food(game_display) for _ in range(food_num)]
        

food_active = [True for _ in range(food_num)]

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        player.handle_event(event)
        player2.handle_event2(event)

    player.tick()
    player2.tick2()
    
    game_display.fill((background_color))
    player.draw()
    player2.draw2()
    x_pos_his.append(player.x)
    y_pos_his.append(player.y)
    x2_pos_his.append(player2.x)
    y2_pos_his.append(player2.y)

    if foods[count1 + count2].active:
        foods[count1 + count2].draw()
    
        
    if player.x == foods[count1 + count2].x and player.y == foods[count1 + count2].y:
        foods[count1 + count2].active = False
        count1 += 1

    if player2.x == foods[count1 + count2].x and player2.y == foods[count1 + count2].y:
        foods[count1 + count2].active = False
        count2 += 1

    if count1 > 0:
        for i in range(count1):
            player.drawbody()
            if (x_pos_his[-(i+2)] == player.x) and (y_pos_his[-(i+2)] == player.y):
                game_over = True
            elif (x_pos_his[-(i+2)] == player2.x) and (y_pos_his[-(i+2)] == player2.y):
                game_over = True

    if count2 > 0:
        for i in range(count2):
            player.drawbody2()
            if (x2_pos_his[-(i+2)] == player2.x) and (y2_pos_his[-(i+2)] == player2.y):
                game_over = True
            elif (x2_pos_his[-(i+2)] == player.x) and (y2_pos_his[-(i+2)] == player.y):
                game_over = True
 
    pygame.display.update()

    food_remains = False

    for food in foods:
        if food.active:
            food_remains = True
    
    if not food_remains:
        game_over = True

    if (player.x < 0) or (player.x > display_size[0]) or (player.y < 0) or (player.y > display_size[1]):
        game_over = True

    if (player2.x < 0) or (player2.x > display_size[0]) or (player2.y < 0) or (player2.y > display_size[1]):
        game_over = True

    clock.tick(tick_val)