import pygame
import random
pygame.init()
game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player: 
    x = 600
    y = 300
    dx = 0
    dy = 0
    body = [[x, y]]
    headx = body[0][0]
    heady = body[0][1]
    memory = 0
    dash = False
    def handle_event(self, event):
        if event.key == pygame.K_LEFT:
            self.dx = -10
            self.dy = 0
        elif event.key == pygame.K_RIGHT:
            self.dx = 10
            self.dy = 0
        elif event.key == pygame.K_UP:
            self.dx = 0
            self.dy = -10
        elif event.key == pygame.K_DOWN:
            self.dx = 0
            self.dy = 10
        elif event.key == pygame.K_RSHIFT:
            self.dash = True
            if self.dx >0:
                self.dx = 20
            elif self.dx < 0:
                self.dx = -20
            if self.dy >0:
                self.dy = 20
            elif self.dy <0:
                self.dy = -20

    def tick(self):
        self.body.insert(0, [self.body[0][0] + self.dx, self.body[0][1] + self.dy])
        if self.dash:
            self.body.insert(1, [self.body[1][0] + self.dx/2, self.body[1][1] + self.dy/2])
            self.body.pop()
        self.headx = self.body[0][0]
        self.heady = self.body[0][1]
        self.body.pop()

    def draw(self):
        a = 0
        for i in self.body:
            if a == 0:
                pygame.draw.rect(game_display, [253, 250, 189], [i[0], i[1], 10, 10])
            else:
                pygame.draw.rect(game_display, [248, 237, 41], [i[0], i[1], 10, 10])
            a += 1

    def remember(self, event):
        if event.key != pygame.K_RSHIFT:
            self.memory = event.key
        else:
            pass    

class Player2: 
    x = 200
    y = 300
    dx = 0
    dy = 0
    body = [[x, y]]
    headx = body[0][0]
    heady = body[0][1]
    memory = 0
    dash = False
    def handle_event(self, event):
        if event.key == pygame.K_a:
            self.dx = -10
            self.dy = 0
        elif event.key == pygame.K_d:
            self.dx = 10
            self.dy = 0
        elif event.key == pygame.K_w:
            self.dx = 0
            self.dy = -10
        elif event.key == pygame.K_s:
            self.dx = 0
            self.dy = 10
        elif event.key == pygame.K_LSHIFT:
            self.dash = True
            if self.dx >0:
                self.dx = 20
            elif self.dx < 0:
                self.dx = -20
            if self.dy >0:
                self.dy = 20
            elif self.dy <0:
                self.dy = -20

    def tick(self):
        self.body.insert(0, [self.body[0][0] + self.dx, self.body[0][1] + self.dy])
        if self.dash:
            self.body.insert(1, [self.body[1][0] + self.dx/2, self.body[1][1] + self.dy/2])
            self.body.pop()
        self.headx = self.body[0][0]
        self.heady = self.body[0][1]
        self.body.pop()

    def draw(self):
        a = 0
        for i in self.body:
            if a == 0:
                pygame.draw.rect(game_display, [252, 210, 253], [i[0], i[1], 10, 10])
            else:
                pygame.draw.rect(game_display, [250, 105, 232], [i[0], i[1], 10, 10])
            a += 1
    def remember(self, event):
        if event.key != pygame.K_RSHIFT:
            self.memory = event.key
        else:
            pass         


            
class Food:
    x = 0
    y = 0
    active = True
    def __init__(self):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
    def draw(self):
        pygame.draw.rect(game_display, GREEN, [self.x, self.y, 10, 10])

def reverse(x):
    if x == pygame.K_LEFT:
        return pygame.K_RIGHT
    elif x == pygame.K_RIGHT:
        return pygame.K_LEFT
    elif x == pygame.K_DOWN:
        return pygame.K_UP
    elif x == pygame.K_UP:
        return pygame.K_DOWN
    elif x == pygame.K_a:
        return pygame.K_d
    elif x == pygame.K_d:
        return pygame.K_a
    elif x == pygame.K_s:
        return pygame.K_w
    elif x == pygame.K_w:
        return pygame.K_s
    else:
        return 0


player = Player()
player2 = Player2()
foods = [Food() for i in range(20)]

game_display.fill(BLACK)
pygame.display.update()
game_over = False

x = 0
y = 0


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        if event.type == pygame.KEYDOWN:
            if len(player.body) >= 2 and reverse(player.memory) == event.key:
                game_over = True
                break
            if len(player2.body) >= 2 and reverse(player2.memory) == event.key:
                game_over = True
                break
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_LSHIFT]:
                player.remember(event)
            if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_RSHIFT]:
                player2.remember(event)
            player.handle_event(event)
            player2.handle_event(event)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                player.dash = False
                if player.dx > 0:
                    player.dx = 10
                elif player.dx < 0:
                    player.dx = -10
                if player.dy > 0:
                    player.dy = 10
                elif player.dy < 0:
                    player.dy = -10
            if event.key == pygame.K_LSHIFT:
                player2.dash = False
                if player2.dx > 0:
                    player2.dx = 10
                elif player2.dx < 0:
                    player2.dx = -10
                if player2.dy > 0:
                    player2.dy = 10
                elif player2.dy < 0:
                    player2.dy = -10


    player.headx, player.heady = player.body[0]
    player2.headx, player2.heady = player2.body[0]
    player.tick()
    player2.tick()
    if player.headx > 800 or player.headx < 0 or player.heady >600 or player.heady <0:
        game_over == True
        break
    if player2.headx > 800 or player2.headx < 0 or player2.heady >600 or player2.heady <0:
        game_over == True
        break
    game_display.fill(BLACK)
    player.draw()
    player2.draw()
    if [player.headx, player.heady] in player2.body or [player2.headx, player2.heady] in player.body:
        game_over == True
        break
    player.headx, player.heady = player.body[0]
    player2.headx, player2.heady = player2.body[0]
    if [player.headx, player.heady] in player.body[1:]:
        game_over = True
    if [player2.headx, player2.heady] in player2.body[1:]:
        game_over = True  
    

    for food in foods:
        if food.active:
            food.draw()
        if [food.x, food.y] in player.body:
            if player.dx < 0:
                player.body.insert(0, [player.headx -10, player.heady])
            elif player.dx > 0:
                player.body.insert(0, [player.headx +10, player.heady])
            elif player.dy < 0:
                player.body.insert(0, [player.headx, player.heady - 10])
            elif player.dy > 0:
                player.body.insert(0, [player.headx, player.heady + 10])
            
            x = random.randint(0, 79) * 10 
            y = random.randint(0, 59) * 10
            while [x, y] in player.body or [x, y] in player2.body:
                x = random.randint(0, 79) * 10 
                y = random.randint(0, 59) * 10

            food.x = x
            food.y = y

        elif [food.x, food.y] in player2.body:
            if player2.dx < 0:
                player2.body.insert(0, [player2.headx -10, player2.heady])
            elif player2.dx > 0:
                player2.body.insert(0, [player2.headx +10, player2.heady])
            elif player2.dy < 0:
                player2.body.insert(0, [player2.headx, player2.heady - 10])
            elif player2.dy > 0:
                player2.body.insert(0, [player2.headx, player2.heady + 10])       
            
            x = random.randint(0, 79) * 10 
            y = random.randint(0, 59) * 10
            while [x, y] in player.body or [x, y] in player2.body:
                x = random.randint(0, 79) * 10 
                y = random.randint(0, 59) * 10

            food.x = x
            food.y = y
    
    player.headx, player.heady = player.body[0]  
    player2.headx, player2.heady = player2.body[0] 
    pygame.display.update()
    clock.tick(10)



