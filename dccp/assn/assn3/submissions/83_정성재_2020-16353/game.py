import pygame
import random

pygame.init()

game_display=pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP42 Snake Game')

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 127, 127)
BLUE = (0, 0, 255)
SKYBLUE = (127, 127, 255)

width = 80
height = 60
pixel_size = 10

food_num = 20

game_over = False

class Snake:
    x = 0
    y = 0
    dx = 0
    dy = 0

class Food:
    active = True
    def __init__(self):
        self.x = random.randint(0, width - 1)
        self.y = random.randint(0, height -1)

snake1_pos = []
snake1 = Snake()
snake1.x = 60
snake1.y = 30
snake2_pos = []
snake2 = Snake()
snake2.x = 20
snake2.y = 30

foods = [Food() for i in range(food_num)]

rflag = 1
lflag = 1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake1.dx = -1
                snake1.dy = 0
            elif event.key == pygame.K_RIGHT:
                snake1.dx = 1
                snake1.dy = 0
            elif event.key == pygame.K_UP:
                snake1.dx = 0
                snake1.dy = -1
            elif event.key == pygame.K_DOWN:
                snake1.dx = 0
                snake1.dy = 1
            if event.key == pygame.K_a:
                snake2.dx = -1
                snake2.dy = 0
            elif event.key == pygame.K_d:
                snake2.dx = 1
                snake2.dy = 0
            elif event.key == pygame.K_w:
                snake2.dx = 0
                snake2.dy = -1
            elif event.key == pygame.K_s:
                snake2.dx = 0
                snake2.dy = 1
            if event.key == pygame.K_RSHIFT:
                rflag = 2
            if event.key == pygame.K_LSHIFT:
                lflag = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                rflag = 1
            if event.key == pygame.K_LSHIFT:
                lflag = 1

    game_display.fill(BLACK)

    for food in foods:
        if food.active:
            for x, y in snake1_pos:
                if x == food.x and y == food.y:
                    food.active = False
                    foods.append(Food())
                    snake1_pos.append([snake1.x, snake1.y])
                    snake1.x += snake1.dx
                    snake1.y += snake1.dy
            if snake1.x == food.x and snake1.y == food.y:
                food.active = False
                foods.append(Food())
                snake1_pos.append([snake1.x, snake1.y])
                snake1.x += snake1.dx
                snake1.y += snake1.dy
            for x, y in snake2_pos:
                if x == food.x and y == food.y:
                    food.active = False
                    foods.append(Food())
                    snake2_pos.append([snake2.x, snake2.y])
                    snake2.x += snake2.dx
                    snake2.y += snake2.dy
            if snake2.x == food.x and snake2.y == food.y:
                food.active = False
                foods.append(Food())
                snake2_pos.append([snake2.x, snake2.y])
                snake2.x += snake2.dx
                snake2.y += snake2.dy

    for food in foods:
        if food.active:
            pygame.draw.rect(game_display, WHITE, [food.x * pixel_size, food.y * pixel_size, pixel_size, pixel_size])

    for i in range(rflag):
        if len(snake1_pos) == 1:
            if snake1.x + snake1.dx == snake1_pos[0][0] and snake1.y + snake1.dy == snake1_pos[0][1]:
                game_over = True
        if snake1.x < 0 or snake1.x >= width or snake1.y < 0 or snake1.y >= height:
            game_over = True
        if snake1.x == snake2.x and snake1.y == snake2.y:
            game_over = True
        for x, y in snake1_pos:
            if snake2.x == x and snake2.y == y:
                game_over = True
            if snake1.x == x and snake1.y == y:
                game_over = True
        for x, y in snake2_pos:
            if snake1.x == x and snake1.y == y:
                game_over = True
        snake1_pos.append([snake1.x, snake1.y])
        del snake1_pos[0]
        snake1.x += snake1.dx
        snake1.y += snake1.dy

    for i in range(lflag):
        if len(snake2_pos) == 1:
            if snake2.x + snake2.dx == snake2_pos[0][0] and snake2.y + snake2.dy == snake2_pos[0][1]:
                game_over = True
        if snake2.x < 0 or snake2.x >= width or snake2.y < 0 or snake2.y >= height:
            game_over = True
        if snake1.x == snake2.x and snake1.y == snake2.y:
            game_over = True
        for x, y in snake1_pos:
            if snake2.x == x and snake2.y == y:
                game_over = True
        for x, y in snake2_pos:
            if snake1.x == x and snake1.y == y:
                game_over = True
            if snake2.x == x and snake2.y == y:
                game_over = True
        snake2_pos.append([snake2.x, snake2.y])
        del snake2_pos[0]
        snake2.x += snake2.dx
        snake2.y += snake2.dy

    for x, y in snake1_pos:
        pygame.draw.rect(game_display, RED, [x * pixel_size, y * pixel_size, pixel_size, pixel_size])
    for x, y in snake2_pos:
        pygame.draw.rect(game_display, BLUE, [x * pixel_size, y * pixel_size, pixel_size, pixel_size])
    pygame.draw.rect(game_display, PINK, [snake1.x * pixel_size, snake1.y * pixel_size, pixel_size, pixel_size])
    pygame.draw.rect(game_display, SKYBLUE, [snake2.x * pixel_size, snake2.y * pixel_size, pixel_size, pixel_size])

    pygame.display.update()
    clock.tick(5)