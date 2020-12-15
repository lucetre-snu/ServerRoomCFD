import pygame
import random

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

pygame.init()

game_display= pygame.display.set_mode((800,600))
pygame.display.set_caption("DCCP Snake Game")

game_over =False 
clock=pygame.time.Clock()
x=400
dx=0
y=300
dy=0
k=10
food_coordinate=[]
food_active=[]
for _ in range(20):
    food_x=random.randint(0,79) 
    food_y=random.randint(0,59)
    food_coordinate.append((10*food_x,10*food_y))
    food_y=300

food_active=[True for _ in range(20)]

while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                game_over=True
                break 
        
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                dx=10
                dy=0
            if event.key==pygame.K_LEFT:
                dx=-10
                dy=0
            if event.key==pygame.K_UP:
                dy=-10
                dx=0
            if event.key==pygame.K_DOWN:
                dy=10
                dx=0
    x+=dx
    y+=dy
    game_display.fill(BLACK)
    pygame.draw.rect(game_display,WHITE,[x,y,10,10])
    for i, (food_x,food_y) in enumerate(food_coordinate):
        pygame.draw.rect(game_display,GREEN,[food_x,food_y,10,10])

    for i, (food_x,food_y) in enumerate(food_coordinate):
        if x==food_x and y==food_y:
            food_coordinate.remove((food_x,food_y))
            a=random.randint(0,79)
            b=random.randint(0,59)
            food_coordinate.append((10*a,10*b))
            
    pygame.display.update()   
    clock.tick(k)
    if x>800 or x<0 or y<0 or y>600:
        game_over=True
    