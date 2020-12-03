from pygame.constants import *
import pygame
import random

class Player:
    x, y, dx, dy = 400, 300, 0, 0
    body_pos={}
    body_before_pos={}
    body_trace={}
    body_num=0
    boost_head_path=[]
    def __init__(self,color1,color2):
        self.color1=color1
        self.color2=color2
        self.boost_state=False
    def handle_event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.dx = -block_size
                self.dy = 0
            elif event.key == K_RIGHT:
                self.dx = block_size
                self.dy = 0
            elif event.key == K_UP:
                self.dx = 0
                self.dy = -block_size
            elif event.key == K_DOWN:
                self.dx = 0
                self.dy = block_size
    def tick(self):
        self.x += self.dx
        self.y += self.dy
        self.body_pos[0]=[self.x,self.y]
    def draw(self):
        try:
            for i in range(1,self.body_num+1):
                self.body_pos[i]=[self.body_before_pos[i-1][0],self.body_before_pos[i-1][1]]
                pygame.draw.rect(game_display, self.color2, [self.body_pos[i][0],self.body_pos[i][1],block_size,block_size])
            for i in range(1,self.body_num+1):
                self.body_before_pos[i]=self.body_pos[i]        
        except:
            pygame.draw.rect(game_display, self.color1, [self.x,self.y,block_size,block_size])    
        else: 
            pygame.draw.rect(game_display, self.color1, [self.x,self.y,block_size,block_size])
        self.body_before_pos[0]=[self.x, self.y]
    def elongate(self):
        self.body_num += 1
    def boost(self):
        self.x += 2*self.dx
        self.y += 2*self.dy
        self.body_pos[0]=[self.x,self.y]
        try:
            for i in range(1,self.body_num+1):
                if i==1:
                    if (self.body_before_pos[i-1][0]!=self.body_pos[i-1][0]) and (self.body_before_pos[i-1][1]!=self.body_pos[i-1][1]):
                        self.body_pos[i]=[self.body_before_pos[i-1][0],self.body_pos[i-1][1]]
                    else:
                        self.body_pos[i]=[(self.body_before_pos[i-1][0]+self.body_pos[i-1][0])/2,(self.body_before_pos[i-1][1]+self.body_pos[i-1][1])/2]
                elif i>=2:
                    self.body_pos[i]=self.body_before_pos[i-2]
                pygame.draw.rect(game_display, self.color2, [self.body_pos[i][0],self.body_pos[i][1],block_size,block_size])
            self.body_trace=self.body_before_pos.copy()
            for i in range(1,self.body_num+1):
                self.body_before_pos[i]=self.body_pos[i]        
        except:
            pygame.draw.rect(game_display, self.color1, [self.x,self.y,block_size,block_size])    
        else: 
            pygame.draw.rect(game_display, self.color1, [self.x,self.y,block_size,block_size])
        self.boost_head_path=[(self.body_before_pos[0][0]+self.x)/2,(self.body_before_pos[0][1]+self.y)/2]
        self.body_before_pos[0]=[self.x, self.y]
    def movement(self):
        if self.boost_state==True:
            self.boost()
        else:
            self.tick()
            self.draw()   
        
class Player_other(Player):
    x, y, dx, dy = 0, 0, 0, 0
    body_pos={}
    body_before_pos={}
    body_trace={}
    body_num=0
    boost_head_path=[]
    def __init__(self,color1,color2):
        self.color1=color1
        self.color2=color2
        self.boost_state=False 
    def handle_event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.dx = -block_size
                self.dy = 0
            elif event.key == K_d:
                self.dx = block_size
                self.dy = 0
            elif event.key == K_w:
                self.dx = 0
                self.dy = -block_size
            elif event.key == K_s:
                self.dx = 0
                self.dy = block_size

class Food:
    def __init__(self,color):
        self.color=color
        self.x = random.randint(0,width/block_size-1)*block_size
        self.y = random.randint(0,height/block_size-1)*block_size
        self.active=True
    def draw(self):
        pygame.draw.rect(game_display, self.color, [self.x,self.y,block_size,block_size])

def intake(player,food):
    global food_coordinates
    if player.boost_state==True:
            if (player.boost_head_path[0]==food.x and player.boost_head_path[1]==food.y):
                food.active = False
                food_coordinates.append(Food(Green))
                food_coordinates.remove(food)
                player.elongate()
                if food_coordinates[-1] in list(player.body_before_pos.values()):
                    food_coordinates[-1].active=False
                    food_coordinates.remove(food_coordinates[-1])
                    food_coordinates.append(Food(Green))
                    player.elongate()
    if player.x == food.x and player.y == food.y:
            food.active = False
            food_coordinates.append(Food(Green))
            food_coordinates.remove(food)
            player.elongate()
            if food_coordinates[-1] in list(player.body_before_pos.values()):
                    food_coordinates[-1].active=False
                    food_coordinates.remove(food_coordinates[-1])
                    food_coordinates.append(Food(Green))
                    player.elongate()

def collide(player):
    global gameover
    for item in list(player.body_before_pos.values())[1:]:
        if player.body_before_pos[0]==item :
            gameover=True
    if player.body_num>1:
        compare=list(player.body_trace.values())[::-1]
        if list(player.body_before_pos.values()) == compare:
            gameover=True
    if (player.x<0 or player.x+block_size>width) or (player.y+block_size>height or player.y<0):
        gameover=True

def collide_each_other(player1,player2):
    global gameover
    for item1 in player1.body_before_pos.values():
        for item2 in player2.body_before_pos.values():    
            if player1.body_before_pos[0]==item2 or player2.body_before_pos[0]==item1 or item1==item2:
                gameover=True
    if player1.boost_state==True and player2.boost_state!=True:
        for item2 in player2.body_before_pos.values():
            if player1.boost_head_path==item2 or player1.body_before_pos[0]==item2:
                gameover=True
    if player2.boost_state==True and player1.boost_state!=True:
        for item1 in player1.body_before_pos.values():
            if player2.boost_head_path==item1 or player2.body_before_pos[0]==item1:
                gameover=True
    if player1.boost_state==True and player2.boost_state==True:
        for item1 in player1.body_before_pos.values():
            for item2 in player2.body_before_pos.values():
                if player1.body_before_pos[0]==item2 or player2.body_before_pos[0]==item1 or item1==item2\
                    or player2.boost_head_path==item1 or player1.boost_head_path==item2:
                    gameover=True

#default setting
White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Pink=(255,150,150)
Green=(0,255,0)
Blue=(0,0,255)
SkyBlue=(150,150,255)

width=800
height=600
block_size=10
prey=20

player1=Player(Pink,Red)
player2=Player_other(SkyBlue,Blue)
food_coordinates=[]
for _ in range(prey):
    food_coordinates.append(Food(Green))

pygame.init()
game_display=pygame.display.set_mode((width,height))
pygame.display.set_caption('DCCP129_Snake Game')
clock=pygame.time.Clock()

gameover=False

while not gameover:
    game_display.fill(Black)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameover=True
            break
        if event.type==KEYDOWN:
            if event.key == K_RSHIFT:
                player1.boost_state=True
        if event.type==KEYUP:
            if event.key == K_RSHIFT:
                player1.boost_state=False
        if event.type==KEYDOWN:
            if event.key == K_LSHIFT:
                player2.boost_state=True
        if event.type==KEYUP:
            if event.key == K_LSHIFT:
                player2.boost_state=False
        player1.handle_event(event) 
        player2.handle_event(event)
    player1.movement()
    player2.movement()
    #collision    
    collide_each_other(player1,player2)
    collide(player1)
    collide(player2)
    #food intake
    tmp_foods=food_coordinates.copy()
    for food in tmp_foods:
        intake(player1,food)
        intake(player2,food)
        if food.active:
            food.draw()
    pygame.display.update()
    clock.tick(10) 