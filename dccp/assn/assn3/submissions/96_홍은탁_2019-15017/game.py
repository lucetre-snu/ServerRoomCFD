import pygame
import random

pygame.init()

game_display = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Snake Game')
game_display.fill((255, 255, 255))
pygame.display.update()

x = 800
y = 300
dx = 0
dy = 0

PLAYERS = [(800, 300)]

a = 200
b = 300
da = 0
db = 0

PLAYERS_2 = [(200, 300)]

clock = pygame.time.Clock()

FOODS = []
while len(FOODS) != 20:
    food_x = random.randint(0, 99) * 10
    food_y = random.randint(0, 59) * 10
    if not (food_x == x and food_y == y) and not (food_x == a and food_y == b) and (food_x, food_y) not in FOODS:
        FOODS.append((food_x, food_y))

for FOOD in FOODS:
    pygame.draw.rect(game_display, (255, 255, 0), [FOOD[0], FOOD[1], 10, 10])

game_over = False
n = 1
k = 1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx != 10:
                dx = -10
                dy = 0
            elif event.key == pygame.K_RIGHT and dx != -10:
                dx = 10
                dy = 0
            elif event.key == pygame.K_UP and dy != 10:
                dx = 0
                dy = -10
            elif event.key == pygame.K_DOWN and dy != -10:
                dx = 0
                dy = 10
            elif event.key == pygame.K_a and da != 10:
                da = -10
                db = 0
            elif event.key == pygame.K_d and da != -10:
                da = 10
                db = 0
            elif event.key == pygame.K_w and db != 10:
                da = 0
                db = -10
            elif event.key == pygame.K_s and db != -10:
                da = 0
                db = 10
            elif event.key == pygame.K_RSHIFT:
                n = 2
            elif event.key == pygame.K_LSHIFT:
                k = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                n = 1
            elif event.key == pygame.K_LSHIFT:
                k = 1
    for i in range(n):
        eat = False

        x += dx
        y += dy

        if not 0 <= x <= 990 or not 0 <= y <= 590:
            game_over = True
            break
        
        if (x, y) in PLAYERS + PLAYERS_2 and not (dx == 0 and dy ==0):
            game_over = True
            break
        else:
            PLAYERS.append((x, y))

        game_display.fill((0, 0, 0))

        for (food_x, food_y) in FOODS:
            if food_x == x and food_y == y:
                FOODS.remove((food_x, food_y))
                while len(FOODS) != 20:
                    f_x = random.randint(0, 99) * 10
                    f_y = random.randint(0, 59) * 10
                    if (f_x, f_y) not in PLAYERS + PLAYERS_2 and (f_x, f_y) not in FOODS:
                        FOODS.append((f_x, f_y))
                eat = True

        for (food_x, food_y) in FOODS:
            pygame.draw.rect(game_display, (255, 255, 0), [food_x, food_y, 10, 10])

        if not eat:
            PLAYERS.remove(PLAYERS[0])
        
        pygame.draw.rect(game_display, (255, 0, 0), [PLAYERS[-1][0], PLAYERS[-1][1], 10, 10])
        for (player_x, player_y) in PLAYERS[:len(PLAYERS)-1]:
            pygame.draw.rect(game_display, (255, 127, 127), [player_x, player_y, 10, 10])

        pygame.draw.rect(game_display, (0, 0, 255), [PLAYERS_2[-1][0], PLAYERS_2[-1][1], 10, 10])
        for (player_x, player_y) in PLAYERS_2[:len(PLAYERS_2)-1]:
            pygame.draw.rect(game_display, (127, 127, 255), [player_x, player_y, 10, 10])

        pygame.display.update()

    for i in range(k):
        eat_2 = False

        a += da
        b += db

        if not 0 <= a <= 990 or not 0 <= b <= 590:
            game_over = True
            break
        
        if (a, b) in PLAYERS + PLAYERS_2 and not (da == 0 and db ==0):
            game_over = True
            break
        else:
            PLAYERS_2.append((a, b))

        game_display.fill((0, 0, 0))

        for (food_x, food_y) in FOODS:
            if food_x == a and food_y == b:
                FOODS.remove((food_x, food_y))
                while len(FOODS) != 20:
                    f_x = random.randint(0, 99) * 10
                    f_y = random.randint(0, 59) * 10
                    if (f_x, f_y) not in PLAYERS + PLAYERS_2 and (f_x, f_y) not in FOODS:
                        FOODS.append((f_x, f_y))
                eat_2 = True

        for (food_x, food_y) in FOODS:
            pygame.draw.rect(game_display, (255, 255, 0), [food_x, food_y, 10, 10])

        if not eat_2:
            PLAYERS_2.remove(PLAYERS_2[0])
        
        pygame.draw.rect(game_display, (255, 0, 0), [PLAYERS[-1][0], PLAYERS[-1][1], 10, 10])
        for (player_x, player_y) in PLAYERS[:len(PLAYERS)-1]:
            pygame.draw.rect(game_display, (255, 127, 127), [player_x, player_y, 10, 10])

        pygame.draw.rect(game_display, (0, 0, 255), [PLAYERS_2[-1][0], PLAYERS_2[-1][1], 10, 10])
        for (player_x, player_y) in PLAYERS_2[:len(PLAYERS_2)-1]:
            pygame.draw.rect(game_display, (127, 127, 255), [player_x, player_y, 10, 10])

        pygame.display.update()

    clock.tick(10)