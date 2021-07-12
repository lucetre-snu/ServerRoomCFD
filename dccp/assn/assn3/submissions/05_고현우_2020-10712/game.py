import random
import pygame
from pygame.constants import QUIT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snack game')
clock = pygame.time.Clock()

game_over = False

x = 400
y = 300
dx = 0
dy = 0

foods = []
eaten = []
for i in range(20):
    food_x = random.randint(0, 79) # 0~78 * 10 0~790+10
    food_y = random.randint(0, 59)
    foods.append((10* food_x, 10* food_y)) # ㅇㅜㅣㅊㅣ ㅈㅗㅈㅓㅇ ㅋㅡㄱㅏㄱㅏ 10ㅇㅣㅁ.
    eaten.append(True)

# game_display.fill(WHITE)
# pygame.draw.rect(game_display, BLACK, [x, 300, 20, 10])
# pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        #print(event) # ㅇㅕㄹㅓㄱㅏㅈㅣ ㅇㅣㅂㅔㄴㅌㅡ ㅇㅗㅏ ㅈㅗㅇㄹㅠ
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
                dy = -10 ### warnging
                dx =0
            elif event.key == pygame.K_DOWN:
                dy = 10
                dx =0

    x += dx
    y += dy            
    game_display.fill(BLACK)
    pygame.draw.rect(game_display, WHITE, [x, y, 10, 10])
    for i, (food_x, food_y) in enumerate(foods): # ㅅㅐㅇㅅㅓㅇㅎㅏㄴㅡㄴ ㄱㅓㅅㅇㅣㅁ! 
        if eaten[i]:
            pygame.draw.rect(game_display, GREEN, [food_x, food_y, 10, 10])
    
    for i, (food_x, food_y) in enumerate(foods):
        if x==food_x and y == food_y:
            eaten[i]=False
    pygame.display.update()    

    # if not any(eaten): # ㅎㅏㄴㄱㅐㅇㅡㅣ ㅇㅛㅅㅗㄹㅏㄷㅗ ㅊㅏㅁㅇㅣㄴㄱㅔ ㅇㅣㅆㅇㅡㅁㅕㄴ ㅌㅏㅁㅇㅡㄹ ㅂㅏㄴㅎㅗㅏㄴㅎㅏㄴㅡㄴ ㅎㅏㅁㅅㅜㅇㅡㅣ ㅇㅕㄱ
    fdrm = False
    for active in eaten:
        if active:
            fdrm = True
    if not fdrm:
        game_over = True

    #pygame.display.update()    
    clock.tick(10)
