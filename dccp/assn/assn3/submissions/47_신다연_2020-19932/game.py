import pygame
import random
from pygame.constants import QUIT 
from pygame.constants import KEYDOWN
from pygame.constants import K_LEFT
from pygame.constants import K_RIGHT
from pygame.constants import K_UP
from pygame.constants import K_DOWN
from pygame.constants import K_w
from pygame.constants import K_a
from pygame.constants import K_s
from pygame.constants import K_d
from pygame.constants import K_RSHIFT
from pygame.constants import K_LSHIFT

#constants
BLACK=(0,0,0)
GREEN=(32, 163, 68)
PINK=(238, 195, 218)
PURPLE=(172, 110, 217)
SKY_BLUE=(174, 209, 247)
BLUE = (98, 107, 215)

display_size = (800, 600)

#lists
player1_body = [[(display_size[0]//2)//2,display_size[1]//2]]
player2_body = [[(display_size[0]//2)*1.5,(display_size[1]//2)]]

#game starter
pygame.init()

#display setting
game_display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Snake Game')

#====================class definition====================#
class Player1:
    x = (display_size[0]//2)//2
    y = display_size[1]//2
    dx = 0
    dy = 0


    def __init__(self, display):
        self.display = display

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                if len(player1_body) != 1 and self.dx == 10:
                    pass
                else:
                    self.dx = -10
                    self.dy = 0
            elif event.key == K_d:
                if len(player1_body) != 1 and self.dx == -10:
                    pass
                else:
                    self.dx = 10
                    self.dy = 0
            elif event.key == K_w:
                if len(player1_body) != 1 and self.dy == 10:
                    pass
                else:
                    self.dy = -10
                    self.dx = 0
            elif event.key == K_s:
                if len(player1_body) != 1 and self.dy == -10:
                    pass
                else:
                    self.dy = 10
                    self.dx = 0                                                

    def handle_tick(self):
        player1_body.insert(0, [player1_body[0][0]+self.dx, player1_body[0][1]+self.dy])
        player1_body.pop(-1)

    def handle_tick_boost(self):
        player1_body.insert(0, [player1_body[0][0]+self.dx, player1_body[0][1]+self.dy])
        player1_body.insert(0, [player1_body[0][0]+self.dx, player1_body[0][1]+self.dy])
        player1_body.pop(-1)
        player1_body.pop(-1)

    def body_extension(self):
        player1_body.insert(1, [player1_body[0][0], player1_body[0][1]])
        player1_body[0] = [player1_body[0][0]+self.dx,player1_body[0][1]+self.dy]       
    
    def draw(self):
        for i in range(len(player1_body)):
            if i == 0:
                pygame.draw.rect(self.display, PINK, [player1_body[i][0],player1_body[i][1], 10, 10])
            else:
                pygame.draw.rect(self.display, PURPLE, [player1_body[i][0],player1_body[i][1], 10, 10])

class Player2:
    x = (display_size[0]//2)*1.5
    y = (display_size[1]//2)
    dx = 0
    dy = 0

    def __init__(self, display):
        self.display = display

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if len(player2_body) != 1 and self.dx == 10:
                    pass
                else:
                    self.dx = -10
                    self.dy = 0
            elif event.key == K_RIGHT:
                if len(player2_body) != 1 and self.dx == -10:
                    pass
                else:
                    self.dx = 10
                    self.dy = 0
            elif event.key == K_UP:
                if len(player2_body) != 1 and self.dy == 10:
                    pass
                else:
                    self.dy = -10 
                    self.dx = 0
            elif event.key == K_DOWN:
                if len(player2_body) != 1 and self.dy == -10:
                    pass
                else:
                    self.dy = 10
                    self.dx = 0

    def handle_tick(self):
        player2_body.insert(0, [player2_body[0][0]+self.dx, player2_body[0][1]+self.dy])
        player2_body.pop(-1)

    def handle_tick_boost(self):
        player2_body.insert(0, [player2_body[0][0]+self.dx, player2_body[0][1]+self.dy])
        player2_body.insert(0, [player2_body[0][0]+self.dx, player2_body[0][1]+self.dy])
        player2_body.pop(-1)
        player2_body.pop(-1)

    def body_extension(self):
        player2_body.insert(1, [player2_body[0][0], player2_body[0][1]])
        player2_body[0] = [player2_body[0][0]+self.dx,player2_body[0][1]+self.dy]      
    
    def draw(self):
        for i in range(len(player2_body)):
            if i == 0:
                pygame.draw.rect(self.display, SKY_BLUE, [player2_body[i][0],player2_body[i][1], 10, 10])
            else:
                pygame.draw.rect(self.display, BLUE, [player2_body[i][0],player2_body[i][1], 10, 10])

class Food:
    active = True
    def __init__(self,display):
        self.x = random.randint(0, display_size[0]//10-1) * 10
        self.y = random.randint(0, display_size[1]//10-1) * 10
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])
        

#=============running game===================#

#game preperation
game_over = False
player1 = Player1(game_display)
player2 = Player2(game_display)
foods = [Food(game_display) for _ in range(20)]

#===================actual game=====================#
while not game_over:

#check player movement
    for event in pygame.event.get():
    #quit button
        if event.type == QUIT:
            game_over = True

    #check player movement
        player1.handle_event(event)
        player2.handle_event(event)

#move the snake
    keys=pygame.key.get_pressed()
    if keys[K_LSHIFT]:
        player1.handle_tick_boost()
    else:
        player1.handle_tick()

    keys=pygame.key.get_pressed()
    if keys[K_RSHIFT]:
        player2.handle_tick_boost()
    else:
        player2.handle_tick()

#draw snake
    game_display.fill(BLACK)
    player1.draw()
    player2.draw()

#reasons to shut down the game
    if player1_body[0][0]<0 or player1_body[0][0]>800 or player1_body[0][1]<0 or player1_body[0][1] > 600 or player2_body[0][0]<0 or player2_body[0][0]>800 or player2_body[0][1]<0 or player2_body[0][1] > 600:
        game_over = True
    if player1_body[0][0] == player2_body[0][0] and player1_body[0][1] == player2_body[0][1]:
        game_over = True

    if len(player1_body) > 1:
        for i in range(len(player1_body)-1):
            if player1_body[0][0] == player1_body[i+1][0] and player1_body[0][1] == player1_body[i+1][1]:
                game_over = True
    if len(player2_body) > 1:
        for i in range(len(player2_body)-1):            
            if player2_body[0][0] == player2_body[i+1][0] and player2_body[0][1] == player2_body[i+1][1]:
                game_over = True

#check if food is eaten
    for food in foods:
        if food.active:
            food.draw()
    #make snake grow for player1
        if keys[K_LSHIFT] and len(player1_body) == 1:
            if player1_body[0][0]+player1.dx == food.x and player1_body[0][1]+player1.dy == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()
            elif player1_body[0][0] == food.x and player1_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()            
        elif keys[K_LSHIFT] and len(player1_body) > 1:
            if player1_body[1][0] == food.x and player1_body[1][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()
            elif player1_body[0][0] == food.x and player1_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()            
        else:
            if player1_body[0][0] == food.x and player1_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()        

    #make snake grow for player2
        if keys[K_RSHIFT] and len(player2_body) == 1:
            if player2_body[0][0]+player1.dx == food.x and player2_body[0][1]+player2.dy == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player2.body_extension()
            elif player2_body[0][0] == food.x and player2_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player2.body_extension()    

        elif keys[K_RSHIFT] and len(player2_body) > 1:
            if player2_body[1][0] == food.x and player2_body[1][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player1.body_extension()
            elif player2_body[0][0] == food.x and player2_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player2.body_extension()            
        else:
            if player2_body[0][0] == food.x and player2_body[0][1] == food.y:
                food.active = False
                new_food = Food(game_display)
                foods.append(new_food)
                player2.body_extension()
    
#display update
    pygame.display.update()

#check if all food is eaten
    food_remains = False

    for food in foods:
        if food.active:
            food_remains = True
        
    if not food_remains:
        game_over = True

#display update
    pygame.display.update()
    pygame.event.pump()                
    pygame.time.Clock().tick(10)