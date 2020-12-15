import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (100, 100, 255)

pygame.init()

tile_size = 10

game_display = pygame.display.set_mode((80*tile_size, 60*tile_size))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()                        

game_over = False

# Player 1
x = 600
y = 300
dx = 0
dy = 0
prev_posx = 0
prev_posy = 0
body = []
body_show = 0

# Player 2
x2 = 200
y2 = 300
dx2 = 0
dy2 = 0
prev_posx2 = 0
prev_posy2 = 0
body2 = []
body2_show = 0

food_coordinates = []
food_num = 20
for _ in range(food_num):
    food_x = random.randint(0, 79)
    food_y = random.randint(0, 59)
    food_coordinates.append((food_x*tile_size, food_y*tile_size))

food_active = [True for _ in range(food_num)]

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -tile_size
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = tile_size
                dy = 0
            elif event.key == pygame.K_UP:
                dx = 0
                dy = -tile_size
            elif event.key == pygame.K_DOWN:
                dx = 0
                dy = tile_size
            elif event.key == pygame.K_RSHIFT:
                if prev_posx == x and prev_posy > y:
                    dx = 0
                    dy = -tile_size*2
                elif prev_posx == x and prev_posy < y:
                    dx = 0
                    dy = tile_size*2
                elif prev_posx > x and prev_posy == y:
                    dx = -tile_size*2
                    dy = 0
                elif prev_posx < x and prev_posy == y:
                    dx = tile_size*2
                    dy = 0
            elif event.key == pygame.K_w:
                dx2 = 0
                dy2 = -tile_size
            elif event.key == pygame.K_s:
                dx2 = 0
                dy2 = tile_size
            elif event.key == pygame.K_a:
                dx2 = -tile_size
                dy2 = 0
            elif event.key == pygame.K_d:
                dx2 = tile_size
                dy2 = 0
            elif event.key == pygame.K_LSHIFT:
                if prev_posx2 == x2 and prev_posy2 > y2:
                    dx2 = 0
                    dy2 = -tile_size*2
                elif prev_posx2 == x2 and prev_posy2 < y2:
                    dx2 = 0
                    dy2 = tile_size*2
                elif prev_posx2 > x2 and prev_posy2 == y2:
                    dx2 = -tile_size*2
                    dy2 = 0
                elif prev_posx2 < x2 and prev_posy2 == y2:
                    dx2 = tile_size*2
                    dy2 = 0                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                if prev_posx == x and prev_posy > y:
                    dx = 0
                    dy = -tile_size
                elif prev_posx == x and prev_posy < y:
                    dx = 0
                    dy = tile_size
                elif prev_posx > x and prev_posy == y:
                    dx = -tile_size
                    dy = 0
                elif prev_posx < x and prev_posy == y:
                    dx = tile_size
                    dy = 0
            elif event.key == pygame.K_LSHIFT:
                if prev_posx2 == x2 and prev_posy2 > y2:
                    dx2 = 0
                    dy2 = -tile_size
                elif prev_posx2 == x2 and prev_posy2 < y2:
                    dx2 = 0
                    dy2 = tile_size
                elif prev_posx2 > x2 and prev_posy2 == y2:
                    dx2 = -tile_size
                    dy2 = 0
                elif prev_posx2 < x2 and prev_posy2 == y2:
                    dx2 = tile_size
                    dy2 = 0                           

    game_display.fill(BLACK)
    
    # Player 1 Position Change
    prev_posx = x
    prev_posy = y
    x += dx
    y += dy
    x_pass = (x + prev_posx) / 2
    y_pass = (y + prev_posy) / 2
    position = [x, y, 10, 10]
    passed_position = [x_pass, y_pass, 10, 10]

    # Player 2 Position Change
    prev_posx2 = x2
    prev_posy2 = y2
    x2 += dx2
    y2 += dy2
    x2_pass = (x2 + prev_posx2) / 2
    y2_pass = (y2 + prev_posy2) / 2
    position2 = [x2, y2, 10, 10]
    passed_position2 = [x2_pass, y2_pass, 10, 10]

    if x >= 800 or x <= -10:
        game_over = True
        break
    if y >= 600 or y <= -10:
        game_over = True
        break
    if x2 >= 800 or x2 <= -10:
        game_over = True
        break
    if y2 >= 600 or y2 <= -10:
        game_over = True
        break

    if x_pass % 10 == 0 and y_pass % 10 == 0:
        body.append(passed_position)
    if x2_pass % 10 == 0 and y2_pass % 10 == 0:
        body2.append(passed_position2)

    show_active = body[(len(body) - body_show):len(body)]
    show_active2 = body2[(len(body2) - body2_show):len(body2)]
    for element in show_active:
        pygame.draw.rect(game_display, WHITE, element)
    for element in show_active2:
        pygame.draw.rect(game_display, YELLOW, element)

    body.append(position)
    body2.append(position2)

    for element in show_active:
        if position == element:
            game_over = True
            break
        elif position2 == element:
            game_over = True
            break
    
    for element in show_active2:
        if position == element:
            game_over = True
            break
        elif position2 == element:
            game_over = True
            break

    pygame.draw.rect(game_display, PURPLE, position)
    pygame.draw.rect(game_display, RED, position2)

    for i, (food_x, food_y) in enumerate(food_coordinates):
        if food_active[i]:
            pygame.draw.rect(game_display, GREEN, [food_x, food_y, 10, 10])

    for i, (food_x, food_y) in enumerate(food_coordinates):
        if (x == food_x and y == food_y) or (x_pass == food_x and y_pass == food_y):
            food_active[i] = False
            food_new_x = random.randint(0, 79)
            food_new_y = random.randint(0, 59)
            food_coordinates.append((food_new_x*tile_size, food_new_y*tile_size))
            food_active.append(True)
            body_show += 1
        if (x2 == food_x and y2 == food_y) or (x2_pass == food_x and y2_pass == food_y):
            food_active[i] = False
            food_new_x2 = random.randint(0, 79)
            food_new_y2 = random.randint(0, 59)
            food_coordinates.append((food_new_x2*tile_size, food_new_y2*tile_size))
            food_active.append(True)
            body2_show += 1

    food_remains = False
    for active in food_active:
        if active:
            food_remains = True
    
    if not food_remains:
        game_over = True

    pygame.display.update()

    clock.tick(10)
