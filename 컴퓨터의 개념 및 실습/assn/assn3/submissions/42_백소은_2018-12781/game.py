import pygame
import random
WHITE=(255,255,255)
BLUE=(0,0,255)
LBLUE=(150,150,255)
GREEN=(0,240,0)
LGREEN=(180,255,180)
RED=(255,0,0)
block_size=10
fps=10

class Things:
    def __init__(self,x,y,color,game,id):
        self.x=x
        self.y=y
        self.color=color
        self.game=game
        self.id=id
        self.active=True
    def key_handle(self,event):
        pass
    def tick_handle(self):
        pass
    def interact(self,other):
        pass
    def draw(self):
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])
  
class Snake(Things):
    def __init__(self,game,id):
        self.bodylength=0
        self.dx=0
        self.dy=0
        self.body=[] 
        self.body_x=None
        self.body_y=None
        self.boost=False
        if id==0:
            color=BLUE
            self.headcolor= LBLUE
            x,y=(60,60)
            self.l=False
            self.r=False
            self.u=False
            self.down=False
        else:
            color=GREEN
            self.headcolor= LGREEN
            x,y=(20,20)
            self.a=False
            self.d=False
            self.w=False
            self.s=False
        super().__init__(x,y,color,game,id)

    def key_handle(self,event):
        if event.type==pygame.KEYDOWN:
            self.allkeys=pygame.key.get_pressed()

            if self.allkeys[pygame.K_LEFT]:
                if self.id==0:
                    self.dx=-1 
                    self.dy=0
                    self.l=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy                
            if self.allkeys[pygame.K_RIGHT]:
                if self.id==0:
                    self.dx=1
                    self.dy=0
                    self.r=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if self.allkeys[pygame.K_UP]:
                if self.id==0:  
                    self.dx=0
                    self.dy=-1
                    self.u=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if self.allkeys[pygame.K_DOWN]:
                if self.id==0:
                    self.dx=0
                    self.dy=1
                    self.down=True  
                else:
                    self.dx=self.dx
                    self.dy=self.dy 
            if event.key==pygame.K_RSHIFT:
                if self.id==0:
                    self.dx*=2
                    self.dy*=2
                    self.boost=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy   
            if self.allkeys[pygame.K_a]:
                if self.id==1:
                    self.dx=-1  
                    self.dy=0
                    self.a=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if self.allkeys[pygame.K_d]:
                if self.id==1:
                    self.dx=1
                    self.dy=0
                    self.d=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if self.allkeys[pygame.K_w]: 
                if self.id==1:
                    self.dx=0
                    self.dy=-1
                    self.w=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if self.allkeys[pygame.K_s]:
                if self.id==1:
                    self.dx=0
                    self.dy=1
                    self.s=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy     
            if event.key==pygame.K_LSHIFT:
                if self.id==1:
                    self.dx*=2
                    self.dy*=2     
                    self.boost=True
                else:
                    self.dx=self.dx
                    self.dy=self.dy
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RSHIFT:
                if self.id==0:
                    self.boost=False   
                    self.dx=self.dx/2
                    self.dy=self.dy/2
                else:
                    self.dx=self.dx
                    self.dy=self.dy
            if event.key==pygame.K_LSHIFT:
                if self.id==1:
                    self.boost=False
                    self.dx=self.dx/2
                    self.dy=self.dy/2
                else:
                    self.dx=self.dx
                    self.dy=self.dy
    def tick_handle(self):
        if not self.boost:
            if len(self.body)!=0:
                for i in range(len(self.body)-1):
                    self.body[i][0]=self.body[i+1][0]
                    self.body[i][1]=self.body[i+1][1]            
                self.body[-1][0]=self.x
                self.body[-1][1]=self.y
            self.x+=self.dx
            self.y+=self.dy

        if self.boost:
            if len(self.body)!=0:
                for i in range(len(self.body)-1):
                    self.body[i][0]=self.body[i+1][0]+self.dx/2
                    self.body[i][1]=self.body[i+1][1]+self.dy/2            
                self.body[-1][0]=self.x+self.dx/2
                self.body[-1][1]=self.y+self.dy/2
            self.x+=self.dx
            self.y+=self.dy              
    def interact(self,other):
        if isinstance(other,Snake):
            if self.x==other.x and self.y==other.y:  
                self.game.game_over=True 
            if len(other.body)!=0: 
                for i in range(len(other.body)):
                    if other.body[i][0]==self.x and other.body[i][1]==self.y:
                        self.game.game_over=True 
        if isinstance(other,Food):
            eat=False
            if len(self.body)!=0 and self.boost:         
                for i in range(len(self.body)):
                    if (self.body[i][0]==other.x and self.body[i][1]==other.y):
                        eat=True
            if (self.x==other.x and self.y==other.y):           
                other.active=False
                self.bodylength+=1
                if not self.boost:
                    self.body_x=self.x+self.dx 
                    self.body_y=self.y+self.dy
                    self.x,self.body_x=self.body_x,self.x
                    self.y,self.body_y=self.body_y,self.y
                    self.body.append([self.body_x,self.body_y])
                elif self.boost:
                    self.body_x=self.x+self.dx/2
                    self.body_y=self.y+self.dy/2
                    self.x,self.body_x=self.body_x,self.x
                    self.y,self.body_y=self.body_y,self.y
                    self.body.append([self.body_x,self.body_y])     
            elif eat: 
                other.active=False
                self.body_x=self.x+self.dx/2
                self.body_y=self.y+self.dy/2
                self.x,self.body_x=self.body_x,self.x
                self.y,self.body_y=self.body_y,self.y
                self.body.append([self.body_x,self.body_y])

        if self.x<0 or self.x>79 or self.y<0 or self.y>79:
            self.game.game_over=True
        for i in range(len(self.body)):
            if self.body[i][0]==self.x and self.body[i][1]==self.y:
                self.game.game_over=True 
    def draw(self):
        if len(self.body)==0:
            pygame.draw.rect(self.game.display,self.headcolor,[self.x*block_size,self.y*block_size,block_size,block_size])
        elif len(self.body)!=0:
            pygame.draw.rect(self.game.display,self.headcolor,[self.x*block_size,self.y*block_size,block_size,block_size])
            for i in range(len(self.body)):
                pygame.draw.rect(self.game.display,self.color,[self.body[i][0]*block_size,self.body[i][1]*block_size,block_size,block_size])

class Food(Things):
    color=RED
    id=0
    def __init__(self,game): 
        id=Food.id
        Food.id+=1
        self.game=game
        if id<=20:
            x=random.randint(0,79)  
            y=random.randint(0,79) 
        else:
            while True:
                x=random.randint(0,79)
                y=random.randint(0,79)
                if len(self.game.s1.body)!=0:
                    for i in range(len(self.game.s1.body)):
                        if not ((self.game.s1.body[i][0]==x and self.game.s1.body[i][1]==y) or (self.game.s1.x==x and self.game.s1.y==y)):
                            empty1=True
                        else:
                            empty1=False
                elif len(self.game.s1.body)==0:
                    if not (self.game.s1.x==x and self.game.s1.y==y):
                        empty1=True
                    else:
                        empty1=False 
                if len(self.game.s2.body)!=0:                             
                    for j in range(len(self.game.s2.body)):
                        if not ((self.game.s2.body[j][0]==x and self.game.s2.body[j][1]==y) or (self.game.s2.x==x and self.game.s2.y==y)):
                            empty2=True 
                        else:
                            empty2=False
                elif len(self.game.s2.body)==0:
                    if not (self.game.s2.x==x and self.game.s2.y==y):
                        empty2=True
                    else:
                        empty2=False               
                if empty1 and empty2:
                    break 
        super().__init__(x,y,self.color,game,id)

class Snake_game:
    def __init__(self,nx,ny):
        pygame.init()
        pygame.display.set_caption("Snake Game(Two-player Ver)")
        self.clock=pygame.time.Clock()
        self.nx=nx
        self.ny=ny
        self.display=pygame.display.set_mode((self.nx*block_size,self.ny*block_size))
        self.game_over=False
        self.members=[]
    def gen_active_mem(self):
        for mem in self.members:
            if mem.active:
                yield mem
    def playgame(self):
        self.s1=Snake(self,0)
        self.s2=Snake(self,1)
        self.members=[self.s1,self.s2,*[Food(self) for i in range(20)]]
        while not self.game_over:
            for event in pygame.event.get(): 
                if event.type==pygame.QUIT:  
                    self.game_over=True
                    break 
                for m in self.gen_active_mem(): 
                    m.key_handle(event)
            for m in self.gen_active_mem(): 
                m.tick_handle() 
            for p in self.gen_active_mem():
                for q in self.gen_active_mem():
                    if p!=q:
                        p.interact(q)
                        q.interact(p)
            self.display.fill(WHITE)
            for m in self.gen_active_mem():
                m.draw()    
            pygame.display.update()

            food_num=0
            for m in self.gen_active_mem():
                if isinstance(m,Food):
                    food_num+=1
            if not food_num==20:
                new_food=Food(self)
                self.members.append(new_food)  
            self.clock.tick(fps)
if __name__=="__main__":
    Snake_game(80,80).playgame()