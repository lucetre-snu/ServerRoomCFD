import pygame
import random

black = (0, 0, 0)
lightred = (255,200,200)
red = (255, 60, 60)
green = (0, 255, 0)
lightblue = (0,200,255)
blue = (0,100,255) 

pygame.init()

sanke_display = pygame.display.set_mode((800, 400))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

game_over = False

x1 = 600
y1 = 200
dx1 = 0
dy1 = 0
player1_snake_List = []
player1_Length_of_snake = 1

x2 = 200
y2 = 200
dx2 = 0
dy2 = 0
player2_snake_List = []
player2_Length_of_snake = 1

def player1_snake(player1_snake_list):
    for x in player1_snake_list:
        if x==player1_snake_list[-1]:
            pygame.draw.rect(sanke_display, lightred, [x[0], x[1], 10, 10])
        else:
            pygame.draw.rect(sanke_display, red, [x[0], x[1], 10, 10])
def player2_snake(player2_snake_list):
    for y in player2_snake_list:
        if y==player2_snake_list[-1]:
            pygame.draw.rect(sanke_display, lightblue, [y[0], y[1], 10, 10])
        else:
            pygame.draw.rect(sanke_display, blue, [y[0], y[1], 10, 10])

foodx1 = random.randint(0,79)*10
foody1 = random.randint(0,39)*10
foodx2 = random.randint(0,79)*10
foody2 = random.randint(0,39)*10
foodx3 = random.randint(0,79)*10
foody3 = random.randint(0,39)*10
foodx4 = random.randint(0,79)*10
foody4 = random.randint(0,39)*10
foodx5 = random.randint(0,79)*10
foody5 = random.randint(0,39)*10
foodx6 = random.randint(0,79)*10
foody6 = random.randint(0,39)*10
foodx7 = random.randint(0,79)*10
foody7 = random.randint(0,39)*10
foodx8 = random.randint(0,79)*10
foody8 = random.randint(0,39)*10
foodx9 = random.randint(0,79)*10
foody9 = random.randint(0,39)*10
foodx10 = random.randint(0,79)*10
foody10 = random.randint(0,39)*10
foodx11 = random.randint(0,79)*10
foody11 = random.randint(0,39)*10
foodx12 = random.randint(0,79)*10
foody12 = random.randint(0,39)*10
foodx13 = random.randint(0,79)*10
foody13 = random.randint(0,39)*10
foodx14 = random.randint(0,79)*10
foody14 = random.randint(0,39)*10
foodx15 = random.randint(0,79)*10
foody15 = random.randint(0,39)*10
foodx16 = random.randint(0,79)*10
foody16 = random.randint(0,39)*10
foodx17 = random.randint(0,79)*10
foody17 = random.randint(0,39)*10
foodx18 = random.randint(0,79)*10
foody18 = random.randint(0,39)*10
foodx19 = random.randint(0,79)*10
foody19 = random.randint(0,39)*10
foodx20 = random.randint(0,79)*10
foody20 = random.randint(0,39)*10

player1_boost=0
player2_boost=0
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx1 = -10
                dy1 = 0
            elif event.key == pygame.K_RIGHT:
                dx1 = 10
                dy1 = 0
            elif event.key == pygame.K_UP:
                dy1 = -10
                dx1 = 0
            elif event.key == pygame.K_DOWN:
                dy1 = 10
                dx1 = 0
            elif event.key==pygame.K_RSHIFT:
                if player1_boost== 0:
                    player1_boost= 1
                elif player1_boost== 1:
                    player1_boost= 0

            elif event.key == pygame.K_a:
                dx2 = -10
                dy2 = 0
            elif event.key == pygame.K_d:
                dx2 = 10
                dy2 = 0
            elif event.key == pygame.K_w:
                dy2 = -10
                dx2 = 0
            elif event.key == pygame.K_s:
                dy2 = 10
                dx2 = 0
            elif event.key==pygame.K_LSHIFT:
                if player2_boost == 0:
                    player2_boost = 1
                elif player2_boost == 1:
                    player2_boost = 0
    x1 += dx1
    y1 += dy1
    if player1_boost == 1:
        x1 += dx1
        y1 += dy1
        
    x2 += dx2
    y2 += dy2
    if player2_boost == 1:
        x2 += dx2
        y2 += dy2

    sanke_display.fill(black)

    if  x1 >= 800 or x1 < 0 or y1 >= 400 or y1 < 0 or x2 >= 800 or x2 < 0 or y2 >= 400 or y2 < 0:
        game_over = True
    
    pygame.draw.rect(sanke_display, green, [foodx1, foody1, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx2, foody2, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx3, foody3, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx4, foody4, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx5, foody5, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx6, foody6, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx7, foody7, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx8, foody8, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx9, foody9, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx10, foody10, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx11, foody11, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx12, foody12, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx13, foody13, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx14, foody14, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx15, foody15, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx16, foody16, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx17, foody17, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx18, foody18, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx19, foody19, 10, 10])
    pygame.draw.rect(sanke_display, green, [foodx20, foody20, 10, 10])

    player1_snake_Head = []
    player1_snake_Head.append(x1)
    player1_snake_Head.append(y1)
    player1_snake_List.append(player1_snake_Head)

    player2_snake_Head = []
    player2_snake_Head.append(x2)
    player2_snake_Head.append(y2)
    player2_snake_List.append(player2_snake_Head)

    if len(player1_snake_List) > player1_Length_of_snake:
        del player1_snake_List[0]
    for x in player1_snake_List[:-1]:
        if x == player1_snake_Head:
            game_over = True

    if len(player2_snake_List) > player2_Length_of_snake:
        del player2_snake_List[0]
    for y in player2_snake_List[:-1]:
        if y == player2_snake_Head:
            game_over = True
        
    for x in player1_snake_List:
        for y in player2_snake_List:
            if x==y:
                game_over = True
 
    player1_snake(player1_snake_List)

    player2_snake(player2_snake_List)

    pygame.display.update()

    if x1 == foodx1 and y1 == foody1:
        foodx1 = random.randint(0,79)*10
        foody1 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx2 and y1 == foody2:
        foodx2 = random.randint(0,79)*10
        foody2 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx3 and y1 == foody3:
        foodx3 = random.randint(0,79)*10
        foody3 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx4 and y1 == foody4:
        foodx4 = random.randint(0,79)*10
        foody4 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx5 and y1 == foody5:
        foodx5 = random.randint(0,79)*10
        foody5 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx6 and y1 == foody6:
        foodx6 = random.randint(0,79)*10
        foody6 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx7 and y1 == foody7:
        foodx7 = random.randint(0,79)*10
        foody7 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx8 and y1 == foody8:
        foodx8 = random.randint(0,79)*10
        foody8 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx9 and y1 == foody9:
        foodx9 = random.randint(0,79)*10
        foody9 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx10 and y1 == foody10:
        foodx10 = random.randint(0,79)*10
        foody10 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx11 and y1 == foody11:
        foodx11 = random.randint(0,79)*10
        foody11 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx12 and y1 == foody12:
        foodx12 = random.randint(0,79)*10
        foody12 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx13 and y1 == foody13:
        foodx13 = random.randint(0,79)*10
        foody13 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx14 and y1 == foody14:
        foodx14 = random.randint(0,79)*10
        foody14 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx15 and y1 == foody15:
        foodx15 = random.randint(0,79)*10
        foody15 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx16 and y1 == foody16:
        foodx16 = random.randint(0,79)*10
        foody16 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx17 and y1 == foody17:
        foodx17 = random.randint(0,79)*10
        foody17 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx18 and y1 == foody18:
        foodx18 = random.randint(0,79)*10
        foody18 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx19 and y1 == foody19:
        foodx19 = random.randint(0,79)*10
        foody19 = random.randint(0,39)*10
        player1_Length_of_snake += 1
    elif x1 == foodx20 and y1 == foody20:
        foodx20 = random.randint(0,79)*10
        foody20 = random.randint(0,39)*10
        player1_Length_of_snake += 1

    elif x2 == foodx1 and y2 == foody1:
        foodx1 = random.randint(0,79)*10
        foody1 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx2 and y2 == foody2:
        foodx2 = random.randint(0,79)*10
        foody2 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx3 and y2 == foody3:
        foodx3 = random.randint(0,79)*10
        foody3 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx4 and y2 == foody4:
        foodx4 = random.randint(0,79)*10
        foody4 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx5 and y2 == foody5:
        foodx5 = random.randint(0,79)*10
        foody5 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx6 and y2 == foody6:
        foodx6 = random.randint(0,79)*10
        foody6 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx7 and y2 == foody7:
        foodx7 = random.randint(0,79)*10
        foody7 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx8 and y2 == foody8:
        foodx8 = random.randint(0,79)*10
        foody8 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx9 and y2 == foody9:
        foodx9 = random.randint(0,79)*10
        foody9 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx10 and y2 == foody10:
        foodx10 = random.randint(0,79)*10
        foody10 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx11 and y2 == foody11:
        foodx11 = random.randint(0,79)*10
        foody11 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx12 and y2 == foody12:
        foodx12 = random.randint(0,79)*10
        foody12 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx13 and y2 == foody13:
        foodx13 = random.randint(0,79)*10
        foody13 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx14 and y2 == foody14:
        foodx14 = random.randint(0,79)*10
        foody14 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx15 and y2 == foody15:
        foodx15 = random.randint(0,79)*10
        foody15 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx16 and y2 == foody16:
        foodx16 = random.randint(0,79)*10
        foody16 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx17 and y2 == foody17:
        foodx17 = random.randint(0,79)*10
        foody17 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx18 and y2 == foody18:
        foodx18 = random.randint(0,79)*10
        foody18 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx19 and y2 == foody19:
        foodx19 = random.randint(0,79)*10
        foody19 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    elif x2 == foodx20 and y2 == foody20:
        foodx20 = random.randint(0,79)*10
        foody20 = random.randint(0,39)*10
        player2_Length_of_snake += 1
    
    pygame.display.update()
    clock.tick(10)