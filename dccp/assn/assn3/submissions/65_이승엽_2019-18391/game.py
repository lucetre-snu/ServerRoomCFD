import pygame
import random

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Pink = (155,0 ,0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Skyblue = (0, 0, 155)

#Class 정의
class Player:
    unit = 10
    x = 400
    y = 300
    dx = 0
    dy = 0
    boost = False
    body = []
    temp = []

    def __init__(self, display):
        self.display = display

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = - self.unit
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                self.dx = + self.unit
                self.dy = 0
            elif event.key == pygame.K_UP:
                self.dy = - self.unit
                self.dx = 0
            elif event.key == pygame.K_DOWN:
                self.dy = + self.unit
                self.dx = 0
            elif event.key == pygame.K_RSHIFT:
                self.boost = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.boost = False

    def handle_tick(self):
        if self.boost == True:
            self.x += self.dx
            self.y += self.dy
            self.x += self.dx
            self.y += self.dy
        else:
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        pygame.draw.rect(self.display, (0, 0, 255), [self.x, self.y, 10, 10])
        for block in self.body:
            pygame.draw.rect(self.display, Skyblue, [block[0], block[1], 10, 10])

    def out(self):
        if self.x <= -10 or self.x >= 800:
            return True
        if self.y <= -10 or self.y >= 600:
            return True
    
    def tail(self):
        self.temp = list(self.body)
        if self.boost == False:
            self.body.append([self.x, self.y, self.dx, self.dy])
            self.body.pop(0)
        elif self.boost == True:
            for bnum in range(len(self.body)):
                if bnum == 0:
                    self.body[bnum][0] += self.dx + self.temp[bnum][2]
                    self.body[bnum][1] += self.dy + self.temp[bnum][3]
                    self.body[bnum][2] = self.dx
                    self.body[bnum][3] = self.dy
                else:
                    self.body[bnum][0] += self.temp[bnum][2] + self.temp[bnum-1][2]
                    self.body[bnum][1] += self.temp[bnum][3] + self.temp[bnum-1][3]
                    self.body[bnum][2] = self.temp[bnum-1][2]
                    self.body[bnum][3] = self.temp[bnum-1][3]
        
    def grow(self):
        self.body.append([self.x, self.y, self.dx, self.dy])

    def collision(self):
        for block in self.body:
            if self.x == block[0] and self.y == block[1]:
                return True

class Food:
    active = True
    def __init__(self, display):
        self.display = display
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10

    def draw(self):
        pygame.draw.rect(self.display, Green, [self.x, self.y, 10, 10])

#게임 설정
pygame.init()
game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake game')
clock = pygame.time.Clock()
game_over = False

#오브젝트 생성
player = Player(game_display)
foods = [Food(game_display) for i in range(20)]

#게임실행
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
#player 체크
        player.handle_event(event)
    if player.out():
        game_over = True
    if player.collision():
        game_over = True
    game_display.fill(Black)
    player.draw()

#음식 먹기
    growth = False
    for food in foods:
        if food.active:
            food.draw()
        if (player.x == food.x) and (player.y == food.y):
            food.active = False
            foods.append(Food(game_display))
            growth = True
    if growth:
        player.grow()
    elif not growth:
        player.tail()
    growth = False
    player.handle_tick()

#디스플레이 업데이트(틱)
    pygame.display.update()
    clock.tick(10)