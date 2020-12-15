import pygame 
import random 
from pygame.constants import QUIT
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(250,40,250)
YELLOW=(255, 255,0)
PURPLE=(0, 105, 100)

pygame.init()
game_display=pygame.display.set_mode((800,600))
pygame.display.set_caption('DCCP Snake Game')
game_over=False
clock=pygame.time.Clock()
hascommon=False
class Snake:
    dy=0
    dx=0
    def __init__(self, display):
        self.location=[(0,0)]
        self.display=display
        self.mostrecent=pygame.K_UP
        self.store=pygame.K_UP
        self.event=pygame
        
    def draw(self):
        for a in range(0, len(self.location)):
            if a==0:
                pygame.draw.rect(self.display, RED, [self.location[a][1], self.location[a][0], 10, 10])
            else:
                pygame.draw.rect(self.display, WHITE, [self.location[a][1], self.location[a][0], 10, 10])
    
    def move(self, event ):
        cur_head = self.location[0]
        y, x = cur_head
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RSHIFT:
                self.store=pygame.K_RSHIFT
                if self.mostrecent==pygame.K_UP:
                    self.dy=-20
                    self.dx=0
                elif self.mostrecent==pygame.K_DOWN:
                    self.dy=20
                    self.dx=0
                elif self.mostrecent==pygame.K_LEFT:
                    self.dy=0
                    self.dx=-20
                elif self.mostrecent==pygame.K_RIGHT:
                    self.dy=0
                    self.dx=20
          

                
            if event.key==pygame.K_UP:
                self.event=event
                self.mostrecent=pygame.K_UP
                self.dy=-10
                self.dx=0
                
            elif event.key==pygame.K_DOWN:
                self.mostrecent=pygame.K_DOWN
                self.event=event
                self.dy=10
                self.dx=0
                
            elif event.key==pygame.K_LEFT:
                self.event=event
                self.mostrecent=pygame.K_LEFT
                self.dy=0
                self.dx=-10
            
            elif event.key==pygame.K_RIGHT:
                self.event=event
                self.mostrecent=pygame.K_RIGHT
                self.dy=0
                self.dx=10
              
    def grow(self):
        last = self.location[-1]
        y, x = last
       
        hascommon=False
        if  self.store==pygame.K_RSHIFT or self.store==pygame.K_UP:
            self.location.append((y + 10, x))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_DOWN:
            self.location.append((y - 10, x))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_LEFT:
            self.location.append((y, x + 10))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_RIGHT:
            self.location.append((y, x - 10))
     
        
                
    def tick(self):
        cur_head = self.location[0]
        y, x = cur_head
           
        self.location = [(y +self.dy, x+self.dx)] + self.location[:-1]
        if self.store==pygame.K_RSHIFT:
            tmp=self.location[1:]
            tmpstore=[]
            for a in tmp:
                tmpstore.append((a[0]+self.dy//2, a[1]+self.dx//2))
            self.location=[self.location[0]]
            self.location.extend(tmpstore)


class Snake2:
    dy=0
    dx=0
    def __init__(self, display):
        self.location=[(100,0)]
        self.display=display
        self.mostrecent=pygame.K_w
        self.store=pygame.K_w
        self.event=pygame
        
    def draw(self):
        for a in range(0, len(self.location)):
            if a==0:
                pygame.draw.rect(self.display, BLUE, [self.location[a][1], self.location[a][0], 10, 10])
            else:
                pygame.draw.rect(self.display, YELLOW, [self.location[a][1], self.location[a][0], 10, 10])
    
    def move(self, event ):
        cur_head = self.location[0]
        y, x = cur_head
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LSHIFT:
                self.store=pygame.K_LSHIFT
                if self.mostrecent==pygame.K_w:
                    self.dy=-20
                    self.dx=0
                elif self.mostrecent==pygame.K_s:
                    self.dy=20
                    self.dx=0
                elif self.mostrecent==pygame.K_a:
                    self.dy=0
                    self.dx=-20
                elif self.mostrecent==pygame.K_d:
                    self.dy=0
                    self.dx=20

            if event.key==pygame.K_w:
                self.event=event
                self.mostrecent=pygame.K_w
                self.dy=-10
                self.dx=0
                
            elif event.key==pygame.K_s:
                self.event=event
                self.mostrecent=pygame.K_s
                self.dy=10
                self.dx=0
                
            elif event.key==pygame.K_a:
                self.event=event
                self.mostrecent=pygame.K_a
                self.dy=0
                self.dx=-10
            
            elif event.key==pygame.K_d:
                self.event=event
                self.mostrecent=pygame.K_d
                self.dy=0
                self.dx=10
              
    def grow(self):
        last = self.location[-1]
        y, x = last
       
        hascommon=False
        if  self.store==pygame.K_LSHIFT or self.store==pygame.K_w:
            self.location.append((y + 10, x))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_s:
            self.location.append((y - 10, x))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_a:
            self.location.append((y, x + 10))
        elif self.store==pygame.K_RSHIFT or self.store==pygame.K_d:
            self.location.append((y, x - 10))
     
        
                
    def tick(self):
        cur_head = self.location[0]
        y, x = cur_head
           
        self.location = [(y +self.dy, x+self.dx)] + self.location[:-1]
        if self.store==pygame.K_LSHIFT:
            tmp=self.location[1:]
            tmpstore=[]
            for a in tmp:
                tmpstore.append((a[0]+self.dy//2, a[1]+self.dx//2))
            self.location=[self.location[0]]
            self.location.extend(tmpstore)

        



class Food:
    active=True
    def __init__(self, display):
        self.x=random.randint(0, 79)*10
        self.y=random.randint(0, 59)*10
        self.display=display
    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y,10,10])


class Food2:
    active=True
    def __init__(self, display):
        self.x=random.randint(0, 79)*10
        self.y=random.randint(0, 59)*10
        self.display=display
    def draw(self):
        pygame.draw.rect(self.display, PURPLE, [self.x, self.y,10,10])






snake=Snake(game_display)
snake2=Snake2(game_display)
foods=[Food(game_display) for _ in range(20)]
foods2=[Food2(game_display) for _ in range(20)]

while not game_over:
    clock.tick(10)
   
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
            break
       
               
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_RSHIFT:

                snake.store=event.key 
        
                snake.move(event)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RSHIFT:
                snake.move(snake.event)
            if event.key==pygame.K_LSHIFT:
                snake2.move(snake2.event)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_d or event.key==pygame.K_s or event.key==pygame.K_a or event.key==pygame.K_LSHIFT:

                snake2.store=event.key 
        
                snake2.move(event)
      
            
    snake.tick()
    snake2.tick()
    for _ in range(1, len(snake.location)):
        if snake.location[_]==snake.location[0]:
            game_over=True
            break
    samehas=False
    for _ in range(0, len(snake.location)):
        for o in range(0, len(snake2.location)):
            if snake.location[_]==snake2.location[o]:
                game_over=True
                break
        if game_over:
            break
       
    for _ in range(1, len(snake2.location)):
        if snake2.location[_]==snake2.location[0]:
            game_over=True
            break

    for _ in range(0, len(snake2.location)):
        for o in range(0, len(snake.location)):
            if snake2.location[_]==snake.location[o]:
                game_over=True
                break
        if game_over:
            break

    game_display.fill(BLACK)
    snake.draw()
    snake2.draw()
    for food in foods:
        
        if food.active:
            food.draw()
            exist=False
            for a in snake.location:
                if a[1]==food.x and a[0]==food.y:
                    exist=True
                    break
            if exist:
                food.active=False
                snake.grow()
                
     
                if game_over:
                    break
                foods.append(Food(game_display))
    for food in foods2:
        
        if food.active:
            food.draw()
            exist=False
            for a in snake2.location:
                if a[1]==food.x and a[0]==food.y:
                    exist=True
                    break
            if exist:
                food.active=False
                snake2.grow()
                
     
                if game_over:
                    break
                foods.append(Food2(game_display))
    for a in snake.location:
        if a[1]>=800 or a[0]>=600 or a[1]<0 or a[0]<0:
            game_over=True
            break
    for a in snake2.location:
        if a[1]>=800 or a[0]>=600 or a[1]<0 or a[0]<0:
            game_over=True
            break
    pygame.display.update()
    clock.tick(10)
    
    