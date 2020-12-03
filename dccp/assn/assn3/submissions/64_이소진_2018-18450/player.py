import pygame
from colors import PINK, RED, SKYBLUE, BLUE
from food import Food

player_color = [(PINK, RED), (SKYBLUE, BLUE)]
player_key = [
    (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT),
    (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT)
]

class GridObject1:
    def __init__(self, x, y, game, color):
        self.x = x
        self.y = y
        self.game = game
        self.color = color
        self.active = True

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def food_generate(self, other):              
        other.active = False
        self.game.objects.append(Food(self.game))    # 새로운 food를 list에 생성

    def tail_generate(self):
        self.n_tail += 1     
        self.game.objects.append(Tail(self))
        self.x += self.dx
        self.y += self.dy
                
    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                self.food_generate(other)
                self.tail_generate()
        if self is not other and isinstance(other, Player):
            if self.x == other.x and self.y == other.y:
                self.game.game_over = True

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
    
class Player(GridObject1):
    __index = 0
    dx = 0
    dy = 0

    def __init__(self, x, y, game):
        self.movement_x = []
        self.movement_y = []
        self.n_tail = 0
        self.index = Player.__index
        self.color_head = player_color[self.index][0]
        self.color_tail = player_color[self.index][1]
        super().__init__(x, y, game, self.color_head)
        Player.__index += 1
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == player_key[self.index][0]:
                self.dx = -1
                self.dy = 0
            elif event.key == player_key[self.index][1]:
                self.dx = 1
                self.dy = 0
            elif event.key == player_key[self.index][2]:
                self.dy = -1
                self.dx = 0
            elif event.key == player_key[self.index][3]:
                self.dy = 1
                self.dx = 0

    def remember(self, x, y):
        self.movement_x.append(x)
        self.movement_y.append(y)
        
    def __for_memory(self):
        del self.movement_x[0]
        del self.movement_y[0]
    
    def tick(self):
        pressed_key = pygame.key.get_pressed()
        if self.n_tail >= 1:
            if self.x + self.dx == self.movement_x[-1] and self.y + self.dy == self.movement_y[-1]:
                self.game.game_over = True
        self.remember(self.x, self.y)
        if pressed_key[player_key[self.index][4]]:    # boost!
            self.x += self.dx
            self.y += self.dy
            self.remember(self.x, self.y)
            self.__for_memory()
        self.x += self.dx
        self.y += self.dy
        self.__for_memory()
    
    def tail_generate(self):
        self.remember(self.x, self.y)
        super().tail_generate()
    
class Tail(GridObject1):
    def __init__(self, head):
        self.head = head
        self.index = self.head.n_tail
        self.x = self.head.movement_x[-1]
        self.y = self.head.movement_y[-1]
        super().__init__(self.x, self.y, self.head.game, self.head.color_tail)
    
    def tick(self):
        self.x = self.head.movement_x[-1 + self.index - self.head.n_tail]
        self.y = self.head.movement_y[-1 + self.index - self.head.n_tail]
    
    def tail_generate(self):
        self.head.remember(self.head.x, self.head.y)
        self.head.n_tail += 1     
        self.head.game.objects.append(Tail(self.head))
        self.head.x += self.head.dx
        self.head.y += self.head.dy

    def interact(self, other):
        super().interact(other)
        if self is not other and isinstance(other, Tail):
            if self.x == other.x and self.y == other.y:
                self.game.game_over = True