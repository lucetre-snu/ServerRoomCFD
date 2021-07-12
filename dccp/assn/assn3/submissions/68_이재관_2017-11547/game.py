import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
    def handle_event(self,evnet):
        pass
    def tick(self):
        pass
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display,self.color,[self.x * block_size ,self.y * block_size,block_size,block_size])

class Player(GridObject):
    dy = 0
    dx = 0
    color = WHITE
    boost = False
    def __init__(self,x,y,game,player_num):
        super().__init__(x,y,game,self.color)
        self.player_num = player_num
        if player_num == 2:
            self.color = YELLOW
    def handle_event(self,event):
        if self.player_num == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_RIGHT: 
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_UP:
                    self.dy = -1
                    self.dx = 0
                elif event.key == pygame.K_DOWN:
                    self.dy = 1
                    self.dx = 0
                if event.key == pygame.K_RSHIFT:
                    self.boost = True
                else:
                   self.boost = False
        elif self.player_num == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_d: 
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_w:
                    self.dy = -1
                    self.dx = 0
                elif event.key == pygame.K_s:
                    self.dy = 1
                    self.dx = 0
                if event.key == pygame.K_LSHIFT:
                    self.boost = True
                else:
                   self.boost = False          
    def handle_tick(self):
        self.x += self.dx
        self.y += self.dy
class Tail(Player):
    color = BLUE
    path = []
    length = 0
    cross = False
    tail_track=[]
    def __init__(self,x,y,game,player_num):
        super().__init__(x,y,game,player_num)
        if self.player_num == 2:
            self.color = RED 
    def handle_event(self,event):
        super().handle_event(event)
    def handle_tick(self):
        self.path.append((self.dx,self.dy))
        if self.length < len(self.path) :
            if self.length == 0:
                self.path = []
            else:
                self.path = self.path[1:]
        self.x += self.dx
        self.y += self.dy
    def draw(self):
        block_size = self.game.block_size
        for i in range(len(self.path)):
            c,d = 0,0
            self.tail_track = []
            for j in range(i+1):
                a,b = self.path[len(self.path)-j-1]
                c,d = c+a,d+b
                self.tail_track.append((self.x-c,self.y-d))
            pygame.draw.rect(self.game.display,self.color,[(self.x-c) * block_size ,(self.y-d) * block_size,block_size,block_size])


class Food(GridObject):
    def __init__(self,game):
        self.color = GREEN
        super().__init__(0,0,game,self.color)
        self.x = random.randint(0,game.n_rows-1)
        self.y = random.randint(0,game.n_heights-1) 

class Game:
    def __init__(self,n_rows,n_heights,block_size=10):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.block_size = block_size
        self.display = pygame.display.set_mode((n_rows*block_size, n_heights*block_size))
        self.n_rows = n_rows
        self.n_heights = n_heights
        self.clock = pygame.time.Clock()
        self.game_over = False
    
    def play(self, n_foods=20,tick=10):
        player_a = Player(40,30, self,1)
        player_b = Player(20,20,self,2)
        foods = [Food(self) for _ in range(n_foods)]
        tail_a = Tail(40,30,self,1)
        tail_b = Tail(20,20,self,2)
        self.tick = tick
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player_a.handle_event(event)
                tail_a.handle_event(event)
                player_b.handle_event(event)
                tail_b.handle_event(event)
            for player, tail in [(player_a,tail_a),(player_b,tail_b)]:        
                player.handle_tick()
                tail.handle_tick() 
                self.display.fill(BLACK)          
                for food in foods:
                    if food.active == True:
                        food.draw()
                    if player.x == food.x and player.y == food.y:
                        food.active = False
                        new_food = Food(self)
                        foods.append(new_food)
                        tail.length += 1
                if player.boost == True:
                    player.handle_tick()
                    tail.handle_tick() 
                    self.display.fill(BLACK)          
                    for food in foods:
                        if food.active == True:
                            food.draw()
                        if player.x == food.x and player.y == food.y:
                            food.active = False
                            new_food = Food(self)
                            foods.append(new_food)
                            tail.length += 1
                food_remains = False
                for food in foods:
                    if food.active == True:
                        food_remains = True
                if food_remains == False:
                    self.game_over = True
                if player.x >= self.n_rows - 1 or player.x <= 0 or player.y >= self.n_heights -1 or player.y <= 0:
                    self.game_over = True
                for tail_other in [tail_a,tail_b]:  
                    if (player.x,player.y) in tail_other.tail_track:
                        self.game_over = True
            tail_a.draw()
            tail_b.draw()
            player_a.draw()
            player_b.draw()
            pygame.display.update()
            self.clock.tick(tick)
                   

if __name__ == "__main__":
    Game(n_rows=80, n_heights=60,block_size=10).play(n_foods=20,tick=10)