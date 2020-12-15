import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (150, 150, 255)

LSHIFT = 1073742049
RSHIFT = 1073742053
W = 119
A = 97
S = 115
D = 100

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y

    def handle_event(self, event):
        pass
    
    def interact(self, other):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    

class Player(GridObject):
    color = LIGHTRED
    dx = 0
    dy = 0
    
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)
        self.tails = []
        self.prevx = 0
        self.prevy = 0
        self.boost_on = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.dx != 1:
                    self.dx = -1
                    self.dy = 0
            elif event.key == pygame.K_RIGHT:
                if self.dx != -1:
                    self.dx = 1
                    self.dy = 0
            elif event.key == pygame.K_UP:
                if self.dy != 1:
                    self.dx = 0
                    self.dy = -1
            elif event.key == pygame.K_DOWN:
                if self.dy != -1:
                    self.dx = 0 
                    self.dy = 1

    def tick(self):
        self.prevx = self.x
        self.prevy = self.y
        for i in self.tails:
            i.tailtick()

        self.x += self.dx
        self.y += self.dy

    def interact(self, other):
        if isinstance(other, Food):
           if self.x == other.x and self.y == other.y:
               other.active = False
               other.eaten_by = self

    def isout(self):        
        rows = self.game.n_rows
        cols = self.game.n_cols
        if self.x < 0 or self.x >= cols or self.y < 0 or self.y >= rows:
            return True
        else:
            return False

class Player2(Player):
    color = LIGHTBLUE
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == A:
                if self.dx != 1:
                    self.dx = -1
                    self.dy = 0
            elif event.key == D:
                if self.dx != -1:
                    self.dx = 1
                    self.dy = 0
            elif event.key == W:
                if self.dy != 1:
                    self.dx = 0
                    self.dy = -1
            elif event.key == S:
                if self.dy != -1:
                    self.dx = 0 
                    self.dy = 1



class Tail(GridObject):
    def __init__(self, game, front, color):
        self.front = front
        self.color = color
        super().__init__(-1, -1, game, self.color)
    
    def tailtick(self):
        self.prevx = self.x
        self.prevy = self.y
        self.x = self.front.prevx
        self.y = self.front.prevy

        

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        self.eaten_by = None
        super().__init__(x, y, game, self.color)


class Game:
    def __init__(self, n_rows, n_cols, block_size = 10):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.block_size = block_size
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

    def play(self, n_foods = 20):
        plyr1 = Player(int(self.n_cols * 2 / 3), self.n_rows / 2, self)
        plyr2 = Player2(int(self.n_cols * 1 / 3), self.n_rows / 2, self)

        self.objects = [
            plyr1, plyr2,
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

                # boost
                if event.type == pygame.KEYDOWN:
                    if event.key == RSHIFT:
                        plyr1.boost_on = True
                    if event.key == LSHIFT:
                        plyr2.boost_on = True

                elif event.type == pygame.KEYUP:
                    if event.key == RSHIFT:
                        plyr1.boost_on = False
                    if event.key == LSHIFT:
                        plyr2.boost_on = False
            
            # Tick
            for obj in self.active_objects():
                if isinstance(obj, Player):
                    obj.tick()
                    if obj.boost_on:
                        obj.tick() # 한 번 더

            # Interact
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    obj1.interact(obj2)
                    obj2.interact(obj1)
            
            # del & create food & append tail
            for i, obj in enumerate(self.objects[:]):
                if isinstance(obj, Food):
                    if not obj.active:
                        if obj.eaten_by == plyr1:
                            if len(plyr1.tails) == 0:       # tail 없을 경우 front == 머리
                                plyr1.tails.append(Tail(self, plyr1, RED))
                                self.objects.append(plyr1.tails[0])
                            else:                           # tail 이미 있으면 front == 맨 뒤 tail
                                plyr1.tails.append(Tail(self, plyr1.tails[-1], RED))
                                self.objects.append(plyr1.tails[-1])

                        elif obj.eaten_by == plyr2:
                            if len(plyr2.tails) == 0:       #
                                plyr2.tails.append(Tail(self, plyr2, BLUE))
                                self.objects.append(plyr2.tails[0])
                            else:                           #
                                plyr2.tails.append(Tail(self, plyr2.tails[-1], BLUE))
                                self.objects.append(plyr2.tails[-1])

                        del self.objects[i]
                        self.objects.append(Food(self))


            # food-food, food-tail 중복제거
            for i, obj1 in enumerate(self.objects[:]):
                for j, obj2 in enumerate(self.objects[:]):
                    if i != j:
                        if isinstance(obj1, Food) and isinstance(obj2, Food):
                            if obj1.x == obj2.x and obj1.y == obj2.y:
                                del self.objects[i]
                                self.objects.append(Food(self))

            for i, obj1 in enumerate(self.objects[:]):
                for obj2 in [*plyr1.tails, *plyr2.tails]:
                    if isinstance(obj1, Food):
                        if obj1.x == obj2.x and obj1.y == obj2.y:
                            del self.objects[i]
                            self.objects.append(Food(self))

            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()


            # 머리가 tail에 닿으면 game over
            for obj in plyr1.tails:
                if plyr1.x == obj.x and plyr1.y == obj.y:
                    self.game_over = True
            
            for obj in plyr2.tails:
                if plyr2.x == obj.x and plyr2.y == obj.y:
                    self.game_over = True


            # player 서로 닿으면 game over
            for obj1 in [plyr1, *plyr1.tails]:
                for obj2 in [plyr2, *plyr2.tails]:
                    if obj1.x == obj2.x and obj1.y == obj2.y:
                        self.game_over = True


            # 화면 밖 game over
            if plyr1.isout() or plyr2.isout():
                self.game_over = True

            self.clock.tick(10)
            

if __name__ == "__main__":
    Game(n_cols = 80, n_rows = 60, block_size = 10).play(n_foods = 20)
