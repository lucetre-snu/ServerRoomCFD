import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 , 255)
PINK = (255,192,203)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.color = color
        self.x = x
        self.y = y

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x*block_size, self.y*block_size, block_size, block_size])

    def interact(self, other):
        pass
 

class Player(GridObject):
    color = WHITE    
    dx = 0
    dy = 0    
    def __init__(self, x, y, game):
        self.STEP = 1
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.dx!=1:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT and self.dx!=-1:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP and self.dy!=1:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_DOWN and self.dy!=-1:
                self.dx = 0
                self.dy = 1
    
    def tick(self):
        temp = self.dx
        temp2 = self.dy
        self.dx = (int)(self.dx * self.STEP)
        self.dy = (int)(self.dy * self.STEP)
        self.x += self.dx
        self.y += self.dy
        self.dx = temp
        self.dy = temp2
    

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:                
                return 1
            else:
                return 0

class leftPlayer(Player):
    color = BLUE
    def __init__(self, x, y, game):
        super().__init__(x,y,game)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and self.dx!=1:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_d and self.dx!=-1:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_w and self.dy!=1:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_s and self.dy!=-1:
                self.dx = 0
                self.dy = 1

class body(Player):
    def __init__(self, ahead, game, color):
        
        self.game = game
        self.x = ahead.x
        self.y = ahead.y
        if(ahead.dx > 0):
            self.x = ahead.x - 1
        elif(ahead.dx < 0):
            self.x = ahead.x + 1
        elif(ahead.dy > 0):
            self.y = ahead.y - 1
        else:
            self.y = ahead.y + 1
        super().__init__(self.x, self.y, self.game)
        
        self.dx = ahead.dx
        self.dy = ahead.dy
        self.STEP = ahead.STEP
        
        self.color = color
    
    def tick(self, ahead):
        self.x = ahead.x
        self.y = ahead.y
        self.dx = ahead.dx
        self.dy = ahead.dy   
  
class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)


class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.foods = []
        self.player = Player(50, 30, self)
        self.leftplayer = leftPlayer(30, 30, self)
        self.playerbodyList = []
        self.leftplayerbodyList = []

    def handleAll(self, event):
        for obj in self.foods:
            obj.handle_event(event)                 
        self.player.handle_event(event)
        self.leftplayer.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            self.player.STEP = 2
        else:
            self.player.STEP = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            self.leftplayer.STEP = 2
        else:
            self.leftplayer.STEP = 1
            
        
    def tickAll(self):
        for obj in self.foods:
            obj.tick()
        
        if(self.player.STEP == 1):
            for i in range(len(self.playerbodyList)-1,-1,-1):
                if(i==0):
                    self.playerbodyList[i].tick(self.player)
                else:
                    self.playerbodyList[i].tick(self.playerbodyList[i-1])
            self.player.tick()
        else:
            for i in range(len(self.playerbodyList)-1,-1,-1):
                if(i==1):
                    self.playerbodyList[i].tick(self.player)
                elif(i==0):
                    self.playerbodyList[i].x = self.player.x + self.player.dx
                    self.playerbodyList[i].y = self.player.y + self.player.dy
                    self.playerbodyList[i].dx = self.player.dx
                    self.playerbodyList[i].dy = self.player.dy
                else:
                    self.playerbodyList[i].tick(self.playerbodyList[i-2])
            self.player.tick()

        if(self.leftplayer.STEP == 1):
            for i in range(len(self.leftplayerbodyList)-1,-1,-1):
                if(i==0):
                    self.leftplayerbodyList[i].tick(self.leftplayer)
                else:
                    self.leftplayerbodyList[i].tick(self.leftplayerbodyList[i-1])
            self.leftplayer.tick()
        else:
            for i in range(len(self.leftplayerbodyList)-1,-1,-1):
                if(i==1):
                    self.leftplayerbodyList[i].tick(self.leftplayer)
                elif(i==0):
                    self.leftplayerbodyList[i].x = self.leftplayer.x + self.leftplayer.dx
                    self.leftplayerbodyList[i].y = self.leftplayer.y + self.leftplayer.dy
                    self.leftplayerbodyList[i].dx = self.leftplayer.dx
                    self.leftplayerbodyList[i].dy = self.leftplayer.dy
                else:
                    self.leftplayerbodyList[i].tick(self.leftplayerbodyList[i-2])
            self.leftplayer.tick()
        

    def drawAll(self):
        for obj in self.foods:
            obj.draw()
        self.player.draw()
        self.leftplayer.draw()
        for obj in self.playerbodyList:
            obj.draw()
        for obj in self.leftplayerbodyList:
            obj.draw()

    def play(self, n_foods=20):
        self.foods = [Food(self) for _ in range(n_foods)]     

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break                    
                self.handleAll(event)                 

            #interact with players and foods
            for obj2 in self.foods:
                if(self.player.interact(obj2) == 1 or (self.playerbodyList != [] and self.playerbodyList[0].interact(obj2) == 1)):                    
                    self.foods.remove(obj2)
                    newFood = Food(self)
                    checking = True
                    while(checking):
                        checking=False
                        for obj in self.foods:
                            if(isinstance(obj,Food) and obj.x == newFood.x and obj.y == newFood.y):
                                newFood = Food(self)
                                checking = True
                                break
                    self.foods.append(newFood)
                    if(self.playerbodyList == []):
                        self.playerbodyList.append(body(self.player, self, RED))
                    else:
                        self.playerbodyList.append(body(self.playerbodyList[-1], self, RED))
                elif(self.leftplayer.interact(obj2) == 1 or (self.leftplayerbodyList != [] and self.leftplayerbodyList[0].interact(obj2) == 1)):
                    self.foods.remove(obj2)
                    newFood = Food(self)
                    checking = True
                    while(checking):
                        checking=False
                        for obj in self.foods:
                            if(isinstance(obj,Food) and obj.x == newFood.x and obj.y == newFood.y):
                                newFood = Food(self)
                                checking = True
                                break
                    self.foods.append(newFood)
                    if(self.leftplayerbodyList == []):
                        self.leftplayerbodyList.append(body(self.leftplayer, self, PINK))
                    else:
                        self.leftplayerbodyList.append(body(self.leftplayerbodyList[-1], self,  PINK))

            for obj in self.playerbodyList:
                if(self.player.x == obj.x and self.player.y == obj.y) or (self.leftplayer.x == obj.x and self.leftplayer.y == obj.y) :
                    self.game_over = True

            for obj in self.leftplayerbodyList:
                if(self.player.x == obj.x and self.player.y == obj.y) or (self.leftplayer.x == obj.x and self.leftplayer.y == obj.y) :
                    self.game_over = True
            
            if self.player.x == self.leftplayer.x and self.player.y == self.leftplayer.y:
                self.game_over = True
            
            if(self.player.x<0 or self.player.y<0 or self.player.x>self.n_cols or self.player.y > self.n_rows):
                self.game_over = True
            if(self.leftplayer.x<0 or self.leftplayer.y<0 or self.leftplayer.x>self.n_cols or self.leftplayer.y > self.n_rows):
                self.game_over = True

            if(self.game_over):
                break
            

            #draw
            self.display.fill(BLACK)
            self.tickAll()
            self.drawAll()
            
            pygame.display.update()

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)