import random
import pygame

White, Black, Red, Green, Blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

class GridObject:
    def __init__(self, x, y, game, color):
        self.x, self.y = x, y #grid column index, row index
        self.game = game
        self.active = True
        self.color = color
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
    dx, dy, boost = 0, 0, 1
    color = (144, 213, 235) #lighter skyblue
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)
        self.bodylist = []
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: self.dx, self.dy = -1, 0 #grid size 고려 X
            elif event.key == pygame.K_RIGHT: self.dx, self.dy = 1, 0
            elif event.key == pygame.K_UP: self.dx, self.dy = 0, -1
            elif event.key == pygame.K_DOWN: self.dx, self.dy = 0, 1
            elif event.key == pygame.K_RSHIFT: self.boost = 2
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_RSHIFT: self.boost = 1
    def tick(self):
        self.x += self.dx*self.boost
        self.y += self.dy*self.boost
        if self.x not in range(self.game.n_cols-1) or self.y not in range(self.game.n_rows-1): 
            self.game.game_over = True
        self.grow()
    def interact(self, other): 
        if self.x == other.x and self.y == other.y: 
            if isinstance(other, Food) and other.active == True: 
                other.active = False
                self.game.objects.append(Food(self.game))
                self.game.objects.append(PlayerBody(self, (80, 188, 223), self.game))
            if isinstance(other, PlayerBody) or isinstance(other, Player2):
                self.game.game_over = True
    def grow(self):
        if self.bodylist: #몸통 그리기
            if self.boost == 1 or (self.boost == 2 and len(self.bodylist) == 1):
                last = self.bodylist[0]
                last.x, last.y = self.x - self.dx, self.y - self.dy
                self.bodylist.remove(last)
                self.bodylist.append(last)
            else:
                a = self.bodylist[0]
                b = self.bodylist[1]
                a.x, a.y = self.x - self.dx, self.y - self.dy
                b.x, b.y = self.x - self.dx*2, self.y - self.dy*2
                self.bodylist.remove(a)
                self.bodylist.remove(b)
                self.bodylist += [b, a]
            
class PlayerBody(GridObject):
    def __init__(self, player, color, game):
        self.player = player
        self.color = color
        x = self.player.x - self.player.dx
        y = self.player.y - self.player.dy
        super().__init__(x, y, game, self.color)
        self.player.bodylist.append(self)
    def interact(self, other): 
        if self.x == other.x and self.y == other.y: 
            if isinstance(other, Food) and other.active == True: 
                other.active = False
                self.game.objects.append(Food(self.game))
                self.game.objects.append(PlayerBody(self.player, self.color, self.game))

class Player2(Player):
    color = (255, 192, 203) #lighter pink
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: self.dx, self.dy = -1, 0 #grid size 고려 X
            elif event.key == pygame.K_d: self.dx, self.dy = 1, 0
            elif event.key == pygame.K_w: self.dx, self.dy = 0, -1
            elif event.key == pygame.K_s: self.dx, self.dy = 0, 1
            elif event.key == pygame.K_LSHIFT: self.boost = 2
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LSHIFT: self.boost = 1
    def interact(self, other): 
        if self.x == other.x and self.y == other.y: 
            if isinstance(other, Food) and other.active == True: 
                other.active = False
                self.game.objects.append(Food(self.game))
                self.game.objects.append(PlayerBody(self, (255, 103, 129), self.game))
            if isinstance(other, PlayerBody) or (isinstance(other, Player) and other != self):
                self.game.game_over = True

class Food(GridObject):
    color = Green
    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1) #x가 10~800
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('My Snake Game')
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size)) 
        self.n_rows, self.n_cols = n_rows, n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = [] 
    def active_objects(self):
        for obj in self.objects:
            if obj.active: yield obj
    def __handle__event(self, event):
        for obj in self.active_objects(): 
            obj.handle_event(event)
    def __tick__(self):
        for obj in self.active_objects(): 
            obj.tick()
    def __interact__(self):
        for obj1 in self.active_objects():
            for obj2 in self.active_objects():
                obj1.interact(obj2)
                obj2.interact(obj1)
    def __draw__(self):
        self.display.fill(Black)
        for obj in self.active_objects(): 
            obj.draw()
        pygame.display.update()
    def play(self, n_foods=20):
        self.objects = [
            *[Food(self) for _ in range(n_foods)],
            Player(60, 30, self),
            Player2(20, 30, self)
        ]
        while not self.game_over: #main display loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                self.__handle__event(event) 
            self.__tick__() 
            self.__interact__()
            self.__draw__()
            self.clock.tick(10) 

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)