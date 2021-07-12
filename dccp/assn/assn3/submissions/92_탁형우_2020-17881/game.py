import pygame
import random


class Player1:
    x=600
    y=300
    dx=0
    dy=0
    boost=False
    direction=0
    headcount=[]
    signal=0
    foodcount=0

    def __init__(self,display):
        self.display=screen

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx=-10
                self.dy=0
            if event.key == pygame.K_RIGHT:
                self.dx=10
                self.dy=0
            if event.key == pygame.K_UP:
                self.dy=-10
                self.dx=0
            if event.key == pygame.K_DOWN:
                self.dy=10
                self.dx=0

            elif event.key == pygame.K_RSHIFT and self.boost== False:
                self.boost=True
            elif event.key == pygame.K_RSHIFT and self.boost== True:
                self.boost=False   

    def drawing(self):
        pygame.draw.rect(self.display,'red',[self.x,self.y,10,10])
        self.headcount.append([self.x,self.y,10,10])
        self.signal=self.signal+1
        if self.foodcount!=0:
            for i in range(0,self.foodcount):
                pygame.draw.rect(self.display,'yellow',self.headcount[self.signal-i-2])


    def tick(self):
        if self.boost==False:
            self.x += self.dx
            self.y += self.dy
        elif self.boost==True:
            self.x += 2*self.dx
            self.y += 2*self.dy
class Player2:
    x=200
    y=300
    dx=0
    dy=0
    boost=False
    direction=0
    headcount=[]
    signal=0
    foodcount=0

    def __init__(self,display):
        self.display=screen

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx=-10
                self.dy=0
            if event.key == pygame.K_d:
                self.dx=10
                self.dy=0
            if event.key == pygame.K_w:
                self.dy=-10
                self.dx=0
            if event.key == pygame.K_s:
                self.dy=10
                self.dx=0

            elif event.key == pygame.K_LSHIFT and self.boost== False:
                self.boost=True
            elif event.key == pygame.K_LSHIFT and self.boost== True:
                self.boost=False   

    def drawing(self):
        pygame.draw.rect(self.display,'blue',[self.x,self.y,10,10])
        self.headcount.append([self.x,self.y,10,10])
        self.signal=self.signal+1
        if self.foodcount!=0:
            for i in range(0,self.foodcount):
                pygame.draw.rect(self.display,'green',self.headcount[self.signal-i-2])

    def tick(self):
        if self.boost==False:
            self.x += self.dx
            self.y += self.dy
        elif self.boost==True:
            self.x += 2*self.dx
            self.y += 2*self.dy

class Food:
    active= True
    def __init__(self,display):
        self.x =  random.randint(0,79)*10
        self.y =  random.randint(0,59)*10
        self.display = screen
    def drawing(self):
        pygame.draw.rect(self.display,'white',[self.x,self.y,10,10])

pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

run=True

player1 = Player1(screen)
player2 = Player2(screen)
foods = [Food(screen)for i in range (0,20)]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            break
        player1.handle_event(event)
        player2.handle_event(event)

    player1.tick()
    player2.tick()

    screen.fill('black')
    player1.drawing()
    player2.drawing()

    if player1.foodcount>=1:
        for q in range(1,player1.foodcount+1):      #1머리 1몸통
            if player1.headcount[player1.signal-1] == player1.headcount[player1.signal-q-2]:
                run = False    
    if player2.foodcount>=1:
        for q in range(1,player2.foodcount+1):      #2머리 2몸통
            if player2.headcount[player2.signal-1] == player2.headcount[player2.signal-q-2]:
                run = False   
    if player1.foodcount!=0 and player2.foodcount!=0:
        for q in range(1,player2.foodcount+1):          #1머리 2몸통
            if player1.headcount[player1.signal-1] == player2.headcount[player2.signal-q-2]:
                run = False   
        for q in range(1,player2.foodcount+1):          #2머리 1몸통
            if player2.headcount[player2.signal-1] == player1.headcount[player1.signal-q-2]:
                run = False  

    for k in range(len(foods)):
        if foods[k].active==True:
            foods[k].drawing()        
        if (player1.x,player1.y) == (foods[k].x, foods[k].y):
            player1.foodcount=player1.foodcount+1       # 점수상승!  
            foods[k].x=random.randint(0,79)*10
            foods[k].y= random.randint(0,59)*10
        if (player2.x,player2.y) == (foods[k].x, foods[k].y):
            player2.foodcount=player2.foodcount+1       # 점수상승!  
            foods[k].x=random.randint(0,79)*10
            foods[k].y= random.randint(0,59)*10

    pygame.display.update()

    if player1.x>800 or player1.x<0 or player1.y>600 or player1.y<0:
        run=False
    if player2.x>800 or player2.x<0 or player2.y>600 or player2.y<0:
        run=False
    clock.tick(10)