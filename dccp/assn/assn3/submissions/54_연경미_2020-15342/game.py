import random
import pygame

WHITE = (255, 255, 255)
WHITE_BODY = (150, 150, 150)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
RED_BODY = (255, 100, 100)
BLUE = (0, 0, 255)
BLUE_BODY = (100, 100, 255)

class Gridobject:

    def __init__(self, x, y, game):
        self.game = game
        self.active = True
        self.x = x # grid column index
        self.y = y # grid row index
        self.ischange = False # condition 2
        self.body = []

    def handle_event(self, event):
        pass
    
    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass

class Player(Gridobject):
    dx = 0
    dy = 0
    px = 0
    py = 0
    
    def __init__(self, x, y, player_num, game):
        super().__init__(x, y, game)
        self.body = [self]
        self.player_num = player_num
        if self.player_num == 1:
            self.color = WHITE
        elif self.player_num == 2:
            self.color = BLUE
        self.clock = pygame.time.Clock()
        self.boost = 1
        
 
    def handle_event(self, event):
        if self.player_num == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_RIGHT:  
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_UP:  
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_DOWN:  
                    self.dx = 0
                    self.dy = 1
                elif event.key == pygame.K_RSHIFT:
                    self.boost = 2
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    self.boost = 1
        if self.player_num == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_d:  
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_w:  
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_s:  
                    self.dx = 0
                    self.dy = 1
                elif event.key == pygame.K_LSHIFT:
                    self.boost = 2
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.boost = 1

    def tick(self):
        self.px = self.x
        self.py = self.y
        self.x += self.dx * self.boost
        self.y += self.dy * self.boost
        for i in range(1, len(self.body)):
            self.body[i].follow(self.body[i-1])

    def grow(self):
        def f(self, dx, dy):
            self.body.insert(1, Body(self.x, self.y, self.px, self.py, self.player_num, self.game))
            self.px = self.x
            self.py = self.y
            self.x += dx
            self.y += dy
        
        f(self, self.dx, self.dy)

    def between(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        elif (self.px <= other.x <= self.x) or (self.px >= other.x >= self.x):
            if (self.py <= other.y <= self.y) or (self.py >= other.y >= self.y):
                return True
            else:
                return False
        return False

    def interact(self, other):
        if isinstance(other, Food):
            if self.between(other):
                other.active = False
                self.grow()
                self.ischange = True # condition 2


class Body(Gridobject):

    def __init__(self, x, y, px, py, player_num, game):
        super().__init__(x, y, game)
        self.px = px
        self.py = py
        self.player_num = player_num
        if self.player_num == 1:
            self.color = WHITE_BODY
        elif self.player_num == 2:
            self.color = BLUE_BODY
    
    def follow(self, former):
        self.px = self.x  
        self.py = self.y
        self.x = former.px
        self.y = former.py

class Food(Gridobject):
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.n_cols-1)
        y = random.randint(0, game.n_rows-1)
        super().__init__(x, y, game)
        

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
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
    
    def play(self, n_foods=20):
        self.objects = [
            Player(40, 30, 1, self), Player(20, 50, 2, self),
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
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1.active and obj2.active:
                        obj1.interact(obj2)
                        obj2.interact(obj1)
                        if obj1.ischange or obj2.ischange:
                            self.objects.append(Food(self)) # condition 2
                            obj1.ischange = False                          
                            obj2.ischange = False
            
            # Draw
            self.display.fill(BLACK)

            for obj in self.active_objects():
                for i in range(1, len(obj.body)):
                    obj.body[i].draw()
                obj.draw()
            


            pygame.display.update()  

            # Global Decision
            food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains = True
            
            if not food_remains:
                self.game_over = True
            
            for obj in self.active_objects(): # condition 2
                if obj.x < 0 or obj.x >= self.n_cols or obj.y < 0 or obj.y >= self.n_rows:
                    self.game_over = True
                    break
            
            for obj in self.active_objects():
                for i in range(1, len(obj.body)):
                    if obj.body[0].x == obj.body[i].x and obj.body[0].y == obj.body[i].y:
                        self.game_over = True
                        break
            
            for i in range(len(self.objects[1].body)):
                if self.objects[0].body[0].between(self.objects[1].body[i]):
                    self.game_over = True
                    break
            for i in range(len(self.objects[0].body)):
                if self.objects[1].body[0].between(self.objects[0].body[i]):
                    self.game_over = True
                    break
            
            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)