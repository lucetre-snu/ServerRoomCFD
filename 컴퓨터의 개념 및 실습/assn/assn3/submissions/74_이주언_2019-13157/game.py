import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
TOMATO = (255,99,71)

GREEN = (0, 255, 0)     

BLUE = (0, 0, 255)
SKY_BLUE = (135,206,235)

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

        if isinstance(self, Player):
            body = self.position[1:]
            for i in range(len(body)):
                body_x = body[i][0]
                body_y = body[i][1]
                pygame.draw.rect(self.game.display, self.body_color, [body_x * block_size, body_y * block_size, block_size, block_size])
  

    def interact(self, other):
        pass

    def move(self):
        pass

class Player(GridObject):
    dx = 0
    dy = 0
    color = WHITE
    
    def __init__(self, x, y, game, head_color, body_color, order, shift_key):
        super().__init__(x, y, game, self.color)
        self.position = [(x, y)]
        self.color = head_color
        self.body_color = body_color
        self.order = order
        self.shift_key = shift_key

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.order == "First":
                if event.key == pygame.K_LEFT and not (self.dx == 1 and self.dy == 0):
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_RIGHT and not (self.dx == -1 and self.dy == 0):
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_UP and not (self.dx == 0 and self.dy == 1):
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_DOWN and not (self.dx == 0 and self.dy == -1):
                    self.dx = 0
                    self.dy = 1
            elif self.order == "Second":
                if event.key == pygame.K_a and not (self.dx == 1 and self.dy == 0):
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_d and not (self.dx == -1 and self.dy == 0):
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_w and not (self.dx == 0 and self.dy == 1):
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_s and not (self.dx == 0 and self.dy == -1):
                    self.dx = 0
                    self.dy = 1
    
    def tick(self):
        self.x += self.dx
        self.y += self.dy


    def interact(self, other):
        if isinstance(other, Food):
            for a, b in self.position:
                if a == other.x and b == other.y:
                    other.active = False
                    tail_position = self.position[-1]
                    x, y = tail_position
                    if self.dx == -1 and self.dy == 0:
                        self.position.append((x + 1, y))
                    elif self.dx == 1 and self.dy == 0:
                        self.position.append((x - 1, y))
                    elif self.dx == 0 and self.dy == -1:
                        self.position.append((x, y + 1))
                    elif self.dx == 0 and self.dy == 1:
                        self.position.append((x, y - 1))


    def move(self):
        head_position = self.position[0]
        x, y = head_position
        if self.dx == -1 and self.dy == 0:
            self.position = [(x - 1, y)] + self.position[:-1]
        elif self.dx == 1 and self.dy == 0:
            self.position = [(x + 1, y)] + self.position[:-1]
        elif self.dx == 0 and self.dy == -1:
            self.position = [(x, y - 1)] + self.position[:-1]
        elif self.dx == 0 and self.dy == 1:
            self.position = [(x, y + 1)] + self.position[:-1]




class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)
    

    def interact(self, other):
        if isinstance(other, Player):
            for a, b in other.position:
                if self.x == a and self.y == b:
                    new_food = Food(self.game)
                    self.game.objects.append(new_food)


class Game:
    block_size = 10
    def __init__(self, n_cols, n_rows):
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
        Player_1 = Player(80, 10, self, TOMATO, RED, "First", pygame.K_RSHIFT)
        Player_2 = Player(20, 50, self, SKY_BLUE, BLUE, "Second", pygame.K_LSHIFT)
        self.objects = [
            Player_1, Player_2, 
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


            # Tick
            for obj in self.active_objects():
                obj.tick()
            
            for obj in self.active_objects():
                obj.move()


            # Interact
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                    obj1.interact(obj2)
                    obj2.interact(obj1)

            shift_event = pygame.key.get_pressed()
            for obj in self.active_objects():
                if isinstance(obj, Player):
                    shift_key = obj.shift_key
                    if shift_event[shift_key]:
                        obj.tick()
                        obj.move()


            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()


            # Global decision
            food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains = True
            if not food_remains:
                self.game_over = True


            # Head Touch Body Game Over
            for obj in self.active_objects():
                if isinstance(obj, Player):
                    for i in obj.position[1:]:
                        if i == obj.position[0]:
                            self.game_over = True
    
            # Players Touch Game Over
            player_list = []
            for obj in self.active_objects():
                if isinstance(obj, Player):
                    player_list.append(obj.position)
            num_players = len(player_list)
            for i in range(num_players):
                for j in range(num_players):
                    if i != j:
                        for k in player_list[i]:
                            for l in player_list[j]:
                                if k == l:
                                    self.game_over = True
    

            # Out of Screen Game Over
            for obj in self.active_objects():
                if isinstance(obj, Player):                    
                    head = obj.position[0]
                    if head[0] > self.n_cols or head[0] < 0 or head[1] > self.n_rows or head[1] < 0:
                        self.game_over = True

            self.clock.tick(10)

if __name__ == "__main__":
    a = Game(n_cols = 100, n_rows = 60)
    a.play(n_foods = 20)