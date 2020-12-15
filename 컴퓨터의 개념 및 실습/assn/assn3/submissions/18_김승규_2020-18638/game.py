import pygame
import random

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
coll=(255,255,0)

class GridObject:
    def __init__(self,x,y,game,color):
        self.game=game
        self.active=True
        self.color=color
        self.x=x        #grid column index
        self.y=y        #grid row index
        
    def handle_event(self,event):
        pass
    
    def tick(self):
        pass

    def draw(self):
        block_size=self.game.block_size
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])

    def interact(self,other):
        pass

class Player(GridObject):
    dx=0
    dy=0
    color=white

    def __init__(self,x,y,game):
        super().__init__(x,y,game,self.color)

    def handle_event(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                self.dx=-1
                self.dy=0
            elif event.key==pygame.K_RIGHT:
                self.dx=+1
                self.dy=0
            elif event.key==pygame.K_UP:
                self.dy=-1
                self.dx=0
            elif event.key==pygame.K_DOWN:
                self.dy=+1
                self.dx=0
            elif event.key==pygame.K_RSHIFT:
                if self.dx==-1 and self.dy==0:
                    self.dx=-1
                    self.dy=0
                elif self.dx==+1 and self.dy==0:
                    self.dx=+1
                    self.dy=0
                elif self.dx==0 and self.dy==-1:
                    self.dx=0
                    self.dy=-1
                elif self.dx==0 and self.dy==+1:
                    self.dx=0
                    self.dy=+1

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

    def interact(self,other):
        if isinstance(other,Food):
            if self.x==other.x and self.y==other.y:
                other.active=False
                
class OtherPlayer(GridObject):
    dx=0
    dy=0
    color=coll

    def __init__(self,x,y,game):
        super().__init__(x,y,game,self.color)

    def handle_event(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                self.dx=-1
                self.dy=0
            elif event.key==pygame.K_d:
                self.dx=+1
                self.dy=0
            elif event.key==pygame.K_w:
                self.dy=-1
                self.dx=0
            elif event.key==pygame.K_s:
                self.dy=+1
                self.dx=0
            elif event.key==pygame.K_LSHIFT:
                if self.dx==-1 and self.dy==0:
                    self.dx=-1
                    self.dy=0
                elif self.dx==+1 and self.dy==0:
                    self.dx=+1
                    self.dy=0
                elif self.dx==0 and self.dy==-1:
                    self.dx=0
                    self.dy=-1
                elif self.dx==0 and self.dy==+1:
                    self.dx=0
                    self.dy=+1

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

    def interact(self,other):
        if isinstance(other,Food):
            if self.x==other.x and self.y==other.y:
                other.active=False

class SubPlayer(GridObject):
    dx=0
    dy=0
    color=red

    def __init__(self,x,y,game):
        super().__init__(x,y,game,self.color)

    def handle_event(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                self.dx=-1
                self.dy=0
            elif event.key==pygame.K_RIGHT:
                self.dx=+1
                self.dy=0
            elif event.key==pygame.K_UP:
                self.dy=-1
                self.dx=0
            elif event.key==pygame.K_DOWN:
                self.dy=+1
                self.dx=0

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

    def interact(self,other):
        if isinstance(other,Food):
            if self.x==other.x and self.y==other.y:
                other.active=False

class OtherSubPlayer(GridObject):
    dx=0
    dy=0
    color=blue

    def __init__(self,x,y,game):
        super().__init__(x,y,game,self.color)

    def handle_event(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                self.dx=-1
                self.dy=0
            elif event.key==pygame.K_RIGHT:
                self.dx=+1
                self.dy=0
            elif event.key==pygame.K_UP:
                self.dy=-1
                self.dx=0
            elif event.key==pygame.K_DOWN:
                self.dy=+1
                self.dx=0

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

    def interact(self,other):
        if isinstance(other,Food):
            if self.x==other.x and self.y==other.y:
                other.active=False


class Food(GridObject):
    color=green

    def __init__(self,game):
        x=random.randint(0,game.n_cols-1)
        y=random.randint(0,game.n_rows-1)
        super().__init__(x,y,game,self.color)
    


class Game:
    block_size=10
    def __init__(self,n_rows,n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
        self.display=pygame.display.set_mode((n_cols*self.block_size,n_rows*self.block_size))
        self.n_rows=n_rows
        self.n_cols=n_cols
        self.clock=pygame.time.Clock()
        self.game_over=False 
        self.objects=[]
        self.others=[]
        

    def play(self,n_foods=20):
        self.objects=[Player(10,30,self),*[Food(self) for _ in range(n_foods)]]      
        route=[]       
        n_meet=1
        follow=[]
        self.others=[OtherPlayer(70,30,self),*self.objects[1:]]            
        oroute=[]
        on_meet=1
        ofollow=[]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    self.game_over=True
                    break

                # Handle Event
                for obj in self.objects:
                    if obj.active:
                        self.objects[0].handle_event(event)
                        asd=0
                        if event.type ==pygame.KEYDOWN:
                            if event.key==pygame.K_RSHIFT:
                                asd=1
                
                for obj in self.others:
                    if obj.active:
                        self.others[0].handle_event(event)
                        zxc=0
                        if event.type ==pygame.KEYDOWN:
                            if event.key==pygame.K_LSHIFT:
                                zxc=1
    

   
            #Tick
            for obj in self.objects:
                if obj.active and asd==0:
                    if isinstance(obj,Player):
                        obj.tick()
                        route.append((obj.x,obj.y))

                elif asd==1 and obj.active:
                    if isinstance(obj,Player):
                        obj.tick()
                        route.append((obj.x,obj.y))
                    

            #Interact
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1.active and obj2.active:
                        obj1.interact(obj2)
                        obj2.interact(obj1)
            
            for obj in self.objects:
                if obj.active and asd==1:
                    if isinstance(obj,Player):
                        obj.tick()
                        route.append((obj.x,obj.y))
                
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1.active and obj2.active:
                        obj1.interact(obj2)
                        obj2.interact(obj1)


            #Draw
            self.display.fill(black)
            for obj in self.objects:
                if obj.active:
                    obj.draw()
                else:
                    obj.x=random.randint(0,self.n_cols-1)
                    obj.y=random.randint(0,self.n_rows-1)
                    obj.active=True
                    obj.draw()
                    n_meet+=1


            #follow Draw
            if n_meet>=2:
                for i in range(n_meet):
                    a,b=route[-i-2]
                    follow.append(SubPlayer(a,b,self))
                for obj in follow[-n_meet:-1]:
                    obj.draw()

            #Tick
            for obj in self.others:
                if obj.active and zxc==0:
                    if isinstance(obj,OtherPlayer):
                        obj.tick()
                        oroute.append((obj.x,obj.y))

                elif zxc==1 and obj.active:
                    if isinstance(obj,OtherPlayer):
                        obj.tick()
                        oroute.append((obj.x,obj.y))
                    

            #Interact
            for obj1 in self.others:
                for obj2 in self.others:
                    if obj1.active and obj2.active:
                        obj1.interact(obj2)
                        obj2.interact(obj1)
            
            for obj in self.others:
                if obj.active and zxc==1:
                    if isinstance(obj,OtherPlayer):
                        obj.tick()
                        oroute.append((obj.x,obj.y))
                
            for obj1 in self.others:
                for obj2 in self.others:
                    if obj1.active and obj2.active:
                        obj1.interact(obj2)
                        obj2.interact(obj1)

            #Draw
            for obj in self.others:
                if obj.active:
                    obj.draw()
                else:
                    obj.x=random.randint(0,self.n_cols-1)
                    obj.y=random.randint(0,self.n_rows-1)
                    obj.active=True
                    obj.draw()
                    on_meet+=1


            #follow Draw
            if on_meet>=2:
                for i in range(on_meet):
                    a,b=oroute[-i-2]
                    ofollow.append(OtherSubPlayer(a,b,self))
                for obj in ofollow[-on_meet:-1]:
                    obj.draw()        
     
            pygame.display.update() 

            #Global Decision
            food_remains=False
            for obj in self.objects:
                if isinstance(obj,Food) and obj.active:
                    food_remains=True
            if not food_remains:
                self.game_over=True
            for obj in self.objects:
                if obj.x>self.n_cols or obj.x<0 or obj.y>self.n_rows or obj.y<0:
                    self.game_over=True
            for obj in follow[-1:-n_meet:-1]:
                if self.objects[0].x==obj.x and self.objects[0].y==obj.y:
                    self.game_over=True
            

            # Global Decision
            food_remains=False
            for obj in self.others:
                if isinstance(obj,Food) and obj.active:
                    food_remains=True
            if not food_remains:
                self.game_over=True
            for obj in self.others:
                if obj.x>self.n_cols or obj.x<0 or obj.y>self.n_rows or obj.y<0:
                    self.game_over=True
            for obj in ofollow[-1:-on_meet:-1]:
                if self.others[0].x==obj.x and self.others[0].y==obj.y:
                    self.game_over=True

            # Global Decision
            for obj3 in follow[-n_meet:-1]:
                if obj3.x==self.others[0].x and obj3.y==self.others[0].y:
                    self.game_over=True
            for obj4 in ofollow[-on_meet:-1]:
                if obj4.x==self.objects[0].x and obj4.y==self.objects[0].y:
                    self.game_over=True       
            if self.others[0].x==self.objects[0].x and self.others[0].y==self.objects[0].y:
                self.game_over=True


            self.clock.tick(10)


if __name__ == "__main__":
    Game(n_rows=60,n_cols=80).play(n_foods=20)

