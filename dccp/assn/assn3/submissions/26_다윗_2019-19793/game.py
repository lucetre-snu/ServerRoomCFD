import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

class Player:
    x = 0
    y = 0
    dx = 0
    dy = 0

    def __init__(self, display):
        self.display = display

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.dx = -10
                player.dy = 0
            elif event.key == pygame.K_RIGHT:
                player.dx = 10
                player.dy = 0
            elif event.key == pygame.K_UP:
                player.dy = -10
                player.dx = 0
            elif event.key == pygame.K_DOWN:
                player.dy = 10
                player.dx = 0
                

    def tick(self):
        self.x += self.dx
        self.y += self.dy
    def draw(self):
        pygame.draw.rect(self.display, WHITE, [self.x, self.y, 10, 10])

class Food:
    x = 0
    y = 0
    active = True
    def __init__(self, display):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.display = display
    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])

game_over = False

player = Player(game_display)
foods = [Food(game_display) for _ in range(20)]

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break 
        player.handle_event(event)

    player.tick()
    game_display.fill(BLACK)
    player.draw()

    for food in foods:
        if food.active:
            food.draw()
        if player.x == food.x and player.y == food.y:
            food.active = False
            new_food = Food(game_display)
            foods.append(new_food)
    
    pygame.display.update()

    if player.x < 0 or player.x > 800 or player.y < 0 or player.y > 600:
        game_over = True

    # food_remains = False
    # for food in foods:
    #     if food.active:
    #         food_remains = True
    
    
    # if not food_remains:
    #     game_over = True

    clock.tick(10)
