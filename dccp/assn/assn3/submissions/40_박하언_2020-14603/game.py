import pygame
import random
import sys
import time

frame_size_x = 800
frame_size_y = 600
pygame.init()

pygame.display.set_caption('DCCP Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIME = (173,216,230)
PINK = (255,192,222)

clock = pygame.time.Clock()


snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-20, 50]]

snake_pos2 = [200, 50]
snake_body2 = [[200, 50], [200-10, 50], [200-20, 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

food_coordinates=[]
for _ in range(20):
    food_x = random.randint(0,79)
    food_y = random.randint(0,59)
    food_coordinates.append((10*food_x,10*food_y))

food_active = [True for _ in range(20)]

d = 'RIGHT'
c = d
d1 = 'RIGHT'
c1 = d1

def game_over(redwon):
    my_font = pygame.font.SysFont('times new roman', 92)
    if redwon:
        game_over_surface = my_font.render('RED WON!', True, RED)
    else:
        game_over_surface = my_font.render('BLUE WON!', True, BLUE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

while True:
    b1 = 1
    b2 = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over(True)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                c = 'UP'
            if event.key == pygame.K_DOWN:
                c = 'DOWN'
            if event.key == pygame.K_LEFT:
                c = 'LEFT'
            if event.key == pygame.K_RIGHT:
                c = 'RIGHT'
            if event.key == pygame.K_RSHIFT:
                b1 = 2

            if event.key == ord('w'):
                c1 = 'UP'
            if event.key == ord('s'):
                c1 = 'DOWN'
            if event.key == ord('a'):
                c1 = 'LEFT'
            if event.key == ord('d'):
                c1 = 'RIGHT'
            if event.key == pygame.K_LSHIFT:
                b2 = 2 
    if c == 'UP' and d != 'DOWN':
        d = 'UP'
    if c == 'DOWN' and d != 'UP':
        d = 'DOWN'
    if c == 'LEFT' and d != 'RIGHT':
        d = 'LEFT'
    if c == 'RIGHT' and d != 'LEFT':
        d = 'RIGHT'

    if d == 'UP':
        snake_pos[1] -= 10*b1
    if d == 'DOWN':
        snake_pos[1] += 10*b1
    if d == 'LEFT':
        snake_pos[0] -= 10*b1
    if d == 'RIGHT':
        snake_pos[0] += 10*b1

    if c1 == 'UP' and d1 != 'DOWN':
        d1 = 'UP'
    if c1 == 'DOWN' and d1 != 'UP':
        d1 = 'DOWN'
    if c1 == 'LEFT' and d1 != 'RIGHT':
        d1 = 'LEFT'
    if c1 == 'RIGHT' and d1 != 'LEFT':
        d1 = 'RIGHT'

    if d1 == 'UP':
        snake_pos2[1] -= 10*b2
    if d1 == 'DOWN':
        snake_pos2[1] += 10*b2
    if d1 == 'LEFT':
        snake_pos2[0] -= 10*b2
    if d1 == 'RIGHT':
        snake_pos2[0] += 10*b2

    
    game_window.fill(BLACK)
    z = 0
    z1 = 0
    for pos in snake_body:
        if z == 0:
            pygame.draw.rect(game_window, PINK, pygame.Rect(pos[0], pos[1], 10, 10))
        else:
            pygame.draw.rect(game_window, RED, pygame.Rect(pos[0], pos[1], 10, 10))
        z+=1

    for pos1 in snake_body2:
        if z1 == 0:
            pygame.draw.rect(game_window, LIME, pygame.Rect(pos1[0], pos1[1], 10, 10))
        elif b2 == 2:
            pygame.draw.rect(game_window, BLUE, pygame.Rect(pos1[0], pos1[1], 10, 10))
        else:
            pygame.draw.rect(game_window, BLUE, pygame.Rect(pos1[0], pos1[1], 10, 10))
        z1+=1

    snake_body.insert(0, list(snake_pos))
    snake_body2.insert(0, list(snake_pos2))
    for i,(food_x,food_y) in enumerate(food_coordinates):
        if food_active[i]:
            pygame.draw.rect(game_window, GREEN,[food_x,food_y,10,10])

    redate = False
    blueate = False
    for i, (food_x, food_y) in enumerate(food_coordinates):
        if snake_pos[0] == food_x and snake_pos[1] == food_y:
            food_active[i]=False
            food_spawn = False
            redate = True
        if snake_pos2[0] == food_x and snake_pos2[1] == food_y:
            food_active[i]=False
            food_spawn = False
            blueate = True
    if food_spawn:
            snake_body.pop()
            snake_body2.pop()

    if not food_spawn:
        food_coordinates.append((10*random.randint(0,79),10*random.randint(0,59)))    
        food_active.append(True)
        food_spawn = True    

    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over(False)
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over(False)
    if snake_pos2[0] < 0 or snake_pos2[0] > frame_size_x-10:
        game_over(True)
    if snake_pos2[1] < 0 or snake_pos2[1] > frame_size_y-10:
        game_over(True)

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over(False)

    for block in snake_body2[1:]:
        if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
            game_over(True)

    for block in snake_body[1:]:
        if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
            game_over(True)
        
    for block in snake_body2[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over(False)
            
    pygame.display.update()
    clock.tick(15)