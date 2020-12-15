import pygame as p
import random as r

from pygame.constants import KEYDOWN, KEYUP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_UP, QUIT, K_a, K_s, K_d, K_w, K_LSHIFT
p.init()   

game_over=False

game_display=p.display.set_mode((800,600))
p.display.set_caption('assng3 - snake game')
clock=p.time.Clock()

black=(0,0,0)
red=(255,0,0)
redhead=(255, 150, 150)
bluehead=(150, 150, 255)
green=(0,255,0)
blue=(0,0,255)

class Player:
    def __init__(self, starting_point, display, color, bodycolor, left, right, up, down, booster):
        self.x=starting_point[0]
        self.y=starting_point[1]
        self.display=display
        self.color=color
        self.bodycolor=bodycolor
        self.game_over=False
        self.left=left
        self.right=right
        self.up=up
        self.down=down
        self.booster=booster
        self.body=0
        self.dx=0
        self.dy=0
        self.body_list=[]
        self.body_x=0
        self.body_y=0
        self.speed=1
        self.list=[]
        self.food_x=0
        self.food_y=0

    def position(self, event):
    
        if event.key==self.left:
            self.dx=-10*self.speed
            self.dy=0
        elif event.key==self.right:
            self.dx=10*self.speed
            self.dy=0
        elif event.key==self.up:
            self.dy=-10*self.speed
            self.dx=0
        elif event.key==self.down:
            self.dy=10*self.speed
            self.dx=0    
       

    def move(self):
        self.x+=self.dx      
        self.y+=self.dy
        

    def draw(self):
        self.interact()
        self.turn()
        p.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])
        
        if self.body==0:
            pass
        else:
            for i in self.body_list[::-1]:
                p.draw.rect(self.display, self.bodycolor, [self.body_x-i[0], self.body_y-i[1], 10, 10])
                self.body_x-=i[0]
                self.body_y-=i[1]
                if self.body_x==self.x and self.body_y==self.y:
                    self.game_over=True
                
                
        

    def interact(self):
        self.body_x=self.x
        self.body_y=self.y
        if self.speed==1:
            self.body_list.append((self.dx, self.dy))
            if len(self.body_list)>self.body:
                del self.body_list[0]
            
        elif self.speed==2:
            self.body_list.append((int(self.dx/2), int(self.dy/2)))
            self.body_list.append((int(self.dx/2), int(self.dy/2)))            
            while len(self.body_list)>self.body:
                del self.body_list[0]    

    def check(self):
        if not (0<=self.x<800 and 0<=self.y<600):
            return True
        else:
            return False

    def boost(self, event):
        if event.key==self.booster:
            self.speed=2
            self.dx*=self.speed
            self.dy*=self.speed

    def slow(self, event):
        if event.key==self.booster:
            self.speed=1
            self.dx=int(self.dx/2)
            self.dy=int(self.dy/2)

    def body_range(self, player):
        self.body_x=self.x
        self.body_y=self.y
        for i in self.body_list[::-1]:
                self.body_x-=i[0]
                self.body_y-=i[1]
                if self.body_x==player.x and self.body_y==player.y:
                    return True
                if player.speed==2:
                    if self.body_x==player.x and self.body_y==player.y:
                        return True
                    elif self.body_x==player.x-int(player.dx/2) and self.body_y==player.y-int(player.dy/2):
                        return True

    def turn(self):
        self.list.append((self.dx, self.dy))
        while len(self.list)>2:
            del self.list[0]
        if self.body>0:
            if self.list[0][0]==self.list[1][0]==0 and self.list[0][1]==-self.list[1][1]:
                self.game_over=True
            if self.list[0][1]==self.list[1][1]==0 and self.list[0][0]==-self.list[1][0]:
                self.game_over=True
            



    
        

class Food:
    food_list=[]
    for k in range(20):
        food_x=r.randint(0,79)
        food_y=r.randint(0,59)
        food_list.append((10*food_x, 10*food_y))
    count=True
    x=0
    y=0

    def __init__(self, display):
        self.display=display

    def draw(self, player):
        self.count=True
        player.food_x=player.x
        player.food_y=player.y
        for i, (food_x, food_y) in enumerate(self.food_list):
            p.draw.rect(self.display, green, [food_x, food_y, 10, 10])
            if player.speed==2:
                if (player.x==food_x and player.y==food_y) or (player.x-int(player.dx/2)==food_x and player.y-int(player.dy/2)==food_y):
                    player.body+=1
                    while self.count:
                        self.x=10*r.randint(0,79)
                        self.y=10*r.randint(0,59)
                        for k in self.food_list:
                            if k==(self.x, self.y):
                                self.count=True
                                break  
                        else: 
                            self.food_list[i]=(self.x, self.y)
                            self.count=False
            elif player.speed==1:
                if player.x==food_x and player.y==food_y:
                    player.body+=1
                    while self.count:
                        self.x=10*r.randint(0,79)
                        self.y=10*r.randint(0,59)
                        for k in self.food_list:
                            number=0
                            if k==(self.x, self.y):
                                self.count=True
                                break
                            
                      
                            
               
                        else: 
                            self.food_list[i]=(self.x, self.y)
                            self.count=False


                    


def final_check(player, player2):
    if player.game_over or player.check() or player2.game_over or player2.check() or player.body_range(player2) or player2.body_range(player) or (player.x==player2.x and player.y==player2.y):
        return True
    else:
        return False
    
    

player=Player((400, 300), game_display, redhead, red, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RSHIFT)
player2=Player((0,0), game_display, bluehead, blue, K_a, K_d, K_w, K_s, K_LSHIFT)
food=Food(game_display)

while not game_over:
    for event in p.event.get():
        if event.type==QUIT:
            game_over=True
        elif event.type==KEYDOWN:
            player.boost(event)
            player.position(event)
            player2.boost(event)
            player2.position(event)
        elif event.type==KEYUP:
            player.slow(event)
            player.position(event)
            player2.slow(event)
            player2.position(event)
            
           
    
    
    player.move()
    player2.move()
    game_display.fill(black)
    
    player.draw()
    player2.draw()
    food.draw(player)
    food.draw(player2)
    
    if game_over:
        pass
    else:
        game_over=final_check(player, player2)
    p.display.update()
    clock.tick(10)
    

