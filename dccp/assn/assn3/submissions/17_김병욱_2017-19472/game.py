import pygame
import random

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
        self.x = x # grid column index
        self.y = y # grid row index

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def trace(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, 10, 10])

    def interact(self, other):
        pass

class Player1(GridObject):
    dx = 0
    dy = 0
    color = (100, 100, 255)

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)
        self.traceX = x
        self.traceY = y
        self.type = 'Player'
        self.tail = self
        self.speed = 1

    def handle_event(self, event):
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

    def speedChange(self, event, v):
        speed = v 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RSHIFT:
                speed = 2
                self.speed = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                speed = 1
                self.speed = 1
        return speed

    def tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def trace(self):
        self.traceX = self.x
        self.traceY = self.y

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.x = random.randint(0, other.game.n_cols - 1) 
                other.y = random.randint(0, other.game.n_rows - 1)

class Player2(GridObject):
    dx = 0
    dy = 0
    color = (255, 100, 100)

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)
        self.traceX = x
        self.traceY = y
        self.type = 'Player'
        self.tail = self
        self.speed = 1

    def handle_event(self, event):
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

    def speedChange(self, event, v):
        speed = v
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LSHIFT:
                speed = 2
                self.speed = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speed = 1
                self.speed = 1
        return speed


    def tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def trace(self):
        self.traceX = self.x
        self.traceY = self.y

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.x = random.randint(0, other.game.n_cols - 1) 
                other.y = random.randint(0, other.game.n_rows - 1)
                
class Tail1(GridObject):
    color = BLUE
    
    def __init__(self, x, y, game, tail):
        self.type = 'Tail'
        self.tail = tail
        self.traceX = x
        self.traceY = y
        super().__init__(x, y, game, self.color)
    
    def tick(self):
        self.x = self.tail.traceX 
        self.y = self.tail.traceY
    
    def trace(self):
        self.traceX = self.x
        self.traceY = self.y

class Tail2(GridObject):
    color = RED
    
    def __init__(self, x, y, game, tail):
        self.type = 'Tail'
        self.tail = tail
        self.traceX = x
        self.traceY = y
        super().__init__(x, y, game, self.color)
    
    def tick(self):
        self.x = self.tail.traceX 
        self.y = self.tail.traceY
    
    def trace(self):
        self.traceX = self.x
        self.traceY = self.y

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1) 
        y = random.randint(0, game.n_rows - 1)
        self.type = 'Food'
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('BangWook Snake Game')
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
    
    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def play(self, n_foods=20):
        self.objects = [
            Player1(60, 30, self),
            Player2(20, 30, self),
            *[Food(self) for i in range(n_foods)]
        ]
        
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                
                # Handle Event
                for obj in self.active_objects():
                    if (type(obj) == Player1):
                        P1speed = obj.speedChange(event, obj.speed)
                    elif (type(obj) == Player2):
                        P2speed = obj.speedChange(event, obj.speed)
                    obj.handle_event(event)  
            
            for i in range(P1speed): # speed control
                # Tick
                for obj in self.active_objects():
                    if (type(obj) == Player1 or type(obj) == Tail1):               
                        obj.trace()
                        obj.tick()

                # Interact
                for obj1 in self.active_objects():
                    for obj2 in self.active_objects():
                        if (obj1.x == obj2.x and obj1.y == obj2.y):
                            if (type(obj1) == Player1 and obj2.type == 'Food'):
                                self.objects.append(Tail1(obj1.traceX, obj1.traceY, self, obj1.tail))
                                obj1.tail = self.objects[-1]
                        obj1.interact(obj2)
                        obj2.interact(obj1)
            for i in range(P2speed):
                # Tick
                for obj in self.active_objects():
                    if (type(obj) == Player2 or type(obj) == Tail2):               
                        obj.trace()
                        obj.tick()

                # Interact
                for obj1 in self.active_objects():
                    for obj2 in self.active_objects():
                        if (obj1.x == obj2.x and obj1.y == obj2.y):
                            if (type(obj1) == Player2 and obj2.type == 'Food'):
                                self.objects.append(Tail2(obj1.traceX, obj1.traceY, self, obj1.tail))
                                obj1.tail = self.objects[-1]
                        obj1.interact(obj2)
                        obj2.interact(obj1)
                            
            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()

            # Global Decision
            food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food) and obj.active:
                    food_remains = True    
            if not food_remains:
                self.game_over = True
            
            for obj in self.active_objects():
                if obj.type == 'Player' and obj.active:
                    if (obj.x < 0 or obj.x > 79) or (obj.y < 0 or obj.y > 59):
                        self.game_over = True
            
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    if obj1.type == 'Player' and obj2.type == 'Tail':
                        if (obj1.x == obj2.x and obj1.y == obj2.y):
                            self.game_over = True
                    elif type(obj1) == Player1 and type(obj2) == Player2:
                        if (obj1.x == obj2.x and obj1.y == obj2.y):
                            self.game_over = True
        
            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)
