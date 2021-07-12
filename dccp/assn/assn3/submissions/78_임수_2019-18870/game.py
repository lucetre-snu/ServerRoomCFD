import pygame as p
import random as r
from player import Player
from player import Player2
from food import Food
        
class Game:
    def __init__(self, size, color):
        p.init()
        self.size = size
        self.screen = p.display.set_mode(size)
        p.display.set_caption("Snake Game")
        self.clock = p.time.Clock()
        self.game_Ended = False
        self.screenColor = color
    
    def play1(self, player, foodColor):
        food_list = list()
        
        while True:
            food = Food(self.size, self.screen)
            count = 0
            for i in food_list:
                if food.x==i.x and food.y==i.y:
                    count += 1
            if count > 0 :
                continue
            food.set_FoodColor(foodColor)
            food_list.append(food)
            if len(food_list)==20:
                break

        player.draw(player.headColor)

        for i in food_list:
            i.draw()
        
        p.display.update()

        boost = False

        while not self.game_Ended:
            self.clock.tick(10)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.game_Ended = True
                    break
                if event.type == p.KEYDOWN:
                    if event.key==p.K_RSHIFT:
                        boost = True
                    player.event_Handling(event)
                if event.type == p.KEYUP:
                    if event.key==p.K_RSHIFT:
                        boost = False

            player.pos_change(boost)

            if player.game_End():
                self.game_Ended = True

            eaten = False

            for i in range(len(food_list)):
                if player.x==food_list[i].x and player.y==food_list[i].y:
                    del food_list[i]
                    player.makeBody_Long(boost)
                    eaten = True
                    break
                if boost:
                    if player.x-player.dx==food_list[i].x and player.y-player.dy==food_list[i].y:
                        del food_list[i]
                        player.makeBody_Long2()
                        eaten = True
                        break
            
            if not eaten:
                player.bodyManager(boost) 

            self.screen.fill(self.screenColor)

            if len(food_list) < 20:
                food_Add = False
                while not food_Add:
                    food = Food(self.size, self.screen)
                    if (food.x == player.x and food.y == player.y) or ([food.x, food.y] in player.bodylist):
                        continue
                    count = 0
                    for i in food_list:
                        if i.x==food.x and i.y==food.y:
                            count += 1
                    if count > 0:
                        continue
                    food.set_FoodColor(foodColor)
                    food_list.append(food)
                    food_Add = True

            player.draw(player.headColor)
            player.bodyDraw(player.bodyColor)

            for i in food_list:
                i.draw()
            
            p.display.update()

            
    def play2(self, player1, player2, foodColor1):
        food_list1 = list()

        while True:
            food = Food(self.size, self.screen)
            count = 0
            for i in food_list1:
                if food.x==i.x and food.y==i.y:
                    count += 1
            if (food.x==player1.x and food.y==player1.y) or (food.x==player2.x and food.y==player2.y):
                count += 1
            if count > 0 :
                continue
            food.set_FoodColor(foodColor1)
            food_list1.append(food)
            if len(food_list1)==20:
                break
        
        
        player1.draw(player1.headColor)
        player2.draw(player2.headColor)

        for i in range(len(food_list1)):
            food_list1[i].draw()
        
        p.display.update()

        boost1 = False
        boost2 = False

        while not self.game_Ended:
            self.clock.tick(10)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.game_Ended = True
                    break
                if event.type == p.KEYDOWN:
                    if event.key==p.K_RSHIFT:
                        boost1 = True
                    if event.key==p.K_LSHIFT:
                        boost2 = True    
                    player1.event_Handling(event)
                    player2.event_Handling(event)
                if event.type == p.KEYUP:
                    if event.key==p.K_RSHIFT:
                        boost1 = False
                    if event.key==p.K_LSHIFT:
                        boost2 = False
            
            player1.pos_change(boost1)
            player2.pos_change(boost2)

            if player1.game_End() or player2.game_End():
                self.game_Ended = True
                
            eaten1 = False
            eaten2 = False

            for i in range(len(food_list1)):
                if player1.x==food_list1[i].x and player1.y==food_list1[i].y:
                    del food_list1[i]
                    player1.makeBody_Long(boost1)
                    eaten1 = True
                    break
                if boost1:
                    if player1.x-player1.dx==food_list1[i].x and player1.y-player1.dy==food_list1[i].y:
                        del food_list1[i]
                        player1.makeBody_Long2()
                        eaten1 = True
                        break
            
            if not eaten1:
                player1.bodyManager(boost1) 

            for i in range(len(food_list1)):
                if player2.x==food_list1[i].x and player2.y==food_list1[i].y:
                    del food_list1[i]
                    player2.makeBody_Long(boost2)
                    eaten2 = True
                    break
                if boost2:
                    if player2.x-player2.dx==food_list1[i].x and player2.y-player2.dy==food_list1[i].y:
                        del food_list1[i]
                        player2.makeBody_Long2()
                        eaten2 = True
                        break
            
            if not eaten2:
                player2.bodyManager(boost2)

            self.screen.fill(self.screenColor)

            if len(food_list1) < 20:
                while True:
                    food = Food(self.size, self.screen)
                    if (food.x == player1.x and food.y == player1.y) or ([food.x, food.y] in player1.bodylist):
                        continue
                    alreadyExist_in_list1 = False
                    for i in food_list1:
                        if i.x==food.x and i.y==food.y:
                            alreadyExist_in_list1 = True
                    if alreadyExist_in_list1:
                        continue
                    food.set_FoodColor(foodColor1)
                    food_list1.append(food)
                    
                    if len(food_list1)==20:
                        break
            
            if (player1.x==player2.x and player1.y==player2.y):
                self.game_Ended = True
            if [player1.x, player1.y] in player2.bodylist:
                self.game_Ended = True
            if [player2.x, player2.y] in player1.bodylist:
                self.game_Ended = True
            if boost1:
                if [player1.x-player1.dx, player1.y-player1.dy] in player2.bodylist:
                    self.game_Ended = True
            if boost2:
                if [player2.x-player2.dx, player2.y-player2.dy] in player1.bodylist:
                    self.game_Ended = True

            player1.draw(player1.headColor)
            player1.bodyDraw(player1.bodyColor)
            player2.draw(player2.headColor)
            player2.bodyDraw(player2.bodyColor)

            for i in food_list1:
                i.draw()

            p.display.update()



SIZE = (800, 400)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 255, 255)




game = Game(SIZE, BLACK)
player1 = Player(SIZE, game.screen)
player1.set_HeadColor(RED)
player1.set_BodyColor(BLUE)
player2 = Player2(SIZE, game.screen)
player2.set_HeadColor(WHITE)
player2.set_BodyColor(YELLOW)
game.play2(player1, player2, GREEN)