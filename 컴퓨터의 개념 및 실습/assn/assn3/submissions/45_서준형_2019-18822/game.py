import random
import pygame
from pygame.constants import QUIT

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

class GridObject:
    def __init__(self, x, y, game, color, num, length,width):
        self.game=game
        self.length=length
        self.width=width
        self.active=True
        self.color=color
        self.num=num
        self.x=x  #grid column index
        self.y=y  #grid row index
    
    def handle_event(self,event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size=self.game.block_size
        if isinstance (self, Food):
            pygame.draw.rect(self.game.display, self.color, [self.x*block_size, self.y*block_size, block_size, block_size])
        else:
            pass

    def interact(self, other):
        pass


class Player(GridObject):
    dx=0
    dy=0
    length=10
    width=10
    detail=[length,width]

    def __init__(self, x, y, game, num):
        self.num=num
        if self.num==1:
            self.color=RED
        elif self.num==2:
            self.color=BLUE
        super().__init__(x, y, game, self.color, self.num, self.length, self.width)
    
    def draw(self):
        block_size=self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x*block_size, self.y*block_size, self.length, self.width])

    def handle_event(self, event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.KMOD_SHIFT:
                self.clock.tick(20)
            if self.num==1:
                if event.key==pygame.K_a:
                    self.dx=-1
                    self.dy=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_d:
                    self.dx=1
                    self.dy=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_w:
                    self.dy=-1
                    self.dx=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_s:
                    self.dy=1
                    self.dx=0
                    self.length,self.width=self.width,self.length
            
            elif self.num==2:
                if event.key==pygame.K_LEFT:
                    self.dx=-1
                    self.dy=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_RIGHT:
                    self.dx=1
                    self.dy=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_UP:
                    self.dy=-1
                    self.dx=0
                    self.length,self.width=self.width,self.length
                elif event.key==pygame.K_DOWN:
                    self.dy=1
                    self.dx=0
                    self.length,self.width=self.width,self.length

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

    def interact(self, other):
        if self.x==other.x and self.y==other.y:
            if isinstance(other, Food):
                other.active=False
                return 'eat'
            elif isinstance(other, Player):
                if self.color!=other.color:
                    other.active=False
                    return 'meet'
                
class Food(GridObject):
    color=GREEN
    length=10
    
    def __init__(self, game):
        x=random.randint(0, game.n_cols-1)
        y=random.randint(0, game.n_rows-1)
        num=0
        length=game.block_size
        width=game.block_size
        super().__init__(x, y, game, self.color, num, length, width)

class Game:
    block_size=10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        self.display=pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size))
        pygame.display.set_caption('DDCP Snake Game')
        self.n_rows=n_rows
        self.n_cols=n_cols
        self.clock=pygame.time.Clock()
        self.game_over=False
        self.objects=[]

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def play(self, n_foods=20):
        
        self.player1=Player(0,self.n_rows/2, self, 1)
        self.player2=Player(self.n_cols-1, self.n_rows/2, self, 2)
        self.foods=[Food(self) for _ in range(n_foods)]
        self.objects=[self.player1, self.player2, *self.foods]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over=True
                    break
                
                # Handle object
                for obj in self.active_objects():
                    obj.handle_event(event)

            # Tick
            for obj in self.active_objects():
                obj.tick()             

            # Interact
            for obj1 in self.objects[0:2]:
                for obj2 in self.active_objects():
                    i1=obj1.interact(obj2)
                    i2=obj2.interact(obj1)

                    if not obj1.active or not obj2.active:
                        # more food create
                        if i1=='eat' or i2=='eat':
                            self.objects.append(Food(self))
                            if i1=='eat':
                                if obj1.width==10:
                                    obj1.length+=10
                                else:
                                    obj1.width+=10

                            elif i2=='eat':
                                if obj2.width==10:
                                    obj2.length+=10
                                else:
                                    obj2.width+=10

                        # two players meet
                        elif i1=='meet' or i2=='meet':
                            if obj1.color!=obj2.color:
                                self.game_over=True
            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()   

            # Global Decision
            food_remains=False

            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains=True

            if not food_remains:
                self.game_over=True

            # End (Out of range)
            for i in range(2):
                if self.objects[i].x>self.n_cols or self.objects[i].x<0 or self.objects[i].y>self.n_rows or self.objects[i].y<0:
                    self.game_over=True
    
            
            self.clock.tick(10)


if __name__=='__main__':
    Game(n_rows=60, n_cols=80).play(n_foods=20)
