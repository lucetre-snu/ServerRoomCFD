import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY_RED = (255, 155, 155)
GREY_GREEN = (155, 255, 155)
GREY_BLUE = (155, 155, 255)

pygame.init()

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
        if isinstance(self, Food):
            pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        elif isinstance(self, Player):
            pygame.draw.rect(self.game.display, self.head_color, [self.head()[0] * block_size, self.head()[1] * block_size, block_size, block_size])
            for i in self.body():
                pygame.draw.rect(self.game.display, self.body_color, [i[0] * block_size, i[1] * block_size, block_size, block_size])

    def interact(self, other):
        pass

class Player(Gridobject):
    dx = 0 
    dy = 0
    head_color = BLUE
    body_color = GREY_BLUE
    color = WHITE

    def __init__(self, x, y, game, color):
        super().__init__(x, y, game, self.color)

    
class Player1(Player):
    dx = 0 
    dy = 0
    head_color = BLUE
    body_color = GREY_BLUE
    color = WHITE

    def __init__(self, x, y, game, color):
        super().__init__(x, y, game, self.color)
        global length1
        length1 = [[self.x, self.y]]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.dx != 1: 
                self.dx = - 1 
                self.dy = 0 
            elif event.key == pygame.K_RIGHT and self.dx != -1:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP and self.dy != 1:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_DOWN and self.dy != -1:
                self.dx = 0
                self.dy = 1
    
    def head(self):
        return length1[0]

    def body(self):
        return length1[1:]
     
    def tick(self):
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_RSHIFT]:
            boost = 2
        else:
            boost = 1
            
        for i in range(0, boost):
            length1.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])   
            del length1[-1]
            

 
    def interact(self, other):
        if isinstance(other, Food):
            if [other.x, other.y] in length1:
                length1.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])
                other.active = False
                self.game.objects.append(Food(self.game)) 
                


class Player2(Player):
    dx = 0 
    dy = 0
    head_color = RED
    body_color = GREY_RED
    color = WHITE

    def __init__(self, x, y, game, color):
        super().__init__(x, y, game, self.color)
        global length2
        length2 = [[self.x, self.y]]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and self.dx != 1: 
                self.dx = - 1 
                self.dy = 0 
            elif event.key == pygame.K_d and self.dx != -1:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_w and self.dy != 1:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_s and self.dy != -1:
                self.dx = 0
                self.dy = 1

    def head(self):
        return length2[0]

    def body(self):
        return length2[1:]
     
    def tick(self):
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            boost = 2
        else:
            boost = 1
            
        for i in range(0, boost):
            length2.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])   
            del length2[-1]
            

    def interact(self, other):
        if isinstance(other, Food):
            if [other.x, other.y] in length2:
                length2.insert(0, [self.head()[0] + self.dx, self.head()[1] + self.dy])
                other.active = False
                self.game.objects.append(Food(self.game))


class Food(Gridobject):
    color = GREEN    
    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)


class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
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
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1.active and obj2.active:
                    obj1.interact(obj2)
                    obj2.interact(obj1)
    
    def __end__(self):
        if not (0 <= Player1.head(Player1)[0] <= self.n_cols - 1 and 0 <= Player1.head(Player1)[1] <= self.n_rows - 1):
            self.game_over = True
        
        if not (0 <= Player2.head(Player2)[0] <= self.n_cols - 1 and 0 <= Player2.head(Player2)[1] <= self.n_rows - 1):
            self.game_over = True
        
        if Player1.head(Player1) in Player1.body(Player1): 
            self.game_over = True

        if Player2.head(Player2) in Player2.body(Player2):
            self.game_over = True

        if Player1.head(Player1) in length2 or Player2.head(Player2) in length1:
            self.game_over = True


    def play(self, n_foods = 20):
        self.objects = [
            Player1(60, 30, self, Player1.color), Player2(20,30, self, Player2.color),
            *[Food(self) for _ in range(n_foods)]
        ]
        while not self.game_over:
            
            self.__handle__event()

            self.__interact__()

            self.__tick__()

            self.display.fill(BLACK)

            self.__draw__()

            pygame.display.update()

            self.__end__()
            
            self.clock.tick(10)
        
        pygame.quit()


if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)