import pygame
import random

class Pixel:
    def __init__(self,name,x,y,c,game):
        self.name=name
        self.x=x
        self.y=y
        self.c=c
        self.game=game
        self.size=game.pixel
        self.active=True
    def interact(self,other):
        pass
    def draw(self):
        pygame.draw.rect(self.game.window,self.c,
        [self.x*self.size,self.y*self.size,self.size,self.size])


class Player(Pixel):
    def __init__(self,name,x,y,c,game):
        super().__init__(name,x,y,c,game)
        self.dx=0
        self.dy=0
        self.speed=1
        self.key=None
        self.score=0
        self.body=[]
        self.myst=False
    
    def control(self,event):
        self.keys=[
            pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,
            pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,
        ]
        if event.type==pygame.KEYDOWN:
            if event.key in self.keys:
                self.key=event.key
        
        #previous direction
        p_dx=self.dx
        p_dy=self.dy
        
        if self.name=='p2':
            if self.key == pygame.K_LEFT:
                self.dx=-1
                self.dy=0
            elif self.key == pygame.K_RIGHT:
                self.dx=1
                self.dy=0
            elif self.key == pygame.K_UP:
                self.dx=0
                self.dy=-1
            elif self.key == pygame.K_DOWN:
                self.dx=0
                self.dy=1
        elif self.name=='p1':
            if self.key == pygame.K_a:
                self.dx=-1
                self.dy=0
            elif self.key == pygame.K_d:
                self.dx=1
                self.dy=0
            elif self.key == pygame.K_w:
                self.dx=0
                self.dy=-1
            elif self.key == pygame.K_s:
                self.dx=0
                self.dy=1
        
        #U-turn check
        if self.score!=0:
            if (self.dx!=0 and p_dx==-self.dx) or (self.dy!=0 and p_dy==-self.dy):
                self.active=False

    def dash(self,event):
        if self.name=='p2':
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RSHIFT:
                self.speed=2
            elif event.type==pygame.KEYUP and event.key==pygame.K_RSHIFT:
                self.speed=1
        elif self.name=='p1':
            if event.type==pygame.KEYDOWN and event.key==pygame.K_LSHIFT:
                self.speed=2
            elif event.type==pygame.KEYUP and event.key==pygame.K_LSHIFT:
                self.speed=1

    def move(self):
        p_x=self.x
        p_y=self.y
        self.x+=self.dx*self.speed
        self.y+=self.dy*self.speed

        #edge check
        if self.x<0 or self.x>self.game.width_n-1 or self.y<0 or self.y>self.game.height_n-1: 
            self.active=False

        #add tail
        if self.speed==2:
            self.body.append([p_x,p_y])
            self.body.append([int((self.x+p_x)/2),int((self.y+p_y)/2)])     
        else:
            self.body.append([p_x,p_y])
        if len(self.body)>self.score:
            self.body=self.body[len(self.body)-self.score:]
    
    def interact(self,other):
        conflict=False
        if self.speed==1:
            if self.x==other.x and self.y==other.y:
                conflict=True
        #dash trail check
        elif self.speed==2:
            if self.dx!=0:
                if (self.x==other.x or self.x-self.dx==other.x) and self.y==other.y:
                        conflict=True
            elif self.dy!=0:
                if self.x==other.x and (self.y-self.dy==other.y or self.y==other.y):
                        conflict=True

        #eat and crash
        if isinstance(other,Food) and conflict:
            other.active=False
            self.score+=1
        elif (isinstance(other,Player) or isinstance(other,Tail)) and conflict:
            if other.name==self.name and [other.x,other.y]==self.body[-1]:
                pass
            else:
                self.active=False

class Tail(Pixel):
    def __init__(self,name,xy,c,game):
        self.xy=xy
        super().__init__(name,self.xy[0],self.xy[1],c,game)

class Food(Pixel):
    color=(0, 255, 76)
    def __init__(self,game,lst):
        self.lst=lst #pixels location check
        self.checklst=[]
        for pixels in lst:
            self.checklst.append([pixels.x,pixels.y])
        self.x=random.randint(0,game.width_n-1)
        self.y=random.randint(0,game.height_n-1)
        while [self.x,self.y] in self.checklst: #overlap check
            self.x=random.randint(0,game.width_n-1)
            self.y=random.randint(0,game.height_n-1)
        super().__init__(self,self.x,self.y,self.color,game)

class Game:
    #CONSTANTS
    def __init__(self,size,width_n,height_n,food_n):
        pygame.init()
        pygame.display.set_caption('Battle Sanke!')
        self.pixel=size
        self.width_n=width_n
        self.height_n=height_n
        self.food_n=food_n
        self.p1_pos=(int(self.width_n*0.1),int(self.height_n*0.1))
        self.p2_pos=(int(self.width_n*0.9),int(self.height_n*0.9))
        self.window=pygame.display.set_mode((self.pixel*self.width_n,self.pixel*self.height_n))
        self.run=True
        self.objects=[]
        self.clock=pygame.time.Clock()
        
    def play(self):
        p1=Player('p1',self.p1_pos[0],self.p1_pos[1],(255, 107, 107),self)
        p2=Player('p2',self.p2_pos[0],self.p2_pos[1],(84, 150, 255),self)
        self.objects=[p1,p2,*[Food(self,self.objects) for _ in range(self.food_n)]]

        while self.run:
            for event in pygame.event.get():
                p1.dash(event)
                p2.dash(event)
                if event.type == pygame.QUIT:
                    self.run=False
                    break
                elif event.type==pygame.KEYDOWN:
                    p1.control(event)
                    p2.control(event)
            p1.move()
            p2.move()

            #objects management
            if len(self.objects)>2+self.food_n:
                self.objects=self.objects[:2+self.food_n]
            for body in p1.body:
                self.objects.append(Tail('p1',body,(255,15,51),self))
            for body in p2.body:
                self.objects.append(Tail('p2',body,(0, 98, 255),self))

            #interact
            for obj_a in self.objects:
                for obj_b in self.objects:
                    if obj_a!=obj_b:
                        obj_a.interact(obj_b)

            #decision
            for (i,obj) in enumerate(self.objects):
                clone=self.objects[:]
                if isinstance(obj,Player) and not(obj.active):
                    self.run=False
                elif isinstance(obj,Food) and not(obj.active):
                    self.objects[i]=Food(self,clone)
            #draw
            self.window.fill((0,0,0))
            for obj in self.objects:
                if obj.active:
                    obj.draw()

            pygame.display.update()
            self.clock.tick(10)

if __name__=="__main__":
    #Game(pixel_size,width_n,height_n,food_n)
    Game(10,80,60,20).play()


    
    
    