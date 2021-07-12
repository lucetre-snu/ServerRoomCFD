import pygame
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Game:
    block_size = 10
    def __init__(self, n_cols, n_rows):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.display = pygame.display.set_mode((n_cols* self.block_size,n_rows* self.block_size))
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.object = []
        self.body = [Head(20, 30, self)]
        self.body1 = [Head(60, 30, self)]

    def active_object(self):
        T = []
        for obj in self.object:
            if obj.active:
                T.append(obj)
        return T

    def play(self, n_foods = 20):
        # Body + Food
        self.object = [
            *self.body,
            *self.body1,
            *[Food(self) for _ in range(n_foods)]]

        speed1 = 1
        speed2 = 1

        self.body1[0].color = RED

        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT:
                        speed1 = 2

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT:
                        speed1 = 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        speed2 = 2

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        speed2 = 1
                
                # Handle event
                for obj in self.body:
                    obj.handle_event(event)

                for obj in self.body1:
                    obj.handle_event1(event)

            # Location Backup
            X1 = []
            Y1 = []
            X2 = []
            Y2 = []
            for i in range(len(self.body)):
                X1.append(self.body[i].x)
                Y1.append(self.body[i].y)

            for i in range(len(self.body1)):
                X2.append(self.body1[i].x)
                Y2.append(self.body1[i].y)

            x1 = None
            y1 = None
            x2 = None
            y2 = None

            # Interact
            for obj1 in self.active_object():
                for obj2 in self.active_object():
                    obj1.interact(obj2)
                    obj2.interact(obj1)
                    if obj1.interact(obj2) != None:
                        t = 0
                        for i in range(len(self.body)):
                            if self.body[i] == obj1:
                                t += 1
                        if t > 0:
                            x1, y1 = obj1.interact(obj2)
                        else:
                            x2, y2 = obj1.interact(obj2)
                    if obj2.interact(obj1):
                        t = 0
                        for i in range(len(self.body)):
                            if self.body[i] == obj2:
                                t += 1
                        if t > 0:
                            x1, y1 = obj2.interact(obj1)
                        else:
                            x2, y2 = obj2.interact(obj1)
            
            # Tick
            if speed1 == 1 and speed2 == 1:
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]

                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]

            if speed1 == 2 and speed2 == 1:
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]
                X1 = []
                Y1 = []
                for i in range(len(self.body)):
                    X1.append(self.body[i].x)
                    Y1.append(self.body[i].y)
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]

                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]

            if speed1 == 1 and speed2 == 2:
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]

                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]
                X2 = []
                Y2 = []
                for i in range(len(self.body1)):
                    X2.append(self.body1[i].x)
                    Y2.append(self.body1[i].y)
                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]

            if speed1 == 2 and speed2 == 2:
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]
                X1 = []
                Y1 = []
                for i in range(len(self.body)):
                    X1.append(self.body[i].x)
                    Y1.append(self.body[i].y)
                for obj in self.body:
                    obj.tick()
                for i in range(len(self.body) - 1):
                    self.body[i+1].x = X1[i]
                    self.body[i+1].y = Y1[i]

                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]
                X2 = []
                Y2 = []
                for i in range(len(self.body1)):
                    X2.append(self.body1[i].x)
                    Y2.append(self.body1[i].y)
                for obj in self.body1:
                    obj.tick()
                for i in range(len(self.body1) - 1):
                    self.body1[i+1].x = X2[i]
                    self.body1[i+1].y = Y2[i]


            # Screen Check
            if self.body[0].x < 0 or self.body[0].x > self.n_cols or self.body[0].y < 0 or self.body[0].y > self.n_rows or self.body1[0].x < 0 or self.body1[0].x > self.n_cols or self.body1[0].y < 0 or self.body1[0].y > self.n_rows:
                self.game_over = True

            # Crash
            self.body[0].crash(self.body)
            self.body1[0].crash(self.body1)
            self.body[0].crash(self.body1)
            self.body1[0].crash(self.body)
                    
            # Food Complement
            T = self.active_object()
            if len(T) != n_foods + len(self.body) + len(self.body1):
                for _ in range(n_foods + len(self.body) + len(self.body1) - len(T)):
                    self.object.append(Food(self))

            # Making Tail
            if x1 != None:
                self.body[0].grow(x1, y1)
            if x2 != None:
                self.body1[0].grow1(x2, y2)

            # Draw
            self.display.fill(BLACK)
            for obj in self.active_object():
                obj.draw()
            
            pygame.display.update()
            
            # Global Decision
            food_remains = False            
            for obj in self.active_object():
                if isinstance(obj, Food):
                    food_remains = True

            if not food_remains:
                self.game_over = True

            self.clock.tick(5)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
    
    def handle_event(self, event):
        pass

    def tick(self):
        pass
    
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass

class Player(GridObject):
    dx = 0
    dy = 0
    color = WHITE

    def __init__(self, x, y, game):
        self.game = game
        super().__init__(x, y, self.game, self.color)

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx, self.dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                self.dx, self.dy = 1, 0
            elif event.key == pygame.K_UP:
                self.dx, self.dy = 0, -1
            elif event.key == pygame.K_DOWN:
                self.dx, self.dy = 0, 1   

    def handle_event1(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx, self.dy = -1, 0
            elif event.key == pygame.K_d:
                self.dx, self.dy = 1, 0
            elif event.key == pygame.K_w:
                self.dx, self.dy = 0, -1
            elif event.key == pygame.K_s:
                self.dx, self.dy = 0, 1                

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False
                return other.x, other.y

    def grow(self, x, y):
        self.game.body.append(Player(x,y,self.game))
        self.game.object.append(self.game.body[len(self.game.body)-1])

    def grow1(self, x, y):
        self.game.body1.append(Player(x,y,self.game))
        self.game.body1[len(self.game.body1)-1].color = (100,100,100)
        self.game.object.append(self.game.body1[len(self.game.body1)-1])

class Head(Player):
    color = BLUE
    def __init__(self, x, y, game):
        super().__init__(x, y, game)

    def tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def crash(self, body):
        for i in range(len(body)-1):
            if self.x == body[i+1].x and self.y == body[i+1].y:
                self.game.game_over = True

class Food(GridObject):
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)

if __name__ == '__main__':
    Game(80, 60).play(20)