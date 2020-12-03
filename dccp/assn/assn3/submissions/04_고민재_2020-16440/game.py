import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
DEEPPINK = (255, 20, 147)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEEPSKYBLUE = (0, 191, 255)

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
key_type1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT]
key_type2 = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT]

class Player:
    def __init__(self, display, color_head, color_body, keytype):
        self.display = display
        self.color_head = color_head
        self.color_body = color_body
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.bef_x = -10
        self.bef_y = -10
        self.dx = 0
        self.dy = 0
        self.snake = []
        self.snake_len = 1
        self.key_type = keytype
        self.food_check = []

    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == self.key_type[0]):
                self.dx -= 10 
                self.dy = 0
            elif (event.key == self.key_type[1]):
                self.dx += 10 
                self.dy = 0 
            elif (event.key == self.key_type[2]):
                self.dy -= 10
                self.dx = 0 
            elif (event.key == self.key_type[3]):
                self.dy += 10 
                self.dx = 0 
            
                
    def handle_tick(self): # 실질적인 이동 함수
        self.bef_x = self.x
        self.bef_y = self.y
        self.x += self.dx
        self.y += self.dy
        self.snake_head = []
        self.snake_head.append(self.x)
        self.snake_head.append(self.y)
        self.snake.append(self.snake_head)
        if (len(self.snake) > self.snake_len):
            del self.snake[0]
             
    def draw(self):
        for x in self.snake:
            if (x == self.snake_head):
                pygame.draw.rect(self.display, self.color_head, [x[0], x[1], 10, 10])
            else:
                pygame.draw.rect(self.display, self.color_body, [x[0], x[1], 10, 10])


class Food:
    def __init__(self, display, color):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.active = True
        self.display = display
        self.color = color

    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])


game_over = False

p1 = Player(game_display, DEEPPINK, ORANGE, key_type1)
p2 = Player(game_display, DEEPSKYBLUE, BLUE, key_type2)
foods = [Food(game_display, GREEN) for _ in range(20)]

while not game_over:
    game_display.fill(BLACK)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_over = True
            break
        p1.handle_event(event)
        p2.handle_event(event)

    if (p1.x < 0 or p1.x >= 800 or p1.y < 0 or p1.y >= 600):
        game_over = True
        break

    if (p2.x < 0 or p2.x >= 800 or p2.y < 0 or p2.y >= 600):
        game_over = True
        break
    
    for x in p1.snake[:-1]:
        if (x == p1.snake_head):
            game_over = True
        
    for x in p2.snake[:-1]:
        if (x == p2.snake_head):
            game_over = True
    
    for x in p1.snake:
        if (p2.snake_head == x):
            game_over = True

    for x in p2.snake:
        if (p1.snake_head == x):
            game_over = True
     
    p1.handle_tick()
    p2.handle_tick() 
    p1.draw()
    p2.draw()


    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RSHIFT]:
        p1.handle_tick()
        p1.draw()
    
    elif pressed[pygame.K_LSHIFT]:
        p2.handle_tick()
        p2.draw()
    
    num = 0

    for food in foods:
        if food.active:
            food.draw()
            num += 1
            
    
    for food in foods:
        if p1.x == food.x and p1.y == food.y and food.active == True:
            food.active = False
            p1.snake_len += 1
            
            if (num <= 20):
                foods.append(Food(game_display, GREEN))
                
        elif p1.bef_x == food.x and p1.bef_y == food.y and food.active == True:
            food.active = False
            p1.snake_len += 1

            if (num <= 20):
                foods.append(Food(game_display, GREEN))

        elif p2.x == food.x and p2.y == food.y and food.active == True:
            food.active = False
            p2.snake_len += 1
            if (num <= 20):
                foods.append(Food(game_display, GREEN))
        
        elif p2.bef_x == food.x and p2.bef_y == food.y and food.active == True:
            food.active = False
            p2.snake_len += 1

            if (num <= 20):
                foods.append(Food(game_display, GREEN))
            

    if (num != 20):
        game_over = True

    pygame.display.update()
    clock.tick(10)