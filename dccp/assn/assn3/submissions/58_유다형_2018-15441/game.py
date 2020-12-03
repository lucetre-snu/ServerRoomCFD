import random
import pygame

PINK = (213, 100, 124)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (135, 206, 235)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x # grid column index
        self.y = y # grid row index
    
    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass

class PlayerA(GridObject):
    color = PINK
    dx = 0
    dy = 0

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.body = []
        self.length = 1
        self.speed = 1
        self.temp = 1
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                self.speed = 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.speed = 1

        if event.type == pygame.KEYDOWN:
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
        if self.speed == 1:
            self.x += self.dx
            self.y += self.dy
        if self.speed == 2:
            self.x += self.dx * 2
            self.y += self.dy * 2

        if self.speed == 1:
            self.head = []
            self.head.append(self.x)
            self.head.append(self.y)
            self.body.append(self.head)
            if len(self.body) > self.length:
                del self.body[0]
        elif self.speed == 2:
            self.head = []
            self.head.append(self.x)
            self.head.append(self.y)
            self.body.append(self.head)
            for i in range(len(self.body)-1):
                self.body[i][0] += self.dx
                self.body[i][1] += self.dy
            if len(self.body) > self.length:
                del self.body[0]    

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False
                self.length += 1
            elif self.speed == 2:
                if self.body[-2][0] == other.x and self.body[-2][1] == other.y:
                    other.active = False
                    self.length += 1

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, RED, [self.head[0] * block_size, self.head[1] * block_size, block_size, block_size])
        for i in range(len(self.body)-1):
            pygame.draw.rect(self.game.display, self.color, [self.body[i][0] * block_size, self.body[i][1] * block_size, block_size, block_size])

class PlayerB(GridObject):
    color = SKYBLUE
    dx = 0
    dy = 0

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.body = []
        self.length = 1
        self.speed = 1
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.speed = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.speed = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
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
        if self.speed == 1:
            self.x += self.dx
            self.y += self.dy
        if self.speed == 2:
            self.x += self.dx * 2
            self.y += self.dy * 2

        if self.speed == 1:
            self.head = []
            self.head.append(self.x)
            self.head.append(self.y)
            self.body.append(self.head)
            if len(self.body) > self.length:
                del self.body[0]
        elif self.speed == 2:
            self.head = []
            self.head.append(self.x)
            self.head.append(self.y)
            self.body.append(self.head)
            for i in range(len(self.body)-1):
                self.body[i][0] += self.dx
                self.body[i][1] += self.dy
            if len(self.body) > self.length:
                del self.body[0]    

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False
                self.length += 1

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, BLUE, [self.head[0] * block_size, self.head[1] * block_size, block_size, block_size])
        for i in range(len(self.body)-1):
            pygame.draw.rect(self.game.display, self.color, [self.body[i][0] * block_size, self.body[i][1] * block_size, block_size, block_size])

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        self.game = game
        x = random.randint(0, 79)
        y = random.randint(0, 59)
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
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

    def play(self, n_foods=20):
        Player1 = PlayerA(60, 30, self)
        Player2 = PlayerB(20, 30, self)
        self.objects = [
            Player1,
            Player2,
            *[Food(self) for _ in range(n_foods)]
        ]
        while not self.game_over:
            # 모든 이벤트 하나하나에 접근
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
            
                # Handle Event
                for obj in self.active_objects():
                    obj.handle_event(event)
            
            # Tick
            for obj in self.active_objects():
                obj.tick()
                for _ in Player1.body[:-1]:
                    if _ == Player1.head: 
                        self.game_over = True
                for _ in Player2.body[:-1]:
                    if _ == Player2.head: 
                        self.game_over = True
                for _ in Player1.body:
                    for __ in Player2.body:
                        if __ == _:
                            self.game_over = True 

            # Interaction
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    obj1.interact(obj2)
                    obj2.interact(obj1)

            # Draw
            self.display.fill(BLACK) #전체를 검정색으로 채우고
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()

            # 먹이 추가
            for i, obj in enumerate(self.objects):
                if obj.active == False:
                    self.objects[i] = Food(self)

            # 게임 종료 조건 - 화면 밖 나가면 꺼지기
            for i in range(len(Player1.body)):
                if Player1.body[i][0] < 1 or Player1.body[i][0] > 78 or Player1.body[i][1] < 1 or Player1.body[i][1] > 58:
                    self.game_over = True
            for i in range(len(Player2.body)):
                if Player2.body[i][0] < 1 or Player2.body[i][0] > 78 or Player2.body[i][1] < 1 or Player2.body[i][1] > 58:
                    self.game_over = True

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows = 60, n_cols = 80).play(n_foods=20)