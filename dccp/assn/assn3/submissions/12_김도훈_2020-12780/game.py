import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock() 


class Player:
    def __init__(self, display, initialX=0, initialY=0):
        self.body = [[initialX, initialY, 0, 0]]
        self.boost = 1
        self.display = display

    def handle_event(self, event, shift, left, right, up, down):
        if event.type == pygame.KEYDOWN:
            if event.key == shift:
                self.boost = 2
            else:
                self.boost = 1
            if event.key == left:
                self.body[0][2] = -10
                self.body[0][3] = 0
            elif event.key == right:
                self.body[0][2] = 10
                self.body[0][3] = 0
            elif event.key == up:
                self.body[0][2] = 0
                self.body[0][3] = -10
            elif event.key == down:
                self.body[0][2] = 0
                self.body[0][3] = 10
    
    def tick(self):
        for j in range(self.boost):
            for i in range(len(self.body)-1):
                self.body[len(self.body)-i-1][0] = int(self.body[len(self.body)-i-2][0])
                self.body[len(self.body)-i-1][1] = int(self.body[len(self.body)-i-2][1])
            self.body[0][0] += self.body[0][2]
            self.body[0][1] += self.body[0][3]
    
    def draw(self, hcolor, bcolor):
        pygame.draw.rect(self.display, hcolor, [self.body[0][0], self.body[0][1], 10, 10])
        for i in range(1, len(self.body)):
            pygame.draw.rect(self.display, bcolor, [self.body[i][0], self.body[i][1], 10, 10])



class Food:
        active = True
        def __init__(self, display):
            self.x = random.randint(0, 79)*10
            self.y = random.randint(0, 59)*10
            self.display = display

        def draw(self, color):
            pygame.draw.rect(self.display, color, [self.x, self.y, 10, 10])

   

game_over = False

display = game_display

player1 = Player(display, 0, 0)
player2 = Player(display, 790, 590)

foods = [Food(display) for _ in range(20)]

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        player1.handle_event(event, pygame.K_RSHIFT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
        player2.handle_event(event, pygame.K_LSHIFT, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)

    player1.tick()
    player2.tick()

    display.fill(BLACK)
    player1.draw(RED, WHITE)
    player2.draw(BLUE, CYAN)

    for i, food in enumerate(foods):
        if food.active:
            food.draw(GREEN)

        if player1.body[0][0] == food.x and player1.body[0][1] == food.y:
            del foods[i]
            foods.append(Food(display))
            player1.body.append([player1.body[0][0], player1.body[0][1], 0, 0])

        elif player2.body[0][0] == food.x and player2.body[0][1] == food.y:
            del foods[i]
            foods.append(Food(display))
            player2.body.append([player2.body[0][0], player2.body[0][1], 0, 0])

    
    pygame.display.update()

    for i in range(len(player1.body)):
        if player1.body[i][0] == player2.body[0][0] and player1.body[i][1] == player2.body[0][1]:
            game_over = True
    for i in range(len(player2.body)):
        if player2.body[i][0] == player1.body[0][0] and player2.body[i][1] == player1.body[0][1]:
            game_over = True        
    
    if len(player1.body) > 2:
        for i in range(1, len(player1.body)-1):
                if player1.body[0][0] == player1.body[i][0] and player1.body[0][1] == player1.body[i][1]:
                    game_over = True
    
    if player1.body[0][0] >= 800 or player1.body[0][0] < 0 or player1.body[0][1] >= 600 or player1.body[0][1] < 0:
        game_over = True

    if len(player2.body) > 2:
        for i in range(1, len(player2.body)-1):
                if player2.body[0][0] == player2.body[i][0] and player2.body[0][1] == player2.body[i][1]:
                    game_over = True
    
    if player2.body[0][0] >= 800 or player2.body[0][0] < 0 or player2.body[0][1] >= 600 or player2.body[0][1] < 0:
        game_over = True

    clock.tick(10)