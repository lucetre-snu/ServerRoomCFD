import pygame
import random
#이게 티 안남 이걸로 제출각

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
count = 0

game_over = False
def game_end():
    global game_over
    game_over = True

class Player:
    dx = 0
    dy = 0
    def __init__(self,display,x,y,boost,color_head,color_tail,keyset):
        self.x = x
        self.y = y
        self.display =display
        self.long = 0
        self.eat = 0
        self.memory = []
        self.time = 10
        self.color_head = color_head
        self.color_tail = color_tail
        self.keyset = keyset
        self.boost = 0
    def others(self, other):
        self.other = other
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keyset[0]:  
                self.dx = -10
                self.dy = 0
            elif event.key == self.keyset[1]:
                self.dx = 10
                self.dy = 0
            elif event.key == self.keyset[2]:
                self.dy = -10
                self.dx = 0
            elif event.key == self.keyset[3]:
                self.dy = 10 
                self.dx = 0
            elif event.key == self.keyset[4]:
                self.boost = 1
        elif event.type == pygame.KEYUP:
            if event.key == self.keyset[4]:
                self.boost = 0

    def tick(self):
        if count % 2 == 1:
            if self.boost == 1:
                self.x += self.dx
                self.y += self.dy
                if self.x > 800 or self.x < 0 or self.y > 600 or self.y < 0:
                    game_end()
            else:
                pass
        else:
            self.x += self.dx
            self.y += self.dy
            if self.x > 800 or self.x < 0 or self.y > 600 or self.y < 0:
                game_end()
    def draw(self):
        if count % 2 == 1:
            if self.boost == 1:            
                if self.long > 0:
                    if (self.x, self.y) in self.memory:
                        game_end()
                if (self.other.x, self.other.y) in self.memory:
                    game_end()
                
                for i in range (0, self.long):
                    pygame.draw.rect(self.display, self.color_tail, [self.memory[i][0], self.memory[i][1], 10, 10])
                pygame.draw.rect(self.display, self.color_head, [self.x, self.y, 10, 10])

                if self.eat == 1:
                    self.memory.insert(0, (self.x, self.y))
                    self.eat = 0
                else:
                    self.memory = self.memory[0:-1]
                    self.memory.insert(0, (self.x, self.y))
            else:
                for i in range (0, self.long):
                    pygame.draw.rect(self.display, self.color_tail, [self.memory[i][0], self.memory[i][1], 10, 10])
                pygame.draw.rect(self.display, self.color_head, [self.x, self.y, 10, 10])
        else:
            if self.long > 0:
                if (self.x, self.y) in self.memory:
                    game_end()
            if (self.other.x, self.other.y) in self.memory:
                game_end()

            for i in range (0, self.long):
                pygame.draw.rect(self.display, self.color_tail, [self.memory[i][0], self.memory[i][1], 10, 10])
            pygame.draw.rect(self.display, self.color_head, [self.x, self.y, 10, 10])

            if self.eat == 1:
                self.memory.insert(0, (self.x, self.y))
                self.eat = 0
            else:
                self.memory = self.memory[0:-1]
                self.memory.insert(0, (self.x, self.y))
    def longer(self):
        self.long += 1
        self.eat = 1
class Food:
    active = True
    def __init__(self,display):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10
        self.display = display
    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])
    def relocation(self):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10

player = Player(game_display,0,0,0,WHITE,RED,[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_RSHIFT])
player2 = Player(game_display,400,300,0,GREY,BLUE,[pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,pygame.K_LSHIFT])

player.others(player2)
player2.others(player)

foods = [Food(game_display) for i in range (20)]

# x = 400
# dx = 0
# y = 300
# dy = 0
    # food_coordinates = []
    # food_active = [True for i in range(3)]
    # for i in range(3):
    #     food_x = random.randint(0, 79)
    #     food_y = random.randint(0, 59)
    #     food_coordinates.append((10 * food_x, 10 * food_y))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end()
        elif event.type == pygame.KEYDOWN:
            player.handle_event(event)  
            player2.handle_event(event)
        elif event.type == pygame.KEYUP:
            player.handle_event(event)
            player2.handle_event(event)
    
    game_display.fill((BLACK))

    player.tick()
    player2.tick()

    player.draw()
    player2.draw()

    count += 1

    for food in foods:
        if food.active:
            food.draw()
        if player.x == food.x and player.y == food.y:
            food.relocation()
            player.longer()
        if player2.x == food.x and player2.y == food.y:
            food.relocation()
            player2.longer()
            
    pygame.display.update()

    food_remains = False
    for food in foods:
        if food.active:
            food_remains = True
    
    if not food_remains:
        game_over = True

    clock.tick(20)