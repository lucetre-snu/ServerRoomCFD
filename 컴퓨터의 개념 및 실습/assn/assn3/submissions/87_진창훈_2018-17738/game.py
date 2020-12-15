import pygame as pg
import random
from pygame.constants import *

#COLORLIST
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50 , 50)
WRED = (255, 100, 100)
GREEN = (0, 255, 0)
BLUE = (50, 50 , 255)
WBLUE = (100, 100, 255)

#PARAMETERS
asp_x = 800
asp_y = 600
aspect_ratio = (asp_x, asp_y)
foodcount = 10

#FONT
#font = pg.font.Font('freesansbold.ttf', 32)

#TEXT
#start_screen = font.render('PRESS ANY KEY', True, GREEN, BLUE)

class Player_1:
    x_pos = (asp_x//30)*10
    y_pos = (asp_y//30)*20
    dx_pos = 10
    dy_pos = 0
    head = WRED
    tail = RED
    tails = []
    score = 0
    boost = False
    life = True

    def __init__(self, display):
        self.display = display
    
    def keystroke(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                if self.dx_pos <= 0:
                    self.dx_pos = -10
                    self.dy_pos = 0
                else:
                    pass
            elif event.key == K_d:
                if self.dx_pos >= 0:
                    self.dx_pos = 10
                    self.dy_pos = 0
                else:
                    pass
            elif event.key == K_w:
                if self.dy_pos <= 0:
                    self.dx_pos = 0
                    self.dy_pos = -10
                else:
                    pass
            elif event.key == K_s:
                if self.dy_pos >= 0:
                    self.dx_pos = 0
                    self.dy_pos = 10
            elif event.key == K_LSHIFT:
                self.boost = True
        elif event.type == KEYUP:
            if event.key == K_LSHIFT:
                self.boost = False

    def locomotion(self):
        self.tails.append([self.x_pos, self.y_pos])
        self.x_pos += self.dx_pos
        self.y_pos += self.dy_pos
        del self.tails[:len(self.tails)-self.score-1]

    def pause(self):
        self.tails.append([self.x_pos, self.y_pos])
        self.x_pos += 0
        self.y_pos += 0

    def refresh(self):
        pg.draw.rect(self.display, self.head, [self.x_pos, self.y_pos, 10, 10])
        for _ in range(len(self.tails)-1, len(self.tails)-self.score-1, -1):
            pg.draw.rect(self.display, self.tail, [self.tails[_][0], self.tails[_][1], 10, 10])

    def death(self, opponent):
        if self.x_pos == opponent.x_pos and self.y_pos == opponent.y_pos:
            self.life = False
        if self.x_pos > asp_x or self.x_pos < 0 or self.y_pos > asp_y or self.y_pos <0:
            self.life = False
        if [self.x_pos, self.y_pos] in opponent.tails or [self.x_pos, self.y_pos] in self.tails[:-1]:
            self.life = False

class Player_2:
    x_pos = (asp_x//30)*20
    y_pos = (asp_y//30)*10
    dx_pos = -10
    dy_pos = 0
    head = WBLUE
    tail = BLUE
    tails = []
    score = 0
    boost = False
    life = True

    def __init__(self, display):
        self.display = display
    
    def keystroke(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if self.dx_pos <= 0:
                    self.dx_pos = -10
                    self.dy_pos = 0
                else:
                    pass
            elif event.key == K_RIGHT:
                if self.dx_pos >= 0:
                    self.dx_pos = 10
                    self.dy_pos = 0
                else:
                    pass
            elif event.key == K_UP:
                if self.dy_pos <= 0:
                    self.dx_pos = 0
                    self.dy_pos = -10
                else:
                    pass
            elif event.key == K_DOWN:
                if self.dy_pos >= 0:
                    self.dx_pos = 0
                    self.dy_pos = 10
            elif event.key == K_RSHIFT:
                self.boost = True
        elif event.type == KEYUP:
            if event.key == K_RSHIFT:
                self.boost = False

    def locomotion(self):
        self.tails.append([self.x_pos, self.y_pos])
        self.x_pos += self.dx_pos
        self.y_pos += self.dy_pos
        del self.tails[:len(self.tails)-self.score-1]

    def pause(self):
        self.tails.append([self.x_pos, self.y_pos])
        self.x_pos += 0
        self.y_pos += 0

    def refresh(self):
        pg.draw.rect(self.display, self.head, [self.x_pos, self.y_pos, 10, 10])
        for _ in range(len(self.tails)-1, len(self.tails)-self.score-1, -1):
            pg.draw.rect(self.display, self.tail, [self.tails[_][0], self.tails[_][1], 10, 10])

    def death(self, opponent):
        if self.x_pos == opponent.x_pos and self.y_pos == opponent.y_pos:
            self.life = False
        if self.x_pos > asp_x or self.x_pos < 0 or self.y_pos > asp_y or self.y_pos <0:
            self.life = False
        if [self.x_pos, self.y_pos] in opponent.tails or [self.x_pos, self.y_pos] in self.tails[:-1]:
            self.life = False

class Food:
    active = True
    def __init__(self, display):
        self.display = display
        self.x = random.randint(0, (asp_x//10))*10
        self.y = random.randint(0, (asp_y//10))*10

    def generate(self):
        pg.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])


class Game:
    def __init__(self):
        #INITIALIZATION
        pg.init()
        pg.font.init()
        self.font1 = pg.font.SysFont('Comic Sans MS', 100)
        self.font2 = pg.font.SysFont('Comic Sans MS', 50)
        self.title = self.font1.render('SNAKE 2P', False, BLUE, RED)
        self.press = self.font2.render('PRESS ANY KEY', False, BLACK, GREEN)
        self.textpos1 = self.title.get_rect(center=(asp_x//2, asp_y//4*1))
        self.textpos2 = self.press.get_rect(center=(asp_x//2, asp_y//4*3))
        
        pg.display.set_caption('SNAKE 2P')
        self.display = pg.display.set_mode(aspect_ratio)
        self.game_over = False
        self.clock = pg.time.Clock()

    def start_screen(self):
        intro = True
        while intro:
            self.display.fill(GREEN)
            self.display.blit(self.title, self.textpos1)
            self.display.blit(self.press, self.textpos2)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    break
                elif event.type == KEYDOWN:
                    intro = False
                    break
            pg.display.update()
    
    def play(self):
        pl_1 = Player_1(self.display)
        pl_2 = Player_2(self.display)
        foods = [Food(self.display) for _ in range(foodcount)]

        while not self.game_over:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.game_over = True
                    break
                pl_1.keystroke(event)
                pl_2.keystroke(event)
            self.display.fill(BLACK)
            if pl_1.boost and pl_2.boost:
                pl_1.locomotion()
                pl_2.locomotion()
                for food in foods:
                    if food.active:
                        food.generate()
                    if pl_1.x_pos == food.x and pl_1.y_pos == food.y:
                        pl_1.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                    elif pl_2.x_pos == food.x and pl_2.y_pos == food.y:
                        pl_2.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                pl_1.refresh()
                pl_2.refresh()
                pl_1.death(pl_2)
                pl_2.death(pl_1)
                if not(pl_1.life) or not(pl_2.life):
                    self.game_over = True
                pg.display.update()
                self.clock.tick(10)
            elif pl_1.boost:
                pl_1.locomotion()
                pl_2.pause()
                for food in foods:
                    if food.active:
                        food.generate()
                    if pl_1.x_pos == food.x and pl_1.y_pos == food.y:
                        pl_1.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                pl_1.refresh()
                pl_2.refresh()
                pl_1.death(pl_2)
                pl_2.death(pl_1)
                if not(pl_1.life) or not(pl_2.life):
                    self.game_over = True
                pg.display.update()
                self.clock.tick(10)
            elif pl_2.boost:
                pl_1.pause()
                pl_2.locomotion()
                for food in foods:
                    if food.active:
                        food.generate()
                    if pl_2.x_pos == food.x and pl_2.y_pos == food.y:
                        pl_2.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                pl_1.refresh()
                pl_2.refresh()
                pl_1.death(pl_2)
                pl_2.death(pl_1)
                if not(pl_1.life) or not(pl_2.life):
                    self.game_over = True
                pg.display.update()
                self.clock.tick(10)
            else:
                pl_1.pause()
                pl_2.pause()
                for food in foods:
                    if food.active:
                        food.generate()
                    if pl_1.x_pos == food.x and pl_1.y_pos == food.y:
                        pl_1.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                    elif pl_2.x_pos == food.x and pl_2.y_pos == food.y:
                        pl_2.score += 1
                        food.active = False
                        foods.append(Food(self.display))
                pl_1.refresh()
                pl_2.refresh()
                pg.display.update()
                self.clock.tick(10)
            self.display.fill(BLACK)
            pl_1.locomotion()
            pl_2.locomotion()
            for food in foods:
                if food.active:
                    food.generate()
                if pl_1.x_pos == food.x and pl_1.y_pos == food.y:
                    pl_1.score += 1
                    food.active = False
                    foods.append(Food(self.display))
                elif pl_2.x_pos == food.x and pl_2.y_pos == food.y:
                    pl_2.score += 1
                    food.active = False
                    foods.append(Food(self.display))
            pl_1.refresh()
            pl_2.refresh()
            pl_1.death(pl_2)
            pl_2.death(pl_1)
            if not(pl_1.life) or not(pl_2.life):
                self.game_over = True
            pg.display.update()   
            self.clock.tick(10)

if __name__ == "__main__":
    Game().start_screen()
    Game().play()
