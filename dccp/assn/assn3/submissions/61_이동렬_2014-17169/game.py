import pygame
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
RED =(255,0,0)
lRED=(255,123,123)
GREEN=(0,255,0)
BLUE=(0,0,255)
lBlue=(123,123,255)
Screen_Width=800
Screen_Height=600
Grid_size=10
speed=10

class Player:
    dx=0; dy=0; snake_length=1; snake_list1=[]; boost=False;snake_list2=[]
    def __init__(self, display,x,y):
        self.display=display
        self.x=x
        self.y=y
    def handle_event1(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                self.dx=+Grid_size; self.dy=0
            elif event.key==pygame.K_LEFT:
                self.dx=-Grid_size; self.dy=0
            elif event.key==pygame.K_UP:
                self.dy=-Grid_size; self.dx=0
            elif event.key==pygame.K_DOWN:
                self.dy=Grid_size; self.dx=0
            elif event.key==pygame.K_RSHIFT:
                self.boost=True
        if event.type== pygame.KEYUP:
            if event.key ==pygame.K_RSHIFT:
                self.boost=False
    def handle_event2(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_d:
                self.dx=+Grid_size; self.dy=0
            elif event.key==pygame.K_a:
                self.dx=-Grid_size; self.dy=0
            elif event.key==pygame.K_w:
                self.dy=-Grid_size; self.dx=0
            elif event.key==pygame.K_s:
                self.dy=Grid_size; self.dx=0
            elif event.key==pygame.K_LSHIFT:
                self.boost=True
        if event.type== pygame.KEYUP:
            if event.key ==pygame.K_LSHIFT:
                self.boost=False

    def tick(self):
        self.x+=self.dx
        self.y+=self.dy
    def draw1(self):
        pygame.draw.rect(self.display, RED, [self.snake_list1[-1][0],self.snake_list1[-1][1],Grid_size,Grid_size]) # Player 초기 설정값
        for x in self.snake_list1[:-1]:
            pygame.draw.rect(self.display, lRED, [x[0],x[1],Grid_size,Grid_size]) # Player1 초기 설정값
    def draw2(self):
        pygame.draw.rect(self.display, BLUE, [self.snake_list2[-1][0],self.snake_list2[-1][1],Grid_size,Grid_size]) # Player 초기 설정값
        for x in self.snake_list2[:-1]:
            pygame.draw.rect(self.display, lBlue, [x[0],x[1],Grid_size,Grid_size]) # Player2 초기 설정값
        
class Food:
    active = True
    def __init__(self,display):
        self.x=Grid_size*random.randint(0,(Screen_Width-10)/Grid_size)
        self.y=10*random.randint(0,(Screen_Height-10)/Grid_size) 
        self.display=display

    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x,self.y,10,10])

class Game:
    block_size=10
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2014-17169 Snake Game")
        self.display=pygame.display.set_mode((Screen_Width,Screen_Height))
        self.clock=pygame.time.Clock()
        self.game_over=False
    
    def play(self, n_foods=20):
        player1 = Player(self.display,Screen_Width/4,Screen_Height/2)
        player2 = Player(self.display,3*Screen_Width/4,Screen_Height/2)
        foods=[Food(self.display) for _ in range(n_foods)]
        while not self.game_over:
            for event in pygame.event.get(): # event가 일어날 때 마다 for 문 돈다.
                if event.type==pygame.QUIT: # 창이 닫히는 이벤트 발생 
                    self.game_over = True
                    break
                player1.handle_event1(event)
                player2.handle_event2(event)
            if player1.x<0 or player1.x>Screen_Width-10 or player1.y<0 or player1.y>Screen_Height-10:
                self.game_over= True
            elif player2.x<0 or player2.x>Screen_Width-10 or player2.y<0 or player2.y>Screen_Height-10:
                self.game_over=True
            player1.tick()
            player2.tick()
        
            self.display.fill(BLACK)
            
            
            for food in foods:
                if food.active:
                    food.draw()
                if player1.x==food.x and player1.y==food.y:
                    i=foods.index(food)
                    del foods[foods.index(food)]            
                    foods.insert(i,Food(self.display))
                    player1.snake_length+=1
                if player2.x==food.x and player2.y==food.y:
                    i=foods.index(food)
                    del foods[foods.index(food)]            
                    foods.insert(i,Food(self.display))
                    player2.snake_length+=1
            
            snake_head1=[]
            snake_head1.append(player1.x)
            snake_head1.append(player1.y)
            player1.snake_list1.append(snake_head1)

            snake_head2=[]
            snake_head2.append(player2.x)
            snake_head2.append(player2.y)
            player2.snake_list2.append(snake_head2)

            if len(player1.snake_list1)>player1.snake_length:
                del player1.snake_list1[0]
            if len(player2.snake_list2)>player2.snake_length:
                del player2.snake_list2[0]
            
            for x in player1.snake_list1[:-1]:
                if x ==snake_head1:
                    self.game_over=True
                elif x==snake_head2:
                    self.game_over=True
            for x in player2.snake_list2[:-1]:
                if x ==snake_head1:
                    self.game_over=True
                elif x==snake_head2:
                    self.game_over=True
            if snake_head1==snake_head2:
                self.game_over=True
                
            player1.draw1()
            player2.draw2()
            
            if player1.boost or player2.boost:
                speed=20
            else:
                speed=10
            pygame.display.update() # display를 업데이트 (while문 한 번마다 업데이트)
            self.clock.tick(speed)# 1초에 괄호 안에 숫자만큼 이 while loop이 돌게끔, 프레임 업데이트 주기 
        


if __name__ =="__main__":
    Game().play(n_foods=20)