import pygame
import random
import time

pygame.init()

X_AXIS = 80
Y_AXIS = 60
BLOCK_SIZE = 10

X1_DEFAULT = 600
Y1_DEFAULT = 300

X2_DEFAULT = 200
Y2_DEFAULT = 300

game_display = pygame.display.set_mode((X_AXIS * BLOCK_SIZE,Y_AXIS * BLOCK_SIZE))
pygame.display.set_caption("DCCP Snake Game")
#clock : 일정기간동안 기다린다
clock = pygame.time.Clock()

#event type 에는 keydown, textinput, keyup, quit,  mousemotion등 있음
#서로 다른 type에 대해서 다른 행동 지정 가능
WHITE = (255,255,255)
GRAY = (180,180,180)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255,153,153)

GREEN = (0,255,0)
BLUE = (0,0,255)
GRAYBLUE = (102,102,153)



class Player1:
    x = X1_DEFAULT
    y = Y1_DEFAULT
    dx = 0
    dy = 0

    bodylist = [] #[head, body1, body2, body3, ....]
    tail = []
    boostOn = False
    direction = 0

    def __init__(self, display):
        self.display = display
        self.bodylist.append([self.x,self.y])

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            #event.key : 실제로 눌려진 키
            if event.key == pygame.K_RSHIFT:
                self.boostOn = True
                #움직임 늦게 반응하는것 조정
                self.dx = self.dx *2
                self.dy = self.dy *2

            elif not self.boostOn:
                if event.key == pygame.K_LEFT and self.direction != 2:
                    self.direction = 1
                    self.dx = -BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_RIGHT and self.direction != 1:
                    self.direction = 2
                    self.dx = BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_UP and self.direction != 4:
                    self.direction = 3
                    self.dx = 0
                    self.dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and self.direction != 3:
                    self.direction = 4
                    self.dx = 0
                    self.dy = BLOCK_SIZE
            elif self.boostOn:
                if event.key == pygame.K_LEFT and self.direction != 2:
                    self.direction = 1
                    self.dx = -2*BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_RIGHT and self.direction != 1:
                    self.direction = 2
                    self.dx = 2*BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_UP and self.direction != 4:
                    self.direction = 3
                    self.dx = 0
                    self.dy = -2*BLOCK_SIZE
                elif event.key == pygame.K_DOWN and self.direction != 3:
                    self.direction = 4
                    self.dx = 0
                    self.dy = 2*BLOCK_SIZE      
            
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.boostOn = False
                #움직임 늦게 반응하는것 조정
                self.dx = self.dx //2
                self.dy = self.dy //2


            
            
    def tick(self):
        self.x += self.dx
        self.y += self.dy

        if self.boostOn:
            if len(self.bodylist)==1:
                self.bodylist[0] = [self.x, self.y]
            else:
                self.bodylist[1:] = [[self.x -self.dx//2,self.y -self.dy//2], *self.bodylist[:-2]]
                self.bodylist[0] = [self.x, self.y]
                self.tail = self.bodylist[-1]
            
        else:
            self.bodylist[1:] = self.bodylist[:-1]
            self.bodylist[0] = [self.x, self.y]
            self.tail = self.bodylist[-1]

        return self.bodylist

    def draw(self):
        for i,[x, y] in enumerate(self.bodylist):
            if i==0:
                pygame.draw.rect(self.display,PINK, [x,y,BLOCK_SIZE,BLOCK_SIZE])
            else:
                pygame.draw.rect(self.display,RED, [x,y,BLOCK_SIZE,BLOCK_SIZE])

    def lengthen(self):
        self.bodylist = [*self.bodylist, self.tail]

class Player2:
    x = X2_DEFAULT
    y = Y2_DEFAULT
    dx = 0
    dy = 0

    bodylist = [] #[head, body1, body2, body3, ....]
    tail = []
    boostOn = False
    direction = 0

    def __init__(self, display):
        self.display = display
        self.bodylist.append([self.x,self.y])

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            #event.key : 실제로 눌려진 키
            if event.key == pygame.K_LSHIFT:
                self.boostOn = True
                #움직임 늦게 반응하는것 조정
                self.dx = self.dx *2
                self.dy = self.dy *2

            elif not self.boostOn:
                if event.key == pygame.K_a and self.direction != 2:
                    self.direction = 1
                    self.dx = -BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_d and self.direction != 1:
                    self.direction = 2
                    self.dx = BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_w and self.direction != 4:
                    self.direction = 3
                    self.dx = 0
                    self.dy = -BLOCK_SIZE
                elif event.key == pygame.K_s and self.direction != 3:
                    self.direction = 4
                    self.dx = 0
                    self.dy = BLOCK_SIZE
            elif self.boostOn:
                if event.key == pygame.K_a and self.direction != 2:
                    self.direction = 1
                    self.dx = -2*BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_d and self.direction != 1:
                    self.direction = 2
                    self.dx = 2*BLOCK_SIZE
                    self.dy = 0
                elif event.key == pygame.K_w and self.direction != 4:
                    self.direction = 3
                    self.dx = 0
                    self.dy = -2*BLOCK_SIZE
                elif event.key == pygame.K_s and self.direction != 3:
                    self.direction = 4
                    self.dx = 0
                    self.dy = 2*BLOCK_SIZE        
            
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.boostOn = False
                #움직임 늦게 반응하는것 조정
                self.dx = self.dx //2
                self.dy = self.dy //2

                # if self.boostOn:
                #     self.boostOn = False
                #     #움직임 늦게 반응하는것 조정
                #     self.dx = self.dx//2
                #     self.dy = self.dy//2
                # else:
                #     self.boostOn = True
                #     #움직임 늦게 반응하는것 조정
                #     self.dx = self.dx *2
                #     self.dy = self.dy *2   
        
            
    def tick(self):
        self.x += self.dx
        self.y += self.dy

        if self.boostOn:
            if len(self.bodylist)==1:
                self.bodylist[0] = [self.x, self.y]
            else:
                self.bodylist[1:] = [[self.x -self.dx//2,self.y -self.dy//2], *self.bodylist[:-2]]
                self.bodylist[0] = [self.x, self.y]
                self.tail = self.bodylist[-1]
            
        else:
            self.bodylist[1:] = self.bodylist[:-1]
            self.bodylist[0] = [self.x, self.y]
            self.tail = self.bodylist[-1]

        return self.bodylist

    def draw(self):
        for i,[x, y] in enumerate(self.bodylist):
            if i==0:
                pygame.draw.rect(self.display,GRAYBLUE, [x,y,BLOCK_SIZE,BLOCK_SIZE])
            else:
                pygame.draw.rect(self.display,BLUE, [x,y,BLOCK_SIZE,BLOCK_SIZE])

    def lengthen(self):
        self.bodylist = [*self.bodylist, self.tail]


class Food:
    active = True
    def __init__(self, display):
        self.x = random.randint(0,X_AXIS-1) * BLOCK_SIZE
        self.y = random.randint(0,Y_AXIS-1) * BLOCK_SIZE
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display,GREEN, [self.x,self.y,BLOCK_SIZE,BLOCK_SIZE])

    def redraw(self):
        self.x = random.randint(0,X_AXIS-1) * BLOCK_SIZE
        self.y = random.randint(0,Y_AXIS-1) * BLOCK_SIZE

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (X_AXIS * BLOCK_SIZE/2,Y_AXIS * BLOCK_SIZE/2)
    game_display.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

FOOD_QUANT = 20
player1 = Player1(game_display)
player2 = Player2(game_display)
foods = [Food(game_display) for _ in range(FOOD_QUANT)]

gameover = False
body_pos1 = []
body_pos2 = []

while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
            break
        player1.handle_event(event)
        player2.handle_event(event)
            
        #player 클래스에서 keydown,keyup으로 쉬프트 확인
        
    game_display.fill(BLACK)
    body_pos1 = player1.tick()
    body_pos2 = player2.tick()
    
    
    #음식 먹으면 그 음식 없애기
    ##########
    #먹을 때 body_pos으로 확인
    for food in foods:
        eat1 = False
        eat2 = False
        if food.active:
            food.draw()
        for x1, y1 in body_pos1:
            if x1 == food.x and y1 == food.y:
                eat1 = True
        for x2, y2 in body_pos2:
            if x2 == food.x and y2 == food.y:
                eat2 = True
        if eat1:
            food = food.redraw()
            #지렁이 길이 늘리기
            player1.lengthen()
        if eat2:
            food = food.redraw()
            #지렁이 길이 늘리기
            player2.lengthen()
    
    player1.draw()
    player2.draw()

    redloss = False
    blueloss = False

    #화면 끝에 다다르면 게임 끝
    if player1.x < 0 or player1.x >= X_AXIS * BLOCK_SIZE:
        redloss = True
    if player1.y < 0 or player1.y >= Y_AXIS * BLOCK_SIZE:
        redloss = True
    if player2.x < 0 or player2.x >= X_AXIS * BLOCK_SIZE:
        blueloss = True
    if player2.y < 0 or player2.y >= Y_AXIS * BLOCK_SIZE:
        blueloss = True

    #지렁이 몸통에 닿으면 게임 끝
    for i in body_pos1[1:]:
        if i == body_pos1[0]:
            #1번 패배(red loss)
        
            redloss = True
        elif i == body_pos2[0]:
            #2번 패배
            
            blueloss = True
    
    for i in body_pos2[1:]:
        if i == body_pos1[0]:
            #1번 패배
            
            redloss = True
        elif i == body_pos2[0]:
            #2패배
            blueloss = True

    if redloss and blueloss:
        message_display("DRAW")
        gameover = True
    elif redloss:
        message_display("BLUE WIN!")
        gameover = True
    elif blueloss:
        message_display("RED WIN!")
        gameover = True


    pygame.display.update()
    clock.tick(10) #숫자는 1초에 몇 번 while이 도느냐.






"""
    for i in range(80):
        st = [10*(i-40),-300]
        ed = [10*(i-40), 300]
        pygame.draw.line(game_display,WHITE,st,ed,1)
"""

# game_display.fill((255,255,255)) #R G B value
# #모양 만들기/ (R, G, B), [x,y,width,height]
# pygame.draw.rect(game_display,(0,0,0),[0,300,20,20])

# #집어넣은 내용을 업데이트, 실제로 표시하도록 하기
# pygame.display.update() #모양 만든것도 이거 update해줘야 나타남