import random
import pygame

BROWN = (160,82,45)
YELLOW = (255,255,0)
GREEN1 = (107,142,35)
GREEN2 = (85,107,47)
WHITE1 = (255,250,240)
WHITE2 = (255,192,203)

pygame.init()

game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption('애벌레 사육')
clock = pygame.time.Clock()

food_coordinates = []
for _ in range(20):
    food_x = random.randint(0,79) #10곱하면 0부터 790
    food_y = random.randint(0,59) 
    food_coordinates.append((10 * food_x, 10 * food_y))
food_x = 300
food_y = 300

class player:

    def __init__(self, display,p1orp2):
        self.display = display
        self.p1orp2 = p1orp2
        if self.p1orp2 == 1:
            self.x = 100
            self.y = 300
        else:
            self.x = 700
            self.y = 300
        self.dx = 0
        self.dy = 0
        self.direction = 0
        self.howfast = 10
        self.length = 1
        self.body = list()
        self.new = list()

    def handle_event(self,event):
        if self.p1orp2 == 1:

            if event.type == pygame.KEYUP: # 오른쪽 shift에서 손 떼면 속도 복귀
                if event.mod == 0:
                    self.howfast = 10

            elif event.type == pygame.KEYDOWN: # 한 칸씩 전진

                if event.mod == 2: # 오른쪽 shift에 손 대고 있으면 속도 2배
                    self.howfast = 20

                if event.key == pygame.K_LEFT and self.direction != 2:
                    self.dx = - 10
                    self.dy = 0
                    self.direction = 1

                elif event.key == pygame.K_RIGHT and self.direction != 1:
                    self.dx = 10
                    self.dy = 0
                    self.direction = 2
                    
                elif event.key == pygame.K_UP and self.direction != 4:
                    self.dy = -10
                    self.dx = 0
                    self.direction = 3
                    
                elif event.key == pygame.K_DOWN and self.direction != 3:
                    self.dy = 10
                    self.dx = 0
                    self.direction = 4 

        elif self.p1orp2 == 2:
            if event.type == pygame.KEYUP: # 왼쪽 shift에서 손 떼면 속도 복귀
                if event.mod == 0:
                    self.howfast = 10
        
            elif event.type == pygame.KEYDOWN: # 한 칸씩 전진

                if event.mod == 1: # 왼쪽 shift에 손 대고 있으면 속도 2배
                    self.howfast = 20

                if event.key == pygame.K_a and self.direction != 2:
                    self.dx = - 10
                    self.dy = 0
                    self.direction = 1

                elif event.key == pygame.K_d and self.direction != 1:
                    self.dx = 10
                    self.dy = 0
                    self.direction = 2
                    
                elif event.key == pygame.K_w and self.direction != 4:
                    self.dy = -10
                    self.dx = 0
                    self.direction = 3
                    
                elif event.key == pygame.K_s and self.direction != 3:
                    self.dy = 10
                    self.dx = 0
                    self.direction = 4 

    def tick(self):
        if self.howfast == 20:
            self.x += self.dx * 2
            self.y += self.dy * 2
        else:
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        self.new = list()
        for i in range(self.length):
            if self.howfast == 10:
                if i == 0: 
                    self.new.append([self.x,self.y,10,10])
                else:
                    self.new.append(self.body[i-1])
            else:
                if i == 0:
                    self.new.append([self.x,self.y,10,10])
                elif i == 1 :
                    self.new.append([self.x-self.dx,self.y-self.dy,10,10])
                else:
                    self.new.append(self.body[i-2])

        for i in range(self.length-1): # 자기 머리가 몸통에 겹쳐지면 즉시 종료
            if [self.x,self.y,10,10] == self.body[i]:
                global gameover
                gameover = True
                break
        
        if self.p1orp2 == 1:
            color1 = GREEN1
            color2 = GREEN2
        else:
            color1 = WHITE1
            color2 = WHITE2
        for i in range(self.length):
            if i == 0:
                pygame.draw.rect(self.display, color1, self.new[0]) # 대가리
            else:
                pygame.draw.rect(self.display, color2, self.new[i]) # 방향에 따라 길이 표현
        self.body = self.new

gameover = False
player1 = player(game_display,1)
player2 = player(game_display,2)

def new_food(): # 새로운 먹이 생성
    global food_x
    global food_y
    food_x = random.randint(0,79)
    food_y = random.randint(0,59) # 뱀 머리랑 몸통 있는 데는 먹이가 안 생기게 처리
    if [10 * food_x, 10 * food_y,10,10] in player1.new or [10 * food_x, 10 * food_y,10,10] in player2.new:
        new_food() 
    food_coordinates.append((10 * food_x, 10 * food_y))

def play():
    global gameover
    while not gameover:

        game_display.fill(BROWN)

        for event in pygame.event.get():
            player1.handle_event(event)
            player2.handle_event(event)

            if event.type == pygame.QUIT: # X 눌러서 창 닫기 
                gameover = True
                break

        player1.tick()
        player2.tick()

        player1.draw()
        player2.draw()

        for i in range(player1.length): # 서로 부닺히면 즉시 종료
            for j in range(player2.length):
                if player1.new[i] == player2.new[j]:
                    gameover = True

        for i, (food_x, food_y) in enumerate(food_coordinates): # 먹이 배치
            pygame.draw.rect(game_display, YELLOW, [food_x,food_y,10,10]) 
                            
        for i, (food_x, food_y) in enumerate(food_coordinates):
            if [food_x, food_y, 10, 10] in player1.new:
                del food_coordinates[i] # p1이 먹는 먹이 삭제
                player1.length += 1 # 먹이 먹을 때마다 길이 하나씩 늘리기
                new_food()

            if [food_x, food_y, 10, 10] in player2.new:
                del food_coordinates[i] #p2가 먹는 먹이 삭제
                player2.length += 1 # 먹이 먹을 때마다 길이 하나씩 늘리기
                new_food()

        if player1.x < 0 or player1.x > 800 or player1.y < 0 or player1.y > 600 : # 화면 밖에 나가면 즉시 종료 
            gameover = True 
        if player2.x < 0 or player2.x > 800 or player2.y < 0 or player2.y > 600 : # 화면 밖에 나가면 즉시 종료 
            gameover = True 

        pygame.display.update()    
        clock.tick(10)
play()
