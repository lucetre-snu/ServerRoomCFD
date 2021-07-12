import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x  # grid column index
        self.y = y  # grid row index
        
    
    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def move(self, x, y):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass    

class Body(GridObject):
    color = BLUE 
    def __init__(self,head):
        if head.way == -1:
            super().__init__(head.x+len(head.body)+1, head.y, head.game,self.color)            
        elif head.way == 1:
            super().__init__(head.x-len(head.body)-1, head.y, head.game,self.color)
        elif head.way == 2:
            super().__init__(head.x, head.y-len(head.body)-1, head.game,self.color)
        elif head.way == -2:
            super().__init__(head.x, head.y+len(head.body)+1, head.game,self.color)
    def move(self, x, y):
        self.x = x
        self.y = y

class Body2(GridObject):
    color = RED
    def __init__(self,head):
        if head.way == -1:
            super().__init__(head.x+len(head.body)+1, head.y, head.game,self.color)            
        elif head.way == 1:
            super().__init__(head.x-len(head.body)-1, head.y, head.game,self.color)
        elif head.way == 2:
            super().__init__(head.x, head.y-len(head.body)-1, head.game,self.color)
        elif head.way == -2:
            super().__init__(head.x, head.y+len(head.body)+1, head.game,self.color)
    def move(self, x, y):
        self.x = x
        self.y = y
    



class Player(GridObject):
    dx = 0
    dy = 0
    color = "royalblue"
    body = []    
    gameset = False
    way = 0 # left: -1 right: 1 up: 2 down: -2
    

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)        

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0               
                self.way = -1                        
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
                self.way = 1
            elif event.key == pygame.K_UP:
                self.dx = 0
                self.dy = -1
                self.way = 2                
            elif event.key == pygame.K_DOWN:
                self.dx = 0
                self.dy = 1
                self.way = -2
            elif event.key == pygame.K_RSHIFT:
                self.dx *=2
                self.dy *=2 
        if event.type == pygame.KEYUP:
            if (self.way == 1 or self.way == -1) and event.key == pygame.K_RSHIFT:
                self.dx = int(self.dx/2)
            elif (self.way == 2 or self.way == -2) and event.key == pygame.K_RSHIFT:
                self.dy = int(self.dy/2)


    def tick(self):          
        for i in range(len(self.body)-1,-1,-1):
            if i == 0:
                if self.dx == -2:
                    self.body[0].move(self.x-1,self.y)
                elif self.dx == 2:
                    self.body[0].move(self.x+1,self.y)
                elif self.dy == -2:
                    self.body[0].move(self.x,self.y-1)
                elif self.dy == 2:
                    self.body[0].move(self.x,self.y+1)
                else:
                    self.body[0].move(self.x,self.y)                
            else:
                if self.dx == -2 or self.dx == 2 or self.dy == -2 or self.dy == 2 :
                    if i == 1:
                        self.body[i].move(self.x,self.y)
                    else:
                        self.body[i].move(self.body[i-2].x, self.body[i-2].y)
                
                else:
                    self.body[i].move(self.body[i-1].x,self.body[i-1].y)                
        self.x += self.dx    
        self.y += self.dy 

    


    def interact(self, other):
        if isinstance(other, Food):            
            if self.x == other.x and self.y == other.y:
                other.active = False
                self.body.append(Body(self))
        elif isinstance(other, Player2):
            if self.x == other.x and self.y == other.y:
                self.gameset = True
        elif isinstance(other,Body):
            if self.x == other.x and self.y == other.y:
                self.gameset = True
        elif isinstance(other,Body2):
            if self.x == other.x and self.y == other.y:
                self.gameset = True


class Player2(GridObject):
    dx = 0
    dy = 0
    color = "orange" 
    body = []
    gameset = False
    way = 0 # left: -1 right: 1 up: 2 down: -2   
    

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)        

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
                self.dy = 0
                self.way = -1                         
            elif event.key == pygame.K_d:
                self.dx = 1
                self.dy = 0
                self.way = 1
            elif event.key == pygame.K_w:
                self.dx = 0
                self.dy = -1
                self.way = 2                
            elif event.key == pygame.K_s:
                self.dx = 0
                self.dy = 1
                self.way = -2
            elif event.key == pygame.K_LSHIFT:
                self.dx *=2
                self.dy *=2 
        if event.type == pygame.KEYUP:
            if (self.way == 1 or self.way == -1) and event.key == pygame.K_RSHIFT:
                self.dx = int(self.dx/2)
            elif (self.way == 2 or self.way == -2) and event.key == pygame.K_RSHIFT:
                self.dy = int(self.dy/2)

    def tick(self):
        for i in range(len(self.body)-1,-1,-1):
            if i == 0:
                if self.dx == -2:
                    self.body[0].move(self.x-1,self.y)
                elif self.dx == 2:
                    self.body[0].move(self.x+1,self.y)
                elif self.dy == -2:
                    self.body[0].move(self.x,self.y-1)
                elif self.dy == 2:
                    self.body[0].move(self.x,self.y+1)
                else:
                    self.body[0].move(self.x,self.y)                
            else:
                if self.dx == -2 or self.dx == 2 or self.dy == -2 or self.dy == 2 :
                    if i == 1:
                        self.body[i].move(self.x,self.y)
                    else:
                        self.body[i].move(self.body[i-2].x, self.body[i-2].y)
                
                else:
                    self.body[i].move(self.body[i-1].x,self.body[i-1].y)                
        self.x += self.dx    
        self.y += self.dy    
    




    def interact(self, other):
        if isinstance(other, Food):            
            if self.x == other.x and self.y == other.y:
                other.active = False
                self.body.append(Body2(self))                
        elif isinstance(other, Player):            
            if self.x == other.x and self.y == other.y:
                self.gameset = True
        elif isinstance(other,Body):
            if self.x == other.x and self.y == other.y:
                self.gameset = True
        elif isinstance(other,Body2):
            if self.x == other.x and self.y == other.y:
                self.gameset = True

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
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    
    def play(self, n_foods = 20):
        self.objects = [
            Player(50, 40, self), Player2(30, 20, self),
            *[Food(self) for _ in range(n_foods)]
        ]        
        while not self.game_over: 
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                # Handle Event
                for obj in self.active_objects():
                    obj.handle_event(event)

            # Tick
            for obj in self.active_objects():
                obj.tick()

            # Interact
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    obj1.interact(obj2)
                    obj2.interact(obj1)
                    if obj1.active == False or obj2.active == False:
                        self.objects.append(Food(self))
                    if isinstance(obj1, Player) and isinstance(obj2, Player2):
                        for obj3 in obj1.body:
                            obj2.interact(obj3)
                        for obj4 in obj2.body:
                            obj1.interact(obj4)
                    elif isinstance(obj1, Player2) and isinstance(obj2, Player):
                        for obj3 in obj1.body:
                            obj2.interact(obj3)
                        for obj4 in obj2.body:
                            obj1.interact(obj4)
                if isinstance(obj1, Player):
                    for obj3 in obj1.body:
                        obj1.interact(obj3)
                elif isinstance(obj1,Player2):
                    for obj3 in obj1.body:
                        obj1.interact(obj3)

                

            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
                if isinstance(obj,Player):
                    for bod in Player.body:
                        bod.draw()
                if isinstance(obj,Player2):
                    for bod in Player2.body:
                        bod.draw()

                          
            pygame.display.update()

            # Global Decision            
            if self.objects[0].x == 0 or self.objects[0].x == 80 or self.objects[0].y == 0 or self.objects[0].y == 60:
                self.game_over = True            
            if self.objects[0].gameset == True:
                self.game_over = True
            if self.objects[1].gameset == True:
                self.game_over = True
        
            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)

