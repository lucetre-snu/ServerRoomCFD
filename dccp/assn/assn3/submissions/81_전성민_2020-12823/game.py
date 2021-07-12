import pygame
import random

pygame.init()
game_display = pygame.display.set_mode((800,600)) # 창 크기 설정
pygame.display.set_caption('2020-12823 전성민 Snake Game') # 창 이름 설정


# 게임에 쓰이는 색깔 정의
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#game_over = False
# game_display.fill(WHITE)
#clock = pygame.time.Clock()
pygame.display.update() #해야지 변경점 업데이트
# clock.tick(60) # 1/60초동안 기다리겠다 frame per second

class GridObject:
    def __init__(self,x,y,game,color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x #grid column index
        self.y = y #grid row index
    
    def handle_event(self,event):
        pass
    
    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])





class Player(GridObject):
    dx = 0
    dy = 0
    color = WHITE
    global pos
    global tail
    global boost
    pos = []
    tail = []
    boost = False

    def __init__(self, x, y, game):
        global pos
        super().__init__(x,y,game,self.color)
        pos=[[self.x,self.y]]
    
    def handle_event(self, event):
        global boost
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0
                boost = False
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
                boost = False
            elif event.key == pygame.K_UP:
                self.dx = 0
                self.dy = -1
                boost = False
            elif event.key == pygame.K_DOWN:
                self.dx = 0
                self.dy = 1
                boost = False
            if event.key== pygame.K_RSHIFT:
                self.dx *=2
                self.dy *=2
                if self.dx > 2:
                    self.dx = 2
                elif self.dx < -2:
                    self.dx = -2
                elif self.dy > 2:
                    self.dy = 2
                elif self.dy < -2:
                    self.dy = -2
                boost = True
    def tick(self):
        global pos
        self.x += self.dx
        self.y += self.dy
        tail = pos[-1]
        if boost == False:
            pos=[[self.x,self.y]]+pos[:-1]
        elif len(pos)==1:
            pos=[[self.x,self.y]]
        else:
            pos=[[self.x,self.y]]+[[self.x-(self.dx/2),self.y-(self.dy/2)]]+pos[:-2]
        
    
    def grow(self):
        global pos
        pos.append(tail)
    
    def draw(self):
        global pos
        for i in range(len(pos)):
            if i==0:
                pygame.draw.rect(self.game.display,WHITE,[self.x*10,self.y*10,10,10])
            else :
                pygame.draw.rect(self.game.display,RED,[pos[i][0]*10,pos[i][1]*10,10,10])


class Player1(GridObject):
    dx = 0
    dy = 0
    color = BLUE
    global pos1
    global tail1
    global boost1
    pos1 = []
    tail1 = []
    boost1 = False

    def __init__(self, x, y, game):
        global pos1
        super().__init__(x,y,game,self.color)
        pos1=[[self.x,self.y]]
    
    def handle_event(self, event):
        global boost1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
                self.dy = 0
                boost1 = False
            elif event.key == pygame.K_d:
                self.dx = 1
                self.dy = 0
                boost1 = False
            elif event.key == pygame.K_w:
                self.dx = 0
                self.dy = -1
                boost1 = False
            elif event.key == pygame.K_s:
                self.dx = 0
                self.dy = 1
                boost1 = False
            if event.key == pygame.K_LSHIFT:
                self.dx *=2
                self.dy *=2
                if self.dx > 2:
                    self.dx = 2
                elif self.dx < -2:
                    self.dx = -2
                elif self.dy > 2:
                    self.dy = 2
                elif self.dy < -2:
                    self.dy = -2
                boost1 = True
    def tick(self):
        global pos1
        self.x += self.dx
        self.y += self.dy
        tail1 = pos1[-1]
        if boost1 == False:
            pos1=[[self.x,self.y]]+pos1[:-1]
        elif len(pos1)==1:
            pos1=[[self.x,self.y]]
        else:        
            pos1=[[self.x,self.y]]+[[self.x-(self.dx/2),self.y-(self.dy/2)]]+pos1[:-2]
        
    
    def grow(self):
        global pos1
        pos1.append(tail1)
    
    def draw(self):
        global pos1
        for i in range(len(pos1)):
            if i==0:
                pygame.draw.rect(self.game.display,BLUE,[self.x*10,self.y*10,10,10])
            else :
                pygame.draw.rect(self.game.display,YELLOW,[pos1[i][0]*10,pos1[i][1]*10,10,10])

class Food(GridObject):
    color = GREEN
    def __init__(self, game):
        x = random.randint(0,game.n_cols-1)
        y = random.randint(0,game.n_rows-1)
        super().__init__(x,y,game,self.color)


class Game:
    global pos
    global pos1
    block_size = 10
    def __init__(self,n_rows,n_cols):
        pygame.init()
        self.display = pygame.display.set_mode((n_cols *self.block_size,n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        pygame.display.set_caption('2020-12823 전성민 Snake Game')
        self.clock =pygame.time.Clock()
        self.game_over = False
        self.objects = []
    
    def play(self):
        player = Player(40,30,self)
        player1 = Player1(60,50,self)
        foods = [Food(self) for i in range(20)]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player.handle_event(event)
                player1.handle_event(event)

    # 플레이어의 위치 확인
            if player.x < 0 or player.x >=80 :
                    self.game_over = True
            elif player.y < 0 or player.y >=60:
                    self.game_over = True
            
            if player1.x < 0 or player1.x >=80 :
                    self.game_over = True
            elif player1.y < 0 or player1.y >=60:
                    self.game_over = True
    
            player.tick()
            player1.tick()
            game_display.fill(BLACK)
            player.draw()
            player1.draw()


            if pos[0] in pos[1:] :
                self.game_over = True
            elif pos[0] in pos1:
                self.game_over = True
            elif pos1[0] in pos1[1:]:
                self.game_over = True
            elif pos1[0] in pos:
                self.game_over = True
    
            for food in foods:
                if food.active:
                    food.draw()
                if player.x == food.x and player.y == food.y:
                    foods.append(Food(self))
                    foods.remove(food)
                    player.grow()
            
                elif player.x == food.x + player.dx/2 and player.y == food.y:
                    foods.append(Food(self))
                    foods.remove(food)
                    player.grow()

                elif player.x == food.x and player.y == food.y + player.dy /2:
                    foods.append(Food(self))
                    foods.remove(food)
                    player.grow()

                if player1.x == food.x and player1.y == food.y:
                    foods.append(Food(self))
                    foods.remove(food)
                    player1.grow()
            
                elif player1.x == food.x + player1.dx/2 and player1.y == food.y:
                    foods.append(Food(self))
                    foods.remove(food)
                    player1.grow()

                elif player1.x == food.x and player1.y == food.y + player1.dy /2:
                    foods.append(Food(self))
                    foods.remove(food)
                    player1.grow()

            pygame.display.update()

            food_remains = False
            for food in foods:
                if food.active:
                    food_remains = True
            if not food_remains:
                self.game_over = True


            self.clock.tick(10)


if __name__ == "__main__":
    Game(n_rows=60,n_cols=80).play()



