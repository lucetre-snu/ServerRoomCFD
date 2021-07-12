import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 153)

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game(2020-13619 이민영)')
clock = pygame.time.Clock()

class Player:
    dx = 0
    dy = 0
    y = 0
    flag = True
    Flag = False

    def __init__(self, display, up, down, left, right, shift, meori, momtong, startingx):
        self.display = display
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.shift = shift
        self.meori = meori
        self.momtong = momtong
        self.prex = []
        self.prey = []
        self.tempx = 0
        self.tempy = 0
        self.x = startingx
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.shift:
                if self.flag == True:
                    self.flag = False
                else:
                    self.flag = True
            if event.key == self.left:
                self.dx = -10
                self.dy = 0
            elif event.key == self.right:
                self.dx = 10
                self.dy = 0
            elif event.key == self.up:
                self.dy = -10
                self.dx = 0
            elif event.key == self.down:
                self.dy = 10  
                self.dx = 0
        

    def tick(self):
        self.x += self.dx
        self.y += self.dy
        self.prex += [self.tempx]
        self.prey += [self.tempy]
        self.tempx = self.x
        self.tempy = self.y
        for food in foods:
            if self.x == food.x and self.y == food.y:
                self.Flag = True
                if food.active == False:
                    pass
                else:
                    food.active = False
                    foods.append(Food(game_display))
        if self.Flag == False:
            del self.prex[0]
            del self.prey[0]
        self.Flag = False
        if self.flag == False:
            self.x += self.dx
            self.y += self.dy
            self.prex += [self.tempx]
            self.prey += [self.tempy]
            self.tempx = self.x
            self.tempy = self.y
            for food in foods:
                if self.x == food.x and self.y == food.y:
                    self.Flag = True
                    if food.active == False:
                        pass
                    else:
                        food.active = False
                        foods.append(Food(game_display))
            if self.Flag == False:
                del self.prex[0]
                del self.prey[0]
            self.Flag = False

    def draw(self):
        self.coordinates = []
        pygame.draw.rect(self.display, self.meori, [self.x, self.y, 10, 10])
        self.coordinates.append([self.x, self.y])
        for i in range(len(self.prex)-1, -1, -1):
            pygame.draw.rect(self.display, self.momtong, [self.prex[i], self.prey[i], 10, 10])
            self.coordinates.append([self.prex[i], self.prey[i]])

class Food:

    active = True

    def __init__(self, display):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])

player1 = Player(game_display, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT, RED, WHITE, 790)
player2 = Player(game_display, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, BLUE, PINK, 0)
foods = [Food(game_display) for _ in range(20)]

game_over = False

def play():
    player1.tick()
    player2.tick()
    game_display.fill(BLACK)
    player1.draw()
    player2.draw()
    for food in foods:
        if food.active:
            pygame.draw.rect(game_display, GREEN, [food.x, food.y, 10, 10])
    for food in foods:
        if food.active == False:
            del food
    pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        player1.handle_event(event)
        player2.handle_event(event)
    play()
    if player1.x < 0 or player1.x >= 800 or player1.y < 0 or player1.y >= 600 or player2.x < 0 or player2.x >= 800 or player2.y < 0 or player2.y >= 600:
        game_over = True
    for i in range(1, len(player1.coordinates)):
        if player1.coordinates[0] == player1.coordinates[i]:
            print(player1.coordinates[0], player1.coordinates[i], i)
            game_over = True
    for i in range(1, len(player2.coordinates)):
        if player2.coordinates[0] == player2.coordinates[i]:
            game_over = True
    for element1 in player1.coordinates:
        for element2 in player2.coordinates:
            if element1 == element2:
                game_over = True
    clock.tick(5)