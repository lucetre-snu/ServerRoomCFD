import pygame
import random
from datetime import datetime
from datetime import timedelta

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
Yellow = (255,255,0)
size = [800,600]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now() 

KEY_DIRECTION1 = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

KEY_DIRECTION2 = {
    pygame.K_w: 'U',
    pygame.K_s: 'D',
    pygame.K_a: 'L',
    pygame.K_d: 'R',
}

def draw_block(screen, color, position):
    block = pygame.Rect((position[1]*10, position[0]*10),(10,10))
    pygame.draw.rect(screen, color, block)

class Snake1:
    def __init__(self):
        self.positions= [(0,2),(0,1),(0,0)]
        self.direction = ''
        self.boost = False

    def draw(self):
        draw_block(screen, WHITE, self.positions[0])
        for position in self.positions[1:]:
            draw_block(screen, RED, position)

    def move(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='N':
            self.positions = [(y-1,x)]+self.positions[:-1]
        elif self.direction =='S':
            self.positions = [(y+1,x)]+self.positions[:-1]
        elif self.direction =='W':
            self.positions = [(y,x-1)]+self.positions[:-1]
        elif self.direction =='E':
            self.positions = [(y,x+1)]+self.positions[:-1]

    def Boost(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='N':
            self.positions = [(y-2,x)]+[(y-1,x)]+self.positions[:-2]
        elif self.direction =='S':
            self.positions = [(y+2,x)]+[(y+1,x)]+self.positions[:-2]
        elif self.direction =='W':
            self.positions = [(y,x-2)]+[(y,x-1)]+self.positions[:-2]
        elif self.direction =='E':
            self.positions = [(y,x+2)]+[(y,x+1)]+self.positions[:-2]


    def grow(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='N':
            self.positions[0] = (y-1,x)
            self.positions.insert(1,(y,x))
        elif self.direction == 'S':
            self.positions[0] = (y+1,x)
            self.positions.insert(1,(y,x))
        elif self.direction == 'W':
            self.positions[0] = (y,x-1)
            self.positions.insert(1,(y,x))
        elif self.direction == 'E':
            self.positions[0] = (y,x+1)
            self.positions.insert(1,(y,x))

class Snake2:
    def __init__(self):
        self.positions= [(58,76),(58,77),(58,78)]
        self.direction = ''
        self.boost = False
        
    def draw(self):
        draw_block(screen, Yellow, self.positions[0])
        for position in self.positions[1:]:
            draw_block(screen, BLUE, position)

    def move(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='U':
            self.positions = [(y-1,x)]+self.positions[:-1]
        elif self.direction =='D':
            self.positions = [(y+1,x)]+self.positions[:-1]
        elif self.direction =='L':
            self.positions = [(y,x-1)]+self.positions[:-1]
        elif self.direction =='R':
            self.positions = [(y,x+1)]+self.positions[:-1]

    def Boost(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='U':
            self.positions = [(y-2,x)]+[(y-1,x)]+self.positions[:-2]
        elif self.direction =='D':
            self.positions = [(y+2,x)]+[(y+1,x)]+self.positions[:-2]
        elif self.direction =='L':
            self.positions = [(y,x-2)]+[(y,x-1)]+self.positions[:-2]
        elif self.direction =='R':
            self.positions = [(y,x+2)]+[(y,x+1)]+self.positions[:-2]


    def grow(self):
        head_position = self.positions[0]
        y,x = head_position
        if self.direction =='U':
            self.positions[0] = (y-1,x)
            self.positions.insert(1,(y,x))
        elif self.direction == 'D':
            self.positions[0] = (y+1,x)
            self.positions.insert(1,(y,x))
        elif self.direction == 'L':
            self.positions[0] = (y,x-1)
            self.positions.insert(1,(y,x))
        elif self.direction == 'R':
            self.positions[0] = (y,x+1)
            self.positions.insert(1,(y,x))

class Food:
    def __init__(self):
        self.position = (random.randint(0,79),random.randint(0,59))
        self.active = True

    def draw(self):
        draw_block(screen, GREEN, self.position) 

def runGame():
    global done, last_moved_time
    snake1 = Snake1()
    snake2 = Snake2()
    foods = [Food() for _ in range(20)]

    while not done:
        screen.fill(BLACK)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                done = True
            if event.type ==pygame.KEYDOWN:
                if event.key in KEY_DIRECTION1:
                    snake1.direction = KEY_DIRECTION1[event.key]
                if event.key in KEY_DIRECTION2:
                    snake2.direction = KEY_DIRECTION2[event.key]
                if event.key == pygame.K_RSHIFT:
                    snake1.boost = True
                if event.key == pygame.K_LSHIFT:
                    snake2.boost = True
            if event.type ==pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    snake1.boost = False
                if event.key == pygame.K_LSHIFT:
                    snake2.boost = False

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            if snake1.boost:
                snake1.Boost()
            if snake2.boost:
                snake2.Boost()
            if not snake1.boost:
                snake1.move()
            if not snake2.boost:
                snake2.move()           
            last_moved_time = datetime.now()
        
        for food in foods:
            if food.active:
                food.draw()

            if food.position in snake1.positions:
                snake1.grow()
                food.active = False
                food.position = None
                foods.append(Food())

            if food.position in snake2.positions:
                snake2.grow()
                food.active = False
                food.position = None
                foods.append(Food())

        
        if (snake1.positions[0] in snake1.positions[1:]) or (snake2.positions[0] in snake2.positions[1:]) or (snake1.positions[0] in snake2.positions[1:]) or (snake2.positions[0] in snake1.positions[1:]):
            done = True

        if not ((0<=snake1.positions[0][0]<=60 and 0<=snake1.positions[0][1]<=80)and(0<=snake2.positions[0][0]<=60 and 0<=snake2.positions[0][1]<=80)):
            done = True

        snake1.draw()
        snake2.draw()
        pygame.display.update()

runGame()
pygame.quit()