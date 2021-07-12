import pygame
import random

WHITE=(255, 255, 255)
BLACK=(0,0,0)
RED=(255, 0, 0)
GREEN=(0,255,0)
BLUE=(0,0, 255)
YELLOW=(255, 255, 0)
MAGENTA=(255, 0, 255)

pygame.init()
game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

class Object:
    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])

class Player(Object):
    dx=0
    dy=0
    score=0
    boost=False
    def __init__(self, display, color=WHITE, reverse=False):
        self.display=display
        self.color=color
        self.reverse=reverse
        self.x=random.randint(0, 79)*10
        self.y=random.randint(0, 59)*10

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.reverse:
                if event.key == pygame.K_LEFT:
                    self.dx= -10
                    self.dy = 0
                elif event.key == pygame.K_RIGHT:
                    self.dx = 10
                    self.dy = 0
                elif event.key == pygame.K_UP:
                    self.dy = -10
                    self.dx=0
                elif event.key == pygame.K_DOWN:
                    self.dy = 10
                    self.dx = 0
                
            elif self.reverse:
                if event.key == pygame.K_a and self.reverse:
                    self.dx= -10
                    self.dy = 0
                elif event.key == pygame.K_d and self.reverse:
                    self.dx = 10
                    self.dy = 0
                elif event.key == pygame.K_w and self.reverse:
                    self.dy = -10
                    self.dx=0
                elif event.key == pygame.K_s and self.reverse:
                    self.dy = 10
                    self.dx = 0
                
    def tick(self):
        self.x+=self.dx
        self.y+=self.dy

class Food(Object):
    active= True
    def __init__(self, display, color=GREEN):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10
        self.display=display
        self.color=color

class Tail(Object):
    active=False
    def __init__(self, display, x, y, color=RED):
        self.display=display
        self.color=color
        self.x=x
        self.y=y

def taildraw(t, p, test):
    if test:
        return True
    else:
        if p.score>=1:
            if t[-2].x==p.x and t[-2].y==p.y:
                return True
            for i in t[-p.score:]:
                i.active=True
                if p.x==i.x and p.y==i.y:
                    return True
            for i in t:
                if i.active==True:
                    i.draw()
        return False

def poscheck(posx, posy, test):
    if test:
        return True
    if posx<0 or posx>790:
        return True
    if posy<0 or posy>590:
        return True
    else:
        return False

def tail_body(t, p, test):
    if test==True:
        return True
    for i in t:
        if i.active==True and i.x==p.x and i.y==p.y:
            return True
    return False

def fooddraw(p):
    for food in foods:
        if food.active:
            food.draw()
            if p.x== food.x and p.y==food.y:
                food.active=False
                foods.append(Food(game_display))
                p.score+=1

player = Player(game_display, YELLOW)
player2 = Player(game_display, MAGENTA, True)
game_over = False
foods =[Food(game_display) for _ in range(20)]
tails=[]
tails2=[]

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_RSHIFT:
                player.boost=True
            if event.key==pygame.K_LSHIFT:
                player2.boost=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RSHIFT:
                player.boost=False
            if event.key==pygame.K_LSHIFT:
                player2.boost=False
        player.handle_event(event)
        player2.handle_event(event)

    player.tick()
    player2.tick()
    
    if player.boost:
        if player.x==player2.x and player.y==player2.y:
            game_over=True
    
        fooddraw(player)
        game_over=taildraw(tails, player, game_over)
        game_over=tail_body(tails, player, game_over)
        game_over=tail_body(tails, player2, game_over)
        game_over=tail_body(tails2, player, game_over)
        game_over=poscheck(player.x, player.y, game_over)
        tails.append(Tail(game_display, player.x, player.y, RED))
        player.tick()
        
    if player2.boost:
        if player.x==player2.x and player.y==player2.y:
            game_over=True
    
        fooddraw(player2)
        game_over=taildraw(tails2, player2, game_over)
        game_over=tail_body(tails2, player2, game_over)
        game_over=tail_body(tails, player2, game_over)
        game_over=tail_body(tails2, player, game_over)
        game_over=poscheck(player2.x, player2.y, game_over)
        tails2.append(Tail(game_display, player2.x, player2.y, BLUE))
        player2.tick()
    
    for i in tails:
        i.active=False
    for i in tails2:
        i.active=False
    
    game_display.fill(BLACK)
    player.draw()
    player2.draw()
    
    if player.x==player2.x and player.y==player2.y:
        game_over=True
    
    fooddraw(player)
    fooddraw(player2)
    game_over=taildraw(tails, player, game_over)
    game_over=taildraw(tails2, player2, game_over)
    game_over=tail_body(tails, player, game_over)
    game_over=tail_body(tails2, player2, game_over)
    game_over=tail_body(tails, player2, game_over)
    game_over=tail_body(tails2, player, game_over)
    game_over=poscheck(player.x, player.y, game_over)
    game_over=poscheck(player2.x, player2.y, game_over)
    tails.append(Tail(game_display, player.x, player.y, RED))
    tails2.append(Tail(game_display, player2.x, player2.y, BLUE))
    
    pygame.display.update()
    for i in tails:
        i.active=False
    for i in tails2:
        i.active=False
    clock.tick(10)