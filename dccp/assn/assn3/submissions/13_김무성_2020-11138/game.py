import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game_over = False

x = 400
dx = 0
y = 300
dy = 0
food_coordinates = []
for _ in range(20):
    food_x = random.randint(0,79)
    food_y = random.randint(0,59)
    food_coordinates.append((10*food_x,10*food_y))


food_active = [True for _ in range(20)]

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -10
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = 10
                dy = 0
            elif event.key == pygame.K_UP:
                dx = 0
                dy = -10
            elif event.key == pygame.K_DOWN:
                dx = 0
                dy = 10

    x += dx
    y += dy
    game_display.fill(BLACK)
    pygame.draw.rect(game_display,WHITE, [x, y, 10, 10])
    for i, (food_x, food_y) in enumerate(food_coordinates):
        if food_active[i]:
            pygame.draw.rect(game_display, GREEN, [food_x, food_y, 10, 10])
    for i, (food_x, food_y) in enumerate(food_coordinates):
        if x == food_x and y == food_y:
            food_active[i] = False
            food_x = random.randint(0,79)
            food_y = random.randint(0,59)
            food_coordinates[i]=(10*food_x,10*food_y)
            food_active[i] = True
    pygame.display.update()

    food_remains = False
    for active in food_active:
        if active:
            food_remains = True
    if not food_remains:
        game_over = True
    
    if x >= 800 or x <= 0:
        game_over = True
    if y >= 600 or y <= 0:
        game_over = True
    clock.tick(10)           