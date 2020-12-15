import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


game_display = pygame.display.set_mode((800,600)) #디스플레이 크기
pygame.display.set_caption('DCCP Snake Game') #게임 이름 정해주기
clock = pygame.time.Clock()

game_over = False

x=400
dx = 0
y = 300
dy = 0

food_coordinates = []
food_active = []
for i in range(20):
    food_x = random.randint(0, 79) # 10~800
    food_y = random.randint(0, 59) # 10~600
    food_coordinates.append((10*food_x, 10*food_y))
    food_active.append(True)

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
                dy = -10
                dx = 0
            elif event.key == pygame.K_DOWN:
                dy = 10
                dx = 0

    x += dx
    y += dy
    game_display.fill(white)
    pygame.draw.rect(game_display, black, [x, y, 10, 10])
    for i, (food_x, food_y) in enumerate(food_coordinates):
        if food_active[i]:
            pygame.draw.rect(game_display, red, [food_x, food_y, 10, 10])
    
    for i, (food_x, food_y) in enumerate(food_coordinates):
        if x == food_x and  y == food_y:
            food_active[i] = False
            
            food_x = random.randint(0, 79) 
            food_y = random.randint(0, 59) 
            food_coordinates.append((10*food_x, 10*food_y))
            food_active.append(True)
            pygame.draw.rect(game_display, red, [food_x, food_y, 10, 10])
            
    pygame.display.update()

    food_remains = False
    for active in food_active:
        if active:
            food_remains = True
    if not food_remains:
        game_over = True

    clock.tick(10)

    if x < 0 or y<0 or x>800 or y>600:
        game_over = True

        
