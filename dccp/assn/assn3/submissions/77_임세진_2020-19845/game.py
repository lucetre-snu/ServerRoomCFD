'''
뱀의 색깔과 관련하여, 노란색 뱀의 몸통 색깔은 비교적 잘보이는 하늘색으로 표현했습니다.
또한 제목은 저의 학번과 SNAKE GAME이라는 것을 알 수 있도록 작성하였습니다.
'''
import pygame
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 178, 102)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (153, 255, 255)
GREEN = (0, 255, 0)


class Player:
    dx = 0
    dy = 0
    player1_lst = []
    player2_lst = []
    change1 = ''
    direction1 = ''
    change2 = ''
    direction2 = ''
    speed1 = 1
    speed2 = 1

    def __init__(self, x, y, game):
        self.game = game
        self.active = True
        self.x = x
        self.y = y
    
    def handle_event1(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RSHIFT]:
            self.speed1 = 2
        else:
            self.speed1 = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change1 = 'left'
            elif event.key == pygame.K_RIGHT:
                self.change1 = 'right'
            elif event.key == pygame.K_UP:
                self.change1 = 'up'
            elif event.key == pygame.K_DOWN:
                self.change1 = 'down'
            
        if self.change1 == 'left' and self.direction1 != 'right':
            self.direction1 = 'left'
            self.dx = -self.speed1
            self.dy = 0
        elif self.change1 == 'right' and self.direction1 != 'left':
            self.direction1 = 'right'
            self.dx = self.speed1
            self.dy = 0
        elif self.change1 == 'up' and self.direction1 != 'down':
            self.direction1 = 'up'
            self.dx = 0
            self.dy = -self.speed1
        elif self.change1 == 'down' and self.direction1 != 'up':
            self.direction1 = 'down'
            self.dx = 0
            self.dy = self.speed1

    def handle_event2(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed2 = 2
        else:
            self.speed2 = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.change2 = 'left'
            elif event.key == pygame.K_d:
                self.change2 = 'right'
            elif event.key == pygame.K_w:
                self.change2 = 'up'
            elif event.key == pygame.K_s:
                self.change2 = 'down'
        
        if self.change2 == 'left' and self.direction2 != 'right':
            self.direction2 = 'left'
            self.dx = -self.speed2
            self.dy = 0
        elif self.change2 == 'right' and self.direction2 != 'left':
            self.direction2 = 'right'
            self.dx = self.speed2
            self.dy = 0
        elif self.change2 == 'up' and self.direction2 != 'down':
            self.direction2 = 'up'
            self.dx = 0
            self.dy = -self.speed2
        elif self.change2 == 'down' and self.direction2 != 'up':
            self.direction2 = 'down'
            self.dx = 0
            self.dy = self.speed2

    def handle_tick(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw1(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, YELLOW, [self.player1_lst[-1][0] * block_size, self.player1_lst[-1][1] * block_size, block_size, block_size])
        k = 1
        length1 = 1
        previous1 = self.player1_lst[-1]
        while True:
            index1 = len(self.player1_lst)-2-k
            if length1 != len(self.player1_lst)//2:
                if self.player1_lst[index1] != previous1:
                    pygame.draw.rect(self.game.display, LIGHTYELLOW, [self.player1_lst[index1][0] * block_size, self.player1_lst[index1][1] * block_size, block_size, block_size])
                    length1 += 1
                    previous1 = self.player1_lst[index1]
                k += 1
            else:
                break

    def draw2(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, RED, [self.player2_lst[-1][0] * block_size, self.player2_lst[-1][1] * block_size, block_size, block_size])
        w = 1
        length2 = 1
        previous2 = self.player2_lst[-1]
        while True:
            index2 = len(self.player2_lst)-2-w
            if length2 != len(self.player2_lst)//2:
                if self.player2_lst[index2] != previous2:
                    pygame.draw.rect(self.game.display, LIGHTRED, [self.player2_lst[index2][0] * block_size, self.player2_lst[index2][1] * block_size, block_size, block_size])
                    length2 += 1
                    previous2 = self.player2_lst[index2]
                w += 1
            else:
                break

    
class Food:
    def __init__ (self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        self.game = game
        self.active = True
        self.x = x
        self.y = y
    
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, GREEN, [self.x * block_size, self.y * block_size, block_size, block_size])


class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game made by 2020-19845 RIM SEJIN")
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
    
    def play(self, n_foods = 20):
        player1 = Player(self.n_cols*3//4, self.n_rows//2, self)
        player2 = Player(self.n_cols//4, self.n_rows//2, self)
        foods = [Food(self) for _ in range(n_foods)]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player1.handle_event1(event)
                player2.handle_event2(event)

            #게임이 끝나는 조건1: 두 마리의 뱀이 영역을 벗어난 경우
            if player1.x < 0 or player1.x >= self.n_cols or player1.y < 0 or player1.y >= self.n_rows:
                self.game_over = True
            if player2.x < 0 or player2.x >= self.n_cols or player2.y < 0 or player2.y >= self.n_rows:
                self.game_over = True
            
            #각각의 뱀에 대한 결과를 각각 적용한다.
            player1.handle_tick()
            player2.handle_tick()
            
            #배경화면 설정
            self.display.fill(BLACK)

            #길이가 0이면, 다음을 수행한다.
            if len(player1.player1_lst) == 0:
                player1.player1_lst.append([player1.x, player1.y])
                player1.player1_lst.append([player1.x, player1.y])
            player1_length = len(player1.player1_lst)

            if len(player2.player2_lst) == 0:
                player2.player2_lst.append([player2.x, player2.y])
                player2.player2_lst.append([player2.x, player2.y])
            player2_length = len(player2.player2_lst)

            #food를 check한다.===========================player1
            GROW1 = False
            for food in foods:
                if food.active:
                    food.draw()
                if [food.x, food.y] in player1.player1_lst:
                    GROW1 = True
                    EatenFood_index = foods.index(food)
                    foods[EatenFood_index] = Food(self)
            if GROW1:
                player1_length += 2
    
            #food를 check한다.===========================player2
            GROW2 = False
            for food in foods:
                if food.active:
                    food.draw()
                if [food.x, food.y] in player2.player2_lst:
                    GROW2 = True
                    EatenFood_index = foods.index(food)
                    foods[EatenFood_index] = Food(self)
            if GROW2:
                player2_length += 2

            
            #player1 정보 update
            player1.player1_lst.append([player1.x, player1.y])
            player1.player1_lst.append([player1.x, player1.y])
            if len(player1.player1_lst) > player1_length:
                del player1.player1_lst[0]
                del player1.player1_lst[0]

            if player1.speed1 == 2:
                for i_idx in range(player1_length-3, 0, -1):
                    if i_idx % 2 == 1:
                        first1 = (player1.player1_lst[i_idx-1][0]+player1.player1_lst[i_idx+1][0])//2
                        second1 = (player1.player1_lst[i_idx-1][1]+player1.player1_lst[i_idx+1][1])//2
                        player1.player1_lst[i_idx][0] = first1
                        player1.player1_lst[i_idx][1] = second1


            #player2 정보 update
            player2.player2_lst.append([player2.x, player2.y])
            player2.player2_lst.append([player2.x, player2.y])
            if len(player2.player2_lst) > player2_length:
                del player2.player2_lst[0]
                del player2.player2_lst[0]

            if player2.speed2 == 2:
                for j_idx in range(player2_length-3, 0, -1):
                    if j_idx % 2 == 1:
                        first2 = (player2.player2_lst[j_idx-1][0]+player2.player2_lst[j_idx+1][0])//2
                        second2 = (player2.player2_lst[j_idx-1][1]+player2.player2_lst[j_idx+1][1])//2
                        player2.player2_lst[j_idx][0] = first2
                        player2.player2_lst[j_idx][1] = second2


            #게임이 끝날 조건2: 뱀의 머리가 몸통이랑 만날 경우
            sub1 = []
            sub2 = []
            if len(player1.player1_lst) != 2 or len(player1.player1_lst) != 0:
                k = 1
                length1 = 1
                previous1 = player1.player1_lst[-1]
                sub1.append(previous1)
                while True:
                    index1 = len(player1.player1_lst)-2-k
                    if length1 != len(player1.player1_lst)//2:
                        if player1.player1_lst[index1] != previous1:
                            sub1.append(player1.player1_lst[index1])
                            length1 += 1
                            previous1 = player1.player1_lst[index1]
                        k += 1
                    else:
                        break
                if sub1[-1] in sub1[:-2]:
                    self.game_over = True
            
            if len(player2.player2_lst) != 2 or len(player2.player2_lst) != 0:
                k = 1
                length2 = 1
                previous2 = player2.player2_lst[-1]
                sub2.append(previous2)
                while True:
                    index2 = len(player2.player2_lst)-2-k
                    if length2 != len(player2.player2_lst)//2:
                        if player2.player2_lst[index2] != previous2:
                            sub2.append(player2.player2_lst[index2])
                            length2 += 1
                            previous2 = player2.player2_lst[index2]
                        k += 1
                    else:
                        break
                if sub2[-1] in sub2[:-2]:
                    self.game_over = True

            
            #위의 과정을 다 수행한 뒤 각각의 뱀을 그려준다.
            player1.draw1()
            player2.draw2()

            ##게임이 끝날 조건3: 두 뱀이 서로 만날 경우
            for p in player1.player1_lst:
                if p in player2.player2_lst:
                    self.game_over = True

            pygame.display.update()
            self.clock.tick(10)


if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)