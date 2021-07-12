import pygame
import random

# 플레이어 및 먹이의 색
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

# 전체적인 네모 모양의 클래스 
class Gridobject:
    def __init__(self, x, y, game, color ):
        self.game = game
        self.color = color
        self.x = x
        self.y = y
        self.active =True
    def handle_event(self, event):
        pass
    def tick(self):
        pass
    def draw(self):
        pass
# 플레이어 클래스: 그리기 
class Player(Gridobject):
    dx = 0
    dy = 0

    def __init__(self,x,y,game, color):
        self.color = color
        super().__init__(x,y,game,color)

    def handle_event(self, event):
        pass

    def tick(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
    
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])
    
    def body(self,n):
        pass
# 각 플레이어 클래스: 조작키 및 몸통 그리기
class Player1(Player):
        def handle_event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_RIGHT:
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_UP:
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_DOWN:
                    self.dx = 0
                    self.dy = 1
                elif event.key == pygame.K_RSHIFT:
                    self.dx, self.dy = self.dx*2, self.dy*2
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    self.dx, self.dy = int(self.dx*0.5), int(self.dy*0.5)
            

        def body(self,n):
            block_size = self.game.block_size
            if n == 0:
                pass
            else:
                for i in range(n):
                    pygame.draw.rect(self.game.display, self.color,[self.game.data1[i][0]*block_size,self.game.data1[i][1]*block_size,block_size,block_size])
# 각 플레이어 클래스: 조작키 및 몸통 그리기
class Player2(Player):
        def handle_event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_d:
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_w:
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_s:
                    self.dx = 0
                    self.dy = 1
                elif event.key == pygame.K_LSHIFT:
                    
                    self.dx, self.dy = self.dx*2, self.dy*2
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.dx, self.dy = int(self.dx*0.5), int(self.dy*0.5)
                
        def body(self,n):
            block_size = self.game.block_size
            if n == 0:
                pass
            else:
                for i in range(n):
                    pygame.draw.rect(self.game.display, self.color,[self.game.data2[i][0]*block_size,self.game.data2[i][1]*block_size,block_size,block_size])

# 먹이 클래스 
class Food(Gridobject):
    color = GREEN
    def __init__(self,game):
        x = random.randint(0, game.n_rows - 1)
        y = random.randint(0, game.n_cols - 1) 
        super().__init__(x, y, game, self.color)   
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display,self.color,[self.x*block_size,self.y*block_size,block_size,block_size])
# 게임 클래스
class Game:
    block_size = 10
    def __init__(self,n_rows,n_cols):
        pygame.init()
        self.display = pygame.display.set_mode((n_rows*self.block_size,n_cols*self.block_size))
        self.n_rows= n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.data1 = []
        self.data2 = []
        self.n1 = 0
        self.n2 = 0
        pygame.display.set_caption("DCCP Snake Game")
    
    def play(self, n_foods = 20):
        player1 = Player1(60,30,self,WHITE)
        player2 = Player2(18,30,self,RED)
        foods = [Food(self) for _ in range(n_foods)]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player1.handle_event(event)
                player2.handle_event(event)
            # 게임이 끝나는 경우
            if player1.x > self.n_rows or player1.x < 0 or player1.y > self.n_cols or player1.y < 0:
                self.game_over = True
                break
            if player2.x > self.n_rows or player2.x < 0 or player2.y > self.n_cols or player2.y < 0:
                self.game_over = True
                break
            if (player1.x, player1.y) == (player2.x, player2.y):
                self.game_over = True
                break      
            if (player1.x, player1.y) in self.data1[:self.n1] or (player1.x, player1.y) in self.data2[:self.n2] :
                self.game_over = True
                break
            if (player2.x, player2.y) in self.data1[:self.n1] or (player2.x, player2.y) in self.data2[:self.n2]:
                self.game_over = True
                break

            #지렁이 움직임, 몸통 부분의 데이터 추가하기 
            player1.tick()
            player2.tick()
            self.data1.insert(0,(player1.x - player1.dx, player1.y - player1.dy))
            self.data2.insert(0,(player2.x - player2.dx, player2.y - player2.dy))
            # 한 플레이어가 소유할 수 있는 최대 데이터 설정 
            if len(self.data1) > 100 :
                self.data1 = self.data1[:100]
            if len(self.data2) > 100:
                self.data2 = self.data2[:100]

            # 지렁이 그리기
            self.display.fill(BLACK)
            player1.draw()
            player2.draw()
            player1.body(self.n1)
            player2.body(self.n2)
            
            #먹이 먹기
            for food in foods:
                if food.active:
                    food.draw()
          
            #먹이 먹고 몸통 불리기 
            for food in foods:
                if player1.x == food.x and player1.y == food.y:
                    food.active = False
                    foods.append(Food(self))
                    self.n1 += 1
                if player2.x == food.x and player2.y == food.y:
                    food.active = False
                    foods.append(Food(self))
                    self.n2 += 1
            
            #속도 
            self.clock.tick(10)

            pygame.display.update()
            
if __name__ == "__main__":
    Game(80,60).play(20)
    