import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

class Gridobject:
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
        block_size = Game.block_size
        if isinstance(self, Player):
            pygame.draw.rect(self.game.display, self.headcolor, [self.head()[0] * block_size, self.head()[1] * block_size, block_size, block_size])
            for i in self.body():
                pygame.draw.rect(self.game.display, self.bodycolor, [i[0] * block_size, i[1] * block_size, block_size, block_size])
        elif isinstance(self, Food):
            pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass


class Player(Gridobject):
    dx = 0 
    dy = 0
    
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

class Player_1(Player):        
    
    headcolor = BLUE
    bodycolor = CYAN
    color = WHITE

    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        global whole_1
        whole_1 = [[self.x, self.y]]
    
    def head(self):
        return whole_1[0]
    def body(self):
        return whole_1[1:]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_LEFT: 
                self.dx = - 1
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
    
    def tick(self):
        pressed_key =  pygame.key.get_pressed()
        if pressed_key[pygame.K_RSHIFT]:
            boost = 2
        else:
            boost = 1
            
        for i in range (boost):
            whole_1.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])   
            if len(whole_1) == 3 and whole_1[0] == whole_1[-1]:
                self.game.game_over = True    
            del whole_1[-1]

    def interact(self, other):
        if isinstance(other, Food):
            if [other.x, other.y] in whole_1:
                whole_1.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])

class Player_2(Player):        
    
    headcolor = RED
    bodycolor = MAGENTA
    color = WHITE

    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        global whole_2
        whole_2 = [[self.x, self.y]]
    
    def head(self):
        return whole_2[0]
    def body(self):
        return whole_2[1:]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_a: 
                self.dx = - 1
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
    
    def tick(self):
        pressed_key =  pygame.key.get_pressed()
        if pressed_key[pygame.K_LSHIFT]:
            boost = 2
        else:
            boost = 1
            
        for i in range (boost):
            whole_2.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])   
            if len(whole_2) == 3 and whole_2[0] == whole_2[-1]:
                self.game.game_over = True
            del whole_2[-1]
        
    def interact(self, other):
        if isinstance(other, Food):
            if [other.x, other.y] in whole_2:
                whole_2.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])
    
class Food(Gridobject):
    color = GREEN    
    
    def __init__(self, game):
        x = random.randint(0, game.n_cols-1)
        y = random.randint(0, game.n_rows-1)
        super().__init__(x, y, game, self.color)

    def interact(self, other):
        if (isinstance(other, Player_1) and [self.x, self.y] in whole_1) or (isinstance(other, Player_2) and [self.x, self.y] in whole_2):
            self.active = False
            self.game.objects.append(Food(self.game))
        
class Game:
    block_size = 10
    
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.display=pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def __handle__event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                break
            for obj in self.active_objects(): 
                obj.handle_event(event)

    def __tick__(self):
        for obj in self.active_objects():           
            obj.tick()    

    def __draw__(self):
        for obj in self.active_objects(): 
            obj.draw()

    def __interact__(self):
        for obj1 in self.active_objects():
            for obj2 in self.active_objects():
                obj2.interact(obj1)
                obj1.interact(obj2)  
    
    def __end__(self):
        if Player_1.head(Player_1)[0] < 0 or Player_1.head(Player_1)[0] > self.n_cols or Player_1.head(Player_1)[1] < 0 or Player_1.head(Player_1)[1] > self.n_rows:
            self.game_over = True
        if Player_2.head(Player_2)[0] < 0 or Player_2.head(Player_2)[0] > self.n_cols or Player_2.head(Player_2)[1] < 0 or Player_2.head(Player_2)[1] > self.n_rows:
            self.game_over = True    
        if Player_1.head(Player_1) in Player_1.body(Player_1) or Player_1.head(Player_1) in whole_2:
            self.game_over = True
        if Player_2.head(Player_2) in Player_2.body(Player_2) or Player_2.head(Player_2) in whole_1:
            self.game_over = True     

    def play(self, n_foods = 20):
        self.objects = [Player_1(60, 45, self), Player_2(20, 15, self), *[Food(self) for i in range(n_foods)]]
        while not self.game_over:
            self.__handle__event()

            self.__tick__()

            self.__interact__()

            self.display.fill(BLACK)

            self.__draw__()

            self.__end__()
           
            pygame.display.update()

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)
    