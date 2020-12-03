import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class GridObject:
    def __init__(self, x, y, game, color):
        self.x = x
        self.y = y
        self.game = game
        self.active = True
        self.color = color

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size=self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

class Player(GridObject):
    color = WHITE
    dx = 0
    dy = 0

    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN :
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

    def tick(self):
        self.x += self.dx
        self.y += self.dy

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False


class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_cols - 1)
        super().__init__(x, y, game, self.color)

    def interact(self, other):
        pass

class Game:
    def __init__(self, n_rows, n_cols, block_size):
        pygame.init()
        pygame.display.set_caption('DCCP snake game')
        self.display = pygame.display.set_mode((n_rows * block_size, n_cols * block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.block_size = block_size
        self.clock = pygame.time.Clock()
        self.game_over = False

    def play(self, x_st, y_st, n_foods, ticks):
        self.objects = [
            Player(x_st, y_st, self),
            *[Food(self) for _ in range(n_foods)]
        ]

        while not self.game_over:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT: #or event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    break
                for obj in self.objects:
                    if obj.active:
                        obj.handle_event(event)

            for obj in self.objects:
                if obj.active:
                    obj.tick()
                    
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1.active and obj2.active:
                        a = int(obj1.active)+int(obj2.active)
                        obj1.interact(obj2)
                        obj2.interact(obj1)
                        if a != int(obj1.active)+int(obj2.active):
                            self.objects.append(Food(self))

            self.display.fill(BLACK)
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

            self.clock.tick(ticks)

if __name__=="__main__":
    Game(n_rows=80, n_cols=60, block_size=10).play(x_st=40, y_st=30, n_foods=20, ticks=10)
