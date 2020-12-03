import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

block_size=10

class Tile:
    def __init__(self,x,y,game,color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])

class Player(Tile):
    dx = 0
    dy = 0
    def __init__(self,x,y,game,color,direction=None,speed=1):
        super().__init__(x,y,game,color)
        self.length = 1
        self.bodylist = []
        self.color = color
        self.direction = direction
        self.speed = speed

    def handle_event1(self,event):
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
                self.direction = 'LEFT'
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                self.direction = 'RIGHT'
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP:
                self.direction = 'UP'
                self.dy = -1
                self.dx = 0
            elif event.key == pygame.K_DOWN:
                self.direction = 'DOWN'
                self.dy = 1
                self.dx = 0
            if event.key == pygame.K_RSHIFT:
                self.speed = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.speed = 1
    
    def handle_event2(self,event):
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_a:
                self.direction = 'LEFT'
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_d:
                self.direction = 'RIGHT'
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_w:
                self.direction = 'UP'
                self.dy = -1
                self.dx = 0
            elif event.key == pygame.K_s:
                self.direction = 'DOWN'
                self.dy = 1
                self.dx = 0

            if event.key == pygame.K_LSHIFT:
                self.speed = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.speed = 1
    
    def movement(self):
        if self.length >= 2:
            cloning = self.bodylist[:]
            for i in range(0,self.length-2):
                self.bodylist[i].x=cloning[i+1].x
                self.bodylist[i].y=cloning[i+1].y
            self.bodylist[self.length-2].x=self.x
            self.bodylist[self.length-2].y=self.y

    def tick(self):
        self.x += self.dx*self.speed
        self.y += self.dy*self.speed
    
    def collision(self):
        for i in self.bodylist:
            if i.x == self.x and i.y == self.y:
                return True

def collision2(player1,player2):
    for i in player1.bodylist:
        if player2.x == i.x and player2.y == i.y:
            return True
    
    for i in player2.bodylist:
        if player1.x == i.x and player1.y == i.y:
            return True
    
    if player1.x == player2.x and player1.y == player2.y:
        return True

class Snakebody(Tile):
    color = WHITE

    def __init__(self,x,y,game):
        super().__init__(x,y,game,self.color)

class Food(Tile):
    color = GREEN

    def __init__(self,game):
        x = random.randint(0,game.n_rows-1)
        y = random.randint(0,game.n_cols-1)
        super().__init__(x,y,game,self.color)

class Game:
    def __init__(self,n_rows,n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.display = pygame.display.set_mode((n_rows*block_size,n_cols*block_size))
        self.clock = pygame.time.Clock()
        self.game_over = False
    
    def play(self,n_foods=20):
        player1 = Player(20,30,self,RED)
        player2 = Player(60,30,self,BLUE)
        foods = [Food(self) for i in range(n_foods)]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player1.handle_event1(event)
                player2.handle_event2(event)

            if (player1.x < 0 or player1.x > self.n_rows or player1.y < 0 or player1.y > self.n_cols or 
                player2.x < 0 or player2.x > self.n_rows or player2.y < 0 or player2.y > self.n_cols):
                self.game_over = True

            player1.tick()          
            player2.tick()
            self.display.fill(BLACK)
            if player1.collision() or player2.collision() or collision2(player1,player2):
                self.game_over = True
            player1.draw()
            for i in player1.bodylist:
                i.draw()
            player1.movement()
            player2.draw()
            for i in player2.bodylist:
                i.draw()
            player2.movement()
         
            for food in foods:
                if food.active:
                    food.draw()
                
                if player1.x == food.x and player1.y==food.y and food.active == True:
                    food.active = False
                    foods.append(Food(self))
                    if player1.direction == 'LEFT':
                        player1.x += -1
                    elif player1.direction == 'RIGHT':
                        player1.x += 1
                    elif player1.direction == 'UP':
                        player1.y += -1
                    elif player1.direction == 'DOWN':
                        player1.y += 1
                    player1.bodylist.append(Snakebody(player1.x,player1.y,self))
                    player1.length += 1
            
                if player2.x == food.x and player2.y==food.y and food.active == True:
                    food.active = False
                    foods.append(Food(self))
                    if player2.direction == 'LEFT':
                        player2.x += -1
                    elif player2.direction == 'RIGHT':
                        player2.x += 1
                    elif player2.direction == 'UP':
                        player2.y += -1
                    elif player2.direction == 'DOWN':
                        player2.y += 1
                    player2.bodylist.append(Snakebody(player2.x,player2.y,self))
                    player2.length += 1
            
            pygame.display.update()
            self.clock.tick(10)
if __name__ == "__main__":
    Game(n_rows=80,n_cols=60).play(n_foods=20)