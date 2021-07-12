import random
from random import randint
import pygame
from pygame.constants import KEYDOWN, KEYUP, K_DOLLAR, K_DOWN, K_LEFT, K_LSHIFT, K_RIGHT, K_RSHIFT, K_UP, K_a, K_d, K_s, K_w, QUIT

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

class Body():
    block_size=10
    x=-50
    y=-50
    def __init__(self,Display):
        self.display=Display

    def draw(self):
        pygame.draw.rect(self.display,blue,[self.x,self.y,self.block_size,self.block_size])

class Body2():
    block_size=10
    x=-70
    y=-70
    def __init__(self,Display):
        self.display=Display

    def draw(self):
        pygame.draw.rect(self.display,(0,255,255),[self.x,self.y,self.block_size,self.block_size])

class Player():
    block_size=10
    x=400
    y=300
    dx=0
    dy=0
    bodys=[]
    move_type=0
    go=False

    def __init__(self,Display):
        self.display=Display
        self.boost=False
    
    def event_handle(self, event):
        if event.type==KEYDOWN:
            if event.key==K_LEFT:
                self.dx=-10
                self.dy=0
                self.move_type=1
            elif event.key==K_RIGHT:
                self.dx=10
                self.dy=0
                self.move_type=2
            elif event.key==K_UP:
                self.dy=-10
                self.dx=0
                self.move_type=3
            elif event.key==K_DOWN:
                self.dy=10
                self.dx=0
                self.move_type=4

    def event_boost(self,event):
        if event.type==KEYDOWN:
            if event.key==K_RSHIFT:
                self.boost=True
        if event.type==KEYUP:
            if event.key==K_RSHIFT:
                self.boost=False

    def moving(self,event):
        if self.move_type==1:
            if event.type==KEYDOWN:
                if event.key==K_RIGHT: 
                    self.go=True
        if self.move_type==2:
            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    self.go=True
        if self.move_type==3:
            if event.type==KEYDOWN:
                if event.key==K_DOWN:
                    self.go=True
        if self.move_type==4:
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    self.go=True

    def tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self):
        pygame.draw.rect(self.display,white,[self.x,self.y,self.block_size,self.block_size])
    
    def body(self):
        n=len(self.bodys)
        if n==0:
            pass
        elif n==1:
            self.bodys[0].x=self.x
            self.bodys[0].y=self.y 
        else:
            for i in range(n-1):
                self.bodys[n-i-1].x=self.bodys[n-i-2].x
                self.bodys[n-i-1].y=self.bodys[n-i-2].y
            self.bodys[0].x=self.x
            self.bodys[0].y=self.y

class Player2():
    block_size=10
    x=200
    y=300
    dx=0
    dy=0
    bodys=[]
    move_type=0
    go=False

    def __init__(self,Display):
        self.display=Display
        self.boost=False
    
    def event_handle(self, event):
        if event.type==KEYDOWN:
            if event.key==K_a:
                self.dx=-10
                self.dy=0
                self.move_type=1
            elif event.key==K_d:
                self.dx=10
                self.dy=0
                self.move_type=2
            elif event.key==K_w:
                self.dy=-10
                self.dx=0
                self.move_type=3
            elif event.key==K_s:
                self.dy=10
                self.dx=0
                self.move_type=4

    def event_boost(self,event):
        if event.type==KEYDOWN:
            if event.key==K_LSHIFT:
                self.boost=True
        if event.type==KEYUP:
            if event.key==K_LSHIFT:
                self.boost=False

    def moving(self,event):
        if self.move_type==1:
            if event.type==KEYDOWN:
                if event.key==K_d:
                    self.go=True
        if self.move_type==2:
            if event.type==KEYDOWN:
                if event.key==K_a:
                    self.go=True
        if self.move_type==3:
            if event.type==KEYDOWN:
                if event.key==K_s:
                    self.go=True
        if self.move_type==4:
            if event.type==KEYDOWN:
                if event.key==K_w:
                    self.go=True

    def tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self):
        pygame.draw.rect(self.display,red,[self.x,self.y,self.block_size,self.block_size])
    
    def body(self):
        n=len(self.bodys)
        if n==0:
            pass
        elif n==1:
            self.bodys[0].x=self.x
            self.bodys[0].y=self.y 
        else:
            for i in range(n-1):
                self.bodys[n-i-1].x=self.bodys[n-i-2].x
                self.bodys[n-i-1].y=self.bodys[n-i-2].y
            self.bodys[0].x=self.x
            self.bodys[0].y=self.y

class Food():
    block_size=10

    active=True

    def __init__(self,GameDisplay):
        self.x=random.randint(0,79)*self.block_size
        self.y=random.randint(0,59)*self.block_size
        self.display=GameDisplay

    def draw(self):
        pygame.draw.rect(self.display,green,[self.x,self.y,self.block_size,self.block_size])

class game():
    block_size=10
    def __init__(self,x_n,y_n):
        pygame.init()
        self.display=pygame.display.set_mode((self.block_size*x_n,self.block_size*y_n))
        pygame.display.set_caption('DCCP Snake Game')
        self.x_n=x_n
        self.y_n=y_n
        self.clock=pygame.time.Clock()
        self.gameover=False
        self.boost=False

    def play(self,n_foods=20):
        player=Player(self.display)
        player2=Player2(self.display)
        foods=[Food(self.display) for _ in range(n_foods)]

        while not self.gameover:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.gameover=True
                    break

                if len(player.bodys)==1:
                    player.moving(event)
                    if player.go:
                        self.gameover=True
                        break
                if len(player2.bodys)==1:
                    player2.moving(event)
                    if player2.go:
                        self.gameover=True
                        break
                
                player.event_handle(event)
                player2.event_handle(event)
                player.event_boost(event)
                player2.event_boost(event)    
                
            player.body()
            player2.body()
            player.tick()
            player2.tick()
            self.display.fill(black)
            player.draw()
            player2.draw()

            for food in foods:
                if food.active:
                    food.draw()
                if player.x==food.x and player.y==food.y:
                    food.active=False
                    food.x=-500
                    food.y=-500
                    foods.append(Food(self.display))
                    player.bodys.append(Body(self.display))
                if player2.x==food.x and player2.y==food.y:
                    food.active=False
                    food.x=-500
                    food.y=-500
                    foods.append(Food(self.display))
                    player2.bodys.append(Body2(self.display))
                for body in player.bodys:
                    if body.x==food.x and body.y==food.y:
                        food.active=False
                        food.x=-500
                        food.y=-500
                        foods.append(Food(self.display))
                        player.bodys.append(Body(self.display))
                for body in player2.bodys:
                    if body.x==food.x and body.y==food.y:
                        food.active=False
                        food.x=-500
                        food.y=-500
                        foods.append(Food(self.display))
                        player2.bodys.append(Body(self.display))

            for body in player.bodys:
                if body.x==player.x and body.y==player.y:
                    self.gameover=True
                    break
                if body.x==player2.x and body.y==player2.y:
                    self.gameover=True
                    break
            for body in player2.bodys:
                if body.x==player.x and body.y==player.y:
                    self.gameover=True
                    break
                if body.x==player2.x and body.y==player2.y:
                    self.gameover=True
                    break
            if player.x==player2.x and player.y==player2.y:
                self.gameover=True

            if player.boost:
                player.body()
                player.tick()
                self.display.fill(black)
                player.draw()
                player2.draw()
            if player2.boost:
                player2.body()
                player2.tick()
                self.display.fill(black)
                player.draw()
                player2.draw()
#부스트 상태에서 스쳐 지나감 방지
            for food in foods:
                if food.active:
                    food.draw()
                if player.x==food.x and player.y==food.y:
                    food.active=False
                    food.x=-500
                    food.y=-500
                    foods.append(Food(self.display))
                    player.bodys.append(Body(self.display))
                if player2.x==food.x and player2.y==food.y:
                    food.active=False
                    food.x=-500
                    food.y=-500
                    foods.append(Food(self.display))
                    player2.bodys.append(Body2(self.display))
                for body in player.bodys:
                    if body.x==food.x and body.y==food.y:
                        food.active=False
                        food.x=-500
                        food.y=-500
                        foods.append(Food(self.display))
                        player.bodys.append(Body(self.display))
                for body in player2.bodys:
                    if body.x==food.x and body.y==food.y:
                        food.active=False
                        food.x=-500
                        food.y=-500
                        foods.append(Food(self.display))
                        player2.bodys.append(Body(self.display))            

            for body in player.bodys:
                body.draw()
            for body in player2.bodys:
                body.draw()
            pygame.display.update()
#부스트 상태에서 스쳐 지나감 방지
            for body in player.bodys:
                if body.x==player.x and body.y==player.y:
                    self.gameover=True
                    break
                if body.x==player2.x and body.y==player2.y:
                    self.gameover=True
                    break
            for body in player2.bodys:
                if body.x==player.x and body.y==player.y:
                    self.gameover=True
                    break
                if body.x==player2.x and body.y==player2.y:
                    self.gameover=True
                    break
            if player.x==player2.x and player.y==player2.y:
                self.gameover=True

            if player.x<0 or player.x>self.x_n*self.block_size or player.y<0 or player.y>self.y_n*self.block_size:
                self.gameover=True
            if player2.x<0 or player2.x>self.x_n*self.block_size or player2.y<0 or player2.y>self.y_n*self.block_size:
                self.gameover=True
            self.clock.tick(10)



game(x_n=80,y_n=60).play(20)