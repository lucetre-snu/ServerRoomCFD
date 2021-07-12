import random
import pygame





WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x # grid column index
        self.y = y  # grid row index

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
    dx, dy, dv = 0, 0, 1
    color = RED # 수정 필요
    temp_x, temp_y = 0, 0
    track = []
    def __init__(self, x, y, game, color):
        super().__init__(x, y, game, color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx, self.dy = -self.dv, 0
            elif event.key == pygame.K_RIGHT:
                self.dx, self.dy = self.dv, 0
            elif event.key == pygame.K_UP:
                self.dx, self.dy = 0, -self.dv
            elif event.key == pygame.K_DOWN:
                self.dx, self.dy = 0, self.dv
            elif event.key == pygame.K_RSHIFT:
                self.game.SHIFT = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.game.SHIFT = False

    def tick(self):
        if [self.x, self.y] not in self.track:
#            if len(self.track) > 50:
#                self.track = self.track[1:50]
#                self.track.append([self.x, self.y])
#            else:
            self.track.append([self.x, self.y])
        self.x += self.dx
        self.y += self.dy
#        print(self.track)

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.x, other.y = random.randint(0, self.game.n_cols - 1), random.randint(0, self.game.n_rows - 1)
                self.game.objects.append(Body_1(self.game))

        if isinstance(self, Player) and not isinstance(self, Body_1):
            if isinstance(other, Body_1):
                if self.x == other.x and self.y == other.y:
                    self.game.game_over = True



class Body_1(Player):
    color = YELLOW
    count_body = 0
    def __init__(self, game):
        Body_1.count_body -= 1
        super().__init__(0, 0, game, self.color)
        self.count_body = Body_1.count_body
        self.x = self.game.objects[0].track[Body_1.count_body][0]
        self.y = self.game.objects[0].track[Body_1.count_body][1]


    def tick(self):
        self.x = self.game.objects[0].track[self.count_body][0]
        self.y = self.game.objects[0].track[self.count_body][1]



class Food(GridObject):
    color = WHITE
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def __init__(self, game):
        x, y = random.randint(0, game.n_cols - 1), random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    SHIFT = False
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('2020-15624 전연재 Snake Game')
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = [] #



    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj # 'yeild'일 때, body append 후 index 꼬이는지 확인 필요.

    def __handle__event(self, event):
        # Handle Event
        for obj in self.active_objects():
            obj.handle_event(event)

    def play(self, n_foods=20):
        self.objects = [Player(40, 30, self, RED), *[Food(self) for i in range(n_foods)]] #
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                self.__handle__event(event)

            # Tick
            for obj in self.active_objects():
                obj.tick()

            # Interact
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    obj1.interact(obj2)
                    obj2.interact(obj1)
#                    if isinstance(obj1, Food) and (obj1.active == False): ## 먹이 재생성 / 수정 필요.
#                        self.objects.pop(self.objects.index(obj1))
#                        self.objects.append(Food(self))
#                    if isinstance(obj2, Food) and (obj1.active == False):
#                        self.objects.pop(self.objects.index(obj2))
#                        self.objects.append(Food(self))
            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()

            # Global Decision
            food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains = True
            if not food_remains:
                self.game_over = True
            for obj in self.active_objects():
                if not (0 <= obj.x <= self.n_cols and 0 <= obj.y <= self.n_rows):
                    self.game_over = True
            if self.SHIFT == False:
                self.clock.tick(10)
            else:
                self.clock.tick(20)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)
