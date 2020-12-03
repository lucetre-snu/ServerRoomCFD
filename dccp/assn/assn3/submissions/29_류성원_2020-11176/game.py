import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HEAD_RED = (255,200,200)
HEAD_BLUE = (200,200,255)

class Player:
        
    def __init__(self, x, y, game, ID):
        self.game = game
        self.ID = ID
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        if self.ID == 1:
            self.color1 = HEAD_RED
            self.color2 = RED
        elif self.ID == 2:
            self.color1 = HEAD_BLUE
            self.color2 = BLUE
        self.length = 0
        self.map = []
        self.tick_time = 1
        self.shift1 = False
        self.shift2 = False
        self.keys = pygame.key.get_pressed()
        

    
    def handle_event(self, event):
        
        if self.ID == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0
                    self.shift1 = True
                elif event.key == pygame.K_RIGHT:
                    self.dx = 1
                    self.dy = 0
                    self.shift1 = True
                elif event.key == pygame.K_UP:
                    self.dy = -1
                    self.dx = 0
                    self.shift1 = True
                elif event.key == pygame.K_DOWN:
                    self.dy = 1
                    self.dx = 0
                    self.shift1 = True
                if event.key == pygame.K_RSHIFT:
                    self.shift2 = True
                if self.shift1 == True and self.shift2 == True:
                    self.tick_time = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    self.tick_time = 1
                    self.shift2 = False
            
        elif self.ID == 2:
            
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_a:
                    self.dx = -1
                    self.dy = 0
                    self.shift1 = True
                elif event.key == pygame.K_d:
                    self.dx = 1
                    self.dy = 0
                    self.shift1 = True
                elif event.key == pygame.K_w:
                    self.dy = -1
                    self.dx = 0
                    self.shift1 = True
                elif event.key == pygame.K_s:
                    self.dy = 1
                    self.dx = 0
                    self.shift1 = True
                if event.key == pygame.K_LSHIFT:
                    self.shift2 = True
                if self.shift1 == True and self.shift2 == True:
                    self.tick_time = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.tick_time = 1
                    self.shift2 = False
        
    def tick(self):

        for i in range(self.tick_time):
            self.x += self.dx
            self.y += self.dy
            map = [self.x, self.y]
            self.map.append(map)

    def draw_head(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color1, [self.x * block_size, self.y * block_size, block_size, block_size])
    
    def draw_body(self):
        block_size = self.game.block_size
        if self.length == 0:
            pass
        else:
            for i in range(self.length):
                pygame.draw.rect(self.game.display, self.color2, [self.map[(-2)+(-1)*i][0] * block_size, self.map[(-2)+(-1)*i][1] * block_size, block_size, block_size])
                if self.x == self.map[(-2)+(-1)*i][0] and self.y == self.map[(-2)+(-1)*i][1]:
                    self.game.game_over = True
    
    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False
                self.game.new_food()
                self.length+=1
            elif self.tick_time == 2 and self.length >= 1: 
                if self.map[(-2)][0] == other.x and self.map[(-2)][1] == other.y:
                    other.active = False
                    self.game.new_food()
                    self.length+=1
        if isinstance(other, Player):
            if self.x == other.x and self.y == other.y:
                self.game.game_over = True
            elif other.length != 0:    
                for i in range(other.length):
                    if self.x == other.map[(-2)+(-1)*i][0] and self.y == other.map[(-2)+(-1)*i][1]:
                        self.game.game_over = True

            


class Food:
    color = GREEN
    def __init__(self, game):
        self.game = game
        self.x = random.randint(0, game.n_cols - 1)
        self.y = random.randint(0, game.n_rows - 1)
        self.active = True        
    def draw(self):
        block_size = self.game.block_size
        if self.active == True:
            pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        else:
            pass
        

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

    def new_food(self):
        self.foods.append(Food(self))
    
    def play(self, n_foods=20):
        a = Player(30, 30, self, 1)
        b = Player(60, 30, self, 2)
        

        self.players = [a,b]
        self.foods = [Food(self) for _ in range(n_foods)]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
            for player in self.players:
                if player.x >= self.n_cols or player.x < 0:
                    self.game_over = True
                    break
                elif player.y >= self.n_rows or player.y < 0 :
                    self.game_over = True
                    break    
                
                # Handle event
                for player in self.players:
                    player.handle_event(event)

            # Tick
            for player in self.players:
                player.tick()
            
            # Interact
            for player in self.players:
                for food in self.foods:
                    player.interact(food)
            
            self.players[0].interact(self.players[1])
            self.players[1].interact(self.players[0])
                    
            
            # Draw
            self.display.fill(BLACK)
            for player in self.players:
                player.draw_head()
                player.draw_body()
            for food in self.foods:
                food.draw()
            pygame.display.update()

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)   