import pygame
import random

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)                 #RGB
SKYBLUE = (92, 209, 229)
LIGHT_SKYBLUE = (178, 235, 224)
PINK = (243, 97, 166)
LIGHT_PINK = (255, 178, 217)

class GridObject:
    def __init__(self, x, y, game):
        self.game = game
        self.x = x
        self.y = y

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):       
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size]) 

class Player(GridObject):
    dx = 0
    dy = 0
    speed_change = False

    def __init__(self, x, y, game, head_color, body_color, Left_Key, Right_Key, Up_Key, Down_Key, Boost_Key):
        super().__init__(x, y, game)
        self.body = [(x, y)]
        self.direction = 0
        self.head_color = head_color
        self.body_color = body_color
        self.clock = pygame.time.Clock()
        self.Left_Key = Left_Key
        self.Right_Key = Right_Key
        self.Up_Key = Up_Key
        self.Down_Key = Down_Key
        self.Boost_Key = Boost_Key

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.Left_Key:
                if len(self.body) != 1 and self.direction == self.Right_Key:
                    pass
                else:
                    self.dx = -1
                    self.dy = 0    
                    self.direction = self.Left_Key
            elif event.key == self.Right_Key:
                if len(self.body) != 1 and self.direction == self.Left_Key:
                    pass
                else:
                    self.dx = 1
                    self.dy = 0       
                    self.direction = self.Right_Key   
            elif event.key == self.Up_Key:
                if len(self.body) != 1 and self.direction == self.Down_Key:
                    pass
                else:
                    self.dx = 0        
                    self.dy = -1   
                    self.direction = self.Up_Key
            elif event.key == self.Down_Key:
                if len(self.body) != 1 and self.direction == self.Up_Key:
                    pass
                else:
                    self.dx = 0        
                    self.dy = 1
                    self.direction = self.Down_Key  
            elif event.key == self.Boost_Key: #boost
                self.boost()
        elif event.type == pygame.KEYUP:
            if event.key == self.Boost_Key:
                self.boost()

    def boost(self):
        if self.speed_change == True:
            self.speed_change = False
        else :
            self.speed_change = True

    def tick(self):    
        x, y = self.body[0]
        self.body = [(x + self.dx, y + self.dy)] + self.body[:-1]

    def player_grow(self):
        x, y = self.body[-1]
        if len(self.body) == 1 :
            if self.direction == self.Left_Key:
                self.body.append((x+1, y))
            elif self.direction == self.Right_Key:
                self.body.append((x-1, y))
            elif self.direction == self.Up_Key:
                self.body.append((x, y+1))
            elif self.direction == self.Down_Key:
                self.body.append((x, y-1))
        else :
            if self.body[-1][0] == self.body[-2][0]:
                if self.body[-1][1] > self.body[-2][1]:
                    self.body.append((x, y+1))
                elif self.body[-1][1] < self.body[-2][1]:
                    self.body.append((x, y-1))
            if self.body[-1][1] == self.body[-2][1]:
                if self.body[-1][0] > self.body[-2][0]:
                    self.body.append((x+1, y))
                elif self.body[-1][0] < self.body[-2][0]:
                    self.body.append((x-1, y))

    def food_interact(self, other):
        other.draw()
        if self.body[0][0] == other.x and self.body[0][1] == other.y:   
            other.x = random.randint(0, self.game.width-1)
            other.y = random.randint(0, self.game.length-1)
            self.player_grow()     

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.head_color, [self.body[0][0] * block_size, self.body[0][1] * block_size, block_size, block_size]) 
        for i in range(len(self.body)-1):    
            pygame.draw.rect(self.game.display, self.body_color, [self.body[i+1][0] * block_size, self.body[i+1][1] * block_size, block_size, block_size]) 

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.width-1)
        y = random.randint(0, game.length-1)
        super().__init__(x, y, game)

class Game:
    block_size = 10
    def __init__(self, width, length):
        pygame.init()
        pygame.display.set_caption('Battle Snake Game')
        self.display = pygame.display.set_mode((width * self.block_size, length * self.block_size))
        self.width = width
        self.length = length
        self.clock = pygame.time.Clock()
        self.game_over = False

    def decision(self, player=[]): 
        for i in range(len(player)):
            self.self_collision(player[i])
            self.boundary_collision(player[i])
        self.collision(player)
    
    def self_collision(self, player):
        x = player.body[0][0]
        y = player.body[0][1]
        for i in range(len(player.body)-1):
            if x == player.body[i+1][0] and y == player.body[i+1][1]:
                self.game_over = True

    def boundary_collision(self, player):
        x = player.body[0][0]
        y = player.body[0][1]
        if x > self.width-1 or x < 0 or y > self.length-1 or y < 0 :
                self.game_over = True

    def collision(self, player):
        self.player1 = player[0]
        self.player2 = player[1]
        for b in self.player2.body:
            if self.player1.body[0] == b:
                self.game_over = True
        for b in self.player1.body:
            if self.player2.body[0] == b:
                self.game_over = True

    def play(self, n_foods=20):
        player = [Player(20, 30, self, SKYBLUE, LIGHT_SKYBLUE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT), \
            Player(40, 30, self, PINK, LIGHT_PINK, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT)]
        check = 0
        game_speed = 10
        foods = [Food(self) for _ in range(n_foods)]
        while not self.game_over:
            check+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.game_over=True
                    break
                for i in range(len(player)):
                    player[i].handle_event(event)
            
            self.display.fill(BLACK)

            for i in range(len(player)):        # boost
                if player[i].speed_change:
                    player[i].tick()
                else:
                    if check % 2 == 0:
                        pass
                    else:
                        player[i].tick()
                player[i].draw()

            for food in foods:                  # players interact with foods
                for i in range(len(player)):      
                    player[i].food_interact(food)

            pygame.display.update()

            self.decision(player)  # when the game ends
            
            self.clock.tick(2*game_speed)

if __name__ == "__main__":
    Game(width = 80, length = 60).play(n_foods=20)