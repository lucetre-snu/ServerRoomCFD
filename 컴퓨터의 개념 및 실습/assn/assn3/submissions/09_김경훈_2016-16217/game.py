import pygame
import random
from pygame.constants import QUIT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (80, 188, 223)

def tuple_minus(x, y):
    return (x[0] - y[0], x[1] - y[1])


class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x       # grid col index
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
    snake_body = []
    prev_position = []
    body_color = RED
    prev_event = None
    speedKey = pygame.K_RSHIFT

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.prev_event == pygame.K_RIGHT:
                    return
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_DOWN:
                if self.prev_event == pygame.K_UP:
                    return
                self.dy = 1
                self.dx = 0
            elif event.key == pygame.K_UP:
                if self.prev_event == pygame.K_DOWN:
                    return
                self.dy = -1
                self.dx = 0
            elif event.key == pygame.K_RIGHT:
                if self.prev_event == pygame.K_LEFT:
                    return
                self.dx = 1
                self.dy = 0
            self.prev_event = event.key

    def tick(self):
        self.prev_position = [(self.x, self.y)]
        self.prev_position.extend(self.snake_body)
        if self.snake_body:
            self.snake_body[0] = (self.x, self.y)
            for num in range(1, len(self.snake_body)):
                self.snake_body[num] = self.prev_position[num]
        if pygame.key.get_pressed()[self.speedKey]:
            self.x += 2*self.dx
            self.y += 2*self.dy
            if self.snake_body:
                if self.dx == -1 and self.dy == 0:
                    self.snake_body[0] = (self.x+1, self.y)
                elif self.dx == 1 and self.dy == 0:
                    self.snake_body[0] = (self.x-1, self.y)
                elif self.dx == 0 and self.dy == -1:
                    self.snake_body[0] = (self.x, self.y+1)
                elif self.dx == 0 and self.dy == 1:
                    self.snake_body[0] = (self.x, self.y-1)    
            for num in range(1, len(self.snake_body)):
                self.snake_body[num] = self.prev_position[num-1]
        else:
            self.x += self.dx
            self.y += self.dy


    def interact(self, other):
        if isinstance(other, Food):
            if pygame.key.get_pressed()[self.speedKey]:    
                if self.dx == -1 and self.dy == 0:
                    if (self.x, self.y) == (other.x, other.y) or (self.x+1, self.y) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 1 and self.dy == 0:
                    if (self.x, self.y) == (other.x, other.y) or (self.x-1, self.y) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 0 and self.dy == -1:
                    if (self.x, self.y) == (other.x, other.y) or (self.x, self.y+1) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 0 and self.dy == 1:
                    if (self.x, self.y) == (other.x, other.y) or (self.x, self.y-1) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
            else:
                if self.x == other.x and self.y == other.y:
                    other.active = False
                    self.increase_size()

    def increase_size(self):
        if pygame.key.get_pressed()[self.speedKey]:
            if self.snake_body:
                if tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (2,0): #right
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-2,0): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (0,2): 
                    self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]+1))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (0,-2): 
                    self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]-1))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (1,-1): 
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-1,-1): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-1,1): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (1,1): 
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
            else:
                if (self.dx, self.dy) == (1,0):
                    self.snake_body.append((self.x-1, self.y))
                elif (self.dx, self.dy) == (-1,0):
                    self.snake_body.append((self.x+1, self.y))
                elif (self.dx, self.dy) == (0,1):
                    self.snake_body.append((self.x, self.y-1))
                elif (self.dx, self.dy) == (0,-1):
                    self.snake_body.append((self.x, self.y+1))
        else:
            self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]))

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        for i in self.snake_body:
            pygame.draw.rect(self.game.display, self.body_color, [i[0] * block_size, i[1] * block_size, block_size, block_size])


class Player2(GridObject):
    dx = 0
    dy = 0
    color = BLUE
    body_color = YELLOW
    snake_body = []
    prev_position = []
    prev_event = None
    speedKey = pygame.K_LSHIFT

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.prev_event == pygame.K_d:
                    return
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_s:
                if self.prev_event == pygame.K_w:
                    return
                self.dy = 1
                self.dx = 0
            elif event.key == pygame.K_w:
                if self.prev_event == pygame.K_s:
                    return
                self.dy = -1
                self.dx = 0
            elif event.key == pygame.K_d:
                if self.prev_event == pygame.K_a:
                    return
                self.dx = 1
                self.dy = 0
            self.prev_event = event.key

    def tick(self):
        self.prev_position = [(self.x, self.y)]
        self.prev_position.extend(self.snake_body)
        if self.snake_body:
            self.snake_body[0] = (self.x, self.y)
            for num in range(1, len(self.snake_body)):
                self.snake_body[num] = self.prev_position[num]
        if pygame.key.get_pressed()[self.speedKey]:
            self.x += 2*self.dx
            self.y += 2*self.dy
            if self.snake_body:
                if self.dx == -1 and self.dy == 0:
                    self.snake_body[0] = (self.x+1, self.y)
                elif self.dx == 1 and self.dy == 0:
                    self.snake_body[0] = (self.x-1, self.y)
                elif self.dx == 0 and self.dy == -1:
                    self.snake_body[0] = (self.x, self.y+1)
                elif self.dx == 0 and self.dy == 1:
                    self.snake_body[0] = (self.x, self.y-1)    
            for num in range(1, len(self.snake_body)):
                self.snake_body[num] = self.prev_position[num-1]
        else:
            self.x += self.dx
            self.y += self.dy


    def interact(self, other):
        if isinstance(other, Food):
            if pygame.key.get_pressed()[self.speedKey]:    
                if self.dx == -1 and self.dy == 0:
                    if (self.x, self.y) == (other.x, other.y) or (self.x+1, self.y) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 1 and self.dy == 0:
                    if (self.x, self.y) == (other.x, other.y) or (self.x-1, self.y) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 0 and self.dy == -1:
                    if (self.x, self.y) == (other.x, other.y) or (self.x, self.y+1) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
                elif self.dx == 0 and self.dy == 1:
                    if (self.x, self.y) == (other.x, other.y) or (self.x, self.y-1) == (other.x, other.y):
                        other.active = False
                        self.increase_size()
            else:
                if self.x == other.x and self.y == other.y:
                    other.active = False
                    self.increase_size()

    def increase_size(self):
        if pygame.key.get_pressed()[self.speedKey]:
            if self.snake_body:
                if tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (2,0): #right
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-2,0): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (0,2): 
                    self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]+1))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (0,-2): 
                    self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]-1))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (1,-1): 
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-1,-1): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (-1,1): 
                    self.snake_body.append((self.prev_position[-1][0]-1, self.prev_position[-1][1]))
                elif tuple_minus(self.snake_body[-1] , self.prev_position[-1]) == (1,1): 
                    self.snake_body.append((self.prev_position[-1][0]+1, self.prev_position[-1][1]))
            else:
                if (self.dx, self.dy) == (1,0):
                    self.snake_body.append((self.x-1, self.y))
                elif (self.dx, self.dy) == (-1,0):
                    self.snake_body.append((self.x+1, self.y))
                elif (self.dx, self.dy) == (0,1):
                    self.snake_body.append((self.x, self.y-1))
                elif (self.dx, self.dy) == (0,-1):
                    self.snake_body.append((self.x, self.y+1))
        else:
            self.snake_body.append((self.prev_position[-1][0], self.prev_position[-1][1]))

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        for i in self.snake_body:
            pygame.draw.rect(self.game.display, self.body_color, [i[0] * block_size, i[1] * block_size, block_size, block_size])



            

class Food(GridObject):
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.n_cols- 1)
        y = random.randint(0, game.n_rows-1)
        super().__init__(x, y, game, self.color)

    def interact(self, other):
        if not self.active:
            self.__init__(self.game)





class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows * self.block_size))
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
            Player(50, 30, self), 
            Player2(30, 30, self),
            *[Food(self) for _ in range(n_foods)]
        ]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
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

            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()

            # Global Decision
            '''food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains = True
            if not food_remains:
                self.game_over = True'''

            # terminate condition
            for obj in self.active_objects():
                if isinstance(obj, Player):
                    player1 = obj
                    temp1 = [(obj.x, obj.y)]
                    temp1.extend(obj.snake_body)
                    if obj.x < 0 or obj.x > self.n_cols or obj.y < 0 or obj.y > self.n_rows :
                        self.game_over = True
                    for i in range(1, len(temp1)):
                        if temp1[0] == temp1[i]:
                            self.game_over = True
                if isinstance(obj, Player2):
                    player2 = obj
                    temp2 = [(obj.x, obj.y)]
                    temp2.extend(obj.snake_body)
                    if obj.x < 0 or obj.x > self.n_cols or obj.y < 0 or obj.y > self.n_rows :
                        self.game_over = True
                    for i in range(1, len(temp2)):
                        if temp2[0] == temp2[i]:
                            self.game_over = True

            temp3 = [temp1[0]]
            temp4 = [temp2[0]]

            if pygame.key.get_pressed()[pygame.K_RSHIFT]:
                temp3.append((temp1[0][0]-player1.dx, temp1[0][1]-player1.dy)) # player1의 head.
                
            for pos2 in temp1:
                for pos1 in temp4:
                    if pos1 == pos2:
                        self.game_over = True

            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                temp4.append((temp2[0][0]-player2.dx, temp2[0][1]-player2.dy)) #player2의 head.


            for pos1 in temp2:
                for pos2 in temp3:
                    if pos2 == pos1:
                        self.game_over = True


            self.clock.tick(10)


if __name__ == "__main__":
    Game(n_rows = 60, n_cols = 80).play(n_foods = 20)