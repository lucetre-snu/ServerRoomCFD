import random
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
magenta =(255, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
mint = (0, 255, 255)
blue = (0, 0, 255)

class Grid_object:
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

    def interact(self, other, game):
        pass


class Player(Grid_object):
    dx = 0
    dy = 0
    length = 1
    color = (0,0,0)
    t_color = (0,0,0)
    trace = []

    def __init__(self, x, y, game, color, t_color, left, right, up, down, boost = False):
        super().__init__(x, y, game, self.color)
        self.boost = boost
        self.color = color
        self.t_color = t_color
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.crash = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.left:
                self.dx = -1
                self.dy = 0
            elif event.key == self.right:
                self.dx = 1
                self.dy = 0
            elif event.key == self.up:
                self.dx = 0
                self.dy = -1
            elif event.key == self.down:
                self.dx = 0
                self.dy = 1

    def tick(self):
        if self.boost == False:
            self.trace.insert(0,(self.x, self.y))
            self.trace = self.trace[0 : self.length - 1]
            self.x += self.dx
            self.y += self.dy
        else:
            self.trace.insert(0,(self.x, self.y))
            self.trace.insert(0,(self.x + self.dx, self.y + self.dy))
            self.trace = self.trace[0 : self.length - 1]
            self.x += 2 * self.dx
            self.y += 2 * self.dy            

    
    def interact(self, other, game):
        if isinstance(other, Food):
            if self.boost == False:
                if self.x == other.x and self.y == other.y:
                    other. x = random.randint(0, game.n_cols - 1)
                    other. y = random.randint(0, game.n_rows - 1)
                    self.length += 1
            else:
                if self.x == other.x and self.y == other.y:
                    other. x = random.randint(0, game.n_cols - 1)
                    other. y = random.randint(0, game.n_rows - 1)
                    self.length += 1
                elif self.x - self.dx == other.x and self.y - self.dy == other.y:
                    other. x = random.randint(0, game.n_cols - 1)
                    other. y = random.randint(0, game.n_rows - 1)
                    self.length += 1

        if isinstance(other, Player):
            if self.trace != []:
                for ele in [(self.x, self.y),*self.trace]:
                    if ele in [(other.x, other.y), *other.trace]:
                        self.crash = True
            else:
                if self.boost == True:
                    for ele in [(self.x, self.y), (self.x - self.dx, self.y - self.dy)]:
                        if ele in [(other.x, other.y), *other.trace]:
                            self.crash = True                


    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        for x, y in self.trace:
            pygame.draw.rect(self.game.display, self.t_color, [x * block_size, y * block_size, block_size, block_size])
      





class Food(Grid_object):
    color = green

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1) 
        super().__init__(x, y, game, self.color)

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])


class Game:
    block_size = 10
    def __init__(self, n_cols, n_rows):
        pygame.init()
        pygame.display.set_caption('dccp102 Snake Game')
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.Lshift = False
        self.Rshift = False

    def play(self, n_foods = 20):
        self.objects = [
            Player(70, 30, self, magenta, red, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN),
            Player(30, 30, self, mint, blue, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s),
            *[Food(self) for _ in range(n_foods)]
        ]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break                

                for obj in self.objects:
                    if obj.active:
                        obj.handle_event(event)

            self.Lshift = pygame.key.get_pressed()[pygame.K_LSHIFT]
            self.Rshift = pygame.key.get_pressed()[pygame.K_RSHIFT]

            self.objects[0].boost = self.Rshift
            self.objects[1].boost = self.Lshift

            for obj in self.objects:
                if obj.active:
                    obj.tick()

            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1 != obj2:
                        if obj1.active and obj2.active:
                            obj1.interact(obj2, self)
                            obj2.interact(obj1, self)



            self.display.fill(black)
            for obj in self.objects:
                if obj.active:
                    obj.draw()
            pygame.display.update()


            food_remains = False
            for obj in self.objects:
                if isinstance(obj, Food) and obj.active:
                    food_remains = True

            if not food_remains:
                self.game_over = True

            if  0 <= self.objects[0].x < self.n_cols and 0 <= self.objects[0].y < self.n_rows:
                pass
            else:
                self.game_over = True 
            if  0 <= self.objects[1].x < self.n_cols and 0 <= self.objects[1].y < self.n_rows:
                pass
            else:
                self.game_over = True 

            for ele in self.objects[0].trace:
                if (self.objects[0].x, self.objects[0].y) == ele:
                    self.game_over = True
            for ele in self.objects[1].trace:
                if (self.objects[1].x, self.objects[1].y) == ele:
                    self.game_over = True
            if self.objects[0].crash == True or self.objects[1].crash == True:
                self.game_over = True

            self.clock.tick(10)  


if __name__ == '__main__':
    Game(n_cols=100, n_rows=60 ).play(n_foods=20)
        