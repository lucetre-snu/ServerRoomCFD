import random
import pygame as p

p.init()

game_display = p.display.set_mode((800,600))
p.display.set_caption("DCCP Snake Game")
clock = p.time.Clock()

class Player:
    x = 0
    y = 0
    dx = 0
    dy = 0
    mx = 0
    my = 0
    nx = 0
    ny = 0
    body = 0
    body_state = []
    num = 0
    def __init__(self, display):
        self.display = display
        

    def handle_event(self, event):
        if self.num == 1:
            if event.type == p.KEYDOWN:
                self.speed = 10
                if event.key == p.K_a:
                    self.dx = -10
                    self.dy = 0
                elif event.key == p.K_d:
                    self.dx = +10
                    self.dy = 0
                elif event.key == p.K_w:
                    self.dx = 0
                    self.dy = -10
                elif event.key == p.K_s:
                    self.dx = 0
                    self.dy = +10
        elif self.num == 2:
            if event.type == p.KEYDOWN:
                self.speed = 10
                if event.key == p.K_LEFT:
                    self.dx = -10
                    self.dy = 0
                elif event.key == p.K_RIGHT:
                    self.dx = +10
                    self.dy = 0
                elif event.key == p.K_UP:
                    self.dx = 0
                    self.dy = -10
                elif event.key == p.K_DOWN:
                    self.dx = 0
                    self.dy = +10            

    def Boost(self, event):
        if event.type == p.KEYDOWN:
            if self.num == 1:
                if event.key == p.K_LSHIFT:
                    if self.dx == 20 or self.dx == -20:
                        pass
                    else:
                        self.dx = 2*self.dx
                    if self.dy == 20 or self.dy == -20:
                        pass
                    else:
                        self.dy = 2*self.dy
            elif self.num == 2:
                if event.key == p.K_RSHIFT:
                    if self.dx == 20 or self.dx == -20:
                        pass
                    else:
                        self.dx = 2*self.dx
                    if self.dy == 20 or self.dy == -20:
                        pass
                    else:
                        self.dy = 2*self.dy
        elif event.type == p.KEYUP:
            if self.num == 1:
                if event.key == p.K_LSHIFT:
                    if self.dx == 20 or self.dx == -20:
                        self.dx = self.dx/2
                    if self.dy == 20 or self.dy == -20:
                        self.dy = self.dy/2
            elif self.num == 2:
                if event.key == p.K_RSHIFT:
                    if self.dx == 20 or self.dx == -20:
                        self.dx = self.dx/2
                    if self.dy == 20 or self.dy == -20:
                        self.dy = self.dy/2

    def tick(self):
        if self.dx == 20 or self.dx == -20 or self.dy == 20 or self.dy == -20:
            self.body_state.append([self.x, self.y])
            self.x += self.dx
            self.y += self.dy
            self.mx = (self.x+self.body_state[-1][0])/2
            self.my = (self.y+self.body_state[-1][1])/2
            for i in range(self.body):
                self.nx = self.body_state[-i-1][0]
                self.ny = self.body_state[-i-1][1]
                self.body_state[-i-1][0] = self.mx
                self.body_state[-i-1][1] = self.my
                self.mx = self.nx
                self.my = self.ny
                    
        else:
            self.body_state.append([self.x, self.y])
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        self.tick()
        if self.num == 1:
            p.draw.rect(self.display, Red_White, [self.x, self.y, 10, 10])
            for i in range(self.body):
                if self.dx == 10 or self.dx == 20:
                    p.draw.rect(self.display, Red, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dx == -10 or self.dx == -20:
                    p.draw.rect(self.display, Red, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dy == -10 or self.dy == -20:
                    p.draw.rect(self.display, Red, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dy == 10 or self.dy == 20:
                    p.draw.rect(self.display, Red, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
        elif self.num == 2:
            p.draw.rect(self.display, Blue_White, [self.x, self.y, 10, 10])
            for i in range(self.body):
                if self.dx == 10 or self.dx == 20:
                    p.draw.rect(self.display, Blue, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dx == -10 or self.dx == -20:
                    p.draw.rect(self.display, Blue, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dy == -10 or self.dy == -20:
                    p.draw.rect(self.display, Blue, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])
                elif self.dy == 10 or self.dy == 20:
                    p.draw.rect(self.display, Blue, [self.body_state[-1-i][0], self.body_state[-1-i][1], 10, 10])         

class Food:
    active = True
    def __init__(self, display):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10
        self.display = display

    def draw(self):
        p.draw.rect(self.display, Green, [self.x, self.y, 10 ,10])
game_over = False

player1 = Player(game_display)
player2 = Player(game_display)
player1.num = 1
player1.x = 300
player1.y = 200
player2.num = 2
player2.x = 500
player2.y = 400
player1.body_state = []
player2.body_state = []


foods = [Food(game_display) for _ in range(20)]

Red_White = (255, 210, 210)
Blue_White = (210, 210, 255)
Black = (0,0,0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0,0,255)


while not game_over:
    for event in p.event.get():
        if event.type == p.QUIT:
            game_over = True
            break
        player1.handle_event(event)
        player2.handle_event(event)
    player1.Boost(event)
    player2.Boost(event)
    game_display.fill(Black)
    player1.draw()
    player2.draw()

    if player1.x >= 800 or player1.x < 0:
        game_over = True
    if player1.y >= 600 or player1.y < 0:
        game_over = True
    if player2.x >= 800 or player2.x < 0:
        game_over = True
    if player2.y >= 600 or player2.y < 0:
        game_over = True
    
    if player2.body == 0:
        if player1.x == player2.x and player1.y == player2.y:
            game_over = True
    else:
        for u in range(player2.body):
            if player1.x == player2.body_state[-1-u][0] and player1.y == player2.body_state[-1-u][1]:
                game_over = True

    if player1.body == 0:
        if player1.x == player2.x and player1.y == player2.y:
            game_over = True
    else:
        for k in range(player1.body):
            if player2.x == player1.body_state[-1-k][0] and player2.y == player1.body_state[-1-k][1]:
                game_over = True

    if player2.body == 0:
        pass
    else:
        for u in range(player2.body):
            if player2.x == player2.body_state[-2-u][0] and player2.y == player2.body_state[-2-u][1]:
                game_over = True
                break
    if player1.body == 0:
        pass
    else:
        for k in range(player1.body):
            if player1.x == player1.body_state[-2-k][0] and player1.y == player1.body_state[-2-k][1]:
                game_over = True
                break

    for k in range(player1.body):
        for u in range(player2.body):
            if player2.body_state[-1-u][0] == player1.body_state[-1-k][0] and player2.body_state[-1-u][1] == player1.body_state[-1-k][1]:
                game_over = True
                break        


    for food in foods:
        if food.active:
           food.draw()
        for k in range(player1.body+1):
            if player1.x == food.x and player1.y == food.y:
                food.x = random.randint(0, 79)*10
                food.y = random.randint(0, 59)*10 
                player1.body += 1
                food.draw()
            elif player1.body_state[-1-k][0] == food.x and player1.body_state[-1-k][1] == food.y:
                food.x = random.randint(0, 79)*10
                food.y = random.randint(0, 59)*10 
                player1.body += 1
                food.draw()

        for k in range(player2.body+1):
            if player2.x == food.x and player2.y == food.y:
                food.x = random.randint(0, 79)*10
                food.y = random.randint(0, 59)*10 
                player2.body += 1
                food.draw()
            elif player2.body_state[-1-k][0] == food.x and player2.body_state[-1-k][1] == food.y:
                food.x = random.randint(0, 79)*10
                food.y = random.randint(0, 59)*10 
                player2.body += 1
                food.draw()
        
    p.display.update()

    clock.tick(10)
    

    