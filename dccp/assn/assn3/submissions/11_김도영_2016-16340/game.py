import pygame
import random

#colors
white = (255,255,255)
black = (0,0,0)
red_head = (255,0,0)
red_body = (100,0,0)
green = (0,255,0)
blue_head = (0,0,255)
blue_body = (0,0,100)

unit = 10
blue_length = 0
red_length = 0

pygame.init()
game_display = pygame.display.set_mode((800,600)) 
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

game_over = False

blue_x = 750
red_x = 50
blue_dx = 0
red_dx = 0
blue_y = 300
red_y = 300
blue_dy = 0
red_dy = 0
prey = 20

food_position = []

for _ in range(prey):
    food_x = random.randint(0, 79)  
    food_y = random.randint(0,59)  
    food_position.append((10*food_x, 10*food_y))

blue_dxy_log = []
red_dxy_log = []

lshift = 1
rshift = 1

while not game_over:
    if blue_length > 0:
        blue_dxy_log.insert(0,(blue_dx,blue_dy))
        if len(blue_dxy_log) > blue_length:
            blue_dxy_log.pop(-1)
    
    if red_length > 0:
        red_dxy_log.insert(0,(red_dx,red_dy))
        if len(red_dxy_log) > red_length:
            red_dxy_log.pop(-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over=True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                blue_dx = -10
                blue_dy = 0
            elif event.key == pygame.K_RIGHT:
                blue_dx = 10
                blue_dy = 0
            elif event.key == pygame.K_UP:
                blue_dx = 0
                blue_dy = -10
            elif event.key == pygame.K_DOWN:
                blue_dx = 0
                blue_dy = 10

            if event.key == pygame.K_a:
                red_dx = -10
                red_dy = 0
            elif event.key == pygame.K_d:
                red_dx = 10
                red_dy = 0
            elif event.key == pygame.K_w:
                red_dx = 0
                red_dy = -10
            elif event.key == pygame.K_s:
                red_dx = 0
                red_dy = 10
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        lshift = 2
    else:
        lshift = 1
    if keys[pygame.K_RSHIFT]:
        rshift = 2
    else:
        rshift = 1

    blue_x += blue_dx*rshift
    blue_y += blue_dy*rshift
    red_x += red_dx*lshift
    red_y += red_dy*lshift

    game_display.fill(black)
    pygame.draw.rect(game_display, blue_head, [blue_x,blue_y,unit,unit])
    pygame.draw.rect(game_display, red_head, [red_x,red_y,unit,unit])
    
    blue_sum_dx, blue_sum_dy = 0, 0
    blue_past = []
    for i in range(len(blue_dxy_log)):
        blue_sum_dx += blue_dxy_log[i][0]
        blue_sum_dy += blue_dxy_log[i][1]
        blue_past_x = blue_x - blue_sum_dx
        blue_past_y = blue_y - blue_sum_dy
        pygame.draw.rect(game_display, blue_body, [blue_past_x,blue_past_y,unit,unit])
        blue_past.append((blue_past_x,blue_past_y))
        if blue_past_x == blue_x and blue_past_y == blue_y:
            game_over = True

    red_sum_dx, red_sum_dy = 0, 0
    red_past = []
    for i in range(len(red_dxy_log)):
        red_sum_dx += red_dxy_log[i][0]
        red_sum_dy += red_dxy_log[i][1]
        red_past_x = red_x - red_sum_dx
        red_past_y = red_y - red_sum_dy
        pygame.draw.rect(game_display, red_body, [red_past_x,red_past_y,unit,unit])
        red_past.append((red_past_x,red_past_y))
        if red_past_x == red_x and red_past_y == red_y:
            game_over = True

    blue_past.append((blue_x,blue_y))
    red_past.append((red_x,red_y))

    for i, (food_x, food_y) in enumerate(food_position):
        pygame.draw.rect(game_display, green, [food_x,food_y,unit,unit])
        if (food_x,food_y) in blue_past:
            food_position.pop(i)
            newfood_x = random.randint(0, 79)
            newfood_y = random.randint(0,59)  
            food_position.insert(i,(10*newfood_x, 10*newfood_y))
            blue_length += 1
        if (food_x,food_y) in red_past:
            food_position.pop(i)
            newfood_x = random.randint(0, 79)
            newfood_y = random.randint(0,59)  
            food_position.insert(i,(10*newfood_x, 10*newfood_y))
            red_length += 1

    pygame.display.update()            
    
    if (blue_x+10)*(blue_x-800)*(blue_y+10)*(blue_y-600) == 0:
        game_over = True
    elif (red_x+10)*(red_x-800)*(red_y+10)*(red_y-600) == 0:
        game_over = True
    
    for blue_position in blue_past:
        if blue_position in red_past:
            game_over = True
    
    clock.tick(10)