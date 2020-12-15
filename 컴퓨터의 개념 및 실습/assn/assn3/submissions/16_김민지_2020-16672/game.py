import pygame
pygame.init()
from pygame.constants import QUIT
from pygame.constants import KEYDOWN
from pygame.constants import KEYUP
import random
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
PINK=(255,192,203)
GREEN=(0,255,0)
BLUE=(0,0,255)
LIGHTBLUE=(135,206,235)
YELLOW=(255,212,0)


game_display=pygame.display.set_mode((800,600))
pygame.display.set_caption('DCCP95 Snake Game')
game_over=False

clock=pygame.time.Clock()


class Player:
    x=600
    y=300
    dx=0
    dy=0
    size=[]
    touch=0

    def __init__(self,display):
        self.display=display
        self.length=0

    def handle_event(self,event):
        if event.type==KEYDOWN:
            
                if event.key==pygame.K_LEFT:
                    self.dx=-10
                    self.dy=0
                elif event.key==pygame.K_RIGHT:
                    self.dx=+10
                    self.dy=0
                elif event.key==pygame.K_UP:
                    self.dy=-10
                    self.dx=0
                elif event.key==pygame.K_DOWN:
                    self.dy=+10
                    self.dx=0  
    def longer(self):
        self.length+=1
        self.size.append(0)

    def tick(self,q):
        speed=1
        if self.length==0:
            pass
        else:
            if self.length!=1:
                for i in range(1,self.length):
                    if q==1 or q==3:
                        if self.dx==10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0]+10,self.size[self.length-i-1][1]]
                        elif self.dy==10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0],self.size[self.length-i-1][1]+10]
                        elif self.dx==-10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0]-10,self.size[self.length-i-1][1]]
                        elif self.dy==-10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0],self.size[self.length-i-1][1]-10]
                    else:
                        self.size[self.length-i]=self.size[self.length-i-1]     
            if q==1 or q==3:
                if self.dx==10:
                    self.size[0]=[self.x+10,self.y]
                elif self.dy==10:
                    self.size[0]=[self.x,self.y+10]
                elif self.dx==-10:
                    self.size[0]=[self.x-10,self.y]
                elif self.dy==-10:
                    self.size[0]=[self.x,self.y-10]
            else:
                self.size[0]=[self.x,self.y]

        if q==1 or q==3:
            speed=2
        self.x+=self.dx*speed
        self.y+=self.dy*speed
        
        

    def tailmoving(self,x,y):
        pygame.draw.rect(self.display,BLUE,[x,y,10,10])
        
    def draw(self):
        pygame.draw.rect(self.display,LIGHTBLUE,[self.x,self.y,10,10])
        if self.length==0:
            pass
        else: 
            for k in range(0,self.length):
                a=self.size[k][0]
                b=self.size[k][1]
                self.tailmoving(a,b)
                if a==self.x and b==self.y:
                    self.touch=1
    def intertouch(self,other):
        for k in range(0,len(other)):
            m=other[k][0]
            n=other[k][1]
            if m==self.x and n==self.y:
                self.touch=1

class Player2:
    x=200
    y=300
    dx=0
    dy=0
    size=[]
    touch=0


    def __init__(self,display):
        self.display=display
        self.length=0

    def handle_event(self,event):
        if event.type==KEYDOWN:
            
                if event.key==pygame.K_a:
                    self.dx=-10
                    self.dy=0
                elif event.key==pygame.K_d:
                    self.dx=+10
                    self.dy=0
                elif event.key==pygame.K_w:
                    self.dy=-10
                    self.dx=0
                elif event.key==pygame.K_s:
                    self.dy=+10
                    self.dx=0  
    def longer(self):
        self.length+=1
        self.size.append(0)

    def tick(self,q):
        speed=1
        if self.length==0:
            pass
        else:
            if self.length!=1:
                for i in range(1,self.length):
                    if q==1 or q==2:
                        if self.dx==10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0]+10,self.size[self.length-i-1][1]]
                        elif self.dy==10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0],self.size[self.length-i-1][1]+10]
                        elif self.dx==-10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0]-10,self.size[self.length-i-1][1]]
                        elif self.dy==-10:
                            self.size[self.length-i]=[self.size[self.length-i-1][0],self.size[self.length-i-1][1]-10]
                    else:
                        self.size[self.length-i]=self.size[self.length-i-1]     
            if q==1 or q==2:
                if self.dx==10:
                    self.size[0]=[self.x+10,self.y]
                elif self.dy==10:
                    self.size[0]=[self.x,self.y+10]
                elif self.dx==-10:
                    self.size[0]=[self.x-10,self.y]
                elif self.dy==-10:
                    self.size[0]=[self.x,self.y-10]
            else:
                self.size[0]=[self.x,self.y]

            
        if q==1 or q==2:
            speed=2
            
        self.x+=self.dx*speed
        self.y+=self.dy*speed
        

    def tailmoving(self,x,y):
        pygame.draw.rect(self.display,RED,[x,y,10,10])
        
    def draw(self):
        pygame.draw.rect(self.display,PINK,[self.x,self.y,10,10])
        if self.length==0:
            pass
        else: 
            for k in range(0,self.length):
                a=self.size[k][0]
                b=self.size[k][1]
                self.tailmoving(a,b)
                if a==self.x and b==self.y:
                    self.touch=1   
    def intertouch(self,other):
        for k in range(0,len(other)):
            m=other[k][0]
            n=other[k][1]
            if m==self.x and n==self.y:
                self.touch=1         
        

class Food:
    active=True
    def __init__(self,display):
        self.x=random.randint(0,79)*10
        self.y=random.randint(0,59)*10
        while True:
            if (self.x==200 and self.y==300) or (self.x==600 and self.y==300):
                self.x=random.randint(0,79)*10
                self.y=random.randint(0,59)*10
            else:
                break
        
        self.display=display

    def draw(self):
        pygame.draw.rect(self.display,YELLOW,[self.x,self.y,10,10])


player=Player(game_display)
player2=Player2(game_display)
foods=[Food(game_display)for _ in range(20)]

while not game_over:
    
    for event in pygame.event.get():
        
        if event.type==QUIT:
            game_over=True
            break
        
        player.handle_event(event)
        player2.handle_event(event)
    
        
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RSHIFT] and keys[pygame.K_LSHIFT]:
        booston=1
    elif keys[pygame.K_LSHIFT]:
        booston=2
    elif keys[pygame.K_RSHIFT]:
        booston=3
    else:
        booston=0
    
    player.tick(booston)
    player2.tick(booston)
    game_display.fill(BLACK)
    player.draw()
    player2.draw()
    player.intertouch(player2.size)
    player2.intertouch(player.size)
    if player.x<0 or player.y<0 or player.x>800 or player.y>600:
        game_over=True
    if player2.x<0 or player2.y<0 or player2.x>800 or player2.y>600:
        game_over=True
    if player.x==player2.x and player.y==player2.y:
        game_over=True

    for food in foods:
        if food.active:
            food.draw()
            if player.x==food.x and player.y==food.y:
                food.active=False
                foods.append(Food(game_display))
                player.longer()
            if player2.x==food.x and player2.y==food.y:
                food.active=False
                foods.append(Food(game_display))
                player2.longer()
        
    pygame.display.update()

    
    if player.touch==1:
        game_over=True
    if player2.touch==1:
        game_over=True


    pygame.display.update()
    clock.tick(10)
    

            